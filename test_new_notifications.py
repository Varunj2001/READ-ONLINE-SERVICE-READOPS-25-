#!/usr/bin/env python
"""
Test script for new notification features
Tests book purchase, login, registration, and due date reminders
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from libapp.notification_manager import notification_manager
from libapp.models import CustomUser

def test_registration_notifications():
    """Test registration notifications"""
    print("=" * 60)
    print("TESTING REGISTRATION NOTIFICATIONS")
    print("=" * 60)
    
    # Get a test user
    user = CustomUser.objects.first()
    if user:
        print(f"Testing with user: {user.username} ({user.email})")
        result = notification_manager.send_registration_notifications(user)
        if result:
            print("✅ Registration notifications sent successfully")
        else:
            print("❌ Registration notifications failed")
    else:
        print("⚠️  No users found for testing")

def test_login_notifications():
    """Test login notifications"""
    print("\n" + "=" * 60)
    print("TESTING LOGIN NOTIFICATIONS")
    print("=" * 60)
    
    user = CustomUser.objects.first()
    if user:
        print(f"Testing with user: {user.username} ({user.email})")
        result = notification_manager.send_login_notifications(user)
        if result:
            print("✅ Login notifications sent successfully")
        else:
            print("❌ Login notifications failed")
    else:
        print("⚠️  No users found for testing")

def test_book_purchase_notifications():
    """Test book purchase notifications"""
    print("\n" + "=" * 60)
    print("TESTING BOOK PURCHASE NOTIFICATIONS")
    print("=" * 60)
    
    user = CustomUser.objects.first()
    if user:
        print(f"Testing with user: {user.username} ({user.email})")
        result = notification_manager.send_book_purchase_notifications(
            user=user,
            book_title="Advanced Computer Science",
            amount=299,
            payment_method="Credit Card"
        )
        if result:
            print("✅ Book purchase notifications sent successfully")
        else:
            print("❌ Book purchase notifications failed")
    else:
        print("⚠️  No users found for testing")

def test_due_date_reminders():
    """Test due date reminder notifications"""
    print("\n" + "=" * 60)
    print("TESTING DUE DATE REMINDER NOTIFICATIONS")
    print("=" * 60)
    
    user = CustomUser.objects.first()
    if user:
        print(f"Testing with user: {user.username} ({user.email})")
        
        # Test different scenarios
        test_cases = [
            ("Advanced Computer Science", datetime.now().date() + timedelta(days=1), 1),  # Due tomorrow
            ("Digital Design", datetime.now().date() - timedelta(days=2), -2),  # Overdue
            ("Computer Networks", datetime.now().date() + timedelta(days=5), 5),  # Due in 5 days
        ]
        
        for book_title, due_date, days_remaining in test_cases:
            print(f"\nTesting: {book_title} (Due: {due_date}, Days: {days_remaining})")
            result = notification_manager.send_due_date_reminders(
                user=user,
                book_title=book_title,
                due_date=due_date,
                days_remaining=days_remaining
            )
            if result:
                print(f"✅ Due date reminder sent successfully for {book_title}")
            else:
                print(f"❌ Due date reminder failed for {book_title}")
    else:
        print("⚠️  No users found for testing")

def test_payment_notifications():
    """Test payment success notifications"""
    print("\n" + "=" * 60)
    print("TESTING PAYMENT SUCCESS NOTIFICATIONS")
    print("=" * 60)
    
    user = CustomUser.objects.first()
    if user:
        print(f"Testing with user: {user.username} ({user.email})")
        result = notification_manager.send_payment_success_notifications(
            user=user,
            amount=150,
            payment_method="UPI",
            book_title="Data Structures and Algorithms"
        )
        if result:
            print("✅ Payment success notifications sent successfully")
        else:
            print("❌ Payment success notifications failed")
    else:
        print("⚠️  No users found for testing")

def main():
    """Main test function"""
    print("ReadOps Library Management System - New Notification Features Test")
    print("=" * 80)
    print("Testing notifications from: arjun5shetty29@gmail.com")
    print("=" * 80)
    
    # Test all notification types
    test_registration_notifications()
    test_login_notifications()
    test_book_purchase_notifications()
    test_due_date_reminders()
    test_payment_notifications()
    
    print("\n" + "=" * 80)
    print("NOTIFICATION FEATURES TEST COMPLETED")
    print("=" * 80)
    print("\n📧 Email notifications will be sent from: arjun5shetty29@gmail.com")
    print("📱 SMS notifications will show success messages")
    print("\nNext steps:")
    print("1. Check the console output above for any errors")
    print("2. Configure Gmail App Password for arjun5shetty29@gmail.com")
    print("3. Test with real SMS provider if needed")
    print("4. Integrate these notifications into your views")

if __name__ == "__main__":
    main()
