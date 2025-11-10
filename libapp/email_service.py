"""
Email Notification Service for ReadOps Library Management System
Handles sending email notifications to registered email addresses
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from .models import MobileNotification

class EmailService:
    """
    Email Service for sending notifications to email addresses
    Replaces SMS notifications with email notifications
    """
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'ReadOps Library <arjun5shetty29@gmail.com>')
        self.site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        
    def send_email(self, to_email, subject, message, html_message=None):
        """
        Send email to the given email address
        Returns True if successful, False otherwise
        """
        try:
            # Check if email is enabled in settings
            if not getattr(settings, 'EMAIL_ENABLED', True):
                print("📧 Email disabled in settings")
                return True  # Return success but don't send
            
            # Send email
            result = send_mail(
                subject=subject,
                message=message,
                from_email=self.from_email,
                recipient_list=[to_email],
                html_message=html_message,
                fail_silently=False
            )
            
            if result:
                print(f"📧 EMAIL SENT SUCCESSFULLY:")
                print(f"   📧 TO: {to_email}")
                print(f"   📝 SUBJECT: {subject}")
                print(f"   📄 MESSAGE: {message[:100]}...")
                print(f"   🔗 FROM: {self.from_email}")
                print("=" * 50)
                return True
            else:
                print(f"❌ Email sending failed")
                return False
                
        except Exception as e:
            error_msg = str(e)
            if "Username and Password not accepted" in error_msg:
                print(f"❌ Email sending failed: Invalid email credentials")
                print(f"   Please check your EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env file")
                print(f"   For Gmail, make sure you're using an App Password, not your regular password")
            elif "Authentication failed" in error_msg:
                print(f"❌ Email sending failed: Authentication failed")
                print(f"   Please verify your email credentials")
            else:
                print(f"❌ Email sending failed: {error_msg}")
            return False
    
    def send_registration_email(self, user):
        """Send welcome email after successful registration"""
        subject = "Welcome to ReadOps Library! 🎉"
        message = f"""
Welcome to ReadOps Library! 🎉

Hello {user.username},

Your account has been successfully created.

📚 Access thousands of books
🔍 Smart search and AI recommendations
📧 Email notifications for all activities
💳 Secure payment options

Start exploring: {self.site_url}

- ReadOps Team
        """.strip()
        
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="margin: 0; font-size: 28px;">📚 ReadOps Library</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px;">Welcome to ReadOps Library! 🎉</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {user.username},</h2>
                
                <p style="color: #666; font-size: 16px; line-height: 1.6;">
                    Your account has been successfully created and you're ready to start exploring our amazing library!
                </p>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #667eea;">
                    <h3 style="color: #333; margin-top: 0;">What you can do:</h3>
                    <ul style="color: #666; line-height: 1.8;">
                        <li>📚 Access thousands of books</li>
                        <li>🔍 Smart search and AI recommendations</li>
                        <li>📧 Email notifications for all activities</li>
                        <li>💳 Secure payment options</li>
                        <li>📱 Mobile-friendly interface</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{self.site_url}" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
                        🚀 Start Exploring
                    </a>
                </div>
                
                <div style="border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px; text-align: center; color: #999; font-size: 14px;">
                    <p>Happy Reading!</p>
                    <p><strong>ReadOps Team</strong></p>
                </div>
            </div>
        </div>
        """
        
        return self.send_email(user.email, subject, message, html_message)
    
    def send_book_borrowed_email(self, user, book, bima_id=None):
        """Send email notification for book borrowing"""
        subject = f"📚 Book Borrowed: {book.title}"
        message = f"""
📚 Book Borrowed Successfully!

Hello {user.username},
You have borrowed: "{book.title}"
Author: {book.author}

🆔 Transaction ID: {bima_id or 'N/A'}
📅 Due Date: {book.end_date.strftime('%Y-%m-%d')}

Please return the book on time to avoid fines.

- ReadOps Library
        """.strip()
        
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="margin: 0; font-size: 28px;">📚 Book Borrowed</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px;">Successfully borrowed!</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {user.username},</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745;">
                    <h3 style="color: #333; margin-top: 0;">📖 Book Details:</h3>
                    <p><strong>Title:</strong> {book.title}</p>
                    <p><strong>Author:</strong> {book.author}</p>
                    <p><strong>Due Date:</strong> {book.end_date.strftime('%B %d, %Y')}</p>
                    {f'<p><strong>Transaction ID:</strong> {bima_id}</p>' if bima_id else ''}
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 20px 0;">
                    <p style="margin: 0; color: #856404;"><strong>⚠️ Important:</strong> Please return the book on time to avoid fines.</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{self.site_url}/dashboard/" style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
                        📋 View My Books
                    </a>
                </div>
                
                <div style="border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px; text-align: center; color: #999; font-size: 14px;">
                    <p>Happy Reading!</p>
                    <p><strong>ReadOps Library</strong></p>
                </div>
            </div>
        </div>
        """
        
        return self.send_email(user.email, subject, message, html_message)
    
    def send_book_returned_email(self, user, book, bima_id=None):
        """Send email notification for book return"""
        subject = f"📚 Book Returned: {book.title}"
        message = f"""
