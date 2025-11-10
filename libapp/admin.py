from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count, Q
from django.contrib.admin import ModelAdmin
from django.utils import timezone
from .models import Book, CustomUser, Payment, Fine, Librarian

# Custom admin site configuration
class LibraryAdminSite(admin.AdminSite):
    site_header = 'Library Management System'
    site_title = 'Library Admin'
    index_title = 'Library Administration'
    index_template = 'admin/library_dashboard.html'
    
    def index(self, request, extra_context=None):
        # Calculate statistics
        lost_books_count = Book.objects.filter(lost_book=True).count()
        pending_fines_count = Fine.objects.filter(status='pending').count()
        total_books = Book.objects.count()
        borrowed_books_count = Book.objects.filter(status='borrowed').count()
        
        # Get recent lost book reports (last 30 days)
        recent_lost_books = Fine.objects.filter(
            created_date__gte=timezone.now() - timezone.timedelta(days=30),
            status='pending'
        ).select_related('user')[:10]
        
        extra_context = extra_context or {}
        extra_context.update({
            'lost_books_count': lost_books_count,
            'pending_fines_count': pending_fines_count,
            'total_books': total_books,
            'borrowed_books_count': borrowed_books_count,
            'recent_lost_books': recent_lost_books,
        })
        
        return super().index(request, extra_context=extra_context)

admin_site = LibraryAdminSite(name='library-admin')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_title', 'amount', 'payment_type', 'payment_date', 'status_badge')
    list_filter = ('payment_type', 'payment_date', 'amount')
    search_fields = ('user__username', 'book_title', 'user__email')
    date_hierarchy = 'payment_date'
    readonly_fields = ('payment_date',)
    
    def status_badge(self, obj):
        return format_html('<span style="background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px;">Paid</span>')
    status_badge.short_description = 'Status'

class FineAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_title', 'amount', 'days_overdue', 'status_badge', 'due_date', 'user_link')
    list_filter = ('status', 'created_date', 'amount', 'days_overdue')
    search_fields = ('user__username', 'book_title', 'user__email')
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date',)
    actions = ['mark_as_paid', 'mark_as_pending', 'mark_as_cancelled']
    list_per_page = 25
    change_list_template = 'admin/fine_stats.html'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'paid': '#28a745',
            'cancelled': '#dc3545'
        }
        return format_html('<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 4px;">{}</span>', 
                          colors.get(obj.status, '#6c757d'), obj.status.title())
    status_badge.short_description = 'Status'
    
    def user_link(self, obj):
        url = reverse('admin:libapp_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}" target="_blank">View User</a>', url)
    user_link.short_description = 'User Profile'
    
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status='paid')
        self.message_user(request, f'{updated} fines marked as paid.')
    mark_as_paid.short_description = "Mark selected fines as paid"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} fines marked as pending.')
    mark_as_pending.short_description = "Mark selected fines as pending"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} fines marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected fines as cancelled"
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            qs = self.get_queryset(request)
        
        # Calculate statistics
        total_fines = qs.aggregate(total=Sum('amount'))['total'] or 0
        pending_fines = qs.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
        paid_fines = qs.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
        cancelled_fines = qs.filter(status='cancelled').aggregate(total=Sum('amount'))['total'] or 0
        
        fine_stats = {
            'total_fines': total_fines,
            'pending_fines': pending_fines,
            'paid_fines': paid_fines,
            'cancelled_fines': cancelled_fines,
            'total_count': qs.count(),
            'pending_count': qs.filter(status='pending').count(),
            'paid_count': qs.filter(status='paid').count(),
            'cancelled_count': qs.filter(status='cancelled').count(),
        }
        
        response.context_data['fine_stats'] = fine_stats
        return response

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'quantity', 'department', 'lost_books_count')
    list_filter = ('department', 'author')
    search_fields = ('title', 'author', 'department', 'subject')
    readonly_fields = ()
    list_per_page = 25
    actions = ['mark_as_lost', 'mark_as_available', 'return_book_action']
    
    def mark_as_lost(self, request, queryset):
        for book in queryset:
            # Create a fine for the lost book if there are users with this book
            users_with_book = CustomUser.objects.filter(books__contains=[{'title': book.title}])
            for user in users_with_book:
                fine = Fine.objects.create(
                    user=user,
                    book_title=book.title,
                    amount=50.00,  # Default to ₹50
                    due_date=timezone.now(),
                    days_overdue=0,
                    status='pending'
                )
                
                # Update user's books list
                updated_books = []
                for b in user.books:
                    if b.get('title') != book.title:
                        updated_books.append(b)
                user.books = updated_books
                user.save()
                
                # Add notification
                if not isinstance(user.notifications, list):
                    user.notifications = []
                user.notifications.append({
                    'message': f'Book "{book.title}" has been marked as lost. A fine of ₹50.00 has been added.',
                    'date': timezone.now().isoformat(),
                    'read': False
                })
                user.save()
        
        # Update book quantity to 0
        updated = queryset.update(quantity=0)
        self.message_user(request, f'{updated} books marked as lost and fines created.')
    mark_as_lost.short_description = "Mark selected books as lost"
    
    def mark_as_available(self, request, queryset):
        # Reset quantity to 1 if it was 0
        for book in queryset:
            if book.quantity == 0:
                book.quantity = 1
                book.save()
        self.message_user(request, f'{queryset.count()} books marked as available.')
    mark_as_available.short_description = "Mark selected books as available"
    
    def return_book_action(self, request, queryset):
        """Return selected books from users who have borrowed them"""
        returned_count = 0
        
        for book in queryset:
            # Find users who have this book
            users_with_book = CustomUser.objects.filter(books__contains=[{'title': book.title}])
            
            for user in users_with_book:
                # Remove the book from user's books list
                updated_books = []
                for b in user.books:
                    if b.get('title') != book.title:
                        updated_books.append(b)
                
                if len(updated_books) < len(user.books):
                    user.books = updated_books
                    user.save()
                    
                    # Increase book quantity
                    book.quantity += 1
                    book.save()
                    
                    returned_count += 1
                    
                    # Create mobile notification
                    notification = MobileNotification.objects.create(
                        user=user,
                        notification_type='BOOK_RETURNED',
                        title=f'Book Returned: {book.title}',
                        message=f'Your book "{book.title}" has been returned by the librarian.',
                        book_title=book.title,
                        book_id=book.id
                    )
        
        if returned_count > 0:
            self.message_user(request, f'Successfully returned {returned_count} books from users.')
        else:
            self.message_user(request, 'No books were currently borrowed by users.')
    return_book_action.short_description = "Return selected books from users"
    
    def lost_books_count(self, obj):
        lost_count = Fine.objects.filter(book_title=obj.title, status='pending').count()
        if lost_count > 0:
            return format_html('<span style="color: #dc3545;">{} lost</span>', lost_count)
        return '0'
    lost_books_count.short_description = 'Lost Reports'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'books_count', 'fines_count', 'total_fines')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_per_page = 25
    
    def books_count(self, obj):
        return len(obj.books) if obj.books else 0
    books_count.short_description = 'Books Borrowed'
    
    def fines_count(self, obj):
        return obj.fines.filter(status='pending').count()
    fines_count.short_description = 'Pending Fines'
    
    def total_fines(self, obj):
        total = sum(fine.amount for fine in obj.fines.filter(status='pending'))
        if total > 0:
            return format_html('<span style="color: #dc3545;">₹{}</span>', total)
        return '₹0'
    total_fines.short_description = 'Total Pending Fines'

# Register models with the default admin site
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Fine, FineAdmin)
admin.site.register(Librarian)
