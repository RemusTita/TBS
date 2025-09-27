import bcrypt


class Customer:

    def __init__(self, first_name: str, last_name: str, address: str, postcode: str, phone_number: str, email: str,
                 password: str, customer_id: int = None, is_hashed: bool = False):
        self.customer_id = customer_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.address: str = address
        self.postcode: str = postcode
        self.phone_number: str = phone_number
        self.email: str = email
        self.user_role: str = "customer"
        if is_hashed:
            self.password = password
        else:
            self.password = self.hash_password(password)

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'user_role': self.user_role
        }

    def check_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
