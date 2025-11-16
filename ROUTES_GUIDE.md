# Library Management System - Complete Routes & Functionality Guide

## 🗺️ Application Routes Map

### Public Routes (No Login Required)

| Route | Method | Description |
|-------|--------|-------------|
| `/` or `/login` | GET, POST | Login page - Authenticates users and redirects based on role |

---

### User Routes (Login Required)

| Route | Method | Description | Functionality |
|-------|--------|-------------|---------------|
| `/dashboard` | GET | User Dashboard | Displays user statistics including current month's fines, books lost, books returned |
| `/books` | GET | Browse Books | Shows all available books with search and filter functionality |
| `/borrow/<book_id>` | POST | Borrow Book | Processes book borrowing, validates availability, creates borrow record |
| `/my-books` | GET | My Borrowed Books | Lists all books borrowed by the user with status and due dates |
| `/search` | GET | Search Books | Alternative search endpoint with query parameters |

---

### Admin Routes (Admin Login Required)

| Route | Method | Description | Functionality |
|-------|--------|-------------|---------------|
| `/admin` | GET | Admin Dashboard | Overview with total books, users, overdue count, active borrows |
| `/admin/books` | GET | Manage Books | Lists all books with edit/delete options |
| `/admin/books/add` | GET, POST | Add Book | Form to add new books to the library |
| `/admin/books/edit/<book_id>` | GET, POST | Edit Book | Form to update existing book information |
| `/admin/books/delete/<book_id>` | POST | Delete Book | Removes book from database (checks for active borrows) |
| `/admin/users` | GET | Manage Users | Lists all users with their statistics |
| `/admin/borrow-records` | GET | Borrow Records | Shows all borrow transactions with filtering |
| `/admin/return-book/<record_id>` | POST | Return Book | Marks book as returned, calculates fine, updates inventory |

---

### Common Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/logout` | GET | Logout | Clears session and redirects to login |

---

### API Routes (JSON Responses)

| Route | Method | Description | Response |
|-------|--------|-------------|----------|
| `/api/books/<book_id>` | GET | Get Book Details | JSON with book information |
| `/api/statistics` | GET | Library Statistics | JSON with library stats (Admin only) |

---

## 📋 Database Models

### User Model
```python
Fields:
- id (Integer, Primary Key)
- username (String, Unique)
- password_hash (String)
- full_name (String)
- is_admin (Boolean)
- created_at (DateTime)

Methods:
- set_password() - Hash and save password
- check_password() - Verify password
- get_active_borrows() - Count active borrowed books
- get_total_fines() - Calculate total outstanding fines
```

### Book Model
```python
Fields:
- id (Integer, Primary Key)
- title (String)
- author (String)
- isbn (String, Unique)
- publisher (String)
- publication_year (Integer)
- category (String)
- description (Text)
- total_copies (Integer)
- available_copies (Integer)
- created_at (DateTime)

Methods:
- is_available() - Check if copies are available
- borrow() - Decrease available copies
- return_book() - Increase available copies
```

### BorrowRecord Model
```python
Fields:
- id (Integer, Primary Key)
- user_id (Foreign Key)
- book_id (Foreign Key)
- borrow_date (DateTime)
- due_date (DateTime)
- return_date (DateTime, nullable)
- status (String: borrowed, returned, overdue)
- fine_amount (Float)

Methods:
- calculate_fine() - Calculate overdue fine
- is_overdue() - Check if book is overdue
- mark_returned() - Process book return
```

---

## 🎯 Key Functionalities

### Authentication & Authorization
```
✓ Session-based authentication
✓ Password hashing (Werkzeug)
✓ Role-based access control
✓ Login required decorators
✓ Admin required decorators
✓ Automatic role-based redirection
```

### Book Operations
```
✓ Add new books with validation
✓ Edit existing book information
✓ Delete books (with active borrow check)
✓ Search by title, author, ISBN
✓ Filter by category
✓ Automatic inventory tracking
✓ ISBN uniqueness validation
```

### Borrowing System
```
✓ One-click book borrowing
✓ Automatic due date calculation (14 days)
✓ Duplicate borrow prevention
✓ Availability checking
✓ Overdue detection
✓ Status updates (borrowed → overdue → returned)
✓ Fine calculation (₹10/day)
✓ Book return processing
```

