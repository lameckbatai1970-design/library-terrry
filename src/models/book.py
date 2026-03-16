from datetime import datetime


class Book:
    """Represents a book in the library."""
    
    def __init__(self, book_id, title, author, isbn, genre, copies_available=1):
        """
        Initialize a Book object.
        
        Args:
            book_id: Unique identifier for the book
            title: Title of the book
            author: Author of the book
            isbn: ISBN of the book
            genre: Genre of the book
            copies_available: Number of available copies
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.copies_available = copies_available
        self.total_copies = copies_available
    
    def to_dict(self):
        """Convert book object to dictionary."""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'genre': self.genre,
            'copies_available': self.copies_available,
            'total_copies': self.total_copies
        }
    
    @staticmethod
    def from_dict(data):
        """Create a Book object from dictionary."""
        book = Book(
            data['book_id'],
            data['title'],
            data['author'],
            data['isbn'],
            data['genre'],
            data.get('copies_available', 1)
        )
        book.total_copies = data.get('total_copies', data.get('copies_available', 1))
        return book
    
    def __str__(self):
        return f"'{self.title}' by {self.author} (ID: {self.book_id})"