📚 Book Returned Successfully!

Hello {user.username},
You have successfully returned: "{book.title}"
Author: {book.author}

🆔 Transaction ID: {bima_id or 'N/A'}
📅 Return Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}

Thank you for returning the book on time!

- ReadOps Library
        """.strip()
        
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #17a2b8, #138496); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="margin: 0; font-size: 28px;">📚 Book Returned</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px;">Successfully returned!</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {user.username},</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #17a2b8;">
                    <h3 style="color: #333; margin-top: 0;">📖 Book Details:</h3>
                    <p><strong>Title:</strong> {book.title}</p>
                    <p><strong>Author:</strong> {book.author}</p>
                    <p><strong>Return Date:</strong> {timezone.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    {f'<p><strong>Transaction ID:</strong> {bima_id}</p>' if bima_id else ''}
                </div>
                
                <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 20px 0;">
                    <p style="margin: 0; color: #155724;"><strong>✅ Thank you!</strong> The book has been successfully returned.</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{self.site_url}/explore/" style="background: linear-gradient(135deg, #17a2b8, #138496); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
                        🔍 Explore More Books
                    </a>
                </div>
                
                <div style="border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px; text-align: center; color: #999; font-size: 14px;">
                    <p>Happy Reading!</p>
                    <p><strong>ReadOps Library</strong></p>
                </div>
            </div>
        </div>
        """
        
        return self.send_email(user.email, subject, message, html_message)
    
    def send_payment_success_email(self, user, amount, payment_method, book_title):
        """Send email notification for successful payment"""
        subject = f"💳 Payment Successful - ₹{amount}"
        message = f"""
💳 Payment Successful!

Hello {user.username},
Payment of ₹{amount} for '{book_title}' has been processed successfully.

💳 Payment Method: {payment_method}
📅 Date: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

Thank you for your payment!

- ReadOps Library
        """.strip()
        
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center;">
                <h1 style="margin: 0; font-size: 28px;">💳 Payment Successful</h1>
                <p style="margin: 10px 0 0 0; font-size: 18px;">Transaction completed!</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Hello {user.username},</h2>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745;">
                    <h3 style="color: #333; margin-top: 0;">💰 Payment Details:</h3>
                    <p><strong>Amount:</strong> ₹{amount}</p>
                    <p><strong>Book:</strong> {book_title}</p>
                    <p><strong>Payment Method:</strong> {payment_method}</p>
                    <p><strong>Date:</strong> {timezone.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <div style="background: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745; margin: 20px 0;">
                    <p style="margin: 0; color: #155724;"><strong>✅ Payment Confirmed!</strong> Your payment has been processed successfully.</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{self.site_url}/dashboard/" style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
                        📋 View My Dashboard
                    </a>
                </div>
                
                <div style="border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px; text-align: center; color: #999; font-size: 14px;">
                    <p>Thank you for your payment!</p>
                    <p><strong>ReadOps Library</strong></p>
                </div>
            </div>
        </div>
        """
        
        return self.send_email(user.email, subject, message, html_message)
    
    def send_overdue_email(self, user, book):
        """Send email notification for overdue books"""
        subject = f"⚠️ Book Overdue: {book.title}"
        message = f"""
⚠️ Book Overdue Reminder

Hello {user.username},
The book "{book.title}" is overdue.

📅 Due Date: {book.end_date.strftime('%Y-%m-%d')}
📚 Book: {book.title}
👤 Author: {book.author}

Please return the book as soon as possible to avoid additional fines.

- ReadOps Library
        """.strip()
        
        return self.send_email(user.email, subject, message)
    
    def send_fine_reminder_email(self, user, fine):
        """Send email notification for fine reminder"""
        subject = f"💰 Fine Reminder: ₹{fine.amount}"
        message = f"""
💰 Fine Reminder

Hello {user.username},
You have a pending fine of ₹{fine.amount} for the book "{fine.book_title}".

📅 Due Date: {fine.due_date.strftime('%Y-%m-%d')}
💰 Amount: ₹{fine.amount}
📚 Book: {fine.book_title}

Please pay the fine to avoid further restrictions.

- ReadOps Library
        """.strip()
        
        return self.send_email(user.email, subject, message)
    
    def send_book_purchase_email(self, user, book_title, amount, payment_method):
        """Send email notification for book purchase"""
        subject = "📚 Book Purchase Confirmation - ReadOps Library"
        message = f"""
Dear {user.username},

Thank you for your purchase! Your book has been successfully added to your library.

📖 Book Details:
   Title: {book_title}
   Amount: ₹{amount}
   Payment Method: {payment_method}
   Purchase Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}