### User Management
```
✓ View all registered users
✓ Active borrow tracking
✓ Fine tracking per user
✓ User statistics display
```

### Dashboard Features

**User Dashboard:**
```
- Current month's fine total
- Books lost count (overdue > 30 days)
- Books returned count
- Quick search functionality
- Navigation to key sections
```

**Admin Dashboard:**
```
- Total books in library
- Total registered users
- Overdue books count
- Active borrows count
- Quick action links
```

---

## 🔄 Workflow Examples

### User Borrowing a Book
1. User logs in → Redirected to `/dashboard`
2. User clicks "Browse Books" → `/books`
3. User searches/browrows books
4. User clicks "Borrow Book" → POST to `/borrow/<book_id>`
5. System validates availability
6. Creates BorrowRecord with due_date = today + 14 days
7. Decreases available_copies by 1
8. Flash success message
9. Redirects to `/my-books`

### Admin Adding a Book
1. Admin logs in → Redirected to `/admin`
2. Admin clicks "Add Book" → `/admin/books/add`
3. Fills form with book details
4. Submits form → POST to `/admin/books/add`
5. System validates ISBN uniqueness
6. Creates new Book record
7. Flash success message
8. Redirects to `/admin/books`

### Admin Processing Return
1. Admin navigates to `/admin/borrow-records`
2. Views list of all borrows
3. Filters by status if needed
4. Clicks "Mark Return" on overdue book
5. POST to `/admin/return-book/<record_id>`
6. System calculates fine based on overdue days
7. Updates record status to 'returned'
8. Increases available_copies
9. Flash message with fine amount
10. Redirects back to records

---

## 🎨 UI Components

### Standardized Elements (via base.html)
```
✓ Consistent navigation bar
✓ Role-based menu items
✓ Flash message system
✓ Footer with user info
✓ Responsive design
✓ Active link highlighting
```

### Page-Specific Components
```
✓ Search bars with filters
✓ Book cards with availability
✓ Data tables with actions
✓ Forms with validation
✓ Status pills/badges
✓ Statistics cards
```

---

## ⚙️ Configuration Options

### app.py Settings
```python
SECRET_KEY - Session security key
SQLALCHEMY_DATABASE_URI - Database location
BORROW_PERIOD - Days (default: 14)
FINE_PER_DAY - Amount (default: ₹10)
```

### Customizable Features
```
- Borrowing period duration
- Fine calculation rate
- Book lost threshold days
- Maximum books per user
- Password requirements
- Session timeout
```

---

## 🔒 Security Features

```
✓ Password hashing (never stored in plain text)
✓ Session-based authentication
✓ CSRF protection (Flask built-in)
✓ SQL injection prevention (SQLAlchemy ORM)
✓ Authorization checks on all routes
✓ Input validation on forms
```

---

## 📊 Database Relationships

```
User (1) ←→ (Many) BorrowRecord
Book (1) ←→ (Many) BorrowRecord

Cascade Deletes:
- Deleting User → Deletes all BorrowRecords
- Deleting Book → Deletes all BorrowRecords
```

---

## 🔄 Status Flow

### Book Status
```
Available → Borrowed → Returned
     ↓
  Overdue (if past due_date)
```

### User Status
```
Active → Has borrowed books
Inactive → No borrowed books
Overdue → Has overdue books
```

---

## 🎯 Smart Features

### Automatic Processing
```
✓ Overdue detection on page load
✓ Fine calculation on demand
✓ Status updates based on dates
✓ Inventory tracking
✓ Book lost detection
```

### Validation Rules
```
✓ ISBN uniqueness
✓ Book availability before borrow
✓ Duplicate borrow prevention
✓ Active borrow check before delete
✓ Form field validation
```

---

## 📈 Future Enhancement Ideas

```
□ User registration system
□ Email notifications
□ Book reservations
□ Advanced reporting
□ Payment integration
□ Book ratings/reviews
□ Multi-library support
□ Mobile app
□ Book recommendations
□ Barcode scanning
```

---

This guide covers all routes, models, and functionality of the Library Management System. Each component is designed to work together seamlessly while maintaining clean code structure and user-friendly interfaces.
