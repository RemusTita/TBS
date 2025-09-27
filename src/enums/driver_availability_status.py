from enum import Enum


class DriverAvailabilityStatus(Enum):
    AVAILABLE = "available"
    ON_BREAK = "on_break"
    ON_TRIP = "on_trip"