🎉 You can now access your book from your digital library.

Happy Reading!
ReadOps Library Team
{self.site_url}
        """.strip()
        
        return self.send_email(user.email, subject, message)
    
    def send_login_notification_email(self, user, login_time):
        """Send email notification for successful login"""
        subject = "🔐 Login Notification - ReadOps Library"
        message = f"""
Dear {user.username},

You have successfully logged into your ReadOps Library account.

📅 Login Details:
   Time: {login_time.strftime('%Y-%m-%d %H:%M:%S')}
   IP Address: {self.site_url}

If this wasn't you, please contact us immediately.

Best regards,
ReadOps Library Team
{self.site_url}
        """.strip()
        
        return self.send_email(user.email, subject, message)
    
    def send_due_date_reminder_email(self, user, book_title, due_date, days_remaining):
        """Send email reminder for book due date"""
        if days_remaining <= 0:
            subject = "⚠️ URGENT: Book Overdue - ReadOps Library"
            urgency = "OVERDUE"
        elif days_remaining == 1:
            subject = "⚠️ Book Due Tomorrow - ReadOps Library"
            urgency = "DUE TOMORROW"
        else:
            subject = f"📅 Book Due in {days_remaining} Days - ReadOps Library"
            urgency = f"DUE IN {days_remaining} DAYS"
        
        message = f"""
Dear {user.username},

{urgency} - Book Return Reminder

📚 Book Details:
   Title: {book_title}
   Due Date: {due_date.strftime('%Y-%m-%d')}
   Status: {urgency}

{'⚠️ Please return the book immediately to avoid fines!' if days_remaining <= 0 else 'Please return the book on or before the due date.'}

📖 You can return the book through:
   - Online return system
   - Visit the library
   - Contact librarian

Best regards,
ReadOps Library Team
{self.site_url}
        """.strip()
        
        return self.send_email(user.email, subject, message)

# Create a global instance
email_service = EmailService()
