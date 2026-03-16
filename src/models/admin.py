import hashlib
from datetime import datetime


class Admin:
    """Represents an admin/owner of the library."""
    
    def __init__(self, admin_id, username, password, email, full_name):
        """
        Initialize an Admin object.
        
        Args:
            admin_id: Unique identifier for the admin
            username: Username for login
            password: Plain text password (will be hashed)
            email: Email address
            full_name: Full name of the admin
        """
        self.admin_id = admin_id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password_hash = self.hash_password(password)
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.last_login = None
    
    @staticmethod
    def hash_password(password):
        """
        Hash a password using SHA256.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """
        Verify if the provided password matches the stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            True if password is correct, False otherwise
        """
        return self.password_hash == self.hash_password(password)
    
    def update_last_login(self):
        """Update the last login timestamp."""
        self.last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def change_password(self, old_password, new_password):
        """
        Change the admin password.
        
        Args:
            old_password: Current password for verification
            new_password: New password to set
            
        Returns:
            True if successful, False if old password is incorrect
        """
        if not self.verify_password(old_password):
            return False
        
        self.password_hash = self.hash_password(new_password)
        return True
    
    def to_dict(self):
        """Convert admin object to dictionary."""
        return {
            'admin_id': self.admin_id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'password_hash': self.password_hash,
            'created_date': self.created_date,
            'last_login': self.last_login
        }
    
    @staticmethod
    def from_dict(data):
        """Create an Admin object from dictionary."""
        # Create without hashing since we have the hash already
        admin = object.__new__(Admin)
        admin.admin_id = data['admin_id']
        admin.username = data['username']
        admin.email = data['email']
        admin.full_name = data['full_name']
        admin.password_hash = data['password_hash']
        admin.created_date = data['created_date']
        admin.last_login = data.get('last_login')
        return admin
    
    def __str__(self):
        return f"{self.full_name} (@{self.username})"
