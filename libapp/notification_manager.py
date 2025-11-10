"""
Notification Manager for ReadOps Library Management System
Handles all types of notifications (email and SMS) for various events
"""

from django.utils import timezone
from datetime import timedelta
from .email_service import email_service
from .sms_service import sms_service
from .models import CustomUser

class NotificationManager:
    """
    Centralized notification manager for all library events
    """
    
    def __init__(self):
        self.email_service = email_service
        self.sms_service = sms_service
    
    def send_registration_notifications(self, user):
        """Send notifications for user registration"""
        print(f"📧📱 Sending registration notifications for {user.username}")
        
        # Send email
        email_result = self.email_service.send_registration_email(user)
        
        # Send SMS if user has phone number
        sms_result = True
        if hasattr(user, 'phone') and user.phone:
            sms_result = self.sms_service.send_registration_sms(user)
        
        return email_result and sms_result
    
    def send_login_notifications(self, user):
        """Send notifications for user login"""
        print(f"📧📱 Sending login notifications for {user.username}")
        
        login_time = timezone.now()
        
        # Send email
        email_result = self.email_service.send_login_notification_email(user, login_time)
        
        # Send SMS if user has phone number
        sms_result = True
        if hasattr(user, 'phone') and user.phone:
            sms_result = self.sms_service.send_login_notification_sms(user, login_time)
        
        return email_result and sms_result
    
    def send_book_purchase_notifications(self, user, book_title, amount, payment_method):
        """Send notifications for book purchase"""
        print(f"📧📱 Sending book purchase notifications for {user.username}")
        
        # Send email
        email_result = self.email_service.send_book_purchase_email(user, book_title, amount, payment_method)
        
        # Send SMS if user has phone number
        sms_result = True
        if hasattr(user, 'phone') and user.phone:
            sms_result = self.sms_service.send_book_purchase_sms(user, book_title, amount, payment_method)
        
        return email_result and sms_result
    
    def send_due_date_reminders(self, user, book_title, due_date, days_remaining):
        """Send notifications for book due date reminders"""
        print(f"📧📱 Sending due date reminders for {user.username}")
        
        # Send email
        email_result = self.email_service.send_due_date_reminder_email(user, book_title, due_date, days_remaining)
        
        # Send SMS if user has phone number
        sms_result = True
        if hasattr(user, 'phone') and user.phone:
            sms_result = self.sms_service.send_due_date_reminder_sms(user, book_title, due_date, days_remaining)
        
        return email_result and sms_result
    
    def send_fine_reminders(self, user, fine):
        """Send notifications for fine reminders"""
        print(f"📧📱 Sending fine reminders for {user.username}")
        
        # Send email
        email_result = self.email_service.send_fine_reminder_email(user, fine)
        
        # Send SMS if user has phone number
        sms_result = True
        if hasattr(user, 'phone') and user.phone:
            sms_result = self.sms_service.send_fine_reminder_sms(user, fine)
        
        return email_result and sms_result
    
    def send_overdue_reminders(self, user, book):
        """Send notifications for overdue book reminders"""
        print(f"📧📱 Sending overdue reminders for {user.username}")
        
        # Send email
        email_result = self.email_service.send_overdue_reminder_email(user, book)
        
        # Send SMS if user has phone number
        sms_result = True
        if hasattr(user, 'phone') and user.phone:
            sms_result = self.sms_service.send_overdue_reminder_sms(user, book)
        
        return email_result and sms_result
    
    def send_payment_success_notifications(self, user, amount, payment_method, book_title=None):
        """Send notifications for successful payment"""
        print(f"📧📱 Sending payment success notifications for {user.username}")
        
        # Send email
        email_result = self.email_service.send_payment_success_email(user, amount, payment_method, book_title)
        
        # Send SMS if user has phone number
        sms_result = True
        if hasattr(user, 'phone') and user.phone:
            sms_result = self.sms_service.send_payment_success_sms(user, amount, payment_method, book_title)
        
        return email_result and sms_result
    
    def send_bulk_due_date_reminders(self):
        """Send due date reminders to all users with books due soon"""
        print("📧📱 Sending bulk due date reminders...")
        
        # This would typically query the database for books due soon
        # For now, we'll just show the structure
        users_with_due_books = CustomUser.objects.all()  # Replace with actual query
        
        success_count = 0
        total_count = 0
        
        for user in users_with_due_books:
            # Check if user has books due soon
            # This is a placeholder - implement actual logic based on your book model
            if hasattr(user, 'borrowed_books'):
                for book in user.borrowed_books.all():
                    due_date = book.due_date  # Assuming this field exists
                    days_remaining = (due_date - timezone.now().date()).days
                    
                    if days_remaining <= 7:  # Send reminder if due within 7 days
                        total_count += 1
                        if self.send_due_date_reminders(user, book.title, due_date, days_remaining):
                            success_count += 1
        
        print(f"📊 Bulk reminders sent: {success_count}/{total_count} successful")
        return success_count, total_count

# Create a global instance
notification_manager = NotificationManager()
