"""
Digital Library Views for ReadOps
Handles online reading, digital books, and QR code payments
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from django.utils import timezone
from django.conf import settings
from django.db import transaction
import qrcode
import io
import base64
from PIL import Image
import json
from datetime import timedelta
from decimal import Decimal

from .models import DigitalBook, DigitalBookAccess, QRPayment, CustomUser


@login_required
def digital_library(request):
    """Digital library catalog"""
    category = request.GET.get('category', '')
    book_type = request.GET.get('type', '')
    free_only = request.GET.get('free_only', '')
    
    books = DigitalBook.objects.filter(is_active=True)
    
    if category:
        books = books.filter(category__icontains=category)
    if book_type:
        books = books.filter(book_type=book_type)
    if free_only == 'true':
        books = books.filter(is_free=True)
    
    # Get user's current access
    user_access = DigitalBookAccess.objects.filter(
        user=request.user,
        status='ACTIVE'
    ).select_related('digital_book')
    
    context = {
        'books': books,
        'user_access': user_access,
        'categories': DigitalBook.objects.values_list('category', flat=True).distinct(),
        'book_types': DigitalBook.BOOK_TYPE_CHOICES,
        'selected_category': category,
        'selected_type': book_type,
        'free_only': free_only,
    }
    
    return render(request, 'libapp/digital_library.html', context)


@login_required
def digital_book_detail(request, book_id):
    """Digital book detail page"""
    book = get_object_or_404(DigitalBook, id=book_id, is_active=True)
    
    # Check if user has active access
    user_access = DigitalBookAccess.objects.filter(
        user=request.user,
        digital_book=book,
        status='ACTIVE'
    ).first()
    
    # Check if access is still valid
    has_valid_access = False
    if user_access and user_access.is_access_valid():
        has_valid_access = True
    
    context = {
        'book': book,
        'user_access': user_access,
        'has_valid_access': has_valid_access,
    }
    
    return render(request, 'libapp/digital_book_detail.html', context)


@login_required
def create_payment_request(request, book_id):
    """Create payment request for digital book access"""
    book = get_object_or_404(DigitalBook, id=book_id, is_active=True)
    access_type = request.POST.get('access_type', 'ONLINE_READING')
    
    if access_type not in ['ONLINE_READING', 'DOWNLOAD']:
        messages.error(request, 'Invalid access type.')
        return redirect('digital_book_detail', book_id=book_id)
    
    # Check if user already has active access
    existing_access = DigitalBookAccess.objects.filter(
        user=request.user,
        digital_book=book,
        access_type=access_type,
        status='ACTIVE'
    ).first()
    
    if existing_access and existing_access.is_access_valid():
        messages.info(request, 'You already have active access to this book.')
        return redirect('digital_book_detail', book_id=book_id)
    
    # Handle free books
    if book.is_free:
        # Create free access immediately
        with transaction.atomic():
            access = DigitalBookAccess.objects.create(
                user=request.user,
                digital_book=book,
                access_type=access_type,
                status='ACTIVE',
                payment_amount=Decimal('0.00'),
                access_start_date=timezone.now(),
                access_end_date=timezone.now() + timedelta(days=365),  # 1 year free access
                payment_reference='FREE_ACCESS'
            )
        
        messages.success(request, f'Free access granted to "{book.title}"!')
        return redirect('digital_book_detail', book_id=book_id)
    
    # Calculate price for paid books
    price = book.online_reading_price if access_type == 'ONLINE_READING' else book.download_price
    
    # Create access record
    access_start = timezone.now()
    access_end = access_start + timedelta(days=5)  # 5 days access
    
    with transaction.atomic():
        digital_access = DigitalBookAccess.objects.create(
            user=request.user,
            digital_book=book,
            access_type=access_type,
            payment_amount=price,
            access_start_date=access_start,
            access_end_date=access_end,
            status='PENDING' if price > 0 else 'ACTIVE'
        )
        
        if price > 0:
            # Create QR payment
            qr_payment = create_qr_payment(digital_access, price)
            return redirect('payment_qr', payment_id=qr_payment.id)
        else:
            messages.success(request, 'Free book access granted!')
            return redirect('digital_book_detail', book_id=book_id)


def create_qr_payment(digital_access, amount):
    """Create QR code payment"""
    # Generate QR code data for UPI payment
    upi_id = "readops@paytm"  # Replace with actual UPI ID
    qr_data = f"upi://pay?pa={upi_id}&pn=ReadOps Library&am={amount}&cu=INR&tn=Digital Book Access"
    
    # Create QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Generate QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code image
    img_buffer = io.BytesIO()
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Create QR payment record
    qr_payment = QRPayment.objects.create(
        user=digital_access.user,
        digital_book_access=digital_access,
        amount=amount,
        qr_code_data=qr_data,
        expires_at=timezone.now() + timedelta(minutes=30)  # 30 minutes expiry
    )
    
    # Save QR code image
    qr_payment.qr_code_image.save(
        f'qr_{qr_payment.id}.png',
        img_buffer,
        save=True
    )
    
    return qr_payment


@login_required
def payment_qr(request, payment_id):
    """Display QR code for payment"""
    qr_payment = get_object_or_404(QRPayment, id=payment_id, user=request.user)
    
    if qr_payment.is_expired():
        messages.error(request, 'Payment request has expired. Please try again.')
        return redirect('digital_book_detail', book_id=qr_payment.digital_book_access.digital_book.id)
    
    context = {
        'qr_payment': qr_payment,
        'book': qr_payment.digital_book_access.digital_book,
    }
    
    return render(request, 'libapp/payment_qr.html', context)


@login_required
def verify_payment(request, payment_id):
    """Verify payment status"""
    qr_payment = get_object_or_404(QRPayment, id=payment_id, user=request.user)
    
    if qr_payment.status == 'COMPLETED':
        return JsonResponse({'status': 'completed', 'message': 'Payment verified successfully!'})
    elif qr_payment.is_expired():
        return JsonResponse({'status': 'expired', 'message': 'Payment request has expired.'})
    else:
        return JsonResponse({'status': 'pending', 'message': 'Payment is still pending.'})


@login_required
def confirm_payment(request, payment_id):
    """Manually confirm payment (for testing purposes)"""
    if not request.user.is_staff:  # Only staff can manually confirm
        messages.error(request, 'Access denied.')
        return redirect('digital_library')
    
    qr_payment = get_object_or_404(QRPayment, id=payment_id)
    
    if qr_payment.status == 'PENDING':
        with transaction.atomic():
            qr_payment.status = 'COMPLETED'
            qr_payment.payment_reference = f"MANUAL_{timezone.now().strftime('%Y%m%d%H%M%S')}"
            qr_payment.save()
            
            # Activate digital access
            digital_access = qr_payment.digital_book_access
            digital_access.status = 'ACTIVE'
            digital_access.payment_reference = qr_payment.payment_reference
            digital_access.save()
            
            messages.success(request, 'Payment confirmed and access activated!')
    
    return redirect('digital_book_detail', book_id=digital_access.digital_book.id)


@login_required
def online_reader(request, book_id):
    """Online book reader"""
    book = get_object_or_404(DigitalBook, id=book_id, is_active=True)
    
    # Check if user has valid access
    user_access = DigitalBookAccess.objects.filter(
        user=request.user,
        digital_book=book,
        access_type='ONLINE_READING',
        status='ACTIVE'
    ).first()
    
    if not user_access or not user_access.is_access_valid():
        messages.error(request, 'You need to purchase access to read this book online.')
        return redirect('digital_book_detail', book_id=book_id)
    
    # For demo purposes, we'll show a sample text
    # In a real implementation, you'd load the actual book content
    sample_content = get_sample_book_content(book)
    
    context = {
        'book': book,
        'user_access': user_access,
        'content': sample_content,
    }
    
    return render(request, 'libapp/online_reader.html', context)


@login_required
def download_book(request, book_id):
    """Download digital book"""
    book = get_object_or_404(DigitalBook, id=book_id, is_active=True)
    
    # Check if user has valid access
    user_access = DigitalBookAccess.objects.filter(
        user=request.user,
        digital_book=book,
        access_type='DOWNLOAD',
        status='ACTIVE'
    ).first()
    
    if not user_access or not user_access.is_access_valid():
        messages.error(request, 'You need to purchase download access for this book.')
        return redirect('digital_book_detail', book_id=book_id)
    
    # Determine file type and file
    file_type = request.GET.get('type', 'pdf')
    
    if file_type == 'pdf' and book.pdf_file:
        file_path = book.pdf_file.path
        filename = f"{book.title}.pdf"
        content_type = 'application/pdf'
    elif file_type == 'word' and book.word_file:
        file_path = book.word_file.path
        filename = f"{book.title}.docx"
        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    else:
        messages.error(request, 'Requested file format not available.')
        return redirect('digital_book_detail', book_id=book_id)
    
    try:
        response = FileResponse(
            open(file_path, 'rb'),
            content_type=content_type,
            as_attachment=True,
            filename=filename
        )
        return response
    except FileNotFoundError:
        messages.error(request, 'File not found.')
        return redirect('digital_book_detail', book_id=book_id)


@login_required
def my_digital_books(request):
    """User's digital book access history"""
    user_access = DigitalBookAccess.objects.filter(
        user=request.user
    ).select_related('digital_book').order_by('-created_date')
    
    context = {
        'user_access': user_access,
    }
    
    return render(request, 'libapp/my_digital_books.html', context)


