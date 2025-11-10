# SYSTEM DESIGN - ReadOps Library Management System

## 5.1 SYSTEM ARCHITECTURE

### Overview
The ReadOps Library Management System follows a modern three-tier architecture built on Django framework, providing a comprehensive solution for both physical and digital library management. The system integrates multiple advanced features including QR code systems, payment processing, analytics, and AI-powered recommendations.

### Architecture Components

#### 1. **Presentation Layer (Frontend)**
- **Web Interface**: HTML5, CSS3, JavaScript, Bootstrap
- **Responsive Design**: Mobile-first approach with cross-device compatibility
- **User Interface Components**:
  - User Dashboard
  - Librarian Dashboard
  - Digital Library Interface
  - Payment Interface
  - Analytics Dashboard
  - QR Code Scanner Interface

#### 2. **Application Layer (Backend)**
- **Django Framework**: Python-based web framework
- **View Controllers**: 
  - Main views (views.py)
  - Digital library views (digital_views.py)
  - QR code views (qr_views.py)
  - Advanced analytics views (advanced_views.py)
- **Business Logic Services**:
  - Email Service (email_service.py)
  - SMS Service (sms_service.py)
  - Advanced Tools (advanced_tools.py)
- **Authentication & Authorization**:
  - Custom user model with role-based access
  - Librarian and regular user permissions
  - Session management

#### 3. **Data Layer**
- **Database**: SQLite3 (development) / PostgreSQL (production)
- **Models**: 12 comprehensive data models
- **File Storage**: Django FileSystemStorage for media files
- **Caching**: Session-based caching for performance

#### 4. **External Services Integration**
- **Payment Gateways**: UPI QR code payments
- **SMS Providers**: Fast2SMS, TextLocal, Twilio
- **Email Services**: SMTP backend integration
- **QR Code Generation**: qrcode library integration

### System Flow Architecture
1. **User Request** → **Django URL Router** → **View Controller**
2. **View Controller** → **Business Logic** → **Model Layer**
3. **Model Layer** → **Database** → **Response Processing**
4. **Response Processing** → **Template Rendering** → **User Interface**

## 5.2 BLOCK DIAGRAM

The block diagram illustrates the high-level system architecture showing the interaction between different components:

```
┌─────────────────────────────────────────────────────────────────┐
│                        READOPS LIBRARY MANAGEMENT SYSTEM      │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   WEB CLIENT     │    │  MOBILE CLIENT  │    │ ADMIN PANEL │ │
│  │   (Browser)      │    │   (Responsive)  │    │             │ │
│  └─────────┬─────────┘    └─────────┬───────┘    └──────┬──────┘ │
│            │                        │                   │        │
│            └────────────────────────┼───────────────────┘        │
│                                     │                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                PRESENTATION LAYER                            │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │   User UI   │ │ Librarian UI│ │ Payment UI  │           │ │
│  │  │  Dashboard  │ │  Dashboard   │ │   Interface │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │ Digital Lib │ │ QR Scanner   │ │ Analytics   │           │ │
│  │  │ Interface   │ │ Interface    │ │ Dashboard   │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                     │                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                APPLICATION LAYER                           │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │   Views     │ │   Services   │ │  Business   │           │ │
│  │  │ Controllers │ │   Layer      │ │   Logic     │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │ Auth &      │ │   Advanced  │ │   QR Code   │           │ │
│  │  │ Security    │ │   Analytics │ │   Services  │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                     │                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                  DATA LAYER                                 │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │   Models    │ │   Database  │ │ File Storage│           │ │
│  │  │   Layer     │ │   (SQLite3) │ │   System    │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                     │                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              EXTERNAL SERVICES INTEGRATION                  │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │   Payment   │ │   SMS       │ │   Email     │           │ │
│  │  │  Gateways   │ │  Services   │ │  Services   │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │ │
│  │  │   QR Code   │ │   File      │ │   Analytics │           │ │
│  │  │ Generation  │ │  Processing │ │   Engine    │           │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘           │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Block Diagram Explanation

#### **Client Layer**
- **Web Client**: Standard web browsers accessing the system
- **Mobile Client**: Responsive web interface optimized for mobile devices
- **Admin Panel**: Specialized interface for librarians and administrators

#### **Presentation Layer**
- **User Interface Components**: Modular UI components for different functionalities
- **Dashboard Interfaces**: Specialized dashboards for users and librarians
- **Payment Interface**: Secure payment processing interface
- **Analytics Dashboard**: Real-time analytics and reporting interface

#### **Application Layer**
- **View Controllers**: Handle HTTP requests and responses
- **Services Layer**: Business logic and external service integration
- **Authentication & Security**: User authentication and authorization
- **Advanced Analytics**: AI-powered analytics and recommendations

#### **Data Layer**
- **Models Layer**: Database models and business entities
- **Database**: SQLite3 for development, scalable to PostgreSQL
- **File Storage**: Media file management system

#### **External Services**
- **Payment Gateways**: UPI and other payment method integration
- **Communication Services**: SMS and email notification services
- **QR Code Services**: QR code generation and processing
- **Analytics Engine**: Advanced analytics and reporting capabilities

## 5.3 USE CASE DIAGRAM

The use case diagram shows the interactions between different actors and the system:

```
                    READOPS LIBRARY MANAGEMENT SYSTEM
                              USE CASE DIAGRAM

    ┌─────────────────┐                    ┌─────────────────┐
    │   REGULAR USER   │                    │   LIBRARIAN     │
    │                 │                    │                 │
    └─────────┬───────┘                    └─────────┬───────┘
              │                                      │
              │                                      │
    ┌─────────▼───────┐                    ┌─────────▼───────┐
    │   USER ACTIONS  │                    │ LIBRARIAN ACTIONS│
    │                 │                    │                 │
    │ • Register      │                    │ • Manage Books  │
    │ • Login/Logout  │                    │ • View Analytics│
    │ • Browse Books  │                    │ • Manage Users  │
    │ • Borrow Books │                    │ • Process QR    │
    │ • Return Books │                    │ • Send Notifications│
    │ • View Cart    │                    │ • Manage Inventory│
    │ • Make Payment │                    │ • Generate Reports│
    │ • Read Digital │                    │ • Bulk Operations│
    │ • View Notifications│               │ • Manage Fines   │
    └─────────┬───────┘                    └─────────┬───────┘
              │                                      │
              └──────────────┬───────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   SYSTEM CORE  │
                    │                │
                    │ ┌─────────────┐│
                    │ │User Management││
                    │ └─────────────┘│
                    │ ┌─────────────┐│
                    │ │Book Management││
                    │ └─────────────┘│
                    │ ┌─────────────┐│
                    │ │Digital Library││
                    │ └─────────────┘│
                    │ ┌─────────────┐│
                    │ │Payment System││
                    │ └─────────────┘│
                    │ ┌─────────────┐│
                    │ │QR Code System││
                    │ └─────────────┘│
                    │ ┌─────────────┐│
                    │ │Notification ││
                    │ │   System    ││
                    │ └─────────────┘│
                    │ ┌─────────────┐│
                    │ │Analytics &  ││
                    │ │AI Features  ││
                    │ └─────────────┘│
                    └────────────────┘
                             │
                    ┌────────▼────────┐
                    │ EXTERNAL SERVICES│
                    │                  │
                    │ • SMS Providers  │
                    │ • Email Services │
                    │ • Payment Gateways│
                    │ • QR Code APIs   │
                    └──────────────────┘
