"""
Advanced Tools for ReadOps Library Management System
This module contains advanced features and utilities for the library system.
"""

from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json
from .models import Book, CustomUser, Fine, Payment, MobileNotification


class LibraryAnalytics:
    """Advanced analytics for library management"""
    
    @staticmethod
    def get_borrowing_trends():
        """Analyze borrowing trends and patterns"""
        users_with_books = CustomUser.objects.filter(books__isnull=False)
        
        # Calculate average books per user
        total_borrowed = sum(len(user.books) for user in users_with_books)
        avg_books_per_user = total_borrowed / len(users_with_books) if users_with_books else 0
        
        # Find most popular books
        book_borrow_counts = {}
        for user in users_with_books:
            for book in user.books:
                book_title = book.get('title', 'Unknown')
                book_borrow_counts[book_title] = book_borrow_counts.get(book_title, 0) + 1
        
        most_popular = sorted(book_borrow_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_borrowed_books': total_borrowed,
            'avg_books_per_user': round(avg_books_per_user, 2),
            'most_popular_books': most_popular,
            'active_borrowers': len(users_with_books)
        }
    
    @staticmethod
    def get_overdue_analysis():
        """Analyze overdue books and fines"""
        current_date = timezone.now().date()
        overdue_books = []
        total_fine_amount = Decimal('0.00')
        
        users_with_books = CustomUser.objects.filter(books__isnull=False)
        
        for user in users_with_books:
            for book in user.books:
                end_date_str = book.get('end_date')
                if end_date_str:
                    end_date = timezone.datetime.fromisoformat(end_date_str).date()
                    if end_date < current_date:
                        days_overdue = (current_date - end_date).days
                        overdue_books.append({
                            'user': user.username,
                            'book_title': book.get('title', 'Unknown'),
                            'days_overdue': days_overdue,
                            'end_date': end_date
                        })
        
        # Calculate total fine amount
        pending_fines = Fine.objects.filter(status='PENDING')
        for fine in pending_fines:
            total_fine_amount += fine.amount
        
        return {
            'overdue_count': len(overdue_books),
            'overdue_books': overdue_books,
            'total_fine_amount': total_fine_amount,
            'pending_fines_count': pending_fines.count()
        }
    
    @staticmethod
    def get_library_health_score():
        """Calculate overall library health score"""
        total_books = Book.objects.count()
        available_books = Book.objects.filter(quantity__gt=0).count()
        borrowed_books = 0
        
        users_with_books = CustomUser.objects.filter(books__isnull=False)
        for user in users_with_books:
            borrowed_books += len(user.books)
        
        # Calculate health metrics
        availability_ratio = (available_books / total_books * 100) if total_books > 0 else 0
        utilization_ratio = (borrowed_books / total_books * 100) if total_books > 0 else 0
        
        # Health score calculation (0-100)
        health_score = (availability_ratio * 0.4) + (utilization_ratio * 0.3) + (30)  # Base score of 30
        
        return {
            'health_score': min(100, max(0, round(health_score, 1))),
            'availability_ratio': round(availability_ratio, 1),
            'utilization_ratio': round(utilization_ratio, 1),
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books
        }


class SmartRecommendations:
    """AI-powered book recommendations"""
    
    @staticmethod
    def get_personalized_recommendations(user):
        """Generate personalized book recommendations based on user's borrowing history"""
        if not hasattr(user, 'books') or not user.books:
            # If no borrowing history, recommend popular books
            return Book.objects.filter(quantity__gt=0).order_by('?')[:5]
        
        # Analyze user's borrowing patterns
        borrowed_subjects = []
        borrowed_authors = []
        
        for book in user.books:
            # Get book details from database
            try:
                book_obj = Book.objects.get(id=book.get('id'))
                borrowed_subjects.append(book_obj.subject)
                borrowed_authors.append(book_obj.author)
            except Book.DoesNotExist:
                continue
        
        # Find similar books
        recommendations = Book.objects.filter(
            Q(subject__in=borrowed_subjects) | Q(author__in=borrowed_authors),
            quantity__gt=0
        ).exclude(
            id__in=[book.get('id') for book in user.books]
        ).distinct()[:10]
        
        return recommendations
    
    @staticmethod
    def get_trending_books():
        """Get trending books based on recent borrowing activity"""
        # This is a simplified version - in a real system, you'd track borrowing timestamps
        popular_books = Book.objects.filter(quantity__gt=0).order_by('?')[:5]
        return popular_books


class NotificationManager:
    """Advanced notification management system"""
    
    @staticmethod
    def send_overdue_reminders():
        """Send automated overdue reminders"""
        current_date = timezone.now().date()
        users_with_books = CustomUser.objects.filter(books__isnull=False)
        
        reminders_sent = 0
        for user in users_with_books:
            for book in user.books:
                end_date_str = book.get('end_date')
                if end_date_str:
                    end_date = timezone.datetime.fromisoformat(end_date_str).date()
                    if end_date < current_date:
                        # Create overdue notification
                        MobileNotification.objects.create(
                            user=user,
                            notification_type='BOOK_OVERDUE',
                            title=f'Overdue Book: {book.get("title", "Unknown")}',
                            message=f'Your book "{book.get("title", "Unknown")}" is overdue. Please return it soon to avoid fines.',
                            book_title=book.get('title', 'Unknown'),
                            book_id=book.get('id'),
                            status='PENDING'
                        )
                        reminders_sent += 1
        
        return reminders_sent
    
    @staticmethod
    def cleanup_expired_notifications():
        """Clean up expired notifications"""
        expired_count = MobileNotification.objects.filter(
            expires_at__lt=timezone.now(),
            status='PENDING'
        ).update(status='EXPIRED')
        
        return expired_count


