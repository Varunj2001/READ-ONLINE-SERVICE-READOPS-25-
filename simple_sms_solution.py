#!/usr/bin/env python3
"""
Simple SMS Solution for ReadOps
This will help you send SMS to 7204310480 using various methods
"""

import webbrowser
import urllib.parse

def send_via_whatsapp():
    """Send message via WhatsApp Web"""
    phone_number = "7204310480"
    message = """Welcome to ReadOps Library! 🎉

Hello readops,
Your account has been successfully created.

📚 Access thousands of books
🔍 Smart search and AI recommendations
📱 Mobile notifications for all activities
💳 Secure payment options

Start exploring: http://127.0.0.1:8000

- ReadOps Team"""
    
    # Format phone number for WhatsApp
    whatsapp_number = f"91{phone_number}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://web.whatsapp.com/send?phone={whatsapp_number}&text={encoded_message}"
    
    print("📱 Opening WhatsApp Web...")
    print(f"📞 Number: +91{phone_number}")
    print(f"📝 Message: {message[:50]}...")
    print()
    print("✅ WhatsApp Web will open. Click 'Send' to deliver the message.")
    
    webbrowser.open(whatsapp_url)
    return True

def send_via_sms_website():
    """Open SMS website for manual sending"""
    phone_number = "7204310480"
    message = """Welcome to ReadOps Library! 🎉

Hello readops,
Your account has been successfully created.

📚 Access thousands of books
🔍 Smart search and AI recommendations
📱 Mobile notifications for all activities
💳 Secure payment options

Start exploring: http://127.0.0.1:8000

- ReadOps Team"""
    
    # Create SMS link
    sms_url = f"sms:+91{phone_number}?body={urllib.parse.quote(message)}"
    
    print("📱 Opening SMS app...")
    print(f"📞 Number: +91{phone_number}")
    print(f"📝 Message: {message[:50]}...")
    print()
    print("✅ SMS app will open. Click 'Send' to deliver the message.")
    
    webbrowser.open(sms_url)
    return True

def show_sms_providers():
    """Show available SMS providers"""
    print("📱 Available SMS Providers for India:")
    print("=" * 50)
    print()
    
    print("1. Fast2SMS (FREE)")
    print("   - Website: https://www.fast2sms.com/")
    print("   - Cost: Free (with limitations)")
    print("   - Steps:")
    print("     a. Sign up at https://www.fast2sms.com/")
    print("     b. Get API key from dashboard")
    print("     c. Update library/settings.py with your API key")
    print()
    
    print("2. TextLocal (PAID)")
    print("   - Website: https://www.textlocal.in/")
    print("   - Cost: ₹0.15-0.20 per SMS")
    print("   - Steps:")
    print("     a. Sign up at https://www.textlocal.in/")
    print("     b. Get API key")
    print("     c. Add credits to account")
    print("     d. Update library/settings.py")
    print()
    
    print("3. Twilio (INTERNATIONAL)")
    print("   - Website: https://www.twilio.com/")
    print("   - Cost: $0.0075 per SMS")
    print("   - Steps:")
    print("     a. Sign up at https://www.twilio.com/")
    print("     b. Get Account SID and Auth Token")
    print("     c. Buy a phone number")
    print("     d. Update library/settings.py")
    print()
    
    print("4. Manual Methods")
    print("   - WhatsApp: Send via WhatsApp Web")
    print("   - SMS App: Use your phone's SMS app")
    print("   - Email: Send to phone's email address")

def main():
    print("📱 ReadOps SMS Solution")
    print("=" * 50)
    print(f"Target Number: 7204310480")
    print()
    
    print("Choose an option:")
    print("1. Send via WhatsApp Web")
    print("2. Send via SMS App")
    print("3. Show SMS Provider Setup")
    print("4. Test Current SMS System")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        send_via_whatsapp()
    elif choice == "2":
        send_via_sms_website()
    elif choice == "3":
        show_sms_providers()
    elif choice == "4":
        print("🧪 Testing current SMS system...")
        import subprocess
        subprocess.run(["python", "manage.py", "test_sms_all_users", "--user", "readops"])
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
