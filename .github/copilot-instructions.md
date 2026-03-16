# Library Management System - Project Instructions

## Project Overview
A comprehensive Library Management System built with Python featuring:
- Book cataloging and inventory management
- Member registration and management
- Book borrowing and returning functionality
- Fine calculation for overdue books
- Search and filter capabilities
- Command-line interface for easy interaction

## Project Structure
```
library-system/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── member.py
│   ├── library.py
│   └── cli.py
├── data/
│   ├── books.json
│   └── members.json
├── main.py
├── README.md
└── requirements.txt
```

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python main.py`

## Features
- Add/Remove/Update books
- Register/Remove members
- Borrow/Return books
- Search books by title or author
- View library inventory
- Calculate and track fines for overdue books
- Persistent data storage using JSON
