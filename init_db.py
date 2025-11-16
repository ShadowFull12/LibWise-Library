"""
Initialize the database and create sample data for the Library Management System.
Run this script once to set up the database with admin and user accounts.
"""

from app import app, db
from models import User, Book, BorrowRecord
from datetime import datetime, timedelta

def init_database():
    """Initialize the database with sample data"""
    
    with app.app_context():
        # Drop all tables and recreate them (for fresh start)
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create Admin User
        print("Creating admin user...")
        admin = User(
            username='admin',
            full_name='Admin User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create Regular Users
        print("Creating regular users...")
        user1 = User(
            username='user',
            full_name='John Doe',
            is_admin=False
        )
        user1.set_password('user123')
        db.session.add(user1)
        
        user2 = User(
            username='alice',
            full_name='Alice Smith',
            is_admin=False
        )
        user2.set_password('alice123')
        db.session.add(user2)
        
        user3 = User(
            username='bob',
            full_name='Bob Johnson',
            is_admin=False
        )
        user3.set_password('bob123')
        db.session.add(user3)
        
        # Commit users first so we can reference them
        db.session.commit()
        
        # Create Sample Books
        print("Creating sample books...")
        books_data = [
            {
                'title': 'Python Programming',
                'author': 'Mark Lutz',
                'isbn': 'B0001',
                'publisher': 'O\'Reilly Media',
                'publication_year': 2013,
                'category': 'Technology',
                'description': 'A comprehensive guide to Python programming.',
                'total_copies': 5,
                'available_copies': 5
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'isbn': 'B0002',
                'publisher': 'Prentice Hall',
                'publication_year': 2008,
                'category': 'Technology',
                'description': 'A handbook of agile software craftsmanship.',
                'total_copies': 3,
                'available_copies': 3
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': 'B0003',
                'publisher': 'Scribner',
                'publication_year': 1925,
                'category': 'Fiction',
                'description': 'A classic American novel about the Jazz Age.',
                'total_copies': 4,
                'available_copies': 4
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': 'B0004',
                'publisher': 'Secker & Warburg',
                'publication_year': 1949,
                'category': 'Fiction',
                'description': 'A dystopian social science fiction novel.',
                'total_copies': 3,
                'available_copies': 3
            },
            {
                'title': 'Sapiens',
                'author': 'Yuval Noah Harari',
                'isbn': 'B0005',
                'publisher': 'Harper',
                'publication_year': 2011,
                'category': 'History',
                'description': 'A brief history of humankind.',
                'total_copies': 4,
                'available_copies': 4
            },
            {
                'title': 'Introduction to Algorithms',
                'author': 'Thomas H. Cormen',
                'isbn': 'B0006',
                'publisher': 'MIT Press',
                'publication_year': 2009,
                'category': 'Technology',
                'description': 'Comprehensive introduction to algorithms.',
                'total_copies': 2,
                'available_copies': 2
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': 'B0007',
                'publisher': 'J. B. Lippincott & Co.',
                'publication_year': 1960,
                'category': 'Fiction',
                'description': 'A classic novel about racial injustice.',
                'total_copies': 5,
                'available_copies': 5
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt',
                'isbn': 'B0008',
                'publisher': 'Addison-Wesley',
                'publication_year': 1999,
                'category': 'Technology',
                'description': 'Your journey to mastery.',
                'total_copies': 3,
                'available_copies': 3
            },
            {
                'title': 'Harry Potter and the Sorcerer\'s Stone',
                'author': 'J.K. Rowling',
                'isbn': 'B0009',
                'publisher': 'Scholastic',
                'publication_year': 1997,
                'category': 'Fiction',
                'description': 'The first book in the Harry Potter series.',
                'total_copies': 6,
                'available_copies': 6
            },
            {
                'title': 'Educated',
                'author': 'Tara Westover',
                'isbn': 'B0010',
                'publisher': 'Random House',
                'publication_year': 2018,
                'category': 'Biography',
                'description': 'A memoir about education and family.',
                'total_copies': 3,
                'available_copies': 3
            }
        ]
        
        books = []
        for book_data in books_data:
            book = Book(**book_data)
            db.session.add(book)
            books.append(book)
        
        db.session.commit()
        
        # Create some sample borrow records
        print("Creating sample borrow records...")
        
        # User1 borrows 2 books
        borrow1 = BorrowRecord(
            user_id=user1.id,
            book_id=books[0].id,  # Python Programming
            borrow_date=datetime.utcnow() - timedelta(days=5),
            due_date=datetime.utcnow() + timedelta(days=9),
            status='borrowed'
        )
        books[0].available_copies -= 1
        db.session.add(borrow1)
        
        # User2 has an overdue book
        borrow2 = BorrowRecord(
            user_id=user2.id,
            book_id=books[1].id,  # Clean Code
            borrow_date=datetime.utcnow() - timedelta(days=20),
            due_date=datetime.utcnow() - timedelta(days=6),
            status='overdue',
            fine_amount=60
        )
        books[1].available_copies -= 1
        db.session.add(borrow2)
        
        # User3 returned a book
        borrow3 = BorrowRecord(
            user_id=user3.id,
            book_id=books[2].id,  # The Great Gatsby
            borrow_date=datetime.utcnow() - timedelta(days=10),
            due_date=datetime.utcnow() - timedelta(days=-4),
            return_date=datetime.utcnow() - timedelta(days=2),
            status='returned',
            fine_amount=0
        )
        db.session.add(borrow3)
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("Database initialized successfully!")
        print("="*50)
        print("\n📚 Library Management System - Demo Accounts")
        print("-"*50)
        print("\n👨‍💼 Admin Account:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n👤 User Accounts:")
        print("   Username: user    | Password: user123")
        print("   Username: alice   | Password: alice123")
        print("   Username: bob     | Password: bob123")
        print("\n" + "="*50)
        print(f"Total Books: {len(books)}")
        print(f"Total Users: 3")
        print(f"Sample Borrow Records: 3")
        print("="*50 + "\n")
        print("✅ You can now run the application with: python app.py")
        print()

if __name__ == '__main__':
    init_database()
