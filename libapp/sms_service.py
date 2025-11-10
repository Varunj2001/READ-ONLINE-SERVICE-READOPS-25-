"""
SMS Notification Service for ReadOps Library Management System
Handles sending SMS notifications to registered mobile numbers
"""

import requests
import json
from django.conf import settings
from django.utils import timezone
from .models import MobileNotification

class SMSService:
    """
    SMS Service for sending notifications to mobile numbers
    Uses a mock SMS service for demonstration purposes
    In production, integrate with services like Twilio, AWS SNS, or local SMS providers
    """
    
    def __init__(self):
        # SMS configuration - supports multiple providers
        self.sender_id = "ReadOps"  # Sender ID for SMS
        
        # Get SMS provider from settings (default: 'mock')
        self.provider = getattr(settings, 'SMS_PROVIDER', 'mock')
        
        if self.provider == 'twilio':
            # Twilio configuration
            self.api_url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
            self.account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
            self.auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
            self.from_number = getattr(settings, 'TWILIO_FROM_NUMBER', '')
            
        elif self.provider == 'textlocal':
            # TextLocal configuration
            self.api_url = "https://api.textlocal.in/send/"
            self.api_key = getattr(settings, 'TEXTLOCAL_API_KEY', '')
            self.sender = getattr(settings, 'TEXTLOCAL_SENDER', 'ReadOps')
            
        elif self.provider == 'fast2sms':
            # Fast2SMS configuration
            self.api_url = "https://www.fast2sms.com/dev/bulk"
            self.api_key = getattr(settings, 'FAST2SMS_API_KEY', '')
            
        else:
            # Mock configuration (default)
            self.api_url = "https://api.sms-service.com/send"  # Mock URL
            self.api_key = "your-sms-api-key"  # Replace with actual API key
        
    def send_sms(self, phone_number, message):
        """
        Send SMS to the given phone number
        Returns True if successful, False otherwise
        """
        try:
            # Check if SMS is enabled in settings
            if not getattr(settings, 'SMS_ENABLED', True):
                print("📱 SMS disabled in settings")
                return True  # Return success but don't send
            
            # Clean phone number (remove spaces, dashes, etc.)
            clean_phone = ''.join(filter(str.isdigit, phone_number))
            
            # Add country code if not present (assuming India +91)
            if not clean_phone.startswith('91') and len(clean_phone) == 10:
                clean_phone = '91' + clean_phone
            
            # Send SMS based on provider
            if self.provider == 'twilio':
                return self._send_twilio_sms(clean_phone, message)
            elif self.provider == 'textlocal':
                return self._send_textlocal_sms(clean_phone, message)
            elif self.provider == 'fast2sms':
                return self._send_fast2sms(clean_phone, message)
            else:
                # Mock SMS sending
                print(f"📱 SMS NOTIFICATION (MOCK MODE):")
                print(f"   📞 TO: {clean_phone}")
                print(f"   📝 MESSAGE: {message}")
                print(f"   🔗 SENDER: {self.sender_id}")
                print(f"   ✅ STATUS: SMS would be sent successfully")
                print(f"✅ SMS SENT SUCCESSFULLY TO: {clean_phone}")
                print("=" * 50)
                return True  # Mock success
            
        except Exception as e:
            print(f"❌ SMS sending failed: {str(e)}")
            return False
    
    def _send_twilio_sms(self, phone_number, message):
        """Send SMS using Twilio"""
        try:
            import base64
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=self.from_number,
                to=f'+{phone_number}'
            )
            
            print(f"📱 Twilio SMS sent successfully: {message_obj.sid}")
            print(f"✅ SMS SENT SUCCESSFULLY TO: {phone_number}")
            return True
            
        except Exception as e:
            print(f"❌ Twilio SMS failed: {str(e)}")
            return False
    
    def _send_textlocal_sms(self, phone_number, message):
        """Send SMS using TextLocal"""
        try:
            data = {
                'apikey': self.api_key,
                'numbers': phone_number,
                'message': message,
                'sender': self.sender
            }
            
            response = requests.post(self.api_url, data=data)
            result = response.json()
            
            if result.get('status') == 'success':
                print(f"📱 TextLocal SMS sent successfully")
                print(f"✅ SMS SENT SUCCESSFULLY TO: {phone_number}")
                return True
            else:
                print(f"❌ TextLocal SMS failed: {result.get('errors', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ TextLocal SMS failed: {str(e)}")
            return False
    
    def _send_fast2sms(self, phone_number, message):
        """Send SMS using Fast2SMS"""
        try:
            headers = {
                'authorization': self.api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'route': 'q',
                'message': message,
                'language': 'english',
                'numbers': phone_number
            }
            
            response = requests.post(self.api_url, headers=headers, data=data)
            result = response.json()
            
            if result.get('return') == True:
                print(f"📱 Fast2SMS sent successfully")
                print(f"✅ SMS SENT SUCCESSFULLY TO: {phone_number}")
                return True
            else:
                print(f"❌ Fast2SMS failed: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Fast2SMS failed: {str(e)}")
            return False
    
    def send_registration_sms(self, user):
        """Send welcome SMS after successful registration"""
        message = f"""
Welcome to ReadOps Library! 🎉

Hello {user.username},
Your account has been successfully created.

📚 Access thousands of books
🔍 Smart search and AI recommendations  
📱 Mobile notifications for all activities
💳 Secure payment options

Start exploring: {settings.SITE_URL}

- ReadOps Team
        """.strip()
        
        return self.send_sms(user.phone, message)
    
    def send_book_borrowed_sms(self, user, book, bima_id):
        """Send SMS when user borrows a book"""
        message = f"""
📚 Book Borrowed Successfully!

Hello {user.username},
You have borrowed: "{book.title}"
Author: {book.author}

🆔 Transaction ID: {bima_id}
📅 Due Date: {book.get('end_date', 'N/A')}

Please return the book on time to avoid fines.

- ReadOps Library
        """.strip()
        
        return self.send_sms(user.phone, message)
    
    def send_book_returned_sms(self, user, book, bima_id):
        """Send SMS when user returns a book"""
        message = f"""
✅ Book Returned Successfully!

Hello {user.username},
You have returned: "{book.title}"
Author: {book.author}

🆔 Transaction ID: {bima_id}
📅 Return Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}

Thank you for using ReadOps Library!

- ReadOps Team
        """.strip()
        
        return self.send_sms(user.phone, message)
    
    def send_payment_success_sms(self, user, amount, payment_method, book_title=None):
        """Send SMS when payment is successful"""
        payment_info = ""
        if book_title:
            payment_info = f"for '{book_title}'"
        
        method_text = {
            'card': 'Credit/Debit Card',
            'netbanking': 'Net Banking',
            'upi': 'UPI Payment',
            'wallet': 'Digital Wallet'
        }.get(payment_method, payment_method)
        
        message = f"""
💳 Payment Successful!

Hello {user.username},
Payment of ₹{amount} {payment_info} has been processed successfully.

💳 Payment Method: {method_text}
📅 Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}

Thank you for your payment!

- ReadOps Library
        """.strip()
        
        return self.send_sms(user.phone, message)
    
    def send_fine_reminder_sms(self, user, fine):
        """Send SMS for fine reminders"""
        message = f"""
⚠️ Fine Reminder

Hello {user.username},
You have a pending fine for: "{fine.book_title}"

💰 Amount: ₹{fine.amount}
📅 Due Date: {fine.due_date.strftime('%Y-%m-%d')}
📊 Days Overdue: {fine.days_overdue}

Please pay the fine to avoid further restrictions.

- ReadOps Library
        """.strip()
        
        return self.send_sms(user.phone, message)
    
    def send_overdue_reminder_sms(self, user, book):
        """Send SMS for overdue book reminders"""
        message = f"""
📚 Book Overdue Reminder

Hello {user.username},
The book "{book.get('title', 'Unknown')}" is overdue.

📅 Due Date: {book.get('end_date', 'N/A')}
⚠️ Please return the book immediately to avoid fines.

- ReadOps Library
        """.strip()
        
        return self.send_sms(user.phone, message)
    
    def send_book_purchase_sms(self, user, book_title, amount, payment_method):
        """Send SMS notification for book purchase"""
        message = f"""
📚 Book Purchase Confirmation

Hello {user.username},
Your book "{book_title}" has been successfully purchased for ₹{amount}.

Payment: {payment_method}
Date: {timezone.now().strftime('%Y-%m-%d')}

Access your book from the digital library.

- ReadOps Library
        """.strip()
        
        return self.send_sms(user.phone, message)
    
    def send_login_notification_sms(self, user, login_time):
        """Send SMS notification for successful login"""
        message = f"""
🔐 Login Notification

Hello {user.username},
You have successfully logged into ReadOps Library.

Time: {login_time.strftime('%Y-%m-%d %H:%M')}

If this wasn't you, contact us immediately.

- ReadOps Library
        """.strip()
        
        return self.send_sms(user.phone, message)
    
    def send_due_date_reminder_sms(self, user, book_title, due_date, days_remaining):
        """Send SMS reminder for book due date"""
        if days_remaining <= 0:
            urgency = "OVERDUE"
            action = "Return immediately to avoid fines!"
        elif days_remaining == 1:
            urgency = "DUE TOMORROW"
            action = "Please return tomorrow."
        else:
            urgency = f"DUE IN {days_remaining} DAYS"
            action = "Please return on time."
        
        message = f"""
⚠️ Book Return Reminder

Hello {user.username},
Book: "{book_title}"
Due: {due_date.strftime('%Y-%m-%d')}
Status: {urgency}

{action}

- ReadOps Library
        """.strip()
        
        return self.send_sms(user.phone, message)

# Global SMS service instance
sms_service = SMSService()
