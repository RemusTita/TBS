import bcrypt


class Administrator:
    def __init__(self, full_name: str, email: str, password: str, admin_id: int = None, is_hashed: bool = False):
        self.admin_id = admin_id
        self.full_name = full_name
        self.email: str = email
        self.user_role: str = "admin"
        if is_hashed:
            self.password = password
        else:
            self.password = self.hash_password(password)

    def to_dict(self):
        return {
            'full_name': self.full_name,
            'email': self.email,
            'admin_id': self.admin_id,
            'user_role': self.user_role
        }

    def check_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
