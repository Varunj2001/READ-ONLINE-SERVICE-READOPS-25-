from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    # store uploads under MEDIA_ROOT/book_covers/ (avoid double 'media/media' path)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    books = models.JSONField(default=list)
    notifications = models.JSONField(default=list, blank=True)
    cart = models.JSONField(default=list)  # Shopping cart for books
    is_librarian = models.BooleanField(default=False)  # Add this field for Librarian identification

    def __str__(self):
        return self.username
    
    @property
    def safe_notifications(self):
        """Ensure notifications is always a list"""
        if not isinstance(self.notifications, list):
            self.notifications = []
            self.save()
        return self.notifications
    
    def add_to_cart(self, book):
        """Add book to user's cart"""
        cart_item = {
            'book_id': book.id,
            'title': book.title,
            'author': book.author,
            'image': book.image.url if book.image else None,
            'department': book.department,
            'subject': book.subject,
            'added_date': timezone.now().isoformat(),
        }
        
        # Check if book is already in cart
        for item in self.cart:
            if item.get('book_id') == book.id:
                return False  # Book already in cart
        
        self.cart.append(cart_item)
        self.save()
        return True
    
    def remove_from_cart(self, book_id):
        """Remove book from user's cart"""
        original_length = len(self.cart)
        self.cart = [item for item in self.cart if item.get('book_id') != book_id]
        if len(self.cart) < original_length:
            self.save()
            return True
        return False
    
    def clear_cart(self):
        """Clear user's cart"""
        self.cart = []
        self.save()
    
    def take_book(self, book):
        start_date = timezone.now()
        end_date = start_date + timezone.timedelta(days=7)  # Changed from 10 to 7 days

        book_info = {
            'title': book.title,
            'id': book.id,
            'image': book.image.url if book.image else None,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }

        self.books.append(book_info)
        self.save()
    
    def extend_book(self, book_id, days=7):
        """Extend book return date"""
        for book in self.books:
            if book.get('id') == book_id:
                current_end_date = timezone.datetime.fromisoformat(book['end_date'])
                new_end_date = current_end_date + timezone.timedelta(days=days)
                book['end_date'] = new_end_date.isoformat()
                book['extended'] = book.get('extended', 0) + 1
                self.save()
                return True
        return False
    
    def return_book(self, book_id):
        """Return a book and remove it from user's books list"""
        original_length = len(self.books)
        # Normalize to string to avoid int/str mismatches from POST data
        target_id = str(book_id)
        self.books = [book for book in self.books if str(book.get('id')) != target_id]
        if len(self.books) < original_length:
            self.save()
            return True
        return False

