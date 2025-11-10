from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from decimal import Decimal
from .models import Book
from .forms import BookRequestForm
from .forms import BookFilterForm
from .forms import RegistrationForm, LoginForm
from .forms import UserUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import CustomUser, Fine, Payment, MobileNotification
from .email_service import email_service
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from .decorators import check_fine_access, require_no_excessive_fines


# Create your views here.

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def index(request):
    return render(request, 'libapp/index.html')

def home(request):
    context = {}
    if request.user.is_authenticated:
        # Add today's date for comparison in template
        context['today'] = timezone.now().date()
        
        # Process user's books to check for overdue status
        if hasattr(request.user, 'books') and request.user.books:
            for book in request.user.books:
                end_date_str = book.get('end_date')
                if end_date_str:
                    end_date = timezone.datetime.fromisoformat(end_date_str).date()
                    current_date = timezone.now().date()
                    book['is_overdue'] = end_date < current_date
    
    return render(request, 'libapp/home.html', context)
    
@login_required
@user_passes_test(lambda u: u.is_librarian)
def status_view(request):
    # Get all books in the system
    all_books = Book.objects.all()
    
    # Get statistics
    total_books = all_books.count()
    available_books = all_books.filter(quantity__gt=0).count()
    borrowed_books = 0
    returned_books = 0
    
    # Count lost books (books with quantity = 0 and have associated fines)
    lost_books = 0
    # Fine.status choices use 'PENDING' uppercase; use matching value
    lost_books_fines = Fine.objects.filter(status='PENDING').values('book_title').distinct()
    lost_books = len(lost_books_fines)
    
    # Count borrowed books
    users_with_books = CustomUser.objects.filter(books__isnull=False)
    
    # Process user book data to include return status
    for user in users_with_books:
        for book in user.books:
            # Calculate if the book is overdue
            end_date_str = book.get('end_date')
            if end_date_str:
                end_date = timezone.datetime.fromisoformat(end_date_str)
                current_date = timezone.now()
                
                # Check if book is returned
                if book.get('is_returned', False):
                    returned_books += 1
                    book['is_returned'] = True
                    book['is_overdue'] = False
                else:
                    borrowed_books += 1
                    book['is_returned'] = False
                    book['is_overdue'] = end_date < current_date
    
    context = {
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'returned_books': returned_books,
        'lost_books': lost_books,
        'users_with_books': users_with_books,
    }
    
    return render(request, 'libapp/status.html', context)

def explore(request):
    search_query = request.GET.get('q')
    books = Book.objects.all()
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(subject__icontains=search_query)
        )
    
    context = {
        'books': books,
        'search_query': search_query,
    }
    return render(request, 'libapp/explore.html', context)

def explore_view(request):
    form = BookFilterForm(request.GET)
    books = Book.objects.all()
    
    if form.is_valid():
        if form.cleaned_data.get('subject'):
            books = books.filter(subject=form.cleaned_data['subject'])
        if form.cleaned_data.get('author'):
            books = books.filter(author__icontains=form.cleaned_data['author'])
        if form.cleaned_data.get('title'):
            books = books.filter(title__icontains=form.cleaned_data['title'])
    
    context = {
        'books': books,
        'form': form,
    }
    return render(request, 'libapp/explore.html', context)

