from tkinter import Tk, mainloop
from database.db_manager import DatabaseManager
from gui.Application import Application
from models.administrator import Administrator
from models.driver import Driver
from services.administrator_service import AdministratorService
from services.booking_service import BookingService
from services.customer_service import CustomerService
from services.driver_service import DriverService

def main():
    print("Starting application setup...")

    try:
        # Initialize database and services
        db_manager = DatabaseManager("src/taxi_booking_system.db")
        booking_service = BookingService(db_manager)
        customer_service = CustomerService(db_manager, booking_service)
        driver_service = DriverService(db_manager)
        administrator_service = AdministratorService(db_manager)

        # Initialize Tkinter application
        root = Tk()
        app = Application(
            root,
            customer_service=customer_service,
            driver_service=driver_service,
            administrator_service=administrator_service,
        )
        app.run()
        root.mainloop()

    except Exception as e:
        print(f"An error occurred: {e}")


# Call the main function to start the application
if __name__ == "__main__":
    main()