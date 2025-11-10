#!/usr/bin/env python
"""
Setup script for email and SMS credentials
This script helps you configure your email and SMS settings
"""

import os
import sys

def create_env_file():
    """Create .env file with template values"""
    env_content = """# Django Configuration
SECRET_KEY=your-secret-key-here

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=ReadOps Library <your-email@gmail.com>

# SMS Configuration
SMS_PROVIDER=mock  # Options: mock, twilio, textlocal, fast2sms

# Twilio Configuration (if using Twilio)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_FROM_NUMBER=your-twilio-phone-number

# TextLocal Configuration (if using TextLocal)
TEXTLOCAL_API_KEY=your-textlocal-api-key
TEXTLOCAL_SENDER=ReadOps

# Fast2SMS Configuration (if using Fast2SMS)
FAST2SMS_API_KEY=your-fast2sms-api-key
"""
    
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"⚠️  {env_file} already exists. Backing up to {env_file}.backup")
        os.rename(env_file, f"{env_file}.backup")
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created {env_file} with template values")
    return env_file

def interactive_setup():
    """Interactive setup for credentials"""
    print("=" * 60)
    print("ReadOps Library Management System - Credential Setup")
    print("=" * 60)
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        create_env_file()
    else:
        print("✅ .env file already exists")
    
    print("\n📧 EMAIL SETUP")
    print("-" * 30)
    print("To enable email notifications, you need to:")
    print("1. Use a Gmail account with 2-factor authentication enabled")
    print("2. Generate an App Password (not your regular password)")
    print("3. Update the .env file with your credentials")
    print("\nGmail App Password setup:")
    print("1. Go to https://myaccount.google.com/security")
    print("2. Enable 2-Step Verification if not already enabled")
    print("3. Go to App passwords and generate a new password for 'Mail'")
    print("4. Copy the 16-character password")
    print("5. Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env")
    
    print("\n📱 SMS SETUP")
    print("-" * 30)
    print("Current SMS provider: MOCK (no real SMS sent)")
    print("\nTo enable real SMS, choose a provider:")
    print("1. Twilio (Recommended) - Works globally")
    print("2. TextLocal - Good for India")
    print("3. Fast2SMS - Good for India")
    print("\nUpdate SMS_PROVIDER in .env file to your chosen provider")
    print("Add the corresponding API credentials")
    
    print("\n🔧 NEXT STEPS")
    print("-" * 30)
    print("1. Edit the .env file with your actual credentials")
    print("2. Run: python test_notifications.py")
    print("3. Check the test results")
    print("4. If successful, restart your Django server")
    
    print("\n📚 For detailed instructions, see: EMAIL_SMS_SETUP_GUIDE.md")

def main():
    """Main setup function"""
    try:
        interactive_setup()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")

if __name__ == "__main__":
    main()
