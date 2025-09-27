from database.db_manager import DatabaseManager
from models.booking import Booking
from models.customer import Customer
from services.booking_service import BookingService


class CustomerService:
    def __init__(self, db_manager: DatabaseManager, booking_service: BookingService):
        self.db_manager = db_manager
        self.booking_service = booking_service
        self._create_tables()

    def _create_tables(self):
        # Create `customers` table
        query_customers = '''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            address TEXT NOT NULL,
            postcode TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_role TEXT NOT NULL
        )
        '''
        self.db_manager.execute_query(query_customers)

    def register(self, first_name, last_name, address, postcode, phone_number, email, password):
        query = '''
        INSERT INTO customers (first_name, last_name, address, postcode, phone_number, email, password, user_role) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        customer = Customer(first_name, last_name, address, postcode, phone_number, email, password)

        self.db_manager.execute_query(query, (
            customer.first_name,
            customer.last_name,
            customer.address,
            customer.postcode,
            customer.phone_number,
            customer.email,
            customer.password,
            customer.user_role
        ))

    def login(self, email: str, password_input: str):
        """Verify customer login."""
        query = "SELECT * FROM customers WHERE email = ?"
        customer_data = self.db_manager.fetch_query(query, (email,))
        if not customer_data:
            print("Invalid email or password.")
            return None
        (customer_id, first_name, last_name, address, postcode, phone_number, email, password, user_role) = \
            customer_data[0]
        customer = Customer(customer_id=customer_id,
                            first_name=first_name,
                            last_name=last_name,
                            address=address,
                            postcode=postcode,
                            phone_number=phone_number,
                            email=email,
                            password=password,
                            is_hashed=True
                            )
        if customer.check_password(password_input):
            return {
                'message': 'Successfully logged in.',
                'customer': customer.to_dict()
            }

        print("Invalid email or password.")
        return None

    def logout(self):
        pass

    def book_taxi(self, customer_id, pickup_location, dropoff_location, date, time):
        booking = Booking(
            customer_id=customer_id,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            date=date,
            time=time
        )
        return self.booking_service.create_booking(booking)

    def cancel_booking(self, booking_id):
        return self.booking_service.cancel_booking(booking_id)

    def view_bookings(self, booking_id: int):
        return self.booking_service.view_booking_details(booking_id)

    def get_booking_history(self, customer_id: int):
        query = '''
            SELECT 
                bookings.booking_id,
                bookings.pickup_location,
                bookings.dropoff_location,
                bookings.date,
                bookings.time,
                bookings.status,
                bookings.driver_id,
                drivers.full_name AS driver_name,
                drivers.vehicle AS driver_vehicle,
                drivers.registration_number AS driver_registration
            FROM bookings
            LEFT JOIN drivers ON bookings.driver_id = drivers.driver_id
            WHERE bookings.customer_id = ?
            ORDER BY bookings.date DESC, bookings.time DESC
        '''

        result = self.db_manager.fetch_query(query, (customer_id,))

        if not result:
            print(f"No completed booking history found for customer {customer_id}")
            return []

        booking_history = []
        for booking in result:
            booking_dict = {
                "booking_id": booking[0],
                "pickup_location": booking[1],
                "dropoff_location": booking[2],
                "date": booking[3],
                "time": booking[4],
                "status": booking[5],
                "driver_id": booking[6],
                "driver_name": booking[7],  # Adding driver name
                "driver_vehicle": booking[8],  # Adding driver vehicle
                "driver_registration": booking[9]  # Adding driver registration number
            }
            booking_history.append(booking_dict)

        return booking_history

    def update_details(self, customer_id: int, first_name: str, last_name: str, address: str, postcode: str,
                       phone_number: str):
        """Update customer details in the database."""
        query = '''
        UPDATE customers
        SET first_name = ?, last_name = ?, address = ?, postcode = ?, phone_number = ?
        WHERE customer_id = ?
        '''
        self.db_manager.execute_query(query, (first_name, last_name, address, postcode, phone_number, customer_id))
