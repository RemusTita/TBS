from tkinter import *
from tkinter import messagebox, ttk
from enums.driver_availability_status import DriverAvailabilityStatus


class DriverFrame(Frame):
    def __init__(self, master, width, height, show_login_frame, driver_service):
        super().__init__(master, bg="#771F1F", width=width, height=height)
        self.driver_service = driver_service
        self.user_data = None
        self.treeview = None
        self.refresh_button = None
        self.on_break_button = None
        self.complete_button = None
        self.navigate_button = None
        self.master = master
        self.width = width
        self.height = height
        self.show_login_frame = show_login_frame

        # Create buttons for Home, On Break, and Log Out
        self.create_buttons()
        self.create_booking_list()
        self.create_refresh_button()

    def create_buttons(self):
        """Create the Home, On Break, and Log Out buttons."""
        button_style = {
            "width": 20,
            "height": 2,
            "font": ("Helvetica", 12),
        }

        # On Break Button
        self.on_break_button = Button(self, text="On Break", bg="red", command=self.toggle_break, **button_style)
        self.on_break_button.place(relx=0.1, rely=0.05, anchor=W)

        # Log Out Button
        logout_button = Button(self, text="Log Out", bg="#4CAF50", command=self.logout, **button_style)
        logout_button.place(relx=0.9, rely=0.05, anchor=E)

        # Buttons to Navigate and Complete Job (Initially hidden)
        self.navigate_button = Button(self, text="Navigate", bg="#4CAF50", command=self.navigate, width=20, height=2,
                                      font=("Helvetica", 12))
        self.complete_button = Button(self, text="Complete Job", bg="#4CAF50", command=self.complete_job, width=20,
                                      height=2, font=("Helvetica", 12))
        self.navigate_button.place_forget()
        self.complete_button.place_forget()

    def toggle_break(self):
        """Toggle the On Break status and update the button text."""
        current_text = self.on_break_button.cget("text")
        if current_text == "On Break":
            self.on_break_button.config(text="Active", bg="#4CAF50")
            print("Driver is now available")
            self.driver_service.update_availability_status(driver_id=self.user_data["driver"]["driver_id"],
                                                           availability_status=DriverAvailabilityStatus.AVAILABLE)
            self.refresh_list()
        else:
            self.on_break_button.config(text="On Break", bg="red")
            print("Driver is now on break")
            # Clear the Treeview data when the driver is on break
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            self.driver_service.update_availability_status(driver_id=self.user_data["driver"]["driver_id"],
                                                           availability_status=DriverAvailabilityStatus.ON_BREAK)

    def get_bookings_from_db(self):
        data = self.driver_service.get_assigned_trips(self.user_data["driver"]["driver_id"])
        return data

    def create_booking_list(self):
        """Create the customer booking list using mock data."""
        # Create the Treeview widget
        self.treeview = ttk.Treeview(self, columns=("B-ID", "Customer Name", "Pickup", "Dropoff", "Date", "Time"),
                                     show="headings")

        # Define column headers
        self.treeview.heading("B-ID", text="Booking ID")
        self.treeview.heading("Customer Name", text="Customer Name")
        self.treeview.heading("Pickup", text="Pickup Address")
        self.treeview.heading("Dropoff", text="Dropoff Address")
        self.treeview.heading("Date", text="Date")
        self.treeview.heading("Time", text="Time")

        # Define column widths
        self.treeview.column("B-ID", width=80, anchor=CENTER)
        self.treeview.column("Customer Name", width=130, anchor=CENTER)
        self.treeview.column("Pickup", width=200, anchor=CENTER)
        self.treeview.column("Dropoff", width=200, anchor=CENTER)
        self.treeview.column("Date", width=80, anchor=CENTER)
        self.treeview.column("Time", width=80, anchor=CENTER)

        # Populate the Treeview initially
        self.populate_treeview()

        # Place the Treeview in the center of the frame
        self.treeview.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Bind selection event to show buttons when a row is selected
        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)

    def populate_treeview(self):
        """Populate the Treeview with bookings."""
        # Clear the existing data in the Treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Fetch and insert bookings if the driver is active
        if self.on_break_button.cget("text") == "Active":
            bookings = self.get_bookings_from_db()
            for booking in bookings:
                self.treeview.insert("", "end", values=(
                    booking["booking_id"], booking["customer_name"], booking["pickup_location"],
                    booking["dropoff_location"], booking["date"], booking["time"]))

    def refresh_list(self):
        """Refresh the list of bookings."""
        self.populate_treeview()

    def create_refresh_button(self):
        """Create a Refresh button to reload the booking list."""
        self.refresh_button = Button(self, text="Refresh", command=self.refresh_list, width=10, height=1, bg="green",
                                     fg="white")
        self.refresh_button.place(relx=0.5, rely=0.75, anchor=CENTER)

    def on_row_select(self, event):
        """Handle the row selection event and show the action buttons."""
        selected_item = self.treeview.selection()
        if selected_item:
            self.navigate_button.place(relx=0.5, rely=0.85, anchor=CENTER)
            self.complete_button.place(relx=0.5, rely=0.95, anchor=CENTER)
        else:
            self.navigate_button.place_forget()
            self.complete_button.place_forget()

    def navigate(self):
        """Handle the Navigate button click."""
        selected_item = self.treeview.selection()
        if selected_item:
            booking_details = self.treeview.item(selected_item, "values")
            pickup_address = booking_details[2]
            dropoff_address = booking_details[3]
            messagebox.showinfo("Navigate", f"Pickup Address: {pickup_address}\nDrop-off Address: {dropoff_address}")

    def complete_job(self):
        """Handle the Complete Job button click."""
        selected_item = self.treeview.selection()
        if selected_item:
            booking_id = self.treeview.item(selected_item, "values")[0]
            customer_name = self.treeview.item(selected_item, "values")[1]
            dropoff_address = self.treeview.item(selected_item, "values")[3]
            messagebox.showinfo("Job Completed",
                                f"Job for {customer_name}, dropoff address {dropoff_address} has been completed.")
            self.treeview.delete(selected_item)
            self.driver_service.complete_trip(booking_id=booking_id, driver_id=self.user_data["driver"]["driver_id"])

    def logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.user_data = None
            self.place_forget()
            self.show_login_frame()

    def configure_user(self, user_data):
        self.user_data = user_data
