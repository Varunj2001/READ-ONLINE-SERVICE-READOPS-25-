#!/usr/bin/env python3
"""
SMS Configuration Script for ReadOps Library
This script helps you configure SMS settings to send real SMS messages
"""

import os
import sys

def configure_sms():
    print("📱 ReadOps SMS Configuration")
    print("=" * 50)
    print()
    
    print("Choose your SMS provider:")
    print("1. TextLocal (Recommended for India) - ₹0.15-0.20 per SMS")
    print("2. Fast2SMS (Free for India) - Limited free SMS")
    print("3. Twilio (International) - $0.0075 per SMS")
    print("4. Keep Mock Mode (Console output only)")
    print()
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == "1":
        configure_textlocal()
    elif choice == "2":
        configure_fast2sms()
    elif choice == "3":
        configure_twilio()
    elif choice == "4":
        print("✅ Keeping Mock Mode - SMS will only show in console")
    else:
        print("❌ Invalid choice. Keeping Mock Mode.")
    
    print("\n🎉 Configuration complete!")
    print("📱 SMS will be sent from 'ReadOps' to your registered mobile number: 7204310480")

def configure_textlocal():
    print("\n🔧 Configuring TextLocal...")
    print("1. Sign up at: https://www.textlocal.in/")
    print("2. Get your API key from the dashboard")
    print("3. Enter your API key below:")
    
    api_key = input("TextLocal API Key: ").strip()
    
    if api_key:
        update_settings("textlocal", {
            "TEXTLOCAL_API_KEY": api_key,
            "TEXTLOCAL_SENDER": "ReadOps"
        })
        print("✅ TextLocal configured successfully!")
    else:
        print("❌ No API key provided. Keeping Mock Mode.")

def configure_fast2sms():
    print("\n🔧 Configuring Fast2SMS...")
    print("1. Sign up at: https://www.fast2sms.com/")
    print("2. Get your API key from the dashboard")
    print("3. Enter your API key below:")
    
    api_key = input("Fast2SMS API Key: ").strip()
    
    if api_key:
        update_settings("fast2sms", {
            "FAST2SMS_API_KEY": api_key
        })
        print("✅ Fast2SMS configured successfully!")
    else:
        print("❌ No API key provided. Keeping Mock Mode.")

def configure_twilio():
    print("\n🔧 Configuring Twilio...")
    print("1. Sign up at: https://www.twilio.com/")
    print("2. Get your Account SID, Auth Token, and Phone Number")
    print("3. Enter your credentials below:")
    
    account_sid = input("Twilio Account SID: ").strip()
    auth_token = input("Twilio Auth Token: ").strip()
    from_number = input("Twilio Phone Number (e.g., +1234567890): ").strip()
    
    if account_sid and auth_token and from_number:
        update_settings("twilio", {
            "TWILIO_ACCOUNT_SID": account_sid,
            "TWILIO_AUTH_TOKEN": auth_token,
            "TWILIO_FROM_NUMBER": from_number
        })
        print("✅ Twilio configured successfully!")
    else:
        print("❌ Incomplete credentials. Keeping Mock Mode.")

def update_settings(provider, config):
    """Update Django settings with SMS configuration"""
    settings_file = "library/settings.py"
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Update SMS_PROVIDER
        content = content.replace("SMS_PROVIDER = 'mock'", f"SMS_PROVIDER = '{provider}'")
        
        # Update configuration values
        for key, value in config.items():
            content = content.replace(f"{key} = ''", f"{key} = '{value}'")
        
        with open(settings_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {settings_file} with {provider} configuration")
        
    except Exception as e:
        print(f"❌ Error updating settings: {str(e)}")
        print("Please manually update library/settings.py with your SMS provider configuration")

if __name__ == "__main__":
    configure_sms()
