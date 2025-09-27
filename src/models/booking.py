from enums.booking_status import BookingStatus


class Booking:
    def __init__(self, pickup_location: str, dropoff_location: str, date: str, time: str, customer_id: int,
                 status: BookingStatus = BookingStatus.PENDING, driver_id=None, booking_id: int = None):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.driver_id = driver_id
        self.pickup_location: str = pickup_location
        self.dropoff_location: str = dropoff_location
        self.date: str = date
        self.time: str = time
        self.status: BookingStatus = status

    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'driver_id': self.driver_id,
            'pickup_location': self.pickup_location,
            'dropoff_location': self.dropoff_location,
            'date': self.date,
            'time': self.time,
            'status': self.status
        }
