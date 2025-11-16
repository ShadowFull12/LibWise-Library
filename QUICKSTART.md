# 🚀 Quick Start Guide - Library Management System

## Getting Started in 3 Steps

### Step 1: Install Dependencies
Open PowerShell in the project directory and run:
```powershell
pip install -r requirements.txt
```

### Step 2: Initialize Database
```powershell
python init_db.py
```

### Step 3: Run the Application
```powershell
python app.py
```

Then open your browser and go to: **http://localhost:5000**

---

## 🔑 Login Credentials

### Admin Access
- **Username**: `admin`
- **Password**: `admin123`

### User Access
- **Username**: `user`
- **Password**: `user123`

---

## 📱 Main Features

### As a User:
1. **Browse Books** - Search and filter the book collection
2. **Borrow Books** - Click "Borrow Book" on any available book
3. **My Books** - View your borrowed books and due dates
4. **Dashboard** - See your borrowing statistics

### As an Admin:
1. **Dashboard** - View library statistics at a glance
2. **Add Book** - Add new books to the collection
3. **Manage Books** - Edit or delete existing books
4. **Manage Users** - View all users and their activity
5. **Borrow Records** - Track all borrowing activity
6. **Return Books** - Process book returns and calculate fines

---

## ⚡ Quick Navigation

Once logged in:

**User Navigation Bar:**
- 🏠 Home - User dashboard
- 📖 Browse Books - View all books
- 📚 My Books - Your borrowed books
- 🚪 Logout

**Admin Navigation Bar:**
- 🏠 Home - Admin dashboard
- ➕ Add Book - Add new books
- 📋 Manage Books - Edit/delete books
- 👥 Manage Users - View users
- 📜 Borrow Records - All transactions
- 🚪 Logout

---

## 🎯 Common Tasks

### Borrow a Book (User)
1. Click **Browse Books** in the navigation
2. Search or browse for a book
3. Click **Borrow Book** on an available book
4. Book is added to **My Books**

### Add a Book (Admin)
1. Click **Add Book** in the navigation
2. Fill in the book details
3. Click **Add Book**
4. Book appears in the collection

### Return a Book (Admin)
1. Go to **Borrow Records**
2. Find the borrowed book
3. Click **Mark Return**
4. Fine is calculated if overdue

---

## 💰 Fine System

- **Borrowing Period**: 14 days
- **Fine Rate**: ₹10 per day
- **Calculation**: Automatic when overdue
- **Status Updates**: Books automatically marked as "Overdue"

---

## 🛠️ Troubleshooting

### Database Issues
If you see database errors, reinitialize:
```powershell
python init_db.py
```

### Port Already in Use
Change port in `app.py` line at the bottom:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Import Errors
Make sure you're in the project directory and run:
```powershell
pip install -r requirements.txt
```

---

## 📂 Project Files

- `app.py` - Main application
- `models.py` - Database models
- `init_db.py` - Database setup
- `templates/` - HTML pages
- `library.db` - Database file (created after init)

---

## 🎨 Features Overview

### ✅ Authentication
- Secure login system
- Password hashing
- Session management
- Role-based access (Admin/User)

### ✅ Book Management
- Add, edit, delete books
- ISBN validation
- Category organization
- Copy tracking

### ✅ Borrowing System
- One-click borrowing
- Automatic due dates
- Overdue detection
- Fine calculation
- Return processing

### ✅ User Interface
- Modern, responsive design
- Consistent navigation
- Flash messages
- Status indicators
- Search and filter

---

## 📞 Need Help?

1. Check the `README.md` for detailed documentation
2. Review code comments in the Python files
3. Test with the demo accounts provided
4. Check Flask documentation at flask.palletsprojects.com

---

**Happy Library Managing! 📚**
