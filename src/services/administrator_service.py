from datetime import datetime
from database.db_manager import DatabaseManager
from enums.booking_status import BookingStatus
from models.administrator import Administrator


class AdministratorService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables for administrators."""
        admins_table = '''
        CREATE TABLE IF NOT EXISTS administrators (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_role TEXT NOT NULL
        )
        '''
        self.db_manager.execute_query(admins_table)

    def create_administrator(self, administrator: Administrator):
        query = '''
        INSERT INTO administrators (full_name, email, password, user_role)
        VALUES (?, ?, ?, ?)
        '''

        self.db_manager.execute_query(query, (
            administrator.full_name,
            administrator.email,
            administrator.password,
            administrator.user_role
        ))

    def login(self, email: str, password_input: str):
        query = "SELECT admin_id, full_name, email, password FROM administrators WHERE email = ?"
        admin_data = self.db_manager.fetch_query(query, (email,))

        if not admin_data:
            print("Invalid email or password.")
            return None

        admin_id, full_name, email, password = admin_data[0]
        admin = Administrator(full_name=full_name,
                              email=email,
                              password=password,
                              admin_id=admin_id,
                              is_hashed=True
                              )

        if admin.check_password(password_input):
            return {
                "message": "Login successful",
                "admin": admin.to_dict()
            }

        print("Invalid email or password.")
        return None

    def logout(self):
        pass

    def _get_bookings(self, unsigned_only):
        query = """
            SELECT 
                bookings.booking_id,
                bookings.customer_id,
                customers.first_name AS customer_first_name,
                customers.last_name AS customer_last_name,
                bookings.pickup_location,
                bookings.dropoff_location,
                bookings.date,
                bookings.time,
                bookings.status
            FROM bookings
            JOIN customers ON bookings.customer_id = customers.customer_id
        """
        params = ()
        if unsigned_only:
            query += "WHERE bookings.status = ?"
            params = (BookingStatus.PENDING.value,)

        result = self.db_manager.fetch_query(query, params)

        if not result:
            print("No bookings found.")
            return None
        bookings = []
        for booking_data in result:
            (booking_id, customer_id, customer_first_name, customer_last_name, pickup_location, dropoff_location, date,
             time, status) = booking_data

            bookings.append({
                "booking_id": booking_id,
                "customer_id": customer_id,
                "customer_first_name": customer_first_name,
                "customer_last_name": customer_last_name,
                "pickup_location": pickup_location,
                "dropoff_location": dropoff_location,
                "date": date,
                "time": time,
                "status": status
            })
        return bookings


    def get_all_bookings(self):
        return self._get_bookings(unsigned_only=False)

    def get_all_drivers(self):
        query = """
            SELECT driver_id, full_name, vehicle, registration_number, availability_status
            FROM drivers
        """
        driver_data = self.db_manager.fetch_query(query)

        drivers = []
        for driver in driver_data:
            drivers.append({
                "driver_id": driver[0],
                "full_name": driver[1],
                "vehicle": driver[2],
                "registration_number": driver[3],
                "availability_status": driver[4]
            })

        return drivers

    def _check_booking_conflict(self, driver_id: int, date: str, time: str) -> bool:
        # Combine date and time into a single datetime object
        booking_datetime = datetime.strptime(f"{date} {time}", "%d-%m-%Y %H:%M")

        # Format the date and time for SQL query
        date_str = booking_datetime.strftime("%d-%m-%Y")
        time_str = booking_datetime.strftime("%H:%M")

        # Query to check for an exact match of the date and time for the driver
        query = """
        SELECT COUNT(*)
        FROM bookings
        WHERE driver_id = ?
        AND date = ?
        AND time = ?
        AND status IN ('pending', 'confirmed')
        """

        # Execute the query and fetch the result
        result = self.db_manager.fetch_query(query, (driver_id, date_str, time_str))

        # If there are any bookings for this driver with the exact same date and time, return True (conflict)
        if result and len(result) > 0:
            conflict_count = result[0][0]  # First element of the first tuple
            return conflict_count > 0  # True if there's a conflict, otherwise False

        return False  # No conflict found

    def assign_driver(self, booking_id: int, driver_id: int) -> bool:
        query_get_booking = "SELECT date, time FROM bookings WHERE booking_id = ?"
        booking_data = self.db_manager.fetch_query(query_get_booking, (booking_id,))

        if not booking_data:
            raise ValueError(f"No booking found with ID {booking_id}.")

        date, time = booking_data[0]
        print(date, time)

        # Check for booking conflicts
        if self._check_booking_conflict(driver_id, date, time):
            print("Conflict: Driver has overlapping bookings around this time.")
            return False

        # Fetch the driver's current availability status
        query_get_driver_status = "SELECT availability_status FROM drivers WHERE driver_id = ?"
        driver_data = self.db_manager.fetch_query(query_get_driver_status, (driver_id,))

        if not driver_data:
            raise ValueError(f"No driver found with ID {driver_id}.")

        # If no conflict and the driver is available, proceed to assign the driver to the booking
        query_update_booking = "UPDATE bookings SET driver_id = ?, status = 'confirmed' WHERE booking_id = ?"
        self.db_manager.execute_query(query_update_booking, (driver_id, booking_id))

        # Update the driver's status to 'on_trip'
        query_update_driver_status = "UPDATE drivers SET availability_status = 'on_trip' WHERE driver_id = ?"
        self.db_manager.execute_query(query_update_driver_status, (driver_id,))

        print("Driver successfully assigned to the booking.")
        return True
