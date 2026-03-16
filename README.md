# Library Management System

A comprehensive Library Management System built with Python for managing books, members, borrowing/returning transactions, and fines with secure admin authentication and privacy protection.

## Features

- **Secure Authentication**: Admin login with SHA256 password hashing
- **Book Management**: Add, remove, update, and list books in the library inventory
- **Member Management**: Register, remove, and update library member information with privacy protection
- **Borrowing System**: Track book borrowing and returning with customizable borrow periods
- **Fine Calculation**: Automatic fine calculation for overdue books (5 currency units per day)
- **Search Functionality**: 
  - Search books by title, author, or ISBN
  - Search members by name or email (with masked email display)
- **Library Statistics**: View comprehensive library inventory and usage statistics
- **Fine Management**: View and pay member fines
- **Account Security**: Change password functionality for admins
- **Privacy Features**: Masked email display in member lists and search results
- **Persistent Storage**: All data is saved to JSON files for persistence between sessions
- **User-Friendly CLI**: Interactive command-line interface with secure login

## Project Structure

```
library-system/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py          # Book class definition
│   │   ├── member.py        # Member class definition
│   │   └── admin.py         # Admin/Owner class definition
│   ├── library.py           # Main Library class with all business logic
│   └── cli.py               # Command-line interface
├── data/
│   ├── books.json           # Books database (auto-created)
│   ├── members.json         # Members database (auto-created)
│   └── admins.json          # Admin accounts (auto-created)
├── main.py                  # Application entry point
├── README.md                # This file
├── requirements.txt         # Project dependencies
└── .github/
    └── copilot-instructions.md  # Project instructions
```

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup Steps

1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application (CLI):
```bash
python main.py
```

Run the application with a graphical user interface (GUI):
```bash
python main.py --gui
```

### First Run - Create Admin Account
On first run, the system will prompt you to create the first admin account:
1. Enter a username for login
2. Provide your full name and email
3. Set a secure password (minimum 6 characters)

### Login
After the initial setup, you will need to log in with your admin credentials every time you start the application:
- **Username**: Your admin username
- **Password**: Your admin password (entered securely without display)
- Maximum 3 login attempts before the application exits

### Main Menu
- **1. Book Management** - Add, remove, update, and list books
- **2. Member Management** - Register, remove, and update members (Protected with privacy)
- **3. Borrow/Return Books** - Manage book borrowing and returns
- **4. Search** - Search books and members
- **5. View Statistics** - See library inventory and usage statistics
- **6. Fine Management** - View and pay member fines
- **7. Account Settings** - Change password and view admin details
- **0. Logout** - Securely log out and return to login screen

## Authentication & Security

### Password Security
- All passwords are hashed using SHA256 algorithm
- Passwords are never stored in plain text
- Minimum password length: 6 characters
- Passwords are entered securely without visual display

### Admin Account Features
- Each admin has a unique username and email
- Account creation date and last login timestamp are tracked
- Change password functionality available in Account Settings
- Session tracking with last login information

## Privacy Protection

### Member Data Privacy
The system implements privacy protection measures:
- **Email Masking**: Member emails are partially masked in list and search results
  - Example: `john@example.com` displays as `j***@example.com`
- **Phone Number Privacy**: Phone numbers are not displayed in member lists (only stored)
- **Selective Display**: Only authenticated admin users can access member information

### Data Protection
- All sensitive data is stored securely
- Admin credentials are password-protected
- Member information requires admin login to access

## Key Features Explained

### Book Management
- **Add Book**: Register a new book with title, author, ISBN, genre, and number of copies
- **Remove Book**: Delete a book from the system
- **Update Book**: Modify book details
- **List Books**: View all books in inventory with availability

### Member Management
- **Register Member**: Create a new member account with name, email, and phone
- **Remove Member**: Delete a member (only if they have no borrowed books)
- **Update Member**: Modify member information
- **List Members**: View all registered members (with email privacy protection)

### Library Operations
- **Borrow Book**: Lend a book to a member (default 14-day period)
- **Return Book**: Register book returns and calculate fines if overdue
- **View Borrowed Books**: See all books borrowed by a specific member

### Search System
- Search books by title, author, or ISBN
- Search members by name or email (results show masked emails)
- Instant results with detailed information

### Fine System
- Automatic fine calculation for overdue books
- Fine rate: 5 currency units per day overdue
- View member fines
- Record fine payments
- Fines are tracked per member

## Data Storage

All data is automatically saved to JSON files in the `data/` directory:
- `books.json` - Contains all book records
- `members.json` - Contains all member records with their borrowing history and fines
- `admins.json` - Contains admin accounts with hashed passwords and login history

Data persists between application sessions.

## Classes Overview

### Admin Class (`src/models/admin.py`)
Represents an admin/owner account with properties:
- `admin_id`: Unique identifier
- `username`: Username for login
- `password_hash`: SHA256 hashed password
- `email`: Admin email address
- `full_name`: Full name of admin
- `created_date`: Account creation timestamp
- `last_login`: Last login timestamp
- Methods:
  - `hash_password()`: Securely hash passwords
  - `verify_password()`: Check login credentials
  - `change_password()`: Update password securely
  - `update_last_login()`: Track login activity

### Book Class (`src/models/book.py`)
Represents a book in the library with properties:
- `book_id`: Unique identifier
- `title`: Book title
- `author`: Author name
- `isbn`: ISBN number
- `genre`: Book genre
- `copies_available`: Number of available copies
- `total_copies`: Total copies in library

### Member Class (`src/models/member.py`)
Represents a library member with properties:
- `member_id`: Unique identifier
- `name`: Member name
- `email`: Member email
- `phone`: Phone number
- `registration_date`: Registration date
- `borrowed_books`: List of borrowed books with dates
- `fine`: Outstanding fine amount

### Library Class (`src/library.py`)
Main class managing all library operations:
- Admin account management and authentication
- Book management (CRUD operations)
- Member management (CRUD operations)
- Borrowing and returning system
- Fine calculation and management
- Search functionality
- Data persistence

## Example Workflow

1. **Register a Member**
   - Menu option: 2 → 1
   - Enter: Name, Email, Phone

2. **Add Books**
   - Menu option: 1 → 1
   - Enter: Title, Author, ISBN, Genre, Copies

3. **Borrow a Book**
   - Menu option: 3 → 1
   - Enter: Member ID, Book ID
   - Specify borrow period (default 14 days)

4. **Return a Book**
   - Menu option: 3 → 2
   - Enter: Member ID, Book ID
   - Fine is calculated if overdue

5. **Check Library Stats**
   - Menu option: 5
   - View total books, available copies, and member statistics

## Error Handling

The system includes error handling for:
- Invalid book/member IDs
- Duplicate entries (ISBN for books, email for members)
- Insufficient book copies
- Members with borrowed books (cannot be removed)
- Invalid numeric input
- Missing data files (automatically created on first run)

## Future Enhancements

Possible improvements for future versions:
- Database integration (SQL/NoSQL)
- Book recommendations based on borrowing history
- Email notifications for overdue books
- Advanced reporting and analytics
- User authentication and roles
- REST API backend
- Web interface

## License

This project is open source and available for educational purposes.

## Author

Terrence Munjoma 

## Support

For issues or questions, please refer to the project documentation or contact the maintainers.
