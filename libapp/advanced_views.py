"""
Advanced Views for ReadOps Library Management System
This module contains advanced views that utilize the advanced tools.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .advanced_tools import (
    LibraryAnalytics, SmartRecommendations, NotificationManager,
    BookInventoryManager, UserBehaviorAnalyzer, AdvancedSearch
)
from .models import Book, CustomUser, Fine, MobileNotification


@login_required
def analytics_dashboard(request):
    """Advanced analytics dashboard for librarians"""
    if not request.user.is_librarian:
        messages.error(request, 'Access denied. Librarian privileges required.')
        return redirect('home')
    
    # Get analytics data
    borrowing_trends = LibraryAnalytics.get_borrowing_trends()
    overdue_analysis = LibraryAnalytics.get_overdue_analysis()
    library_health = LibraryAnalytics.get_library_health_score()
    
    context = {
        'borrowing_trends': borrowing_trends,
        'overdue_analysis': overdue_analysis,
        'library_health': library_health,
        'page_title': 'Library Analytics Dashboard'
    }
    
    return render(request, 'libapp/analytics_dashboard.html', context)


@login_required
def smart_recommendations(request):
    """AI-powered book recommendations"""
    recommendations = SmartRecommendations.get_personalized_recommendations(request.user)
    trending_books = SmartRecommendations.get_trending_books()
    
    context = {
        'recommendations': recommendations,
        'trending_books': trending_books,
        'page_title': 'Smart Recommendations'
    }
    
    return render(request, 'libapp/smart_recommendations.html', context)


@login_required
def inventory_management(request):
    """Advanced inventory management for librarians"""
    if not request.user.is_librarian:
        messages.error(request, 'Access denied. Librarian privileges required.')
        return redirect('home')
    
    low_stock_books = BookInventoryManager.get_low_stock_books()
    out_of_stock_books = BookInventoryManager.get_out_of_stock_books()
    restock_suggestions = BookInventoryManager.suggest_restock()
    
    context = {
        'low_stock_books': low_stock_books,
        'out_of_stock_books': out_of_stock_books,
        'restock_suggestions': restock_suggestions,
        'page_title': 'Inventory Management'
    }
    
    return render(request, 'libapp/inventory_management.html', context)


@login_required
def user_behavior_analysis(request):
    """User behavior analysis and insights"""
    user_patterns = UserBehaviorAnalyzer.get_user_reading_patterns(request.user)
    leaderboard = UserBehaviorAnalyzer.get_reading_leaderboard()
    
    context = {
        'user_patterns': user_patterns,
        'leaderboard': leaderboard,
        'page_title': 'Reading Behavior Analysis'
    }
    
    return render(request, 'libapp/user_behavior_analysis.html', context)


@login_required
def advanced_search(request):
    """Advanced search with fuzzy matching"""
    query = request.GET.get('q', '')
    search_results = []
    
    if query:
        search_results = AdvancedSearch.fuzzy_search(query)
    
    context = {
        'query': query,
        'search_results': search_results,
        'page_title': 'Advanced Search'
    }
    
    return render(request, 'libapp/advanced_search.html', context)


@login_required
def similar_books(request, book_id):
    """Find books similar to a specific book"""
    similar_books = AdvancedSearch.get_similar_books(book_id)
    original_book = get_object_or_404(Book, id=book_id)
    
    context = {
        'original_book': original_book,
        'similar_books': similar_books,
        'page_title': f'Books Similar to {original_book.title}'
    }
    
    return render(request, 'libapp/similar_books.html', context)


@login_required
@user_passes_test(lambda u: u.is_librarian)
def notification_management(request):
    """Advanced notification management for librarians"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'send_overdue_reminders':
            reminders_sent = NotificationManager.send_overdue_reminders()
            messages.success(request, f'{reminders_sent} overdue reminders sent.')
        
        elif action == 'cleanup_expired':
            expired_count = NotificationManager.cleanup_expired_notifications()
            messages.success(request, f'{expired_count} expired notifications cleaned up.')
        
        return redirect('notification_management')
    
    # Get notification statistics
    total_notifications = MobileNotification.objects.count()
    pending_notifications = MobileNotification.objects.filter(status='PENDING').count()
    confirmed_notifications = MobileNotification.objects.filter(status='CONFIRMED').count()
    expired_notifications = MobileNotification.objects.filter(status='EXPIRED').count()
    
    context = {
        'total_notifications': total_notifications,
        'pending_notifications': pending_notifications,
        'confirmed_notifications': confirmed_notifications,
        'expired_notifications': expired_notifications,
        'page_title': 'Notification Management'
    }
    
    return render(request, 'libapp/notification_management.html', context)