# Model for Librarian
class Librarian(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

# Model for Payment
class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('LOST', 'Lost Book Payment'),
        ('FINE', 'Late Return Fine'),
        ('PURCHASE', 'Book Purchase'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('netbanking', 'Net Banking'),
        ('upi', 'UPI Payment'),
        ('wallet', 'Digital Wallet'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    book_title = models.CharField(max_length=100)  # Store book title separately in case book is deleted
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    bank_name = models.CharField(max_length=100, blank=True, null=True)  # For net banking
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.payment_type} - {self.book_title}"

# Model for Fine
class Fine(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fines')
    book_title = models.CharField(max_length=100)
    book_id = models.IntegerField(null=True, blank=True)  # Store book ID for reference
    due_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('5.00'))
    days_overdue = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.book_title} - {self.amount}"
        
    def calculate_fine(self):
        """Calculate fine based on days overdue"""
        if self.days_overdue <= 0:
            return Decimal('0.00')
        
        # Base fine of 5.00
        fine_amount = Decimal('5.00')
        
        # Add 5.00 for every 5 days overdue
        additional_periods = (self.days_overdue - 1) // 5
        fine_amount += Decimal('5.00') * additional_periods
        
        return fine_amount

# Model for Digital Books
class DigitalBook(models.Model):
    BOOK_TYPE_CHOICES = [
        ('RELIGIOUS', 'Religious/Spiritual'),
        ('EDUCATIONAL', 'Educational'),
        ('LITERATURE', 'Literature'),
        ('TECHNICAL', 'Technical'),
        ('OTHER', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    book_type = models.CharField(max_length=20, choices=BOOK_TYPE_CHOICES)
    category = models.CharField(max_length=100)  # e.g., "Hindu Scriptures", "Programming"
    cover_image = models.ImageField(upload_to='digital_book_covers/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='digital_books/pdf/', blank=True, null=True)
    word_file = models.FileField(upload_to='digital_books/word/', blank=True, null=True)
    online_reading_price = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    download_price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

# Model for Digital Book Access
class DigitalBookAccess(models.Model):
    ACCESS_TYPE_CHOICES = [
        ('ONLINE_READING', 'Online Reading'),
        ('DOWNLOAD', 'Download'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='digital_access')
    digital_book = models.ForeignKey(DigitalBook, on_delete=models.CASCADE, related_name='access_records')
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    access_start_date = models.DateTimeField()
    access_end_date = models.DateTimeField()
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.digital_book.title} - {self.access_type}"
    
    def is_access_valid(self):
        """Check if the access is still valid"""
        from django.utils import timezone
        return self.status == 'ACTIVE' and timezone.now() < self.access_end_date

# Model for QR Code Payments
class QRPayment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('EXPIRED', 'Expired'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='qr_payments')
    digital_book_access = models.ForeignKey(DigitalBookAccess, on_delete=models.CASCADE, related_name='qr_payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code_data = models.TextField()  # QR code data for payment
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"QR Payment - {self.user.username} - {self.amount}"
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

# Model for Mobile Notifications
class MobileNotification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('BOOK_BORROWED', 'Book Borrowed'),
        ('BOOK_RETURNED', 'Book Returned'),
        ('BOOK_OVERDUE', 'Book Overdue'),
        ('FINE_IMPOSED', 'Fine Imposed'),
        ('REMINDER', 'Reminder'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED', 'Expired'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mobile_notifications')
    bima_id = models.CharField(max_length=20, unique=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    book_title = models.CharField(max_length=100, blank=True, null=True)
    book_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_date = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    response_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"BIMA-{self.bima_id} - {self.user.username} - {self.title}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def generate_bima_id(self):
        """Generate a unique BIMA ID"""
        import random
        import string
        
        # Generate random alphanumeric string
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        bima_id = f"BIMA-{random_part}"
        
        # Ensure uniqueness
        while MobileNotification.objects.filter(bima_id=bima_id).exists():
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            bima_id = f"BIMA-{random_part}"
        
        return bima_id
    
    def save(self, *args, **kwargs):
        if not self.bima_id:
            self.bima_id = self.generate_bima_id()
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)  # 24 hours expiry
        super().save(*args, **kwargs)


# QR Code Models for User Identification and Tracking
class UserQRCode(models.Model):
    """Model to store user QR codes for identification"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='qr_code')
    qr_code_data = models.TextField(help_text="QR code data containing user information")
    qr_code_image = models.ImageField(upload_to='user_qr_codes/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"QR Code - {self.user.username}"
    
    def generate_qr_data(self):
        """Generate QR code data with user information"""
        import json
        from django.utils import timezone
        
        user_data = {
            'user_id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'phone': self.user.phone,
            'full_name': f"{self.user.first_name} {self.user.last_name}".strip(),
            'is_librarian': self.user.is_librarian,
            'created_date': (self.created_date or timezone.now()).isoformat(),
        }
        return json.dumps(user_data)
    
    def save(self, *args, **kwargs):
        if not self.qr_code_data:
            self.qr_code_data = self.generate_qr_data()
        super().save(*args, **kwargs)


class QRScanLog(models.Model):
    """Model to track QR code scans by librarians"""
    SCAN_TYPE_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CHECK_IN', 'Check In'),
        ('CHECK_OUT', 'Check Out'),
        ('VERIFICATION', 'Verification'),
    ]
    
    scanned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scan_logs')
    scanned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scans_performed')
    scan_type = models.CharField(max_length=20, choices=SCAN_TYPE_CHOICES, default='VERIFICATION')
    scan_timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, blank=True, null=True, help_text="Location where scan occurred")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the scan")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-scan_timestamp']
        verbose_name = "QR Scan Log"
        verbose_name_plural = "QR Scan Logs"
    
    def __str__(self):
        return f"{self.scanned_user.username} - {self.scan_type} by {self.scanned_by.username} at {self.scan_timestamp}"
    
    @property
    def scan_date(self):
        return self.scan_timestamp.date()
    
    @property
    def scan_time(self):
        return self.scan_timestamp.time()
