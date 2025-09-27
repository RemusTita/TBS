from tkinter import *
from tkinter import ttk, messagebox


class AssignDriverFrame(Toplevel):
    """A separate frame to assign a driver to a booking."""

    def __init__(self, master, booking_details, treeview, selected_item, admin_service):
        super().__init__(master)
        self.title("Assign Driver")
        self.geometry("600x400")  # Default size of the popup window
        self.booking_details = booking_details
        self.treeview = treeview
        self.selected_item = selected_item
        self.admin_service = admin_service

        # Center the window relative to the parent
        self.center_window(master)

        # Display Booking Details
        Label(self, text=f"Assign Driver to Booking ID: {booking_details['booking_id']}", font=("Helvetica", 14)).pack(
            pady=10)
        Label(self, text=f"Customer Name: {booking_details['customer_first_name']}", font=("Helvetica", 12)).pack(
            pady=5)
        Label(self, text=f"Pickup: {booking_details['pickup_location']}", font=("Helvetica", 12)).pack(pady=5)
        Label(self, text=f"Date & Time: {booking_details['date']} at {booking_details['time']}",
              font=("Helvetica", 12)).pack(pady=5)

        get_drivers = self.admin_service.get_all_drivers()

        available_drivers = [
            f"{driver['driver_id']}: {driver['full_name']} - {driver['vehicle']} ({driver['registration_number']})"
            for driver in get_drivers if driver['availability_status'] in ['available', 'on_trip']
        ]

        # Driver Selection
        Label(self, text="Select Driver:", font=("Helvetica", 12)).pack(pady=10)
        self.driver_combobox = ttk.Combobox(self, values=available_drivers, state="readonly", width=35)
        self.driver_combobox.pack(pady=10)

        # Confirm Button
        Button(self, text="Assign Driver", command=self.select_driver, bg="#4CAF50", fg="white",
               font=("Helvetica", 12)).pack(pady=20)

    def center_window(self, master):
        """Center the Toplevel window relative to the parent window."""
        window_width = 400
        window_height = 300

        # Get the dimensions of the parent (root or AdminFrame)
        parent_x = master.winfo_rootx()
        parent_y = master.winfo_rooty()
        parent_width = master.winfo_width()
        parent_height = master.winfo_height()

        # Calculate the center position
        center_x = parent_x + (parent_width // 2) - (window_width // 2)
        center_y = parent_y + (parent_height // 2) - (window_height // 2)

        # Set the geometry of the popup
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    def select_driver(self):
        """Handle driver assignment."""
        selected_driver = self.driver_combobox.get()
        driver_id = selected_driver.split(':')[0]

        if not selected_driver:
            messagebox.showwarning("No Driver Selected", "Please select a driver to assign.")

        success = self.admin_service.assign_driver(self.booking_details["booking_id"], driver_id)

        if success:
            messagebox.showinfo("Success",
                                f"{selected_driver} assigned to Booking ID {self.booking_details['booking_id']}")
            self.treeview.delete(self.selected_item)
        else:
            messagebox.showerror("Error",
                                 f"Failed to assign Driver {selected_driver}). Conflict: Driver has overlapping bookings around this time.")
        self.destroy()
