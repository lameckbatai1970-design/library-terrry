import json
import os
from datetime import datetime
from src.models.book import Book
from src.models.member import Member
from src.models.admin import Admin


class Library:
    """Main Library Management System class."""
    
    def __init__(self, books_file='data/books.json', members_file='data/members.json', admin_file='data/admins.json'):
        """
        Initialize the Library.
        
        Args:
            books_file: Path to books JSON file
            members_file: Path to members JSON file
            admin_file: Path to admins JSON file
        """
        self.books_file = books_file
        self.members_file = members_file
        self.admin_file = admin_file
        self.books = {}  # {book_id: Book object}
        self.members = {}  # {member_id: Member object}
        self.admins = {}  # {admin_id: Admin object}
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(books_file), exist_ok=True)
        
        self.load_data()
    
    def load_data(self):
        """Load books, members, and admins from JSON files."""
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as f:
                books_data = json.load(f)
                for book_id, book_data in books_data.items():
                    self.books[book_id] = Book.from_dict(book_data)
        
        if os.path.exists(self.members_file):
            with open(self.members_file, 'r') as f:
                members_data = json.load(f)
                for member_id, member_data in members_data.items():
                    self.members[member_id] = Member.from_dict(member_data)
        
        if os.path.exists(self.admin_file):
            with open(self.admin_file, 'r') as f:
                admins_data = json.load(f)
                for admin_id, admin_data in admins_data.items():
                    self.admins[admin_id] = Admin.from_dict(admin_data)
    
    def save_data(self):
        """Save books, members, and admins to JSON files."""
        # Save books
        books_data = {book_id: book.to_dict() for book_id, book in self.books.items()}
        with open(self.books_file, 'w') as f:
            json.dump(books_data, f, indent=4)
        
        # Save members
        members_data = {member_id: member.to_dict() for member_id, member in self.members.items()}
        with open(self.members_file, 'w') as f:
            json.dump(members_data, f, indent=4)
        
        # Save admins
        admins_data = {admin_id: admin.to_dict() for admin_id, admin in self.admins.items()}
        with open(self.admin_file, 'w') as f:
            json.dump(admins_data, f, indent=4)
    
    # ==================== BOOK OPERATIONS ====================
    
    def add_book(self, title, author, isbn, genre, copies=1):
        """
        Add a new book to the library.
        
        Args:
            title: Title of the book
            author: Author of the book
            isbn: ISBN of the book
            genre: Genre of the book
            copies: Number of copies to add
            
        Returns:
            Book ID if successful, None otherwise
        """
        book_id = f"B{len(self.books) + 1:04d}"
        
        if isbn in [book.isbn for book in self.books.values()]:
            return None  # Book already exists
        
        book = Book(book_id, title, author, isbn, genre, copies)
        self.books[book_id] = book
        self.save_data()
        return book_id
    
    def remove_book(self, book_id):
        """
        Remove a book from the library.
        
        Args:
            book_id: ID of the book to remove
            
        Returns:
            True if successful, False otherwise
        """
        if book_id in self.books:
            del self.books[book_id]
            self.save_data()
            return True
        return False
    
    def update_book(self, book_id, title=None, author=None, genre=None, copies=None):
        """
        Update book information.
        
        Args:
            book_id: ID of the book to update
            title: New title (optional)
            author: New author (optional)
            genre: New genre (optional)
            copies: New number of copies (optional)
            
        Returns:
            True if successful, False otherwise
        """
        if book_id not in self.books:
            return False
        
        book = self.books[book_id]
        if title:
            book.title = title
        if author:
            book.author = author
        if genre:
            book.genre = genre
        if copies is not None:
            difference = copies - book.total_copies
            book.total_copies = copies
            book.copies_available += difference
        
        self.save_data()
        return True
    
    def get_book(self, book_id):
        """Get a book by ID."""
        return self.books.get(book_id)
    
    def list_books(self):
        """Get all books in the library."""
        return list(self.books.values())
    
    def search_books(self, query, search_type='title'):
        """
        Search books by title or author.
        
        Args:
            query: Search query string
            search_type: 'title', 'author', or 'isbn'
            
        Returns:
            List of matching books
        """
        results = []
        query_lower = query.lower()
        
        for book in self.books.values():
            if search_type == 'title' and query_lower in book.title.lower():
                results.append(book)
            elif search_type == 'author' and query_lower in book.author.lower():
                results.append(book)
            elif search_type == 'isbn' and query == book.isbn:
                results.append(book)
        
        return results
    
    # ==================== MEMBER OPERATIONS ====================
    
    def register_member(self, name, email, phone):
        """
        Register a new library member.
        
        Args:
            name: Name of the member
            email: Email of the member
            phone: Phone number of the member
            
        Returns:
            Member ID if successful, None otherwise
        """
        member_id = f"M{len(self.members) + 1:04d}"
        
        if email in [member.email for member in self.members.values()]:
            return None  # Member already exists
        
        member = Member(member_id, name, email, phone)
        self.members[member_id] = member
        self.save_data()
        return member_id
    
    def remove_member(self, member_id):
        """
        Remove a member from the library.
        
        Args:
            member_id: ID of the member to remove
            
        Returns:
            True if successful, False otherwise
        """
        if member_id in self.members:
            member = self.members[member_id]
            if member.borrowed_books:
                return False  # Cannot remove member with borrowed books
            del self.members[member_id]
            self.save_data()
            return True
        return False
    
    def update_member(self, member_id, name=None, email=None, phone=None):
        """
        Update member information.
        
        Args:
            member_id: ID of the member to update
            name: New name (optional)
            email: New email (optional)
            phone: New phone (optional)
            
        Returns:
            True if successful, False otherwise
        """
        if member_id not in self.members:
            return False
        
        member = self.members[member_id]
        if name:
            member.name = name
        if email:
            member.email = email
        if phone:
            member.phone = phone
        
        self.save_data()
        return True
    
    def get_member(self, member_id):
        """Get a member by ID."""
        return self.members.get(member_id)
    
    def list_members(self):
        """Get all members in the library."""
        return list(self.members.values())
    
    def search_members(self, query, search_type='name'):
        """
        Search members by name or email.
        
        Args:
            query: Search query string
            search_type: 'name' or 'email'
            
        Returns:
            List of matching members
        """
        results = []
        query_lower = query.lower()
        
        for member in self.members.values():
            if search_type == 'name' and query_lower in member.name.lower():
                results.append(member)
            elif search_type == 'email' and query_lower in member.email.lower():
                results.append(member)
        
        return results
    
    # ==================== BORROW/RETURN OPERATIONS ====================
    
    def borrow_book(self, member_id, book_id, borrow_days=14):
        """
        Record a book borrowing transaction.
        
        Args:
            member_id: ID of the member borrowing the book
            book_id: ID of the book being borrowed
            borrow_days: Number of days allowed for borrowing
            
        Returns:
            True if successful, False otherwise
        """
        if member_id not in self.members or book_id not in self.books:
            return False
        
        book = self.books[book_id]
        if book.copies_available <= 0:
            return False  # No copies available
        
        member = self.members[member_id]
        
        # Check if member already borrowed this book
        for borrowed in member.borrowed_books:
            if borrowed['book_id'] == book_id:
                return False  # Already borrowed
        
        book.copies_available -= 1
        member.add_borrowed_book(book_id, borrow_days)
        self.save_data()
        return True
    
    def return_book(self, member_id, book_id):
        """
        Record a book return transaction.
        
        Args:
            member_id: ID of the member returning the book
            book_id: ID of the book being returned
            
        Returns:
            Fine amount if overdue, None if not found or no fine
        """
        if member_id not in self.members or book_id not in self.books:
            return None
        
        member = self.members[member_id]
        borrowed_book = member.return_borrowed_book(book_id)
        
        if borrowed_book is None:
            return None  # Book not found in borrowed list
        
        book = self.books[book_id]
        book.copies_available += 1
        
        # Calculate fine if overdue
        due_date = datetime.strptime(borrowed_book['due_date'], '%Y-%m-%d')
        current_date = datetime.now()
        fine = 0.0
        
        if current_date > due_date:
            overdue_days = (current_date - due_date).days
            fine = overdue_days * 5  # 5 currency units per day
            member.fine -= fine if member.fine > 0 else 0
        
        self.save_data()
        return fine
    
    def get_member_borrowed_books(self, member_id):
        """
        Get all books borrowed by a member.
        
        Args:
            member_id: ID of the member
            
        Returns:
            List of borrowed book records
        """
        if member_id not in self.members:
            return None
        
        return self.members[member_id].borrowed_books
    
    # ==================== UTILITY OPERATIONS ====================
    
    def get_library_stats(self):
        """Get library statistics."""
        total_books = sum(book.total_copies for book in self.books.values())
        available_books = sum(book.copies_available for book in self.books.values())
        total_members = len(self.members)
        total_borrowed = sum(len(member.borrowed_books) for member in self.members.values())
        
        return {
            'total_book_titles': len(self.books),
            'total_book_copies': total_books,
            'available_copies': available_books,
            'borrowed_copies': total_borrowed,
            'total_members': total_members,
            'members_with_borrowed_books': len([m for m in self.members.values() if m.borrowed_books])
        }
    
    def pay_fine(self, member_id, amount):
        """
        Record a fine payment for a member.
        
        Args:
            member_id: ID of the member
            amount: Amount to pay
            
        Returns:
            True if successful, False otherwise
        """
        if member_id not in self.members:
            return False
        
        member = self.members[member_id]
        member.fine = max(0, member.fine - amount)
        self.save_data()
        return True
    
    # ==================== ADMIN OPERATIONS ====================
    
    def create_admin(self, username, password, email, full_name):
        """
        Create a new admin account.
        
        Args:
            username: Username for login
            password: Password (will be hashed)
            email: Email address
            full_name: Full name
            
        Returns:
            Admin ID if successful, None if username already exists
        """
        # Check if username already exists
        if any(admin.username == username for admin in self.admins.values()):
            return None
        
        admin_id = f"A{len(self.admins) + 1:04d}"
        admin = Admin(admin_id, username, password, email, full_name)
        self.admins[admin_id] = admin
        self.save_data()
        return admin_id
    
    def authenticate_admin(self, username, password):
        """
        Authenticate an admin user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Admin object if authentication successful, None otherwise
        """
        for admin in self.admins.values():
            if admin.username == username and admin.verify_password(password):
                admin.update_last_login()
                self.save_data()
                return admin
        return None
    
    def get_admin(self, admin_id):
        """Get an admin by ID."""
        return self.admins.get(admin_id)
    
    def get_admin_by_username(self, username):
        """Get an admin by username."""
        for admin in self.admins.values():
            if admin.username == username:
                return admin
        return None