```

### Use Case Diagram Explanation

#### **Actors**
1. **Regular User**: Library members who borrow books and access digital content
2. **Librarian**: Library staff who manage the system and assist users

#### **User Use Cases**
- **Authentication**: Register, login, logout
- **Book Management**: Browse, search, borrow, return books
- **Digital Library**: Access online reading, download books
- **Payment**: Make payments for fines and digital content
- **Notifications**: Receive and view notifications
- **Personal Features**: View cart, reading history, recommendations

#### **Librarian Use Cases**
- **System Management**: Manage books, users, inventory
- **Analytics**: View reports, analytics dashboard
- **QR Operations**: Scan QR codes, process payments
- **Communication**: Send notifications, manage alerts
- **Administrative**: Bulk operations, fine management, reporting

#### **System Core Components**
- **User Management**: Authentication, authorization, profile management
- **Book Management**: Physical and digital book catalog
- **Payment System**: Transaction processing and verification
- **QR Code System**: QR generation, scanning, and tracking
- **Notification System**: Multi-channel communication
- **Analytics & AI**: Smart recommendations and insights

#### **External Services**
- **Communication**: SMS and email providers
- **Payment**: UPI and other payment gateways
- **QR Services**: QR code generation and processing APIs

## 5.4 CLASS DIAGRAM

The class diagram shows the data models and their relationships:

```
                    READOPS LIBRARY MANAGEMENT SYSTEM
                              CLASS DIAGRAM

┌─────────────────────────────────────────────────────────────────┐
│                        CORE MODELS                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CustomUser    │    │      Book       │    │   Librarian     │
│                 │    │                 │    │                 │
│ - username      │    │ - title         │    │ - user (FK)     │
│ - email         │    │ - description   │    │                 │
│ - phone         │    │ - author        │    │                 │
│ - books (JSON)  │    │ - quantity      │    │                 │
│ - notifications │   │ - department    │    │                 │
│ - cart (JSON)   │    │ - subject       │    │                 │
│ - is_librarian  │    │ - image         │    │                 │
│                 │    │                 │    │                 │
│ + take_book()   │    │                 │    │                 │
│ + return_book() │    │                 │    │                 │
│ + add_to_cart() │    │                 │    │                 │
│ + extend_book() │    │                 │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │ 1:1                  │                      │
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UserQRCode    │    │    Payment       │    │      Fine       │
│                 │    │                 │    │                 │
│ - user (FK)     │    │ - user (FK)     │    │ - user (FK)     │
│ - qr_code_data  │    │ - book (FK)     │    │ - book_title    │
│ - qr_code_image │    │ - book_title    │    │ - book_id       │
│ - is_active     │    │ - amount        │    │ - due_date      │
│ - created_date  │    │ - payment_type  │    │ - amount        │
│ - updated_date  │    │ - payment_method│    │ - days_overdue  │
│                 │    │ - bank_name     │    │ - status         │
│ + generate_qr_  │    │ - payment_date  │    │ - created_date  │
│   data()        │    │                 │    │ - last_updated  │
└─────────┬───────┘    └─────────┬───────┘    │                 │
          │                      │            │ + calculate_    │
          │                      │            │   fine()        │
          │                      │            └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   QRScanLog     │    │ DigitalBook     │    │MobileNotification│