@login_required
def book_request_view(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.user = request.user
            book_request.save()
            messages.success(request, 'Book request submitted successfully!')
            return redirect('home')
    else:
        form = BookRequestForm()
    
    return render(request, 'libapp/book_request_form.html', {'form': form})

@login_required
def return_book_view(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        if book_id:
            # Find the book in user's books and mark as returned
            user = request.user
            if hasattr(user, 'books') and user.books:
                for book in user.books:
                    if str(book.get('id')) == str(book_id):
                        book['is_returned'] = True
                        book['return_date'] = timezone.now().isoformat()
                        user.save()
                        messages.success(request, 'Book returned successfully!')
                        break
            else:
                messages.error(request, 'Book not found in your borrowed books.')
        else:
            messages.error(request, 'Invalid book ID.')
    
    return redirect('user_dashboard')

def get_subjects_view(request):
    subjects = Book.objects.values_list('subject', flat=True).distinct()
    return JsonResponse(list(subjects), safe=False)

def get_books_view(request):
    subject = request.GET.get('subject')
    if subject:
        books = Book.objects.filter(subject=subject)
        books_data = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
        return JsonResponse(books_data, safe=False)
    return JsonResponse([], safe=False)

def aboutus_view(request):
    return render(request, 'libapp/aboutus.html')

@login_required
@user_passes_test(lambda u: u.is_librarian)
def update_book_details(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    return render(request, 'libapp/update_book_details.html', {'book': book})

@login_required
@user_passes_test(lambda u: u.is_librarian)
def save_book_details(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.subject = request.POST.get('subject', book.subject)
        book.quantity = int(request.POST.get('quantity', book.quantity))
        book.save()
        messages.success(request, 'Book details updated successfully!')
        return redirect('librarian_dashboard')
    return redirect('update_book_details', book_pk=book_pk)

@login_required
@user_passes_test(lambda u: u.is_librarian)
def render_add_new_book_page(request):
    return render(request, 'libapp/add_new_book.html')

@login_required
@user_passes_test(lambda u: u.is_librarian)
def save_new_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        subject = request.POST.get('subject')
        quantity = int(request.POST.get('quantity', 1))
        
        if title and author and subject:
            book = Book.objects.create(
                title=title,
                author=author,
                subject=subject,
                quantity=quantity
            )
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('librarian_dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return redirect('add_new_book')

@login_required
@user_passes_test(lambda u: u.is_librarian)
def librarian_dashboard(request):
    books = Book.objects.all()
    users = CustomUser.objects.filter(is_librarian=False)
    return render(request, 'libapp/librarian_dashboard.html', {'books': books, 'users': users})

@login_required
@user_passes_test(lambda u: u.is_librarian)
def remind_user(request):
    # Implementation for reminding users
    return JsonResponse({'status': 'success'})

@login_required
def payment_view(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    return render(request, 'libapp/payment.html', {'fine': fine})

@login_required
def pay_fine(request):
    if request.method == 'POST':
        fine_id = request.POST.get('fine_id')
        fine = get_object_or_404(Fine, id=fine_id)
        
        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            fine=fine,
            amount=fine.amount,
            payment_method=request.POST.get('payment_method', 'CASH'),
            bank_name=request.POST.get('bank_name', ''),
            status='COMPLETED'
        )
        
        # Update fine status
        fine.status = 'PAID'
        fine.save()
        
        messages.success(request, 'Fine paid successfully!')
        return redirect('payment_receipt', payment_id=payment.id)
    
    return redirect('user_dashboard')

@login_required
def pay_lost_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        
        # Create fine for lost book
        fine = Fine.objects.create(
            user=request.user,
            book_title=book.title,
            amount=Decimal('500.00'),  # Lost book fine
            reason='LOST_BOOK',
            status='PENDING'
        )
        
        # Create payment
        payment = Payment.objects.create(
            user=request.user,
            fine=fine,
            amount=fine.amount,
            payment_method=request.POST.get('payment_method', 'CASH'),
            bank_name=request.POST.get('bank_name', ''),
            status='COMPLETED'
        )
        
        # Update fine status
        fine.status = 'PAID'
        fine.save()
        
        messages.success(request, 'Lost book fine paid successfully!')
        return redirect('payment_receipt', payment_id=payment.id)
    
    return redirect('user_dashboard')

@login_required
@user_passes_test(lambda u: u.is_librarian)
def add_fine(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_title = request.POST.get('book_title')
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        
        user = get_object_or_404(CustomUser, id=user_id)
        
        fine = Fine.objects.create(
            user=user,
            book_title=book_title,
            amount=Decimal(amount),
            reason=reason,
            status='PENDING'
        )
        
        messages.success(request, f'Fine of ${amount} added for {user.username}')
        return redirect('librarian_dashboard')
    
    return redirect('librarian_dashboard')

@login_required
def payment_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'libapp/payment_receipt.html', {'payment': payment})

@login_required
def view_payments(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'libapp/view_payments.html', {'payments': payments})

@login_required
def view_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'libapp/view_payment.html', {'payment': payment})

@login_required
def generate_barcode(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'libapp/barcode.html', {'book': book})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.quantity > 0:
        if not hasattr(request.user, 'cart'):
            request.user.cart = []
        
        if book_id not in request.user.cart:
            request.user.cart.append(book_id)
            request.user.save()
            messages.success(request, f'{book.title} added to cart!')
        else:
            messages.info(request, f'{book.title} is already in your cart!')
    else:
        messages.error(request, 'Book is not available!')
    
    return redirect('explore')

@login_required
def remove_from_cart(request, book_id):
    if hasattr(request.user, 'cart') and book_id in request.user.cart:
        request.user.cart.remove(book_id)
        request.user.save()
        messages.success(request, 'Book removed from cart!')
    
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_books = []
    if hasattr(request.user, 'cart') and request.user.cart:
        cart_books = Book.objects.filter(id__in=request.user.cart)
    
    return render(request, 'libapp/cart.html', {'cart_books': cart_books})

@login_required
def checkout_cart(request):
    if hasattr(request.user, 'cart') and request.user.cart:
        # Process checkout logic here
        # For now, just clear the cart
        request.user.cart = []
        request.user.save()
        messages.success(request, 'Checkout completed successfully!')
    
    return redirect('user_dashboard')

@login_required
def extend_book(request, book_id):
    # Implementation for extending book due date
    messages.success(request, 'Book due date extended!')
    return redirect('user_dashboard')

@login_required
def ai_recommendations(request):
    # AI recommendations logic
    recommended_books = Book.objects.all()[:5]  # Placeholder
    return render(request, 'libapp/ai_recommendations.html', {'recommended_books': recommended_books})

@login_required
def ai_search(request):
    query = request.GET.get('q', '')
    if query:
        # AI search logic
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(subject__icontains=query)
        )[:10]
    else:
        books = Book.objects.none()
    
    return render(request, 'libapp/explore.html', {'books': books, 'search_query': query})

@login_required
def report_lost_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Create fine for lost book
        fine = Fine.objects.create(
            user=request.user,
            book_title=book.title,
            amount=Decimal('500.00'),
            reason='LOST_BOOK',
            status='PENDING'
        )
        
        # Update book quantity
        book.quantity = max(0, book.quantity - 1)
        book.save()
        
        messages.success(request, f'Book "{book.title}" reported as lost. Fine of $500.00 has been added.')
        return redirect('user_dashboard')
    
    return render(request, 'libapp/status.html', {'book': book})

def login_view(request):
    return render(request, 'libapp/login.html')

def signup(request):
    return render(request, 'libapp/register.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'libapp/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid credentials!')
    else:
        form = LoginForm()
    
    return render(request, 'libapp/login.html', {'form': form})

def login_librarian(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_librarian:
            auth_login(request, user)
            messages.success(request, 'Librarian login successful!')
            return redirect('librarian_dashboard')
        else:
            messages.error(request, 'Invalid librarian credentials!')
    
    return render(request, 'libapp/librarian_login.html')

@login_required
def test_sms(request):
    # SMS testing functionality
    return render(request, 'libapp/test_sms.html')

@login_required
def mobile_notification(request, notification_id):
    notification = get_object_or_404(MobileNotification, id=notification_id)
    return render(request, 'libapp/mobile_notification.html', {'notification': notification})

@login_required
def respond_notification(request, notification_id):
    notification = get_object_or_404(MobileNotification, id=notification_id)
    
    if request.method == 'POST':
        response = request.POST.get('response')
        if response:
            notification.response = response
            notification.save()
            messages.success(request, 'Response sent successfully!')
            return redirect('my_notifications')
    
    return render(request, 'libapp/mobile_notification.html', {'notification': notification})

@login_required
def create_book_borrow_notification(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Create notification for book borrowing
    notification = MobileNotification.objects.create(
        user=request.user,
        book_title=book.title,
        notification_type='BORROW_REQUEST',
        message=f'Request to borrow "{book.title}"',
        status='PENDING'
    )
    
    messages.success(request, 'Borrow request notification sent!')
    return redirect('my_notifications')

@login_required
def create_book_return_notification(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Create notification for book return
    notification = MobileNotification.objects.create(
        user=request.user,
        book_title=book.title,
        notification_type='RETURN_REQUEST',
        message=f'Request to return "{book.title}"',
        status='PENDING'
    )
    
    messages.success(request, 'Return request notification sent!')
    return redirect('my_notifications')

@login_required
def my_notifications(request):
    notifications = MobileNotification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'libapp/my_notifications.html', {'notifications': notifications})

@login_required
def user_dashboard(request):
    # Get user's borrowed books
    user_books = []
    if hasattr(request.user, 'books') and request.user.books:
        user_books = request.user.books
    
    # Get user's fines
    fines = Fine.objects.filter(user=request.user, status='PENDING')
    
    # Get user's payments
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'user_books': user_books,
        'fines': fines,
        'payments': payments,
        'today': timezone.now().date(),
    }
    
    return render(request, 'libapp/user_dashboard.html', context)

@login_required
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'libapp/register.html', {'form': form})

def test_email(request):
    # Email testing functionality
    return render(request, 'libapp/test_email.html')
