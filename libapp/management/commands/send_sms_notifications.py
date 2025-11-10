"""
Django management command to send SMS notifications for overdue books and fines
Run with: python manage.py send_sms_notifications
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from libapp.models import CustomUser, Fine
from libapp.sms_service import sms_service

class Command(BaseCommand):
    help = 'Send SMS notifications for overdue books and pending fines'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending SMS',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No SMS will be sent'))
        
        # Send fine reminders
        self.send_fine_reminders(dry_run)
        
        # Send overdue book reminders
        self.send_overdue_reminders(dry_run)
        
        self.stdout.write(self.style.SUCCESS('SMS notification process completed'))

    def send_fine_reminders(self, dry_run=False):
        """Send SMS reminders for pending fines"""
        pending_fines = Fine.objects.filter(status='PENDING')
        
        self.stdout.write(f'Found {pending_fines.count()} pending fines')
        
        for fine in pending_fines:
            if dry_run:
                self.stdout.write(f'Would send fine reminder to {fine.user.username} ({fine.user.phone})')
            else:
                try:
                    success = sms_service.send_fine_reminder_sms(fine.user, fine)
                    if success:
                        self.stdout.write(f'✅ Fine reminder sent to {fine.user.username}')
                    else:
                        self.stdout.write(f'❌ Failed to send fine reminder to {fine.user.username}')
                except Exception as e:
                    self.stdout.write(f'❌ Error sending fine reminder to {fine.user.username}: {str(e)}')

    def send_overdue_reminders(self, dry_run=False):
        """Send SMS reminders for overdue books"""
        today = timezone.now().date()
        overdue_users = []
        
        # Find users with overdue books
        for user in CustomUser.objects.filter(is_librarian=False):
            overdue_books = []
            for book in user.books:
                end_date_str = book.get('end_date')
                if end_date_str:
                    try:
                        end_date = timezone.datetime.fromisoformat(end_date_str.replace('Z', '+00:00')).date()
                        if end_date < today:
                            overdue_books.append(book)
                    except:
                        continue
            
            if overdue_books:
                overdue_users.append((user, overdue_books))
        
        self.stdout.write(f'Found {len(overdue_users)} users with overdue books')
        
        for user, overdue_books in overdue_users:
            if dry_run:
                self.stdout.write(f'Would send overdue reminder to {user.username} ({user.phone}) for {len(overdue_books)} books')
            else:
                try:
                    # Send reminder for each overdue book
                    for book in overdue_books:
                        success = sms_service.send_overdue_reminder_sms(user, book)
                        if success:
                            self.stdout.write(f'✅ Overdue reminder sent to {user.username} for "{book.get("title", "Unknown")}"')
                        else:
                            self.stdout.write(f'❌ Failed to send overdue reminder to {user.username}')
                except Exception as e:
                    self.stdout.write(f'❌ Error sending overdue reminder to {user.username}: {str(e)}')
