"""
Django management command to test email and SMS notifications
Run with: python manage.py test_notifications
"""

from django.core.management.base import BaseCommand
from libapp.email_service import email_service
from libapp.sms_service import sms_service
from libapp.models import CustomUser

class Command(BaseCommand):
    help = 'Test email and SMS notification functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to test with',
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to test with',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing ReadOps Notifications'))
        self.stdout.write('=' * 50)
        
        # Test email
        test_email = options.get('email', 'test@example.com')
        self.stdout.write(f'\n📧 Testing email to: {test_email}')
        
        email_result = email_service.send_email(
            to_email=test_email,
            subject='ReadOps Test Email',
            message='This is a test email from ReadOps Library Management System.'
        )
        
        if email_result:
            self.stdout.write(self.style.SUCCESS('✅ Email test PASSED'))
        else:
            self.stdout.write(self.style.ERROR('❌ Email test FAILED'))
        
        # Test SMS
        test_phone = options.get('phone', '1234567890')
        self.stdout.write(f'\n📱 Testing SMS to: {test_phone}')
        
        sms_result = sms_service.send_sms(
            phone_number=test_phone,
            message='Test SMS from ReadOps Library Management System'
        )
        
        if sms_result:
            self.stdout.write(self.style.SUCCESS('✅ SMS test PASSED'))
        else:
            self.stdout.write(self.style.ERROR('❌ SMS test FAILED'))
        
        # Test with actual users
        self.stdout.write('\n👥 Testing with actual users...')
        users = CustomUser.objects.all()[:3]  # Test with first 3 users
        
        if users:
            for user in users:
                self.stdout.write(f'\nTesting with user: {user.username}')
                
                # Test email
                if user.email:
                    email_result = email_service.send_registration_email(user)
                    if email_result:
                        self.stdout.write(f'  ✅ Email to {user.email} - PASSED')
                    else:
                        self.stdout.write(f'  ❌ Email to {user.email} - FAILED')
                
                # Test SMS
                if hasattr(user, 'phone') and user.phone:
                    sms_result = sms_service.send_sms(
                        phone_number=user.phone,
                        message=f'Hello {user.username}! Test SMS from ReadOps.'
                    )
                    if sms_result:
                        self.stdout.write(f'  ✅ SMS to {user.phone} - PASSED')
                    else:
                        self.stdout.write(f'  ❌ SMS to {user.phone} - FAILED')
        else:
            self.stdout.write('⚠️  No users found in database')
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('Notification test completed!')
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Check the output above for any errors')
        self.stdout.write('2. If using real providers, check your email/phone')
        self.stdout.write('3. Update .env file with real credentials if needed')
