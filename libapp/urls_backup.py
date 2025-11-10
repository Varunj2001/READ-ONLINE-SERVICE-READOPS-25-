from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    # Map the search-based explore to name 'explore' to fix NoReverseMatch
    path('explore/', explore, name='explore'),
    # Keep filter-based explore available under a separate route/name
    path('explore_filters/', explore_view, name='explore_view'),
    path('book_request/', book_request_view, name='book_request'),
    path('get_subjects/', get_subjects_view, name='get_subjects'),
    path('get_books/', get_books_view, name='get_books'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('signup/', signup, name='signup'),
    path('update_user/', update_user, name='update_user'),
    path('login_user/', login_user, name='login_user'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('return_book/', return_book_view, name='return_book'),
    path('aboutus/', aboutus_view, name='aboutus_view'),
    path('login_librarian/', login_librarian, name='login_librarian'),
    path('update_book_details/<int:book_pk>/', update_book_details, name='update_book_details'),
    path('save_book_details/<int:book_pk>/', save_book_details, name='save_book_details'),
    path('add_book/', render_add_new_book_page, name='add_new_book'),
    path('save_book/', save_new_book, name='save_new_book'),
    path('ldashboard/', librarian_dashboard, name='librarian_dashboard'),
    path('remind_user/', remind_user, name='remind_user'),
    path('status/', status_view, name='status_view'),
    path('report_lost/<int:book_id>/', report_lost_book, name='report_lost'),
    path('payment/<int:fine_id>/', payment_view, name='payment'),
    path('pay_fine/', pay_fine, name='pay_fine'),
    path('pay_lost_book/', pay_lost_book, name='pay_lost_book'),
    path('add_fine/', add_fine, name='add_fine'),
    path('payment_receipt/<int:payment_id>/', payment_receipt, name='payment_receipt'),
    path('view_payments/', view_payments, name='view_payments'),
    path('view_payment/<int:payment_id>/', view_payment, name='view_payment'),
    path('generate_barcode/<int:book_id>/', generate_barcode, name='generate_barcode'),
    # Cart functionality
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('checkout/', checkout_cart, name='checkout_cart'),
    path('extend_book/<int:book_id>/', extend_book, name='extend_book'),
    # AI features
    path('ai-recommendations/', ai_recommendations, name='ai_recommendations'),
    path('ai-search/', ai_search, name='ai_search'),
    # Mobile notifications
    path('mobile-notification/<int:notification_id>/', mobile_notification, name='mobile_notification'),
    path('respond-notification/<int:notification_id>/', respond_notification, name='respond_notification'),
    path('create-borrow-notification/<int:book_id>/', create_book_borrow_notification, name='create_book_borrow_notification'),
    path('create-return-notification/<int:book_id>/', create_book_return_notification, name='create_book_return_notification'),
    path('my-notifications/', my_notifications, name='my_notifications'),
    path('test-sms/', test_sms, name='test_sms'),
    path('test-email/', test_email, name='test_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)