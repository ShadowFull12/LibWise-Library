# Library Management System

A full-fledged library book borrowing management portal built with Flask, Python, and SQLite. This application provides a complete solution for managing books, users, and borrowing operations with separate interfaces for administrators and regular users.

## Features

### For Users
- 📚 **Browse Books**: Search and filter books by title, author, ISBN, or category
- 📖 **Borrow Books**: Easy one-click borrowing system
- 📋 **My Books**: View all borrowed books with due dates and status
- 💰 **Fine Tracking**: Automatic fine calculation for overdue books
- 📊 **Dashboard**: Personal statistics and borrowing history

### For Administrators
- 👨‍💼 **Admin Dashboard**: Overview of library statistics
- ➕ **Add Books**: Add new books to the library collection
- ✏️ **Edit Books**: Update book information
- 🗑️ **Delete Books**: Remove books from the system
- 👥 **User Management**: View all users and their borrowing statistics
- 📜 **Borrow Records**: Manage all borrowing records with filtering options
- ✅ **Return Books**: Mark books as returned and calculate fines

## Technology Stack

- **Backend**: Flask (Python 3.x)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Authentication**: Session-based authentication with password hashing
- **Styling**: Custom CSS with gradient designs and responsive layout

## Team Members

| Name | Student Code | Role |
|------|--------------|------|
| Kumaresh Pradhan | BWU/BTA/24/508 | Frontend |
| Debosmita Banerjee | BWU/BTA/24/683 | Frontend |
| Shreya Jana | BWU/BTA/24/527 | Backend |
| Aritra Mukherjee | BWU/BTA/24/510 | Backend |
| Anushuya Bose | BWU/BTA/24/509 | Database |

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd "python mini project"
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Initialize the database**
   ```powershell
   python init_db.py
   ```
   This will create the database and populate it with sample data including:
   - Admin account
   - 3 user accounts
   - 10 sample books
   - 3 sample borrow records

4. **Run the application**
   ```powershell
   python app.py
   ```

5. **Access the application**
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Demo Accounts

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

### User Account
- **Username**: `user`
- **Password**: `user123`

## Project Structure

```
python mini project/
├── app.py                  # Main Flask application
├── models.py              # Database models (User, Book, BorrowRecord)
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── library.db            # SQLite database (created after init)
└── templates/
    ├── base.html         # Base template with navbar and footer
    ├── librarylogin.html # Login page
    ├── dashboard.html    # User dashboard
    ├── Admindashbord.html # Admin dashboard
    ├── borrowbooks.html  # Browse books page
    ├── addbook.html      # Add/Edit book form
    ├── Managebook(Admin).html # Manage books page
    ├── Manageuser.html   # Manage users page
    └── borrowrecord.html # Borrow records page
```

## Key Features Explained

### Authentication System
- Secure password hashing using Werkzeug
- Session-based authentication
- Role-based access control (Admin/User)
- Login required decorators for protected routes

### Book Management
- CRUD operations for books
- ISBN uniqueness validation
- Automatic inventory tracking
- Category-based organization

### Borrowing System
- 14-day borrowing period
- Automatic overdue detection
- Fine calculation (₹10 per day)
- Duplicate borrow prevention
- Return date tracking

### Database Models

#### User
- Username, password (hashed)
- Full name
- Admin flag
- Relationships to borrow records

#### Book
- Title, author, ISBN
- Publisher, publication year
- Category, description
- Total and available copies
- Relationships to borrow records

#### BorrowRecord
- User and book references
- Borrow date, due date, return date
- Status (borrowed, overdue, returned)
- Fine amount calculation

## Routes Overview

### Public Routes
- `/` or `/login` - Login page

### User Routes
- `/dashboard` - User dashboard
- `/books` - Browse all books
- `/borrow/<book_id>` - Borrow a book
- `/my-books` - View borrowed books

### Admin Routes
- `/admin` - Admin dashboard
- `/admin/books` - Manage books
- `/admin/books/add` - Add new book
- `/admin/books/edit/<id>` - Edit book
- `/admin/books/delete/<id>` - Delete book
- `/admin/users` - Manage users
- `/admin/borrow-records` - View all borrow records
- `/admin/return-book/<id>` - Mark book as returned

### Common Routes
- `/logout` - Logout user

## Configuration

### Change Secret Key
For production, update the secret key in `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

### Fine Per Day
To change the fine amount, modify the `calculate_fine()` method in `models.py`:
```python
def calculate_fine(self, fine_per_day=10):  # Change 10 to your desired amount
```

### Borrowing Period
To change the borrowing period, update the `borrow_book()` route in `app.py`:
```python
due_date=datetime.utcnow() + timedelta(days=14)  # Change 14 to desired days
```

## Troubleshooting

### Database Issues
If you encounter database errors, reinitialize the database:
```powershell
python init_db.py
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use a different port
```

### Module Not Found
Ensure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

## Future Enhancements

- [ ] User registration system
- [ ] Email notifications for due dates
- [ ] Book reservations
- [ ] Advanced search with multiple filters
- [ ] Export reports to PDF/Excel
- [ ] Book cover image uploads
- [ ] Rating and review system
- [ ] Fine payment integration

## License

This project is created for educational purposes.

## Support

For issues or questions, please check the code comments or review the Flask documentation.

---

**Developed with ❤️ using Flask & Python**