def get_sample_book_content(book):
    """Get sample content for the book (for demo purposes)"""
    if 'bhagavad' in book.title.lower() or 'geeta' in book.title.lower():
        return """
        <h2>Bhagavad Gita - Chapter 1</h2>
        <h3>Arjuna's Dilemma</h3>
        <p>Dhritarashtra said: O Sanjaya, assembled in the holy field of Kurukshetra and eager to fight, what did my sons and the sons of Pandu do?</p>
        
        <p>Sanjaya said: Having seen the army of the Pandavas drawn up in battle array, King Duryodhana approached his teacher and spoke these words:</p>
        
        <p>"Behold, O Teacher, this mighty army of the sons of Pandu, arrayed by the son of Drupada, your talented disciple.</p>
        
        <p>Here are heroes, mighty archers, equal in battle to Bhima and Arjuna: Yuyudhana, Virata, and Drupada, of the great car (mighty warriors).</p>
        
        <p>Drishtaketu, Chekitana, and the valiant king of Kashi, Purujit, and Kuntibhoja, and Shaibya, the best of men.</p>
        
        <p>Yudhamanyu, the strong, and Uttamauja, the brave; the son of Subhadra, and the sons of Draupadi, all of great chariots.</p>
        
        <p>Know them also, O best of the twice-born, the distinguished ones on our side, the leaders of my army. I will name them for your information.</p>
        """
    elif 'ramayana' in book.title.lower():
        return """
        <h2>Ramayana - Bala Kanda</h2>
        <h3>The Birth of Rama</h3>
        <p>In the city of Ayodhya, there lived a great king named Dasharatha. He was righteous and just, loved by all his subjects.</p>
        
        <p>King Dasharatha had three queens: Kausalya, Kaikeyi, and Sumitra. Despite having everything, the king was sad because he had no children.</p>
        
        <p>One day, the great sage Vishwamitra came to the court of King Dasharatha and requested the help of Rama and Lakshmana to protect his yajna from demons.</p>
        
        <p>Rama and Lakshmana, though young, were brave and skilled warriors. They accompanied Vishwamitra and successfully protected the yajna.</p>
        """
    else:
        return f"""
        <h2>{book.title}</h2>
        <h3>Chapter 1</h3>
        <p>This is a sample content for {book.title} by {book.author}.</p>
        
        <p>In a real implementation, this would be the actual book content loaded from the digital file.</p>
        
        <p>The content would be formatted and displayed in a reader-friendly format with proper typography and navigation.</p>
        
        <p>Users would be able to navigate through chapters, bookmark pages, and have a smooth reading experience.</p>
        """


@login_required
def add_digital_book(request):
    """Add new digital book (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('digital_library')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        book_type = request.POST.get('book_type')
        category = request.POST.get('category')
        online_price = request.POST.get('online_reading_price', 50.00)
        download_price = request.POST.get('download_price', 100.00)
        is_free = request.POST.get('is_free') == 'on'
        
        if title and author and description:
            book = DigitalBook.objects.create(
                title=title,
                author=author,
                description=description,
                book_type=book_type,
                category=category,
                online_reading_price=online_price,
                download_price=download_price,
                is_free=is_free
            )
            
            # Handle file uploads
            if 'cover_image' in request.FILES:
                book.cover_image = request.FILES['cover_image']
            if 'pdf_file' in request.FILES:
                book.pdf_file = request.FILES['pdf_file']
            if 'word_file' in request.FILES:
                book.word_file = request.FILES['word_file']
            
            book.save()
            messages.success(request, f'Digital book "{book.title}" added successfully!')
            return redirect('digital_library')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    context = {
        'book_types': DigitalBook.BOOK_TYPE_CHOICES,
    }
    
    return render(request, 'libapp/add_digital_book.html', context)
