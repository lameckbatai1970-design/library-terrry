from src.library import Library
from src.models.book import Book
from src.models.member import Member
from datetime import datetime
import getpass


class LibraryCLI:
    """Command-line interface for the Library Management System."""
    
    def __init__(self):
        """Initialize the CLI with a Library instance."""
        self.library = Library()
        self.current_admin = None  # Tracks logged-in admin
    
    def show_welcome(self):
        """Display welcome screen and handle login/admin creation."""
        print("\n" + "="*60)
        print(" " * 15 + "LIBRARY MANAGEMENT SYSTEM")
        print(" " * 20 + "Welcome!")
        print("="*60)
        
        # Check if any admins exist
        if not self.library.admins:
            self.create_first_admin()
        else:
            self.login_screen()
    
    def create_first_admin(self):
        """Create the first admin account."""
        print("\n" + "="*60)
        print("NO ADMIN ACCOUNT FOUND - CREATE FIRST ADMIN")
        print("="*60)
        
        username = input("\nEnter admin username: ").strip()
        if not username:
            print("✗ Username cannot be empty.")
            return
        
        full_name = input("Enter full name: ").strip()
        email = input("Enter email: ").strip()
        
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        
        if password != confirm_password:
            print("✗ Passwords do not match.")
            return
        
        if len(password) < 6:
            print("✗ Password must be at least 6 characters.")
            return
        
        admin_id = self.library.create_admin(username, password, email, full_name)
        if admin_id:
            print(f"✓ First admin account created successfully! (ID: {admin_id})")
            print("You can now log in with your credentials.\n")
            self.current_admin = self.library.get_admin(admin_id)
        else:
            print("✗ Failed to create admin account.")
    
    def login_screen(self):
        """Display login screen and authenticate user."""
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            print("\n" + "="*60)
            print("LOGIN")
            print("="*60)
            
            username = input("\nEnter username: ").strip()
            password = getpass.getpass("Enter password: ")
            
            admin = self.library.authenticate_admin(username, password)
            
            if admin:
                self.current_admin = admin
                print(f"\n✓ Welcome, {admin.full_name}!")
                return
            else:
                attempts += 1
                remaining = max_attempts - attempts
                print(f"✗ Invalid credentials. {remaining} attempt(s) remaining.")
        
        print("\n✗ Maximum login attempts exceeded. Exiting...")
        exit()
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print(f"LIBRARY MANAGEMENT SYSTEM - User: {self.current_admin.full_name}")
        print("="*60)
        print("\n1. Book Management")
        print("2. Member Management (Protected)")
        print("3. Borrow/Return Books")
        print("4. Search")
        print("5. View Statistics")
        print("6. Fine Management")
        print("7. Account Settings")
        print("8. Dashboard")
        print("0. Logout")
        print("-"*60)

    def show_dashboard(self):
        """Show a quick dashboard with key stats and account info."""
        stats = self.library.get_library_stats()

        print("\n" + "="*60)
        print(" DASHBOARD ".center(60, "="))
        print("="*60)
        print(f"Logged in as: {self.current_admin.full_name} (@{self.current_admin.username})")
        if self.current_admin.last_login:
            print(f"Last login: {self.current_admin.last_login}")
        print("\n-- Library Overview --")
        print(f"Total books: {stats['total_book_titles']}")
        print(f"Total copies: {stats['total_book_copies']}")
        print(f"Available copies: {stats['available_copies']}")
        print(f"Borrowed copies: {stats['borrowed_copies']}")
        print(f"Total members: {stats['total_members']}")
        print(f"Members with borrowed books: {stats['members_with_borrowed_books']}")
        print("="*60)

    def display_book_menu(self):
        """Display book management options."""
        print("\n--- BOOK MANAGEMENT ---")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Update a book")
        print("4. List all books")
        print("0. Back to main menu")
    
    def display_member_menu(self):
        """Display member management options."""
        print("\n--- MEMBER MANAGEMENT ---")
        print("1. Register a member")
        print("2. Remove a member")
        print("3. Update member info")
        print("4. List all members")
        print("0. Back to main menu")
    
    def display_search_menu(self):
        """Display search options."""
        print("\n--- SEARCH ---")
        print("1. Search books by title")
        print("2. Search books by author")
        print("3. Search books by ISBN")
        print("4. Search members by name")
        print("5. Search members by email")
        print("0. Back to main menu")
    
    # ==================== BOOK OPERATIONS ====================
    
    def add_book(self):
        """Add a new book to the library."""
        print("\n--- ADD A BOOK ---")
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        isbn = input("Enter ISBN: ").strip()
        genre = input("Enter genre: ").strip()
        
        try:
            copies = int(input("Enter number of copies (default 1): ") or "1")
        except ValueError:
            print("Invalid input. Setting copies to 1.")
            copies = 1
        
        book_id = self.library.add_book(title, author, isbn, genre, copies)
        
        if book_id:
            print(f"✓ Book added successfully! Book ID: {book_id}")
        else:
            print("✗ Failed to add book. Book ISBN already exists or invalid input.")
    
    def remove_book(self):
        """Remove a book from the library."""
        print("\n--- REMOVE A BOOK ---")
        book_id = input("Enter book ID to remove: ").strip()
        
        if self.library.remove_book(book_id):
            print("✓ Book removed successfully!")
        else:
            print("✗ Book not found.")
    
    def update_book(self):
        """Update book information."""
        print("\n--- UPDATE A BOOK ---")
        book_id = input("Enter book ID to update: ").strip()
        
        book = self.library.get_book(book_id)
        if not book:
            print("✗ Book not found.")
            return
        
        print(f"Current: {book}")
        print("(Press Enter to skip a field)")
        
        title = input("New title: ").strip() or None
        author = input("New author: ").strip() or None
        genre = input("New genre: ").strip() or None
        
        try:
            copies_input = input("New number of copies: ").strip()
            copies = int(copies_input) if copies_input else None
        except ValueError:
            print("Invalid number. Skipping copies update.")
            copies = None
        
        if self.library.update_book(book_id, title, author, genre, copies):
            print("✓ Book updated successfully!")
        else:
            print("✗ Failed to update book.")
    
    def list_books(self):
        """Display all books in the library."""
        books = self.library.list_books()
        
        if not books:
            print("\n✗ No books in the library.")
            return
        
        print("\n--- ALL BOOKS ---")
        print(f"{'ID':<8} {'Title':<20} {'Author':<15} {'Genre':<10} {'Available':<10}")
        print("-" * 65)
        
        for book in sorted(books, key=lambda b: b.book_id):
            print(f"{book.book_id:<8} {book.title:<20} {book.author:<15} {book.genre:<10} {book.copies_available}/{book.total_copies}")
    
    # ==================== MEMBER OPERATIONS ====================
    
    def register_member(self):
        """Register a new library member."""
        print("\n--- REGISTER A MEMBER ---")
        name = input("Enter member name: ").strip()
        email = input("Enter email: ").strip()
        phone = input("Enter phone number: ").strip()
        
        member_id = self.library.register_member(name, email, phone)
        
        if member_id:
            print(f"✓ Member registered successfully! Member ID: {member_id}")
        else:
            print("✗ Failed to register member. Email already exists or invalid input.")
    
    def remove_member(self):
        """Remove a member from the library."""
        print("\n--- REMOVE A MEMBER ---")
        member_id = input("Enter member ID to remove: ").strip()
        
        if self.library.remove_member(member_id):
            print("✓ Member removed successfully!")
        else:
            print("✗ Member not found or has borrowed books that must be returned first.")
    
    def update_member(self):
        """Update member information."""
        print("\n--- UPDATE MEMBER INFO ---")
        member_id = input("Enter member ID to update: ").strip()
        
        member = self.library.get_member(member_id)
        if not member:
            print("✗ Member not found.")
            return
        
        print(f"Current: {member}")
        print("(Press Enter to skip a field)")
        
        name = input("New name: ").strip() or None
        email = input("New email: ").strip() or None
        phone = input("New phone: ").strip() or None
        
        if self.library.update_member(member_id, name, email, phone):
            print("✓ Member updated successfully!")
        else:
            print("✗ Failed to update member.")
    
    def list_members(self):
        """Display all members in the library with privacy protection."""
        members = self.library.list_members()
        
        if not members:
            print("\n✗ No members registered.")
            return
        
        print("\n--- ALL MEMBERS (Privacy Protected) ---")
        print(f"{'ID':<8} {'Name':<20} {'Email':<25} {'Books':<8} {'Fine':<8}")
        print("-" * 75)
        
        for member in sorted(members, key=lambda m: m.member_id):
            books_count = len(member.borrowed_books)
            # Mask email - show first char and last domain
            email_parts = member.email.split('@')
            masked_email = f"{email_parts[0][0]}***@{email_parts[1]}" if len(email_parts) > 1 else "***"
            print(f"{member.member_id:<8} {member.name:<20} {masked_email:<25} {books_count:<8} {member.fine:.2f}")
    
    # ==================== BORROW/RETURN OPERATIONS ====================
    
    def borrow_book(self):
        """Record a book borrowing transaction."""
        print("\n--- BORROW A BOOK ---")
        member_id = input("Enter member ID: ").strip()
        book_id = input("Enter book ID: ").strip()
        
        try:
            days = int(input("Number of days to borrow (default 14): ") or "14")
        except ValueError:
            print("Invalid input. Using 14 days.")
            days = 14
        
        if self.library.borrow_book(member_id, book_id, days):
            member = self.library.get_member(member_id)
            book = self.library.get_book(book_id)
            print(f"✓ {member.name} borrowed '{book.title}' for {days} days")
        else:
            print("✗ Failed to borrow book. Check member ID, book ID, and availability.")
    
    def return_book(self):
        """Record a book return transaction."""
        print("\n--- RETURN A BOOK ---")
        member_id = input("Enter member ID: ").strip()
        book_id = input("Enter book ID: ").strip()
        
        result = self.library.return_book(member_id, book_id)
        
        if result is not None:
            member = self.library.get_member(member_id)
            book = self.library.get_book(book_id)
            if result > 0:
                print(f"✓ {member.name} returned '{book.title}'")
                print(f"⚠ Overdue fine: {result:.2f}")
            else:
                print(f"✓ {member.name} returned '{book.title}' on time!")
        else:
            print("✗ Failed to return book. Check member ID and book ID.")
    
    def view_member_books(self):
        """View books borrowed by a member."""
        print("\n--- BORROWED BOOKS ---")
        member_id = input("Enter member ID: ").strip()
        
        books = self.library.get_member_borrowed_books(member_id)
        
        if books is None:
            print("✗ Member not found.")
            return
        
        if not books:
            print(f"✗ This member has no borrowed books.")
            return
        
        member = self.library.get_member(member_id)
        print(f"\nBooks borrowed by {member.name}:")
        print(f"{'Book ID':<10} {'Title':<20} {'Borrow Date':<12} {'Due Date':<12}")
        print("-" * 55)
        
        for borrowed in books:
            book = self.library.get_book(borrowed['book_id'])
            print(f"{borrowed['book_id']:<10} {book.title:<20} {borrowed['borrow_date']:<12} {borrowed['due_date']:<12}")
    
    # ==================== SEARCH OPERATIONS ====================
    
    def search_books_by_title(self):
        """Search books by title."""
        query = input("Enter book title to search: ").strip()
        results = self.library.search_books(query, 'title')
        self.display_search_results(results)
    
    def search_books_by_author(self):
        """Search books by author."""
        query = input("Enter author name to search: ").strip()
        results = self.library.search_books(query, 'author')
        self.display_search_results(results)
    
    def search_books_by_isbn(self):
        """Search books by ISBN."""
        query = input("Enter ISBN to search: ").strip()
        results = self.library.search_books(query, 'isbn')
        self.display_search_results(results)
    
    def search_members_by_name(self):
        """Search members by name."""
        query = input("Enter member name to search: ").strip()
        results = self.library.search_members(query, 'name')
        self.display_member_search_results(results)
    
    def search_members_by_email(self):
        """Search members by email."""
        query = input("Enter member email to search: ").strip()
        results = self.library.search_members(query, 'email')
        self.display_member_search_results(results)
    
    def display_search_results(self, results):
        """Display book search results."""
        if not results:
            print("\n✗ No books found.")
            return
        
        print(f"\n--- SEARCH RESULTS ({len(results)} found) ---")
        print(f"{'ID':<8} {'Title':<20} {'Author':<15} {'ISBN':<15} {'Available':<10}")
        print("-" * 70)
        
        for book in results:
            print(f"{book.book_id:<8} {book.title:<20} {book.author:<15} {book.isbn:<15} {book.copies_available}/{book.total_copies}")
    
    def display_member_search_results(self, results):
        """Display member search results."""
        if not results:
            print("\n✗ No members found.")
            return
        
        print(f"\n--- SEARCH RESULTS ({len(results)} found) ---")
        print(f"{'ID':<8} {'Name':<20} {'Email':<25} {'Books':<8}")
        print("-" * 65)
        
        for member in results:
            # Mask email - show first char and last domain
            email_parts = member.email.split('@')
            masked_email = f"{email_parts[0][0]}***@{email_parts[1]}" if len(email_parts) > 1 else "***"
            books_count = len(member.borrowed_books)
            print(f"{member.member_id:<8} {member.name:<20} {masked_email:<25} {books_count:<8}")
    
    # ==================== UTILITY OPERATIONS ====================
    
    def view_statistics(self):
        """Display library statistics."""
        stats = self.library.get_library_stats()
        
        print("\n--- LIBRARY STATISTICS ---")
        print(f"Total Book Titles: {stats['total_book_titles']}")
        print(f"Total Book Copies: {stats['total_book_copies']}")
        print(f"Available Copies: {stats['available_copies']}")
        print(f"Borrowed Copies: {stats['borrowed_copies']}")
        print(f"Total Members: {stats['total_members']}")
        print(f"Members with Borrowed Books: {stats['members_with_borrowed_books']}")
    
    def manage_fines(self):
        """Manage member fines."""
        print("\n--- FINE MANAGEMENT ---")
        print("1. View member fine")
        print("2. Pay fine")
        print("0. Back to main menu")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            self.view_fine()
        elif choice == "2":
            self.pay_fine()
        elif choice != "0":
            print("Invalid choice.")
    
    def view_fine(self):
        """View fine for a member."""
        member_id = input("Enter member ID: ").strip()
        member = self.library.get_member(member_id)
        
        if not member:
            print("✗ Member not found.")
            return
        
        member.calculate_fine()
        print(f"\nFine for {member.name}: {member.fine:.2f}")
    
    def pay_fine(self):
        """Record a fine payment."""
        member_id = input("Enter member ID: ").strip()
        member = self.library.get_member(member_id)
        
        if not member:
            print("✗ Member not found.")
            return
        
        member.calculate_fine()
        print(f"Current fine: {member.fine:.2f}")
        
        try:
            amount = float(input("Enter payment amount: "))
            
            if self.library.pay_fine(member_id, amount):
                print(f"✓ Payment processed successfully!")
                member = self.library.get_member(member_id)
                print(f"Remaining fine: {member.fine:.2f}")
            else:
                print("✗ Failed to process payment.")
        except ValueError:
            print("Invalid amount.")
    
    # ==================== MAIN LOOP ====================
    
    def run(self):
        """Run the CLI application."""
        # Show welcome and login screen
        self.show_welcome()

        # Show dashboard after login
        self.show_dashboard()
        
        # Main menu loop
        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.book_menu()
            elif choice == "2":
                self.member_menu()
            elif choice == "3":
                self.borrow_return_menu()
            elif choice == "4":
                self.search_menu()
            elif choice == "5":
                self.view_statistics()
            elif choice == "6":
                self.manage_fines()
            elif choice == "7":
                self.account_settings()
            elif choice == "8":
                self.show_dashboard()
            elif choice == "0":
                print(f"\n✓ Logged out successfully. Thank you for using Library Management System!")
                self.current_admin = None
                self.login_screen()  # Back to login
                self.show_dashboard()
            else:
                print("Invalid choice. Please try again.")
    
    def book_menu(self):
        """Book management menu loop."""
        while True:
            self.display_book_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.update_book()
            elif choice == "4":
                self.list_books()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def member_menu(self):
        """Member management menu loop."""
        while True:
            self.display_member_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.register_member()
            elif choice == "2":
                self.remove_member()
            elif choice == "3":
                self.update_member()
            elif choice == "4":
                self.list_members()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def borrow_return_menu(self):
        """Borrow/return menu loop."""
        while True:
            print("\n--- BORROW/RETURN BOOKS ---")
            print("1. Borrow a book")
            print("2. Return a book")
            print("3. View borrowed books")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.borrow_book()
            elif choice == "2":
                self.return_book()
            elif choice == "3":
                self.view_member_books()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def search_menu(self):
        """Search menu loop."""
        while True:
            self.display_search_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.search_books_by_title()
            elif choice == "2":
                self.search_books_by_author()
            elif choice == "3":
                self.search_books_by_isbn()
            elif choice == "4":
                self.search_members_by_name()
            elif choice == "5":
                self.search_members_by_email()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
    
    # ==================== ACCOUNT SETTINGS ====================
    
    def account_settings(self):
        """Display account settings menu."""
        while True:
            print("\n--- ACCOUNT SETTINGS ---")
            print(f"Logged in as: {self.current_admin.full_name} (@{self.current_admin.username})")
            print(f"Email: {self.current_admin.email}")
            print(f"Created: {self.current_admin.created_date}")
            if self.current_admin.last_login:
                print(f"Last Login: {self.current_admin.last_login}")
            print("\n1. Change password")
            print("0. Back to main menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.change_password()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def change_password(self):
        """Change admin password."""
        print("\n--- CHANGE PASSWORD ---")
        
        old_password = getpass.getpass("Enter current password: ")
        
        if not self.current_admin.verify_password(old_password):
            print("✗ Current password is incorrect.")
            return
        
        new_password = getpass.getpass("Enter new password (min 6 characters): ")
        
        if len(new_password) < 6:
            print("✗ Password must be at least 6 characters.")
            return
        
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if new_password != confirm_password:
            print("✗ Passwords do not match.")
            return
        
        if self.current_admin.change_password(old_password, new_password):
            self.library.save_data()
            print("✓ Password changed successfully!")
        else:
            print("✗ Failed to change password.")
