from datetime import datetime, timedelta


class Member:
    """Represents a library member."""
    
    def __init__(self, member_id, name, email, phone, registration_date=None):
        """
        Initialize a Member object.
        
        Args:
            member_id: Unique identifier for the member
            name: Name of the member
            email: Email of the member
            phone: Phone number of the member
            registration_date: Date of registration
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.registration_date = registration_date or datetime.now().strftime('%Y-%m-%d')
        self.borrowed_books = []  # List of {book_id, borrow_date, due_date}
        self.fine = 0.0
    
    def add_borrowed_book(self, book_id, borrow_days=14):
        """
        Record a borrowed book.
        
        Args:
            book_id: ID of the borrowed book
            borrow_days: Number of days allowed for borrowing
        """
        borrow_date = datetime.now().strftime('%Y-%m-%d')
        due_date = (datetime.now() + timedelta(days=borrow_days)).strftime('%Y-%m-%d')
        
        self.borrowed_books.append({
            'book_id': book_id,
            'borrow_date': borrow_date,
            'due_date': due_date
        })
    
    def return_borrowed_book(self, book_id):
        """
        Record a returned book.
        
        Args:
            book_id: ID of the returned book
            
        Returns:
            The borrowed book record if found, None otherwise
        """
        for book in self.borrowed_books:
            if book['book_id'] == book_id:
                self.borrowed_books.remove(book)
                return book
        return None
    
    def calculate_fine(self, fine_per_day=5):
        """
        Calculate fine for overdue books.
        
        Args:
            fine_per_day: Fine amount per day overdue
            
        Returns:
            Total fine amount
        """
        total_fine = 0.0
        current_date = datetime.now()
        
        for book in self.borrowed_books:
            due_date = datetime.strptime(book['due_date'], '%Y-%m-%d')
            if current_date > due_date:
                overdue_days = (current_date - due_date).days
                total_fine += overdue_days * fine_per_day
        
        self.fine = total_fine
        return total_fine
    
    def to_dict(self):
        """Convert member object to dictionary."""
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'registration_date': self.registration_date,
            'borrowed_books': self.borrowed_books,
            'fine': self.fine
        }
    
    @staticmethod
    def from_dict(data):
        """Create a Member object from dictionary."""
        member = Member(
            data['member_id'],
            data['name'],
            data['email'],
            data['phone'],
            data.get('registration_date')
        )
        member.borrowed_books = data.get('borrowed_books', [])
        member.fine = data.get('fine', 0.0)
        return member
    
    def __str__(self):
        return f"{self.name} (ID: {self.member_id}, Email: {self.email})"
