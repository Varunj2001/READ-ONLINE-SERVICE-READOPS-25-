#!/usr/bin/env python3
"""
Send Real SMS to Mobile Number 7204310480
This script will send an actual SMS to your mobile phone
"""

import requests
import json

def send_sms_via_fast2sms():
    """Send SMS using Fast2SMS (Free for India)"""
    
    # Your mobile number
    phone_number = "7204310480"
    
    # Message to send
    message = """Welcome to ReadOps Library! 🎉

Hello readops,
Your account has been successfully created.

📚 Access thousands of books
🔍 Smart search and AI recommendations
📱 Mobile notifications for all activities
💳 Secure payment options

Start exploring: http://127.0.0.1:8000

- ReadOps Team"""
    
    print(f"📱 Sending SMS to: {phone_number}")
    print(f"📝 Message: {message[:50]}...")
    print()
    
    # Fast2SMS API (you need to get your API key from https://www.fast2sms.com/)
    api_key = "your-api-key-here"  # Replace with your actual API key
    
    if api_key == "your-api-key-here":
        print("❌ Please get your Fast2SMS API key first!")
        print("1. Go to: https://www.fast2sms.com/")
        print("2. Sign up for free")
        print("3. Get your API key from dashboard")
        print("4. Replace 'your-api-key-here' with your actual API key")
        return False
    
    # Fast2SMS API endpoint
    url = "https://www.fast2sms.com/dev/bulk"
    
    # Headers
    headers = {
        'authorization': api_key,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Data
    data = {
        'route': 'q',
        'message': message,
        'language': 'english',
        'numbers': phone_number
    }
    
    try:
        print("🚀 Sending SMS via Fast2SMS...")
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        
        if result.get('return') == True:
            print("✅ SMS sent successfully!")
            print(f"📱 Message ID: {result.get('request_id', 'N/A')}")
            print(f"📞 Sent to: +91{phone_number}")
            return True
        else:
            print("❌ SMS failed to send")
            print(f"Error: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending SMS: {str(e)}")
        return False

def send_sms_via_textlocal():
    """Send SMS using TextLocal"""
    
    phone_number = "7204310480"
    message = "Welcome to ReadOps Library! Your account has been created successfully. Start exploring: http://127.0.0.1:8000 - ReadOps Team"
    
    print(f"📱 Sending SMS to: {phone_number}")
    print(f"📝 Message: {message[:50]}...")
    print()
    
    # TextLocal API
    api_key = "your-textlocal-api-key"  # Replace with your actual API key
    
    if api_key == "your-textlocal-api-key":
        print("❌ Please get your TextLocal API key first!")
        print("1. Go to: https://www.textlocal.in/")
        print("2. Sign up and get API key")
        print("3. Replace 'your-textlocal-api-key' with your actual API key")
        return False
    
    url = "https://api.textlocal.in/send/"
    data = {
        'apikey': api_key,
        'numbers': phone_number,
        'message': message,
        'sender': 'ReadOps'
    }
    
    try:
        print("🚀 Sending SMS via TextLocal...")
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get('status') == 'success':
            print("✅ SMS sent successfully!")
            print(f"📱 Message ID: {result.get('messages', [{}])[0].get('id', 'N/A')}")
            print(f"📞 Sent to: +91{phone_number}")
            return True
        else:
            print("❌ SMS failed to send")
            print(f"Error: {result.get('errors', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending SMS: {str(e)}")
        return False

def main():
    print("📱 ReadOps SMS Sender")
    print("=" * 50)
    print(f"Target Number: 7204310480")
    print()
    
    print("Choose SMS provider:")
    print("1. Fast2SMS (Free for India)")
    print("2. TextLocal (Paid - ₹0.15-0.20 per SMS)")
    print("3. Test both")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        send_sms_via_fast2sms()
    elif choice == "2":
        send_sms_via_textlocal()
    elif choice == "3":
        print("Testing Fast2SMS...")
        send_sms_via_fast2sms()
        print("\nTesting TextLocal...")
        send_sms_via_textlocal()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
