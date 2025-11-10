from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
import json
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from .models import CustomUser, UserQRCode, QRScanLog, Book
from .decorators import librarian_required


@login_required
def generate_user_qr(request):
    """Generate or retrieve user's QR code"""
    user = request.user
    
    # Get or create QR code for user
    qr_code, created = UserQRCode.objects.get_or_create(
        user=user,
        defaults={'qr_code_data': ''}
    )
    
    # Generate QR code image if not exists
    if not qr_code.qr_code_image:
        qr_data = qr_code.generate_qr_data()
        qr_code.qr_code_data = qr_data
        
        # Generate QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image to model
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        qr_code.qr_code_image.save(
            f'qr_{user.username}_{user.id}.png',
            ContentFile(buffer.getvalue()),
            save=True
        )
    
    return render(request, 'libapp/user_qr_code.html', {
        'qr_code': qr_code,
        'user': user,
        'created': created
    })


@librarian_required
def qr_scanner(request):
    """QR code scanner interface for librarians"""
    return render(request, 'libapp/qr_scanner.html')


@librarian_required
def scan_qr_code(request):
    """Process scanned QR code and show user details"""
    if request.method == 'POST':
        try:
            qr_data = request.POST.get('qr_data')
            scan_type = request.POST.get('scan_type', 'VERIFICATION')
            location = request.POST.get('location', '')
            notes = request.POST.get('notes', '')
            
            # Parse QR code data
            user_data = json.loads(qr_data)
            user_id = user_data.get('user_id')
            
            # Get user
            scanned_user = get_object_or_404(CustomUser, id=user_id)
            
            # Create scan log
            scan_log = QRScanLog.objects.create(
                scanned_user=scanned_user,
                scanned_by=request.user,
                scan_type=scan_type,
                location=location,
                notes=notes,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Get user's recent activity
            recent_scans = QRScanLog.objects.filter(
                scanned_user=scanned_user
            ).order_by('-scan_timestamp')[:10]
            
            # Get user's borrowed books
            borrowed_books = []
            if scanned_user.books:
                for book_data in scanned_user.books:
                    if isinstance(book_data, dict) and book_data.get('book_id'):
                        try:
                            book = Book.objects.get(id=book_data['book_id'])
                            borrowed_books.append({
                                'book': book,
                                'borrow_date': book_data.get('borrow_date'),
                                'due_date': book_data.get('due_date'),
                                'is_overdue': book_data.get('is_overdue', False)
                            })
                        except Book.DoesNotExist:
                            continue
            
            return render(request, 'libapp/user_details.html', {
                'scanned_user': scanned_user,
                'scan_log': scan_log,
                'recent_scans': recent_scans,
                'borrowed_books': borrowed_books,
                'scan_type': scan_type
            })
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            messages.error(request, f'Invalid QR code data: {str(e)}')
            return redirect('qr_scanner')
        except Exception as e:
            messages.error(request, f'Error processing QR code: {str(e)}')
            return redirect('qr_scanner')
    
    return redirect('qr_scanner')


@librarian_required
def qr_tracking_dashboard(request):
    """Dashboard for tracking QR code scans"""
    # Get filter parameters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    user_search = request.GET.get('user_search')
    scan_type_filter = request.GET.get('scan_type')
    
    # Base queryset
    scans = QRScanLog.objects.all()
    
    # Apply filters
    if date_from:
        scans = scans.filter(scan_timestamp__date__gte=date_from)
    if date_to:
        scans = scans.filter(scan_timestamp__date__lte=date_to)
    if user_search:
        scans = scans.filter(
            Q(scanned_user__username__icontains=user_search) |
            Q(scanned_user__email__icontains=user_search) |
            Q(scanned_user__first_name__icontains=user_search) |
            Q(scanned_user__last_name__icontains=user_search)
        )
    if scan_type_filter:
        scans = scans.filter(scan_type=scan_type_filter)
    
    # Pagination
    paginator = Paginator(scans, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_scans = scans.count()
    today_scans = scans.filter(scan_timestamp__date=timezone.now().date()).count()
    unique_users = scans.values('scanned_user').distinct().count()
    
    # Scan types statistics
    scan_types_stats = {}
    for scan_type, _ in QRScanLog.SCAN_TYPE_CHOICES:
        count = scans.filter(scan_type=scan_type).count()
        scan_types_stats[scan_type] = count
    
    # Recent activity
    recent_scans = scans.order_by('-scan_timestamp')[:10]
    
    context = {
        'page_obj': page_obj,
        'total_scans': total_scans,
        'today_scans': today_scans,
        'unique_users': unique_users,
        'scan_types_stats': scan_types_stats,
        'recent_scans': recent_scans,
        'scan_type_choices': QRScanLog.SCAN_TYPE_CHOICES,
        'date_from': date_from,
        'date_to': date_to,
        'user_search': user_search,
        'scan_type_filter': scan_type_filter,
    }
    
    return render(request, 'libapp/qr_tracking_dashboard.html', context)


@librarian_required
def export_scan_data(request):
    """Export scan data in CSV or PDF format"""
    export_format = request.GET.get('format', 'csv')
    
    # Get filter parameters (same as dashboard)
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    user_search = request.GET.get('user_search')
    scan_type_filter = request.GET.get('scan_type')
    
    # Base queryset
    scans = QRScanLog.objects.all()
    
    # Apply filters
    if date_from:
        scans = scans.filter(scan_timestamp__date__gte=date_from)
    if date_to:
        scans = scans.filter(scan_timestamp__date__lte=date_to)
    if user_search:
        scans = scans.filter(
            Q(scanned_user__username__icontains=user_search) |
            Q(scanned_user__email__icontains=user_search) |
            Q(scanned_user__first_name__icontains=user_search) |
            Q(scanned_user__last_name__icontains=user_search)
        )
    if scan_type_filter:
        scans = scans.filter(scan_type=scan_type_filter)
    
    if export_format == 'csv':
        return export_csv(scans)
    elif export_format == 'pdf':
        return export_pdf(scans)
    else:
        messages.error(request, 'Invalid export format')
        return redirect('qr_tracking_dashboard')


def export_csv(scans):
    """Export scan data as CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qr_scan_logs.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Scan ID', 'Scanned User', 'User Email', 'User Phone', 'Scanned By',
        'Scan Type', 'Scan Date', 'Scan Time', 'Location', 'Notes', 'IP Address'
    ])
    
    for scan in scans:
        writer.writerow([
            scan.id,
            scan.scanned_user.username,
            scan.scanned_user.email,
            scan.scanned_user.phone,
            scan.scanned_by.username,
            scan.get_scan_type_display(),
            scan.scan_date,
            scan.scan_time,
            scan.location or '',
            scan.notes or '',
            scan.ip_address or ''
        ])
    
    return response


def export_pdf(scans):
    """Export scan data as PDF"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="qr_scan_logs.pdf"'
    
    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    title = Paragraph("QR Code Scan Logs Report", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Summary
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12
    )
    summary = Paragraph(f"Total Scans: {scans.count()}", summary_style)
    story.append(summary)
    story.append(Spacer(1, 20))
    
    # Table data
    table_data = [['Scan ID', 'User', 'Email', 'Scanned By', 'Type', 'Date', 'Time', 'Location']]
    
    for scan in scans:
        table_data.append([
            str(scan.id),
            scan.scanned_user.username,
            scan.scanned_user.email,
            scan.scanned_by.username,
            scan.get_scan_type_display(),
            str(scan.scan_date),
            str(scan.scan_time),
            scan.location or 'N/A'
        ])
    
    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(table)
    
    # Build PDF
    doc.build(story)
    return response


@librarian_required
def user_scan_history(request, user_id):
    """View detailed scan history for a specific user"""
    user = get_object_or_404(CustomUser, id=user_id)
    scans = QRScanLog.objects.filter(scanned_user=user).order_by('-scan_timestamp')
    
    # Pagination
    paginator = Paginator(scans, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics for this user
    total_scans = scans.count()
    first_scan = scans.last() if scans.exists() else None
    last_scan = scans.first() if scans.exists() else None
    
    # Scan types for this user
    user_scan_types = {}
    for scan_type, _ in QRScanLog.SCAN_TYPE_CHOICES:
        count = scans.filter(scan_type=scan_type).count()
        user_scan_types[scan_type] = count
    
    context = {
        'user': user,
        'page_obj': page_obj,
        'total_scans': total_scans,
        'first_scan': first_scan,
        'last_scan': last_scan,
        'user_scan_types': user_scan_types,
    }
    
    return render(request, 'libapp/user_scan_history.html', context)
