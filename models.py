from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_active_borrows(self):
        """Get count of active borrowed books"""
        return BorrowRecord.query.filter_by(
            user_id=self.id, 
            status='borrowed'
        ).count()
    
    def get_total_fines(self):
        """Calculate total outstanding fines"""
        records = BorrowRecord.query.filter_by(user_id=self.id).all()
        return sum(record.fine_amount for record in records if record.fine_amount > 0)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True, cascade='all, delete-orphan')
    
    def is_available(self):
        """Check if book has available copies"""
        return self.available_copies > 0
    
    def borrow(self):
        """Decrease available copies when borrowed"""
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False
    
    def return_book(self):
        """Increase available copies when returned"""
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False
    
    def __repr__(self):
        return f'<Book {self.title}>'


class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='borrowed')  # borrowed, returned, overdue
    fine_amount = db.Column(db.Float, default=0.0)
    
    def calculate_fine(self, fine_per_day=10):
        """Calculate fine based on overdue days"""
        if self.return_date:
            # Fine for late return
            if self.return_date > self.due_date:
                overdue_days = (self.return_date - self.due_date).days
                self.fine_amount = overdue_days * fine_per_day
        else:
            # Fine for current overdue
            if datetime.utcnow() > self.due_date:
                overdue_days = (datetime.utcnow() - self.due_date).days
                self.fine_amount = overdue_days * fine_per_day
                self.status = 'overdue'
        return self.fine_amount
    
    def is_overdue(self):
        """Check if book is overdue"""
        if not self.return_date and datetime.utcnow() > self.due_date:
            return True
        return False
    
    def mark_returned(self):
        """Mark book as returned"""
        self.return_date = datetime.utcnow()
        self.status = 'returned'
        self.calculate_fine()
    
    def __repr__(self):
        return f'<BorrowRecord {self.id}>'
