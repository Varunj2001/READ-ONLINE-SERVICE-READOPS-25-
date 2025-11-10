#!/usr/bin/env python
"""
Test script for email and SMS notifications
Run this script to test if email and SMS are working properly
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from libapp.email_service import email_service
from libapp.sms_service import sms_service
from libapp.models import CustomUser

def test_email():
    """Test email functionality"""
    print("=" * 50)
    print("TESTING EMAIL FUNCTIONALITY")
    print("=" * 50)
    
    # Create a test user
    test_email = "test@example.com"
    test_subject = "ReadOps Test Email"
    test_message = """
    Hello!
    
    This is a test email from ReadOps Library Management System.
    
    If you receive this email, the email functionality is working correctly!
    
    Best regards,
    ReadOps Team
    """
    
    try:
        result = email_service.send_email(
            to_email=test_email,
            subject=test_subject,
            message=test_message
        )
        
        if result:
            print("✅ Email test PASSED - Email would be sent successfully")
        else:
            print("❌ Email test FAILED - Email sending failed")
            
    except Exception as e:
        print(f"❌ Email test FAILED with error: {str(e)}")

def test_sms():
    """Test SMS functionality"""
    print("\n" + "=" * 50)
    print("TESTING SMS FUNCTIONALITY")
    print("=" * 50)
    
    test_phone = "1234567890"  # Test phone number
    test_message = """
    Hello! This is a test SMS from ReadOps Library Management System.
    If you receive this SMS, the SMS functionality is working correctly!
    - ReadOps Team
    """
    
    try:
        result = sms_service.send_sms(
            phone_number=test_phone,
            message=test_message
        )
        
        if result:
            print("✅ SMS test PASSED - SMS would be sent successfully")
        else:
            print("❌ SMS test FAILED - SMS sending failed")
            
    except Exception as e:
        print(f"❌ SMS test FAILED with error: {str(e)}")

def test_user_notifications():
    """Test notifications with actual user data"""
    print("\n" + "=" * 50)
    print("TESTING USER NOTIFICATIONS")
    print("=" * 50)
    
    try:
        # Get the first user from database
        user = CustomUser.objects.first()
        
        if user:
            print(f"Testing with user: {user.username} ({user.email})")
            
            # Test registration email
            print("\n📧 Testing registration email...")
            email_result = email_service.send_registration_email(user)
            
            if email_result:
                print("✅ Registration email test PASSED")
            else:
                print("❌ Registration email test FAILED")
            
            # Test SMS if user has phone number
            if hasattr(user, 'phone') and user.phone:
                print(f"\n📱 Testing SMS to {user.phone}...")
                sms_result = sms_service.send_sms(
                    phone_number=user.phone,
                    message="Test SMS from ReadOps Library Management System"
                )
                
                if sms_result:
                    print("✅ SMS test PASSED")
                else:
                    print("❌ SMS test FAILED")
            else:
                print("⚠️  No phone number found for user, skipping SMS test")
        else:
            print("⚠️  No users found in database, skipping user notification tests")
            
    except Exception as e:
        print(f"❌ User notification test FAILED with error: {str(e)}")

def main():
    """Main test function"""
    print("ReadOps Library Management System - Notification Test")
    print("=" * 60)
    
    # Test basic email functionality
    test_email()
    
    # Test basic SMS functionality
    test_sms()
    
    # Test with actual user data
    test_user_notifications()
    
    print("\n" + "=" * 60)
    print("NOTIFICATION TEST COMPLETED")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check the console output above for any errors")
    print("2. If using real email/SMS providers, check your email/phone")
    print("3. Update your .env file with real credentials for production use")
    print("4. See EMAIL_SMS_SETUP_GUIDE.md for detailed setup instructions")

if __name__ == "__main__":
    main()
