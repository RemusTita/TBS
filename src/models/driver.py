import bcrypt
from enums.driver_availability_status import DriverAvailabilityStatus


class Driver:

    def __init__(self, email: str, password: str, vehicle: str, registration_number: str, full_name: str,
                 status: DriverAvailabilityStatus = DriverAvailabilityStatus.AVAILABLE, driver_id: int = None,
                 is_hashed=False):
        self.driver_id: int = driver_id
        self.full_name: str = full_name
        self.vehicle: str = vehicle
        self.registration_number: str = registration_number
        self.availability_status: DriverAvailabilityStatus = status
        self.email: str = email
        self.user_role: str = "driver"
        if is_hashed:
            self.password = password
        else:
            self.password = self.hash_password(password)

    def to_dict(self):
        return {
            'email': self.email,
            'vehicle': self.vehicle,
            'registration_number': self.registration_number,
            'full_name': self.full_name,
            'availability_status': self.availability_status,
            'driver_id': self.driver_id,
            'user_role': self.user_role
        }

    def check_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
