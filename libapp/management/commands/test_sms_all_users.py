"""
Django management command to test SMS for all users
Run with: python manage.py test_sms_all_users
"""

from django.core.management.base import BaseCommand
from libapp.models import CustomUser
from libapp.sms_service import sms_service

class Command(BaseCommand):
    help = 'Send test SMS to all registered users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Test SMS for specific username only',
        )

    def handle(self, *args, **options):
        username = options.get('user')
        
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                users = [user]
                self.stdout.write(f'Testing SMS for user: {username}')
            except CustomUser.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User {username} not found'))
                return
        else:
            users = CustomUser.objects.filter(is_librarian=False)
            self.stdout.write(f'Testing SMS for {users.count()} users')
        
        for user in users:
            self.stdout.write(f'\n📱 Testing SMS for: {user.username} ({user.phone})')
            try:
                success = sms_service.send_registration_sms(user)
                if success:
                    self.stdout.write(self.style.SUCCESS(f'✅ SMS test successful for {user.username}'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ SMS test failed for {user.username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error testing SMS for {user.username}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 SMS testing completed!'))
