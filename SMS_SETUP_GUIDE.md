# 📱 SMS Setup Guide for ReadOps Library

## Current Status
- ✅ SMS service is configured and ready
- ✅ Sender ID: "ReadOps" 
- ✅ Phone number formatting: +91 (India)
- ⚠️ Currently in MOCK mode (console output only)

## To Send Real SMS to Your Mobile Phone:

### Option 1: TextLocal (Recommended for India)
1. **Sign up at**: https://www.textlocal.in/
2. **Get API Key**: Login → API → Get API Key
3. **Update settings.py**:
   ```python
   SMS_PROVIDER = 'textlocal'
   TEXTLOCAL_API_KEY = 'your-api-key-here'
   TEXTLOCAL_SENDER = 'ReadOps'
   ```

### Option 2: Fast2SMS (Free for India)
1. **Sign up at**: https://www.fast2sms.com/
2. **Get API Key**: Dashboard → API Key
3. **Update settings.py**:
   ```python
   SMS_PROVIDER = 'fast2sms'
   FAST2SMS_API_KEY = 'your-api-key-here'
   ```

### Option 3: Twilio (International)
1. **Sign up at**: https://www.twilio.com/
2. **Get credentials**: Console → Account Info
3. **Update settings.py**:
   ```python
   SMS_PROVIDER = 'twilio'
   TWILIO_ACCOUNT_SID = 'your-account-sid'
   TWILIO_AUTH_TOKEN = 'your-auth-token'
   TWILIO_FROM_NUMBER = '+1234567890'  # Your Twilio number
   ```

## Test SMS Functionality

### Method 1: Web Interface
1. Go to: http://127.0.0.1:8000/dashboard/
2. Click "Test SMS Notifications" button
3. Click "Send Test SMS"

### Method 2: Command Line
```bash
python manage.py test_sms_all_users --user your_username
```

## SMS Messages You'll Receive

### Registration Welcome
```
From: ReadOps

Welcome to ReadOps Library! 🎉

Hello [username],
Your account has been successfully created.

📚 Access thousands of books
🔍 Smart search and AI recommendations
📱 Mobile notifications for all activities
💳 Secure payment options

Start exploring: http://127.0.0.1:8000

- ReadOps Team
```

### Book Borrowed
```
From: ReadOps

📚 Book Borrowed Successfully!

Hello [username],
You have borrowed: "[book title]"
Author: [author name]

🆔 Transaction ID: BIMA-ABC12345
📅 Due Date: 2024-01-15

Please return the book on time to avoid fines.

- ReadOps Library
```

### Payment Confirmation
```
From: ReadOps

💳 Payment Successful!

Hello [username],
Payment of ₹[amount] for '[book title]' has been processed successfully.

💳 Payment Method: [payment method]
📅 Date: 2024-01-10 14:30:00

Thank you for your payment!

- ReadOps Library
```

## Troubleshooting

### If SMS not received:
1. Check phone number format (should be 10 digits)
2. Verify SMS provider credentials
3. Check console output for errors
4. Ensure SMS_ENABLED = True in settings

### Current Phone Number:
- Your registered number: 7204310480
- Formatted for SMS: +917204310480

## Cost Information
- **TextLocal**: ₹0.15-0.20 per SMS
- **Fast2SMS**: Free (with limitations)
- **Twilio**: $0.0075 per SMS (international)

Choose the provider that works best for your needs!
