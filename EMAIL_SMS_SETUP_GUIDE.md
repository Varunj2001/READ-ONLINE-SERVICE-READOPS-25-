# Email and SMS Setup Guide for ReadOps Library Management System

This guide will help you configure email and SMS notifications for your ReadOps library system.

## Email Configuration

### 1. Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Copy the 16-character password

3. **Update your `.env` file** (create one in the project root):
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=ReadOps Library <your-email@gmail.com>
```

### 2. Alternative Email Providers

You can also use other SMTP providers by updating the settings in `library/settings.py`:

- **Outlook/Hotmail**: `smtp-mail.outlook.com`, port 587
- **Yahoo**: `smtp.mail.yahoo.com`, port 587
- **Custom SMTP**: Update `EMAIL_HOST` and `EMAIL_PORT` accordingly

## SMS Configuration

### 1. Mock Mode (Default - No Real SMS)
The system runs in mock mode by default, which prints SMS messages to the console instead of sending real SMS.

### 2. Twilio (Recommended for Production)

1. **Sign up** at [Twilio.com](https://www.twilio.com)
2. **Get your credentials** from the Twilio Console:
   - Account SID
   - Auth Token
   - Phone Number (for sending SMS)

3. **Update your `.env` file**:
```env
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_FROM_NUMBER=your-twilio-phone-number
```

### 3. TextLocal (India-focused)

1. **Sign up** at [TextLocal.in](https://www.textlocal.in)
2. **Get your API key** from the dashboard
3. **Update your `.env` file**:
```env
SMS_PROVIDER=textlocal
TEXTLOCAL_API_KEY=your-api-key
TEXTLOCAL_SENDER=ReadOps
```

### 4. Fast2SMS (India-focused)

1. **Sign up** at [Fast2SMS.com](https://www.fast2sms.com)
2. **Get your API key** from the dashboard
3. **Update your `.env` file**:
```env
SMS_PROVIDER=fast2sms
FAST2SMS_API_KEY=your-api-key
```

## Testing Your Configuration

### Test Email
1. Go to `/test-email/` in your browser
2. Click "Send Test Email"
3. Check your email inbox

### Test SMS
1. Go to `/test-sms/` in your browser
2. Click "Send Test SMS"
3. Check your phone for the SMS

## Troubleshooting

### Email Issues
- **Authentication Error**: Check your Gmail app password
- **Connection Error**: Verify your internet connection and SMTP settings
- **Spam Folder**: Check your spam/junk folder

### SMS Issues
- **API Key Error**: Verify your API credentials
- **Phone Number Format**: Ensure phone numbers include country code (e.g., +91 for India)
- **Provider Error**: Check if your SMS provider account has sufficient balance

## Environment Variables

Create a `.env` file in your project root with the following variables:

```env
# Django
SECRET_KEY=your-secret-key

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=ReadOps Library <your-email@gmail.com>

# SMS
SMS_PROVIDER=mock
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=
TEXTLOCAL_API_KEY=
TEXTLOCAL_SENDER=ReadOps
FAST2SMS_API_KEY=
```

## Production Considerations

1. **Use environment variables** for all sensitive credentials
2. **Enable HTTPS** for production
3. **Monitor email/SMS delivery** rates
4. **Set up proper error handling** and logging
5. **Consider rate limiting** for SMS to avoid spam

## Support

If you encounter issues:
1. Check the Django logs for error messages
2. Verify your credentials are correct
3. Test with a simple email/SMS first
4. Check your provider's documentation for specific requirements
