"""Graphical user interface for the Library Management System.

This module provides a simple Tkinter-based interface to the existing
library backend (src/library.py). It aims to keep things lightweight and
work on systems without additional UI frameworks.

Run with:
    python gui.py

Or from the project root:
    python -m gui
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox

from src.library import Library


class LibraryGUI(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("900x650")
        self.minsize(850, 600)

        self.library = Library()
        self.current_admin = None

        self._ensure_assets()
        self._build_ui()

    def _ensure_assets(self):
        """Ensure asset files exist (logo images, etc.)."""
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        os.makedirs(assets_dir, exist_ok=True)

        logo_path = os.path.join(assets_dir, "logo.ppm")
        if not os.path.exists(logo_path):
            self._create_default_logo(logo_path)

        # Load as a PhotoImage to ensure the UI can show an image
        try:
            self.logo_image = tk.PhotoImage(file=logo_path)
        except Exception:
            self.logo_image = None

    def _create_default_logo(self, path):
        """Create a simple PPM logo image file (no external dependencies)."""
        # PPM P3 format: plain-text RGB, easy to generate.
        width, height = 120, 60
        header = f"P3\n{width} {height}\n255\n"
        rows = []

        for y in range(height):
            row = []
            for x in range(width):
                if 10 < x < 60 and 10 < y < 50:
                    # blue book block
                    row.append("34 118 190")
                elif 65 < x < 110 and 10 < y < 50:
                    # light background for text
                    row.append("240 240 240")
                else:
                    row.append("255 255 255")
            rows.append(" ".join(row))

        with open(path, "w", encoding="utf-8") as f:
            f.write(header)
            f.write("\n".join(rows))

    # ------------------------------------------------------------------
    # UI setup
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Top header / logo area
        header = ttk.Frame(self, padding=(12, 12))
        header.pack(fill="x")

        if getattr(self, "logo_image", None):
            logo_label = ttk.Label(header, image=self.logo_image)
            logo_label.image = self.logo_image
            logo_label.pack(side="left")
        else:
            self.logo_canvas = tk.Canvas(header, width=200, height=60, highlightthickness=0)
            self.logo_canvas.pack(side="left")
            self._draw_logo(self.logo_canvas)

        title_label = ttk.Label(
            header,
            text="Library Management",
            font=("Segoe UI", 18, "bold"),
        )
        title_label.pack(side="left", padx=(10, 0), pady=(6, 0))

        # Main area
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=12, pady=6)

        self._show_login_screen()

    def _draw_logo(self, canvas: tk.Canvas):
        """Draw a simple logo using canvas shapes (no external images required)."""
        canvas.delete("all")
        canvas.create_rectangle(5, 10, 55, 50, outline="#28527a", fill="#2f80ed", width=2)
        canvas.create_rectangle(15, 18, 45, 46, outline="white", width=1)
        canvas.create_text(110, 30, text="LIB", anchor="w", font=("Segoe UI", 14, "bold"), fill="#333")
        canvas.create_text(110, 44, text="SYSTEM", anchor="w", font=("Segoe UI", 9), fill="#555")

    def _clear_container(self):
        for child in self.container.winfo_children():
            child.destroy()

    # ------------------------------------------------------------------
    # Login / Admin setup
    # ------------------------------------------------------------------
    def _show_login_screen(self):
        self._clear_container()

        frame = ttk.Frame(self.container, padding=14)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Welcome to the Library", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 8))

        if not self.library.admins:
            ttk.Label(frame, text="No admins found. Create the first admin account.").grid(
                row=1, column=0, columnspan=2, pady=(0, 8)
            )
            self._render_admin_creation(frame, start_row=2)
            return

        self._render_login_form(frame, start_row=1)

    def _render_admin_creation(self, parent, start_row=0):
        self.admin_username = tk.StringVar()
        self.admin_full_name = tk.StringVar()
        self.admin_email = tk.StringVar()
        self.admin_password = tk.StringVar()
        self.admin_confirm = tk.StringVar()

        ttk.Label(parent, text="Username:").grid(row=start_row, column=0, sticky="e", pady=4)
        ttk.Entry(parent, textvariable=self.admin_username, width=30).grid(row=start_row, column=1, pady=4)

        ttk.Label(parent, text="Full name:").grid(row=start_row + 1, column=0, sticky="e", pady=4)
        ttk.Entry(parent, textvariable=self.admin_full_name, width=30).grid(row=start_row + 1, column=1, pady=4)

        ttk.Label(parent, text="Email:").grid(row=start_row + 2, column=0, sticky="e", pady=4)
        ttk.Entry(parent, textvariable=self.admin_email, width=30).grid(row=start_row + 2, column=1, pady=4)

        ttk.Label(parent, text="Password:").grid(row=start_row + 3, column=0, sticky="e", pady=4)
        ttk.Entry(parent, textvariable=self.admin_password, width=30, show="*").grid(row=start_row + 3, column=1, pady=4)

        ttk.Label(parent, text="Confirm:").grid(row=start_row + 4, column=0, sticky="e", pady=4)
        ttk.Entry(parent, textvariable=self.admin_confirm, width=30, show="*").grid(row=start_row + 4, column=1, pady=4)

        btn = ttk.Button(parent, text="Create Admin", command=self._create_first_admin)
        btn.grid(row=start_row + 5, column=0, columnspan=2, pady=(12, 0))

    def _create_first_admin(self):
        username = self.admin_username.get().strip()
        full_name = self.admin_full_name.get().strip()
        email = self.admin_email.get().strip()
        password = self.admin_password.get().strip()
        confirm = self.admin_confirm.get().strip()

        if not username or not full_name or not email:
            messagebox.showwarning("Missing fields", "Please fill in all fields.")
            return

        if password != confirm:
            messagebox.showerror("Password mismatch", "The passwords do not match.")
            return

        if len(password) < 6:
            messagebox.showerror("Invalid password", "Password must be at least 6 characters.")
            return

        admin_id = self.library.create_admin(username, password, email, full_name)
        if admin_id:
            messagebox.showinfo("Success", "Admin account created. Please login.")
            self._show_login_screen()
        else:
            messagebox.showerror("Error", "Failed to create admin. Username may already exist.")

    def _render_login_form(self, parent, start_row=0):
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(parent, text="Username:").grid(row=start_row, column=0, sticky="e", pady=4)
        ttk.Entry(parent, textvariable=self.username_var, width=30).grid(row=start_row, column=1, pady=4)

        ttk.Label(parent, text="Password:").grid(row=start_row + 1, column=0, sticky="e", pady=4)
        ttk.Entry(parent, textvariable=self.password_var, show="*", width=30).grid(row=start_row + 1, column=1, pady=4)

        login_btn = ttk.Button(parent, text="Login", command=self._login)
        login_btn.grid(row=start_row + 2, column=0, columnspan=2, pady=(12, 0))

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Missing credentials", "Enter both username and password.")
            return

        admin = self.library.authenticate_admin(username, password)
        if not admin:
            messagebox.showerror("Login failed", "Invalid username or password.")
            return

        self.current_admin = admin
        self._show_main_app()

    # ------------------------------------------------------------------
    # Main application UI
    # ------------------------------------------------------------------
    def _show_main_app(self):
        self._clear_container()

        # Top row: active user info + logout
        toolbar = ttk.Frame(self.container)
        toolbar.pack(fill="x", pady=(0, 4))

        user_label = ttk.Label(
            toolbar,
            text=f"Logged in as: {self.current_admin.full_name} (@{self.current_admin.username})",
            font=("Segoe UI", 10),
        )
        user_label.pack(side="left", padx=6)

        logout_btn = ttk.Button(toolbar, text="Logout", command=self._logout)
        logout_btn.pack(side="right", padx=6)

        # Tabs
        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True)

        self._build_dashboard_tab()
        self._build_books_tab()
        self._build_members_tab()
        self._build_borrow_tab()
        self._build_search_tab()
        self._build_stats_tab()
        self._build_account_tab()

        # Refresh data when tab changes
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self._refresh_current_tab())

    def _logout(self):
        self.current_admin = None
        self.library.save_data()
        self._show_login_screen()

    def _refresh_current_tab(self):
        # Called when user changes tab; refresh current view
        current = self.notebook.select()
        widget = self.nametowidget(current)
        refresh_method = getattr(widget, "refresh", None)
        if callable(refresh_method):
            refresh_method()

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------
    def _build_dashboard_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Dashboard")

        self.dashboard_stats = ttk.Label(frame, justify="left", font=("Segoe UI", 10))
        self.dashboard_stats.pack(anchor="nw")

        self._update_dashboard_stats()

        # Quick action buttons
        actions = ttk.Frame(frame)
        actions.pack(anchor="nw", pady=8)

        ttk.Button(actions, text="Add Book", command=lambda: self.notebook.select(1)).grid(row=0, column=0, padx=4)
        ttk.Button(actions, text="Register Member", command=lambda: self.notebook.select(2)).grid(row=0, column=1, padx=4)
        ttk.Button(actions, text="Borrow/Return", command=lambda: self.notebook.select(3)).grid(row=0, column=2, padx=4)

        frame.refresh = self._update_dashboard_stats

    def _update_dashboard_stats(self):
        stats = self.library.get_library_stats()
        text = (
            f"Total books: {stats['total_book_titles']}\n"
            f"Total copies: {stats['total_book_copies']}\n"
            f"Available copies: {stats['available_copies']}\n"
            f"Borrowed copies: {stats['borrowed_copies']}\n"
            f"Total members: {stats['total_members']}\n"
            f"Members with borrowed books: {stats['members_with_borrowed_books']}\n"
        )
        self.dashboard_stats.config(text=text)

    # ------------------------------------------------------------------
    # Books Tab
    # ------------------------------------------------------------------
    def _build_books_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Books")

        top = ttk.Frame(frame)
        top.pack(fill="x")

        form = ttk.LabelFrame(top, text="Book Details")
        form.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.book_id_var = tk.StringVar()
        self.book_title_var = tk.StringVar()
        self.book_author_var = tk.StringVar()
        self.book_isbn_var = tk.StringVar()
        self.book_genre_var = tk.StringVar()
        self.book_copies_var = tk.StringVar()

        row = 0
        ttk.Label(form, text="ID (for update/remove):").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.book_id_var, width=15).grid(row=row, column=1, pady=4)
        row += 1
        ttk.Label(form, text="Title:").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.book_title_var, width=35).grid(row=row, column=1, pady=4)
        row += 1
        ttk.Label(form, text="Author:").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.book_author_var, width=35).grid(row=row, column=1, pady=4)
        row += 1
        ttk.Label(form, text="ISBN:").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.book_isbn_var, width=35).grid(row=row, column=1, pady=4)
        row += 1
        ttk.Label(form, text="Genre:").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.book_genre_var, width=35).grid(row=row, column=1, pady=4)
        row += 1
        ttk.Label(form, text="Copies:").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.book_copies_var, width=10).grid(row=row, column=1, sticky="w", pady=4)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=row + 1, column=0, columnspan=2, pady=(8, 0))
        ttk.Button(btn_frame, text="Add", command=self._add_book).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Update", command=self._update_book).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Remove", command=self._remove_book).grid(row=0, column=2, padx=4)

        # Book list
        list_frame = ttk.LabelFrame(frame, text="Books")
        list_frame.pack(fill="both", expand=True, pady=(10, 0))

        columns = ("book_id", "title", "author", "genre", "available")
        self.books_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.books_tree.heading(col, text=col.replace("_", " ").title())
            self.books_tree.column(col, anchor="w")
        self.books_tree.pack(fill="both", expand=True, side="left")
        self.books_tree.bind("<<TreeviewSelect>>", self._on_book_selected)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.books_tree.yview)
        self.books_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frame.refresh = self._refresh_books
        self._refresh_books()

    def _add_book(self):
        title = self.book_title_var.get().strip()
        author = self.book_author_var.get().strip()
        isbn = self.book_isbn_var.get().strip()
        genre = self.book_genre_var.get().strip()
        copies = self.book_copies_var.get().strip() or "1"

        if not title or not author or not isbn:
            messagebox.showwarning("Missing data", "Title, author and ISBN are required.")
            return

        try:
            copies_int = int(copies)
        except ValueError:
            messagebox.showerror("Invalid input", "Copies must be a number.")
            return

        book_id = self.library.add_book(title, author, isbn, genre, copies_int)
        if book_id:
            messagebox.showinfo("Added", f"Book added with ID: {book_id}")
            self._refresh_books()
        else:
            messagebox.showerror("Error", "Failed to add book. ISBN may already exist.")

    def _update_book(self):
        book_id = self.book_id_var.get().strip()
        if not book_id:
            messagebox.showwarning("Missing ID", "Provide the book ID to update.")
            return

        title = self.book_title_var.get().strip() or None
        author = self.book_author_var.get().strip() or None
        genre = self.book_genre_var.get().strip() or None
        copies = self.book_copies_var.get().strip()
        copies_val = None
        if copies:
            try:
                copies_val = int(copies)
            except ValueError:
                messagebox.showerror("Invalid input", "Copies must be a number.")
                return

        if self.library.update_book(book_id, title, author, genre, copies_val):
            messagebox.showinfo("Updated", "Book updated successfully.")
            self._refresh_books()
        else:
            messagebox.showerror("Error", "Book not found.")

    def _remove_book(self):
        book_id = self.book_id_var.get().strip()
        if not book_id:
            messagebox.showwarning("Missing ID", "Provide the book ID to remove.")
            return

        if messagebox.askyesno("Confirm", "Remove this book permanently?"):
            if self.library.remove_book(book_id):
                messagebox.showinfo("Removed", "Book removed.")
                self._refresh_books()
            else:
                messagebox.showerror("Error", "Book not found.")

    def _on_book_selected(self, event):
        selected = self.books_tree.selection()
        if not selected:
            return
        item = self.books_tree.item(selected[0])
        values = item["values"]
        self.book_id_var.set(values[0])
        self.book_title_var.set(values[1])
        self.book_author_var.set(values[2])
        self.book_genre_var.set(values[3])

    def _refresh_books(self):
        for row in self.books_tree.get_children():
            self.books_tree.delete(row)

        for book in sorted(self.library.list_books(), key=lambda b: b.book_id):
            self.books_tree.insert(
                "",
                "end",
                values=(
                    book.book_id,
                    book.title,
                    book.author,
                    book.genre,
                    f"{book.copies_available}/{book.total_copies}",
                ),
            )

    # ------------------------------------------------------------------
    # Members Tab
    # ------------------------------------------------------------------
    def _build_members_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Members")

        top = ttk.Frame(frame)
        top.pack(fill="x")

        form = ttk.LabelFrame(top, text="Member Details")
        form.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.member_id_var = tk.StringVar()
        self.member_name_var = tk.StringVar()
        self.member_email_var = tk.StringVar()
        self.member_phone_var = tk.StringVar()

        row = 0
        ttk.Label(form, text="ID (for update/remove):").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.member_id_var, width=15).grid(row=row, column=1, pady=4)
        row += 1
        ttk.Label(form, text="Name:").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.member_name_var, width=35).grid(row=row, column=1, pady=4)
        row += 1
        ttk.Label(form, text="Email:").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.member_email_var, width=35).grid(row=row, column=1, pady=4)
        row += 1
        ttk.Label(form, text="Phone:").grid(row=row, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.member_phone_var, width=35).grid(row=row, column=1, pady=4)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=row + 1, column=0, columnspan=2, pady=(8, 0))
        ttk.Button(btn_frame, text="Register", command=self._register_member).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Update", command=self._update_member).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Remove", command=self._remove_member).grid(row=0, column=2, padx=4)

        # Member list
        list_frame = ttk.LabelFrame(frame, text="Members")
        list_frame.pack(fill="both", expand=True, pady=(10, 0))

        columns = ("member_id", "name", "email", "borrowed", "fine")
        self.members_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.members_tree.heading(col, text=col.replace("_", " ").title())
            self.members_tree.column(col, anchor="w")
        self.members_tree.pack(fill="both", expand=True, side="left")
        self.members_tree.bind("<<TreeviewSelect>>", self._on_member_selected)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.members_tree.yview)
        self.members_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frame.refresh = self._refresh_members
        self._refresh_members()

    def _register_member(self):
        name = self.member_name_var.get().strip()
        email = self.member_email_var.get().strip()
        phone = self.member_phone_var.get().strip()

        if not name or not email:
            messagebox.showwarning("Missing data", "Name and email are required.")
            return

        member_id = self.library.register_member(name, email, phone)
        if member_id:
            messagebox.showinfo("Registered", f"Member registered with ID: {member_id}")
            self._refresh_members()
        else:
            messagebox.showerror("Error", "Failed to register member. Email may already exist.")

    def _update_member(self):
        member_id = self.member_id_var.get().strip()
        if not member_id:
            messagebox.showwarning("Missing ID", "Provide the member ID to update.")
            return

        name = self.member_name_var.get().strip() or None
        email = self.member_email_var.get().strip() or None
        phone = self.member_phone_var.get().strip() or None

        if self.library.update_member(member_id, name, email, phone):
            messagebox.showinfo("Updated", "Member updated successfully.")
            self._refresh_members()
        else:
            messagebox.showerror("Error", "Member not found.")

    def _remove_member(self):
        member_id = self.member_id_var.get().strip()
        if not member_id:
            messagebox.showwarning("Missing ID", "Provide the member ID to remove.")
            return

        if messagebox.askyesno("Confirm", "Remove this member permanently?"):
            if self.library.remove_member(member_id):
                messagebox.showinfo("Removed", "Member removed.")
                self._refresh_members()
            else:
                messagebox.showerror("Error", "Cannot remove member (they may have borrowed books or not exist).")

    def _on_member_selected(self, event):
        selected = self.members_tree.selection()
        if not selected:
            return
        item = self.members_tree.item(selected[0])
        values = item["values"]
        self.member_id_var.set(values[0])
        self.member_name_var.set(values[1])
        self.member_email_var.set(values[2])

    def _refresh_members(self):
        for row in self.members_tree.get_children():
            self.members_tree.delete(row)

        for member in sorted(self.library.list_members(), key=lambda m: m.member_id):
            email_parts = member.email.split("@")
            masked = f"{email_parts[0][0]}***@{email_parts[1]}" if len(email_parts) > 1 else "***"
            self.members_tree.insert(
                "",
                "end",
                values=(
                    member.member_id,
                    member.name,
                    masked,
                    len(member.borrowed_books),
                    f"{member.fine:.2f}",
                ),
            )

    # ------------------------------------------------------------------
    # Borrow / Return Tab
    # ------------------------------------------------------------------
    def _build_borrow_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Borrow/Return")

        form = ttk.LabelFrame(frame, text="Borrow / Return")
        form.pack(fill="x", pady=(0, 10))

        self.borrow_member_id = tk.StringVar()
        self.borrow_book_id = tk.StringVar()
        self.borrow_days = tk.StringVar(value="14")

        ttk.Label(form, text="Member ID:").grid(row=0, column=0, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.borrow_member_id, width=20).grid(row=0, column=1, pady=4)
        ttk.Label(form, text="Book ID:").grid(row=0, column=2, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.borrow_book_id, width=20).grid(row=0, column=3, pady=4)
        ttk.Label(form, text="Days:").grid(row=0, column=4, sticky="e", pady=4)
        ttk.Entry(form, textvariable=self.borrow_days, width=6).grid(row=0, column=5, pady=4)

        ttk.Button(form, text="Borrow", command=self._borrow_book).grid(row=1, column=1, pady=8)
        ttk.Button(form, text="Return", command=self._return_book).grid(row=1, column=3, pady=8)

        self.borrow_status = ttk.Label(frame, text="", foreground="#003366")
        self.borrow_status.pack(anchor="w", pady=(0, 10))

        record_frame = ttk.LabelFrame(frame, text="Borrowed Books")
        record_frame.pack(fill="both", expand=True)

        cols = ("member_id", "book_id", "borrow_date", "due_date")
        self.borrowed_tree = ttk.Treeview(record_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.borrowed_tree.heading(col, text=col.replace("_", " ").title())
            self.borrowed_tree.column(col, anchor="w")
        self.borrowed_tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(record_frame, orient="vertical", command=self.borrowed_tree.yview)
        self.borrowed_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frame.refresh = self._refresh_borrowed
        self._refresh_borrowed()

    def _borrow_book(self):
        member_id = self.borrow_member_id.get().strip()
        book_id = self.borrow_book_id.get().strip()
        days_text = self.borrow_days.get().strip() or "14"

        if not member_id or not book_id:
            messagebox.showwarning("Missing data", "Member ID and Book ID are required.")
            return

        try:
            days = int(days_text)
        except ValueError:
            messagebox.showerror("Invalid input", "Days must be a number.")
            return

        if self.library.borrow_book(member_id, book_id, days):
            self.borrow_status.config(text=f"Successfully borrowed book {book_id} for member {member_id}.")
            self._refresh_borrowed()
            self._refresh_books()
            self._refresh_members()
        else:
            messagebox.showerror("Error", "Borrow failed (invalid IDs, no copies available, or already borrowed).")

    def _return_book(self):
        member_id = self.borrow_member_id.get().strip()
        book_id = self.borrow_book_id.get().strip()

        if not member_id or not book_id:
            messagebox.showwarning("Missing data", "Member ID and Book ID are required.")
            return

        fine = self.library.return_book(member_id, book_id)
        if fine is None:
            messagebox.showerror("Error", "Return failed (invalid member or book ID).")
            return

        if fine > 0:
            messagebox.showinfo("Returned", f"Book returned. Overdue fine: {fine:.2f}")
        else:
            messagebox.showinfo("Returned", "Book returned on time.")

        self._refresh_borrowed()
        self._refresh_books()
        self._refresh_members()

    def _refresh_borrowed(self):
        for row in self.borrowed_tree.get_children():
            self.borrowed_tree.delete(row)

        for member in self.library.list_members():
            for borrowed in member.borrowed_books:
                self.borrowed_tree.insert(
                    "",
                    "end",
                    values=(
                        member.member_id,
                        borrowed["book_id"],
                        borrowed["borrow_date"],
                        borrowed["due_date"],
                    ),
                )

    # ------------------------------------------------------------------
    # Search Tab
    # ------------------------------------------------------------------
    def _build_search_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Search")

        self.search_type = tk.StringVar(value="title")
        self.search_query = tk.StringVar()

        search_bar = ttk.Frame(frame)
        search_bar.pack(fill="x")

        ttk.Radiobutton(search_bar, text="Title", variable=self.search_type, value="title").pack(side="left")
        ttk.Radiobutton(search_bar, text="Author", variable=self.search_type, value="author").pack(side="left")
        ttk.Radiobutton(search_bar, text="ISBN", variable=self.search_type, value="isbn").pack(side="left")

        ttk.Entry(search_bar, textvariable=self.search_query, width=40).pack(side="left", padx=8)
        ttk.Button(search_bar, text="Search", command=self._perform_search).pack(side="left")

        self.search_results = ttk.Treeview(frame, columns=("id", "title", "author", "isbn", "available"), show="headings")
        for col in ("id", "title", "author", "isbn", "available"):
            self.search_results.heading(col, text=col.title())
            self.search_results.column(col, anchor="w")
        self.search_results.pack(fill="both", expand=True, pady=(8, 0))

    def _perform_search(self):
        query = self.search_query.get().strip()
        if not query:
            messagebox.showwarning("Missing query", "Enter a search query.")
            return

        results = self.library.search_books(query, self.search_type.get())
        for row in self.search_results.get_children():
            self.search_results.delete(row)

        for book in results:
            self.search_results.insert(
                "",
                "end",
                values=(
                    book.book_id,
                    book.title,
                    book.author,
                    book.isbn,
                    f"{book.copies_available}/{book.total_copies}",
                ),
            )

    # ------------------------------------------------------------------
    # Stats Tab
    # ------------------------------------------------------------------
    def _build_stats_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Stats")

        self.stats_text = ttk.Label(frame, justify="left", font=("Segoe UI", 10))
        self.stats_text.pack(anchor="nw")

        frame.refresh = self._update_stats
        self._update_stats()

    def _update_stats(self):
        stats = self.library.get_library_stats()
        text = (
            f"Total book titles: {stats['total_book_titles']}\n"
            f"Total book copies: {stats['total_book_copies']}\n"
            f"Available copies: {stats['available_copies']}\n"
            f"Borrowed copies: {stats['borrowed_copies']}\n"
            f"Total members: {stats['total_members']}\n"
            f"Members with borrowed books: {stats['members_with_borrowed_books']}\n"
        )
        self.stats_text.config(text=text)

    # ------------------------------------------------------------------
    # Account Tab
    # ------------------------------------------------------------------
    def _build_account_tab(self):
        frame = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(frame, text="Account")

        self.account_info = ttk.Label(frame, justify="left", font=("Segoe UI", 10))
        self.account_info.pack(anchor="nw")

        change_frame = ttk.LabelFrame(frame, text="Change Password")
        change_frame.pack(fill="x", pady=(12, 0))

        self.current_password = tk.StringVar()
        self.new_password = tk.StringVar()
        self.confirm_password = tk.StringVar()

        ttk.Label(change_frame, text="Current:").grid(row=0, column=0, sticky="e", pady=4)
        ttk.Entry(change_frame, textvariable=self.current_password, show="*", width=30).grid(row=0, column=1, pady=4)
        ttk.Label(change_frame, text="New:").grid(row=1, column=0, sticky="e", pady=4)
        ttk.Entry(change_frame, textvariable=self.new_password, show="*", width=30).grid(row=1, column=1, pady=4)
        ttk.Label(change_frame, text="Confirm:").grid(row=2, column=0, sticky="e", pady=4)
        ttk.Entry(change_frame, textvariable=self.confirm_password, show="*", width=30).grid(row=2, column=1, pady=4)

        ttk.Button(change_frame, text="Change Password", command=self._change_password).grid(row=3, column=0, columnspan=2, pady=8)

        frame.refresh = self._update_account_info
        self._update_account_info()

    def _update_account_info(self):
        if not self.current_admin:
            return

        info = (
            f"Username: {self.current_admin.username}\n"
            f"Full name: {self.current_admin.full_name}\n"
            f"Email: {self.current_admin.email}\n"
            f"Created: {self.current_admin.created_date}\n"
            f"Last login: {self.current_admin.last_login or 'N/A'}\n"
        )
        self.account_info.config(text=info)

    def _change_password(self):
        old = self.current_password.get().strip()
        new = self.new_password.get().strip()
        confirm = self.confirm_password.get().strip()

        if not old or not new:
            messagebox.showwarning("Missing data", "Provide both current and new passwords.")
            return

        if new != confirm:
            messagebox.showerror("Mismatch", "New password and confirmation do not match.")
            return

        if len(new) < 6:
            messagebox.showerror("Weak password", "Password must be at least 6 characters.")
            return

        if not self.current_admin.change_password(old, new):
            messagebox.showerror("Error", "Current password is incorrect.")
            return

        self.library.save_data()
        messagebox.showinfo("Success", "Password changed successfully.")
        self.current_password.set("")
        self.new_password.set("")
        self.confirm_password.set("")


def main():
    app = LibraryGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
