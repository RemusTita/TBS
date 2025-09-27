from database.db_manager import DatabaseManager
from enums.booking_status import BookingStatus
from models.booking import Booking


class BookingService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self._create_tables()

    def _create_tables(self):
        query = '''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            driver_id INTEGER,
            pickup_location TEXT NOT NULL,
            dropoff_location TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (driver_id) REFERENCES drivers (driver_id)
        )
        '''
        self.db_manager.execute_query(query)

    def create_booking(self, booking: Booking, driver_id: int = None):
        # Insert the booking
        booking_query = '''
        INSERT INTO bookings (driver_id, customer_id, pickup_location, dropoff_location, date, time, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cursor = self.db_manager.execute_query(booking_query, (
            driver_id,
            booking.customer_id,
            booking.pickup_location,
            booking.dropoff_location,
            booking.date,
            booking.time,
            booking.status.value
        ))

        booking_id = self.db_manager.get_last_insert_id(cursor)

        return {
            'message': 'Booking created',
            'booking_id': booking_id,
            'booking': booking.to_dict(),
        }

    def view_booking_details(self, booking_id: int):
        query = '''
                SELECT 
                    bookings.booking_id,
                    bookings.customer_id,
                    bookings.driver_id,
                    bookings.pickup_location,
                    bookings.dropoff_location,
                    bookings.date,
                    bookings.time,
                    bookings.status,
                    drivers.full_name AS driver_name,
                    drivers.vehicle AS driver_vehicle,
                    drivers.registration_number AS driver_registration
                FROM bookings
                LEFT JOIN drivers ON bookings.driver_id = drivers.driver_id
                WHERE bookings.booking_id = ?
            '''

        result = self.db_manager.fetch_query(query, (booking_id,))

        if not result:
            print("Booking not found")
            return None

        booking_data = result[0]
        (booking_id, customer_id, driver_id, pickup_location, dropoff_location, date, time, status, driver_full_name,
         driver_vehicle, driver_registration_number) = booking_data

        booking = {
            "booking_id": booking_id,
            "customer_id": customer_id,
            "driver_id": driver_id,
            "pickup_location": pickup_location,
            "dropoff_location": dropoff_location,
            "date": date,
            "time": time,
            "status": status,
        }

        driver = {
            "driver_id": driver_id,
            "full_name": driver_full_name,
            "vehicle": driver_vehicle,
            "registration_number": driver_registration_number,
        }

        booking_details = {
            "booking": booking,
            "driver": driver,
        }

        return booking_details


    def cancel_booking(self, booking_id):
        # First, get the current booking details
        query_get_booking = """
        SELECT driver_id, status
        FROM bookings
        WHERE booking_id = ?
        """
        current_booking = self.db_manager.fetch_query(query_get_booking, (booking_id,))

        if not current_booking:
            raise ValueError(f"No booking found with ID {booking_id}")

        current_driver_id, current_status = current_booking[0]

        if current_status == BookingStatus.CANCELLED.value:
            print(f"Booking {booking_id} its already cancelled.")
            return True

        # Update the booking status to cancelled
        query_update_booking = """
        UPDATE bookings
        SET status = ?, driver_id = NULL
        WHERE booking_id = ?
        """
        self.db_manager.execute_query(query_update_booking,
                                      (BookingStatus.CANCELLED.value, booking_id))

        # If there was a driver assigned, update their status to available
        if current_driver_id is not None:
            query_update_driver = """
            UPDATE drivers
            SET availability_status = 'available'
            WHERE driver_id = ?
            """
            self.db_manager.execute_query(query_update_driver, (current_driver_id,))

        print(f"Booking {booking_id} has been cancelled successfully.")
        return True