@login_required
def reading_insights(request):
    """Personal reading insights and statistics"""
    user_patterns = UserBehaviorAnalyzer.get_user_reading_patterns(request.user)
    
    # Get user's current books with detailed info
    current_books = []
    if hasattr(request.user, 'books') and request.user.books:
        for book in request.user.books:
            try:
                book_obj = Book.objects.get(id=book.get('id'))
                current_books.append({
                    'book': book_obj,
                    'borrow_data': book
                })
            except Book.DoesNotExist:
                continue
    
    # Calculate reading streak (simplified)
    reading_streak = len(request.user.books) if hasattr(request.user, 'books') else 0
    
    context = {
        'user_patterns': user_patterns,
        'current_books': current_books,
        'reading_streak': reading_streak,
        'page_title': 'My Reading Insights'
    }
    
    return render(request, 'libapp/reading_insights.html', context)


@login_required
def book_analytics(request, book_id):
    """Detailed analytics for a specific book"""
    book = get_object_or_404(Book, id=book_id)
    
    # Find users who have borrowed this book
    users_with_book = CustomUser.objects.filter(
        books__contains=[{'title': book.title}]
    )
    
    # Calculate book popularity metrics
    total_borrows = users_with_book.count()
    current_borrowers = users_with_book.count()
    
    # Get similar books
    similar_books = AdvancedSearch.get_similar_books(book_id)
    
    context = {
        'book': book,
        'total_borrows': total_borrows,
        'current_borrowers': current_borrowers,
        'similar_books': similar_books,
        'page_title': f'Analytics for {book.title}'
    }
    
    return render(request, 'libapp/book_analytics.html', context)


@login_required
def export_user_data(request):
    """Export user's reading data as JSON"""
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        'borrowed_books': request.user.books if hasattr(request.user, 'books') else [],
        'reading_patterns': UserBehaviorAnalyzer.get_user_reading_patterns(request.user),
        'export_date': timezone.now().isoformat()
    }
    
    response = JsonResponse(user_data, json_dumps_params={'indent': 2})
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}_reading_data.json"'
    
    return response


@login_required
@user_passes_test(lambda u: u.is_librarian)
def bulk_operations(request):
    """Bulk operations for librarians"""
    if request.method == 'POST':
        operation = request.POST.get('operation')
        
        if operation == 'send_reminders':
            reminders_sent = NotificationManager.send_overdue_reminders()
            messages.success(request, f'{reminders_sent} overdue reminders sent.')
        
        elif operation == 'cleanup_notifications':
            expired_count = NotificationManager.cleanup_expired_notifications()
            messages.success(request, f'{expired_count} expired notifications cleaned up.')
        
        elif operation == 'update_inventory':
            # Update inventory based on current borrowing status
            updated_count = 0
            for book in Book.objects.all():
                # Count how many users currently have this book
                current_borrowers = CustomUser.objects.filter(
                    books__contains=[{'title': book.title}]
                ).count()
                
                # Update quantity if needed
                if book.quantity != current_borrowers:
                    book.quantity = max(0, book.quantity - current_borrowers)
                    book.save()
                    updated_count += 1
            
            messages.success(request, f'{updated_count} books inventory updated.')
    
    return render(request, 'libapp/bulk_operations.html', {'page_title': 'Bulk Operations'})

@login_required
@user_passes_test(lambda u: u.is_librarian)
def bulk_operations_ldashboard_redirect(request):
    """Redirect from bulk-operations/ldashboard to librarian dashboard"""
    from django.shortcuts import redirect
    return redirect('librarian_dashboard')