class BookInventoryManager:
    """Advanced book inventory management"""
    
    @staticmethod
    def get_low_stock_books(threshold=2):
        """Get books with low stock"""
        return Book.objects.filter(quantity__lte=threshold, quantity__gt=0)
    
    @staticmethod
    def get_out_of_stock_books():
        """Get books that are out of stock"""
        return Book.objects.filter(quantity=0)
    
    @staticmethod
    def suggest_restock():
        """Suggest books that need restocking based on demand"""
        # Find books that are frequently borrowed but have low stock
        low_stock_books = Book.objects.filter(quantity__lte=2, quantity__gt=0)
        
        suggestions = []
        for book in low_stock_books:
            # Check if book is currently borrowed using a different approach
            # Get all users and check their books manually (SQLite compatible)
            borrowed_count = 0
            for user in CustomUser.objects.all():
                if user.books:  # Check if user has books
                    for user_book in user.books:
                        if isinstance(user_book, dict) and user_book.get('title') == book.title:
                            borrowed_count += 1
                            break
            
            if borrowed_count > 0:
                suggestions.append({
                    'book': book,
                    'current_stock': book.quantity,
                    'borrowed_count': borrowed_count,
                    'priority': 'High' if book.quantity == 1 else 'Medium'
                })
        
        return sorted(suggestions, key=lambda x: x['borrowed_count'], reverse=True)


class UserBehaviorAnalyzer:
    """Analyze user behavior patterns"""
    
    @staticmethod
    def get_user_reading_patterns(user):
        """Analyze user's reading patterns"""
        if not hasattr(user, 'books') or not user.books:
            return {
                'total_books_borrowed': 0,
                'favorite_subjects': [],
                'favorite_authors': [],
                'average_borrowing_duration': 0,
                'reading_level': 'Beginner'
            }
        
        subjects = []
        authors = []
        borrowing_durations = []
        
        for book in user.books:
            try:
                book_obj = Book.objects.get(id=book.get('id'))
                subjects.append(book_obj.subject)
                authors.append(book_obj.author)
                
                # Calculate borrowing duration
                start_date_str = book.get('start_date')
                if start_date_str:
                    start_date = timezone.datetime.fromisoformat(start_date_str)
                    duration = (timezone.now() - start_date).days
                    borrowing_durations.append(duration)
            except Book.DoesNotExist:
                continue
        
        # Analyze patterns
        subject_counts = {}
        for subject in subjects:
            subject_counts[subject] = subject_counts.get(subject, 0) + 1
        
        author_counts = {}
        for author in authors:
            author_counts[author] = author_counts.get(author, 0) + 1
        
        favorite_subjects = sorted(subject_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        favorite_authors = sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        avg_duration = sum(borrowing_durations) / len(borrowing_durations) if borrowing_durations else 0
        
        # Determine reading level
        total_books = len(user.books)
        if total_books >= 20:
            reading_level = 'Expert'
        elif total_books >= 10:
            reading_level = 'Advanced'
        elif total_books >= 5:
            reading_level = 'Intermediate'
        else:
            reading_level = 'Beginner'
        
        return {
            'total_books_borrowed': total_books,
            'favorite_subjects': [item[0] for item in favorite_subjects],
            'favorite_authors': [item[0] for item in favorite_authors],
            'average_borrowing_duration': round(avg_duration, 1),
            'reading_level': reading_level
        }
    
    @staticmethod
    def get_reading_leaderboard():
        """Get reading leaderboard of most active users"""
        users_with_books = CustomUser.objects.filter(books__isnull=False)
        
        leaderboard = []
        for user in users_with_books:
            total_books = len(user.books)
            leaderboard.append({
                'user': user.username,
                'total_books': total_books,
                'email': user.email
            })
        
        return sorted(leaderboard, key=lambda x: x['total_books'], reverse=True)[:10]


class AdvancedSearch:
    """Advanced search functionality"""
    
    @staticmethod
    def fuzzy_search(query, limit=10):
        """Fuzzy search for books with partial matching"""
        if not query:
            return Book.objects.none()
        
        # Split query into words
        query_words = query.lower().split()
        
        books = Book.objects.filter(quantity__gt=0)
        scored_books = []
        
        for book in books:
            score = 0
            title_words = book.title.lower().split()
            author_words = book.author.lower().split()
            subject_words = book.subject.lower().split()
            
            # Score based on word matches
            for word in query_words:
                for title_word in title_words:
                    if word in title_word or title_word in word:
                        score += 3
                
                for author_word in author_words:
                    if word in author_word or author_word in word:
                        score += 2
                
                for subject_word in subject_words:
                    if word in subject_word or subject_word in word:
                        score += 1
            
            if score > 0:
                scored_books.append((book, score))
        
        # Sort by score and return top results
        scored_books.sort(key=lambda x: x[1], reverse=True)
        return [book for book, score in scored_books[:limit]]
    
    @staticmethod
    def get_similar_books(book_id):
        """Find books similar to the given book"""
        try:
            target_book = Book.objects.get(id=book_id)
            
            # Find books with same subject or author
            similar_books = Book.objects.filter(
                Q(subject=target_book.subject) | Q(author=target_book.author),
                quantity__gt=0
            ).exclude(id=book_id)[:5]
            
            return similar_books
        except Book.DoesNotExist:
            return Book.objects.none()
