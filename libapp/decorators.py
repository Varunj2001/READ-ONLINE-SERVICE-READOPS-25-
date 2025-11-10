from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from .models import Fine

def check_fine_access(view_func):
    """
    Decorator to check if user has access restrictions due to fines.
    Allows access to basic functions but restricts borrowing new books.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user has excessive fines (more than 3 pending fines)
            pending_fines_count = Fine.objects.filter(user=request.user, status='pending').count()
            
            # Allow access to basic functions (returning books, viewing dashboard, etc.)
            allowed_views = ['user_dashboard', 'return_book', 'report_lost_book', 'payment_view', 'pay_fine', 'view_payments']
            current_view = view_func.__name__
            
            if pending_fines_count > 3 and current_view not in allowed_views:
                messages.warning(request, f'You have {pending_fines_count} pending fines. Please clear some fines to access this feature.')
                return redirect('payment_view')
                
        return view_func(request, *args, **kwargs)
    return wrapped_view

def require_no_excessive_fines(view_func):
    """
    Decorator to completely restrict access for users with excessive fines.
    Used for borrowing new books and other premium features.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            pending_fines_count = Fine.objects.filter(user=request.user, status='pending').count()
            total_pending_amount = sum(fine.amount for fine in Fine.objects.filter(user=request.user, status='pending'))
            
            # Block access if user has more than 3 pending fines OR total pending amount > ₹50
            if pending_fines_count > 3 or total_pending_amount > 50:
                messages.error(request, f'Access restricted: You have {pending_fines_count} pending fines totaling ₹{total_pending_amount}. Please clear your fines to continue.')
                return redirect('payment_view')
                
        return view_func(request, *args, **kwargs)
    return wrapped_view

def librarian_required(view_func):
    """
    Decorator to ensure only librarians can access certain views.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        
        if not request.user.is_librarian:
            messages.error(request, 'Access denied. This page is only available to librarians.')
            return redirect('user_dashboard')
            
        return view_func(request, *args, **kwargs)
    return wrapped_view