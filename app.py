from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, User, Book, BorrowRecord
from datetime import datetime, timedelta
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Context processor to make current user available in all templates
@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None}


# ==================== Authentication Routes ====================

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('librarylogin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        # Validation
        if not username or not password or not full_name:
            flash('All fields are required.', 'danger')
            return render_template('signup.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters long.', 'danger')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('signup.html')
        
        # Create new user
        new_user = User(
            username=username,
            full_name=full_name,
            is_admin=False
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


# ==================== User Dashboard Routes ====================

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    
    # Get statistics for user
    active_borrows = BorrowRecord.query.filter_by(
        user_id=user.id, 
        status='borrowed'
    ).count()
    
    overdue_borrows = BorrowRecord.query.filter_by(
        user_id=user.id, 
        status='overdue'
    ).count()
    
    # Calculate current month's fine
    current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_records = BorrowRecord.query.filter(
        BorrowRecord.user_id == user.id,
        BorrowRecord.borrow_date >= current_month_start
    ).all()
    
    current_month_fine = sum(record.calculate_fine() for record in current_month_records)
    
    # Books lost (overdue for more than 30 days)
    books_lost = 0
    for record in BorrowRecord.query.filter_by(user_id=user.id, status='overdue').all():
        if (datetime.utcnow() - record.due_date).days > 30:
            books_lost += 1
    
    # Books returned
    books_returned = BorrowRecord.query.filter_by(
        user_id=user.id, 
        status='returned'
    ).count()
    
    return render_template('dashboard.html', 
                         current_month_fine=current_month_fine,
                         books_lost=books_lost,
                         books_returned=books_returned,
                         active_borrows=active_borrows,
                         overdue_borrows=overdue_borrows)


@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    
    # Build search query
    book_query = Book.query
    
    if query:
        book_query = book_query.filter(
            db.or_(
                Book.title.ilike(f'%{query}%'),
                Book.author.ilike(f'%{query}%'),
                Book.isbn.ilike(f'%{query}%')
            )
        )
    
    if category and category != 'all':
        book_query = book_query.filter_by(category=category)
    
    books = book_query.all()
    
    return render_template('borrowbooks.html', books=books, search_query=query)


@app.route('/books')
@login_required
def show_books():
    """Show all available books"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    book_query = Book.query
    
    if query:
        book_query = book_query.filter(
            db.or_(
                Book.title.ilike(f'%{query}%'),
                Book.author.ilike(f'%{query}%'),
                Book.isbn.ilike(f'%{query}%')
            )
        )
    
    if category:
        book_query = book_query.filter_by(category=category)
    
    books = book_query.all()
    categories = db.session.query(Book.category).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('borrowbooks.html', books=books, categories=categories)


@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    """Borrow a book"""
    book = Book.query.get_or_404(book_id)
    user = User.query.get(session['user_id'])
    
    # Check if book is available
    if not book.is_available():
        flash('This book is not available for borrowing.', 'warning')
        return redirect(url_for('show_books'))
    
    # Check if user already has this book
    existing_borrow = BorrowRecord.query.filter_by(
        user_id=user.id,
        book_id=book_id,
        status='borrowed'
    ).first()
    
    if existing_borrow:
        flash('You have already borrowed this book.', 'warning')
        return redirect(url_for('show_books'))
    
    # Create borrow record
    borrow_record = BorrowRecord(
        user_id=user.id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14),  # 14 days borrowing period
        status='borrowed'
    )
    
    # Decrease available copies
    book.borrow()
    
    db.session.add(borrow_record)
    db.session.commit()
    
    flash(f'Successfully borrowed "{book.title}". Due date: {borrow_record.due_date.strftime("%Y-%m-%d")}', 'success')
    return redirect(url_for('my_books'))


@app.route('/my-books')
@login_required
def my_books():
    """Show user's borrowed books"""
    user = User.query.get(session['user_id'])
    
    # Update status for overdue books
    active_records = BorrowRecord.query.filter_by(
        user_id=user.id,
        status='borrowed'
    ).all()
    
    for record in active_records:
        if record.is_overdue():
            record.status = 'overdue'
            record.calculate_fine()
    
    db.session.commit()
    
    # Get all user's borrow records
    borrow_records = BorrowRecord.query.filter_by(user_id=user.id).order_by(
        BorrowRecord.borrow_date.desc()
    ).all()
    
    return render_template('borrowrecord.html', records=borrow_records, is_user_view=True)


# ==================== Admin Routes ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    total_books = Book.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    
    # Overdue books
    overdue_count = BorrowRecord.query.filter_by(status='overdue').count()
    
    # Active borrows
    active_borrows = BorrowRecord.query.filter_by(status='borrowed').count()
    active_borrows += BorrowRecord.query.filter_by(status='overdue').count()
    
    return render_template('Admindashbord.html',
                         total_books=total_books,
                         total_users=total_users,
                         overdue_count=overdue_count,
                         active_borrows=active_borrows)


@app.route('/admin/books')
@admin_required
def manage_books():
    """Manage all books"""
    books = Book.query.order_by(Book.created_at.desc()).all()
    return render_template('Managebook(Admin).html', books=books)


@app.route('/admin/books/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    """Add new book"""
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        publisher = request.form.get('publisher')
        publication_year = request.form.get('publication_year')
        category = request.form.get('category')
        description = request.form.get('description')
        total_copies = request.form.get('total_copies', 1, type=int)
        
        # Check if ISBN already exists
        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            flash('A book with this ISBN already exists.', 'danger')
            return redirect(url_for('add_book'))
        
        # Create new book
        book = Book(
            title=title,
            author=author,
            isbn=isbn,
            publisher=publisher,
            publication_year=int(publication_year) if publication_year else None,
            category=category,
            description=description,
            total_copies=total_copies,
            available_copies=total_copies
        )
        
        db.session.add(book)
        db.session.commit()
        
        flash(f'Book "{title}" added successfully!', 'success')
        return redirect(url_for('manage_books'))
    
    return render_template('addbook.html')


@app.route('/admin/books/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    """Edit existing book"""
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.isbn = request.form.get('isbn')
        book.publisher = request.form.get('publisher')
        publication_year = request.form.get('publication_year')
        book.publication_year = int(publication_year) if publication_year else None
        book.category = request.form.get('category')
        book.description = request.form.get('description')
        
        new_total = request.form.get('total_copies', type=int)
        if new_total:
            # Adjust available copies proportionally
            borrowed = book.total_copies - book.available_copies
            book.total_copies = new_total
            book.available_copies = max(0, new_total - borrowed)
        
        db.session.commit()
        
        flash(f'Book "{book.title}" updated successfully!', 'success')
        return redirect(url_for('manage_books'))
    
    return render_template('addbook.html', book=book, is_edit=True)


@app.route('/admin/books/delete/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    """Delete a book"""
    book = Book.query.get_or_404(book_id)
    
    # Check if book has active borrows
    active_borrows = BorrowRecord.query.filter_by(
        book_id=book_id,
        status='borrowed'
    ).count()
    
    active_borrows += BorrowRecord.query.filter_by(
        book_id=book_id,
        status='overdue'
    ).count()
    
    if active_borrows > 0:
        flash('Cannot delete book with active borrows.', 'danger')
        return redirect(url_for('manage_books'))
    
    db.session.delete(book)
    db.session.commit()
    
    flash(f'Book "{book.title}" deleted successfully.', 'success')
    return redirect(url_for('manage_books'))


@app.route('/admin/users')
@admin_required
def manage_users():
    """Manage all users"""
    users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).all()
    
    # Calculate statistics for each user
    user_stats = []
    for user in users:
        active_borrows = BorrowRecord.query.filter(
            BorrowRecord.user_id == user.id,
            BorrowRecord.status.in_(['borrowed', 'overdue'])
        ).count()
        
        total_fine = sum(
            record.calculate_fine() 
            for record in BorrowRecord.query.filter_by(user_id=user.id).all()
        )
        
        user_stats.append({
            'user': user,
            'active_borrows': active_borrows,
            'total_fine': total_fine
        })
    
    return render_template('Manageuser.html', user_stats=user_stats)


@app.route('/admin/borrow-records')
@admin_required
def borrow_records():
    """View all borrow records"""
    status_filter = request.args.get('status', 'all')
    
    # Build query based on filter
    query = BorrowRecord.query
    
    if status_filter == 'borrowed':
        query = query.filter_by(status='borrowed')
    elif status_filter == 'overdue':
        query = query.filter_by(status='overdue')
    elif status_filter == 'returned':
        query = query.filter_by(status='returned')
    
    # Update fines for all records
    all_records = BorrowRecord.query.all()
    for record in all_records:
        if record.status in ['borrowed', 'overdue']:
            record.calculate_fine()
    db.session.commit()
    
    records = query.order_by(BorrowRecord.borrow_date.desc()).all()
    
    return render_template('borrowrecord.html', records=records, is_admin_view=True)


@app.route('/admin/return-book/<int:record_id>', methods=['POST'])
@admin_required
def return_book(record_id):
    """Mark a book as returned"""
    record = BorrowRecord.query.get_or_404(record_id)
    
    if record.status == 'returned':
        flash('This book has already been returned.', 'info')
        return redirect(url_for('borrow_records'))
    
    # Mark as returned
    record.mark_returned()
    
    # Return book copy
    book = Book.query.get(record.book_id)
    book.return_book()
    
    db.session.commit()
    
    fine_msg = f' Fine: ₹{record.fine_amount}' if record.fine_amount > 0 else ''
    flash(f'Book returned successfully.{fine_msg}', 'success')
    
    return redirect(url_for('borrow_records'))


# ==================== API Routes (for AJAX) ====================

@app.route('/api/books/<int:book_id>')
@login_required
def get_book_details(book_id):
    """Get book details as JSON"""
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'publisher': book.publisher,
        'publication_year': book.publication_year,
        'category': book.category,
        'description': book.description,
        'total_copies': book.total_copies,
        'available_copies': book.available_copies,
        'is_available': book.is_available()
    })


@app.route('/api/statistics')
@admin_required
def get_statistics():
    """Get library statistics as JSON"""
    total_books = Book.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    active_borrows = BorrowRecord.query.filter(
        BorrowRecord.status.in_(['borrowed', 'overdue'])
    ).count()
    overdue_books = BorrowRecord.query.filter_by(status='overdue').count()
    
    return jsonify({
        'total_books': total_books,
        'total_users': total_users,
        'active_borrows': active_borrows,
        'overdue_books': overdue_books
    })


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# ==================== Template Filters ====================

@app.template_filter('datetime_format')
def datetime_format(value, format='%Y-%m-%d'):
    """Format datetime objects"""
    if value is None:
        return "Not returned"
    if isinstance(value, str):
        return value
    return value.strftime(format)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
