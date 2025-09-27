from database.db_manager import DatabaseManager
from enums.driver_availability_status import DriverAvailabilityStatus
from models.driver import Driver


class DriverService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self._create_tables()

    def _create_tables(self):
        query = '''
        CREATE TABLE IF NOT EXISTS drivers (
            driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            vehicle TEXT NOT NULL,
            registration_number TEXT UNIQUE NOT NULL,
            availability_status NOT NULL DEFAULT 'available',
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_rule TEXT NOT NULL
        )
        '''
        self.db_manager.execute_query(query)

    def add_driver(self, driver: Driver):
        query = '''
        INSERT INTO drivers (full_name, email, password, vehicle, registration_number, availability_status, user_rule) 
        VALUES (?,?,?,?,?,?,?)
        '''

        self.db_manager.execute_query(query, (
            driver.full_name,
            driver.email,
            driver.password,
            driver.vehicle,
            driver.registration_number,
            driver.availability_status.value,
            driver.user_role
        ))

    def login(self, email: str, password_input: str):
        """Verify driver login."""
        query = "SELECT driver_id, full_name, email, password, vehicle, registration_number, availability_status FROM drivers WHERE email = ?"
        driver_data = self.db_manager.fetch_query(query, (email,))

        if not driver_data:
            print("Invalid email or password.")
            return None

        (driver_id, full_name, email, password, vehicle, registration_number, availability_status) = driver_data[0]

        driver = Driver(email=email,
                        password=password,
                        vehicle=vehicle,
                        registration_number=registration_number,
                        full_name=full_name,
                        status=availability_status,
                        driver_id=driver_id,
                        is_hashed=True
                        )

        if driver.check_password(password_input):
            return {
                'message': 'Successfully logged in.',
                'driver': driver.to_dict()
            }

        print("Invalid email or password.")
        return None

    def logout(self):
        pass

    def update_availability_status(self, driver_id: int, availability_status: DriverAvailabilityStatus):

        # Update the driver's status in the database
        query = """
        UPDATE drivers
        SET availability_status = ?
        WHERE driver_id = ?
        """

        self.db_manager.execute_query(query, (availability_status.value, driver_id))
        print(f"Driver {driver_id}'s status updated to {availability_status.value}")
        return True

    def get_assigned_trips(self, driver_id):
        query = """
            SELECT 
                bookings.booking_id,
                customers.first_name AS customer_first_name,
                customers.last_name AS customer_last_name,
                bookings.pickup_location,
                bookings.dropoff_location,
                bookings.date,
                bookings.time
            FROM bookings
            JOIN customers ON bookings.customer_id = customers.customer_id
            WHERE bookings.driver_id = ? AND bookings.status IN ('confirmed', 'in_progress')
            ORDER BY bookings.date, bookings.time
            """

        result = self.db_manager.fetch_query(query, (driver_id,))

        if not result:
            print(f"No assigned trips found for driver {driver_id}")
            return []

        assigned_trips = []

        for trip in result:
            assigned_trips.append({
                "booking_id": trip[0],
                "customer_name": f"{trip[1]} {trip[2]}",
                "pickup_location": trip[3],
                "dropoff_location": trip[4],
                "date": trip[5],
                "time": trip[6],
            })

        return assigned_trips

    def complete_trip(self, booking_id, driver_id):
        # First, verify the booking exists and is assigned to the given driver
        query_check_booking = """
        SELECT status
        FROM bookings
        WHERE booking_id = ? AND driver_id = ?
        """
        result = self.db_manager.fetch_query(query_check_booking, (booking_id, driver_id))

        if not result:
            print(f"No booking found with ID {booking_id} assigned to driver {driver_id}")
            return False

        current_status = result[0][0]
        if current_status not in ['confirmed', 'in_progress']:
            print(f"Booking {booking_id} is not in a state that can be completed (current status: {current_status})")
            return False

        # Update the booking status to completed
        query_update_booking = """
        UPDATE bookings
        SET status = 'completed'
        WHERE booking_id = ?
        """
        self.db_manager.execute_query(query_update_booking, (booking_id,))

        # Update the driver's status to available
        query_update_driver = """
        UPDATE drivers
        SET availability_status = 'available'
        WHERE driver_id = ?
        """
        self.db_manager.execute_query(query_update_driver, (driver_id,))

        print(f"Trip for booking {booking_id} has been marked as completed. Driver {driver_id} is now available.")
        return True