│                 │    │                 │    │                 │
│ - scanned_user  │    │ - title         │    │ - user (FK)     │
│   (FK)          │    │ - author        │    │ - bima_id       │
│ - scanned_by    │    │ - description   │    │ - notification_ │
│   (FK)          │    │ - book_type     │    │   type          │
│ - scan_type     │    │ - category      │    │ - title         │
│ - scan_timestamp│    │ - cover_image   │    │ - message       │
│ - location      │    │ - pdf_file      │    │ - book_title    │
│ - notes         │    │ - word_file     │    │ - book_id       │
│ - ip_address    │    │ - online_reading│    │ - status        │
│ - user_agent    │    │   _price        │    │ - created_date  │
│                 │    │ - download_price│    │ - expires_at    │
│ + scan_date     │    │ - is_free       │    │ - response_date │
│ + scan_time     │    │ - is_active     │    │                 │
└─────────┬───────┘    │ - created_date  │    │ + generate_    │
          │            │ - updated_date  │    │   bima_id()     │
          │            └─────────┬───────┘    │ + is_expired()  │
          │                      │            └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ DigitalBookAccess│    │   QRPayment     │    │                 │
│                 │    │                 │    │                 │
│ - user (FK)     │    │ - user (FK)     │    │                 │
│ - digital_book  │    │ - digital_book_ │    │                 │
│   (FK)          │    │   access (FK)   │    │                 │
│ - access_type   │    │ - amount        │    │                 │
│ - status        │    │ - qr_code_data  │    │                 │
│ - payment_amount│    │ - qr_code_image │    │                 │
│ - access_start_ │    │ - status        │    │                 │
│   date          │    │ - payment_ref   │    │                 │
│ - access_end_   │    │ - created_date  │    │                 │
│   date          │    │ - expires_at    │    │                 │
│ - payment_ref   │    │                 │    │                 │
│ - qr_code       │    │ + is_expired()  │    │                 │
│ - created_date  │    │                 │    │                 │
│                 │    │                 │    │                 │
│ + is_access_    │    │                 │    │                 │
│   valid()       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Class Diagram Explanation

#### **Core User Management**
- **CustomUser**: Extended Django user model with additional fields for library-specific functionality
- **Librarian**: Specialized user type with librarian privileges
- **UserQRCode**: QR code generation and management for user identification

#### **Book Management**
- **Book**: Physical book model with inventory tracking
- **DigitalBook**: Digital book model with pricing and file management
- **DigitalBookAccess**: Tracks user access to digital content

#### **Transaction Management**
- **Payment**: Payment transaction records
- **QRPayment**: QR code-based payment processing
- **Fine**: Fine calculation and tracking system

#### **Communication & Tracking**
- **MobileNotification**: In-app notification system with BIMA IDs
- **QRScanLog**: Audit trail for QR code scanning activities

#### **Key Relationships**
1. **CustomUser** ↔ **Book**: Many-to-many through JSON field for borrowed books
2. **CustomUser** ↔ **DigitalBook**: Many-to-many through DigitalBookAccess
3. **CustomUser** ↔ **Payment**: One-to-many for payment history
4. **CustomUser** ↔ **Fine**: One-to-many for fine records
5. **CustomUser** ↔ **MobileNotification**: One-to-many for notifications
6. **CustomUser** ↔ **UserQRCode**: One-to-one for QR identification
7. **CustomUser** ↔ **QRScanLog**: One-to-many for scan tracking

#### **Key Methods**
- **CustomUser**: `take_book()`, `return_book()`, `add_to_cart()`, `extend_book()`
- **Fine**: `calculate_fine()` for automated fine calculation
- **MobileNotification**: `generate_bima_id()`, `is_expired()`
- **UserQRCode**: `generate_qr_data()` for QR code generation
- **DigitalBookAccess**: `is_access_valid()` for access validation
- **QRPayment**: `is_expired()` for payment expiry checking

This comprehensive class diagram represents the complete data model of the ReadOps Library Management System, showing all entities, their attributes, relationships, and key methods that drive the system's functionality.
