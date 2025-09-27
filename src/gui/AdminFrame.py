from tkinter import *
from tkinter import messagebox, ttk
from gui.AssignDriverFrame import AssignDriverFrame


class AdminFrame(Frame):
    def __init__(self, master, window_width, window_height, show_login_frame, admin_service):
        super().__init__(master, bg="#771F1F", width=window_width, height=window_height)
        self.admin_service = admin_service
        self.user_data = None
        self.treeview_all_bookings = None
        self.all_bookings_frame = None
        self.title_label = None
        self.refresh_button = None
        self.treeview_admin = None
        self.assign_job_button = None
        self.logout_button = None
        self.view_all_bookings = None
        self.master = master
        self.width = window_width
        self.height = window_height
        self.show_login_frame = show_login_frame

        self.create_buttons()
        self.create_booking_list()
        self.create_refresh_button()

    def create_buttons(self):
        button_style = {
            "width": 20,  # Increase width
            "height": 2,  # Increase height
            "font": ("Helvetica", 12),  # Adjust font size
        }

        # View all bookings
        self.view_all_bookings = Button(self, text="View All Bookings", bg="#4CAF50", command=self.show_all_bookings,
                                        **button_style)
        self.view_all_bookings.place(relx=0.1, rely=0.05, anchor=W)

        # Log Out Button
        self.logout_button = Button(self, text="Log Out", bg="#4CAF50", command=self.logout, **button_style)
        self.logout_button.place(relx=0.9, rely=0.05, anchor=E)

        # Assign Button
        self.assign_job_button = Button(self, text="Complete Job", bg="#4CAF50", command=self.assign_driver_booking,
                                        **button_style)
        self.assign_job_button.place_forget()

    def show_all_bookings(self):
        """Show all bookings in a separate frame."""
        # Create the "All Bookings" frame if it doesn't exist
        if self.all_bookings_frame is None:
            self.create_all_bookings_frame()

        # Clear and populate the Treeview
        self.populate_all_bookings_treeview()

        # Hide current frame and show "All Bookings" frame
        self.place_forget()
        self.all_bookings_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def create_all_bookings_frame(self):
        """Create the frame to display all bookings."""
        self.all_bookings_frame = Frame(self.master, bg="#771F1F", width=self.width, height=self.height)

        # Title Label
        title_label = Label(self.all_bookings_frame, text="All Bookings", font=("Helvetica", 16, "bold"), bg="#4CAF50",
                            fg="white")
        title_label.pack(fill=X, pady=10)

        # Treeview for displaying all bookings
        self.treeview_all_bookings = ttk.Treeview(self.all_bookings_frame, columns=(
            "Booking ID", "Customer ID", "Customer Name", "Pickup Address", "Dropoff Address", "Date", "Time",
            "Status"), show="headings")

        # Define column headers
        self.treeview_all_bookings.heading("Booking ID", text="Booking ID")
        self.treeview_all_bookings.heading("Customer ID", text="Customer ID")
        self.treeview_all_bookings.heading("Customer Name", text="Customer Name")
        self.treeview_all_bookings.heading("Pickup Address", text="Pickup Address")
        self.treeview_all_bookings.heading("Dropoff Address", text="Dropoff Address")
        self.treeview_all_bookings.heading("Date", text="Date")
        self.treeview_all_bookings.heading("Time", text="Time")
        self.treeview_all_bookings.heading("Status", text="Status")

        # Define column widths
        self.treeview_all_bookings.column("Booking ID", width=80, anchor=CENTER)
        self.treeview_all_bookings.column("Customer ID", width=80, anchor=CENTER)
        self.treeview_all_bookings.column("Customer Name", width=120, anchor=CENTER)
        self.treeview_all_bookings.column("Pickup Address", width=150, anchor=CENTER)
        self.treeview_all_bookings.column("Dropoff Address", width=150, anchor=CENTER)
        self.treeview_all_bookings.column("Date", width=80, anchor=CENTER)
        self.treeview_all_bookings.column("Time", width=50, anchor=CENTER)
        self.treeview_all_bookings.column("Status", width=80, anchor=CENTER)

        # Add Treeview to the frame
        self.treeview_all_bookings.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Add a back button
        back_button = Button(self.all_bookings_frame, text="Back", bg="#4CAF50", fg="white", font=("Helvetica", 14),
                             command=self.go_back_to_admin_frame)
        back_button.pack(pady=10)

    def get_bookings_from_db(self):
        try:
            # Attempt to get the booking history using the customer_id
            data = self.admin_service.get_all_bookings()

            # If data is returned, print it
            if data:
                return data
            else:
                print("No booking history found.")
                return None

        except Exception as e:
            # If an error occurs, print the error message
            print(f"An error occurred while fetching booking history: {e}")

    def populate_all_bookings_treeview(self):
        """Populate the Treeview with all bookings."""
        # Clear existing items in the Treeview
        for item in self.treeview_all_bookings.get_children():
            self.treeview_all_bookings.delete(item)

        # Fetch all bookings
        bookings = self.get_bookings_from_db()

        if bookings:
            filtered_bookings = [
                booking for booking in bookings
                if booking['status'] in ['confirmed', 'cancelled', 'completed']
            ]
        else:
            filtered_bookings = []

        sorted_bookings = sorted(filtered_bookings, key=lambda x: x['date'], reverse=True)

        if sorted_bookings is not None:
            # Insert fetched data into the Treeview
            for booking in sorted_bookings:
                self.treeview_all_bookings.insert("", "end", values=(
                    booking["customer_id"], booking["booking_id"], booking["customer_first_name"],
                    booking["pickup_location"], booking["dropoff_location"],
                    booking["date"], booking["time"], booking["status"]
                ))

    def go_back_to_admin_frame(self):
        """Go back to the main admin frame."""
        self.all_bookings_frame.place_forget()
        self.place(relx=0.5, rely=0.5, anchor=CENTER)

    def logout(self):
        """Handle the action when the LogOut button is clicked."""
        # Confirm logout
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.user_data = None
            self.place_forget()
            self.show_login_frame()
            print("Logged out successfully")

    def create_booking_list(self):
        """Create the customer booking list using mock data."""
        # Get the mock bookings data

        bookings = self.get_bookings_from_db()

        # Create the Treeview widget
        self.treeview_admin = ttk.Treeview(self, columns=(
            "Booking ID", "Customer ID", "Customer Name", "Pickup Address", "Dropoff Address", "Date", "Time",
            "Status"), show="headings")

        # Define columns headers
        # self.treeview.heading("ID", text="ID")
        self.treeview_admin.heading("Booking ID", text="Booking ID")
        self.treeview_admin.heading("Customer ID", text="Customer ID")
        self.treeview_admin.heading("Customer Name", text="Customer Name")
        self.treeview_admin.heading("Pickup Address", text="Dropoff Address")
        self.treeview_admin.heading("Dropoff Address", text="Dropoff Address")
        self.treeview_admin.heading("Date", text="Date")
        self.treeview_admin.heading("Time", text="Time")
        self.treeview_admin.heading("Status", text="Status")

        # Define column widths
        # self.treeview.column("ID", width=0, anchor=CENTER)
        self.treeview_admin.column("Booking ID", width=80, anchor=CENTER)
        self.treeview_admin.column("Customer ID", width=80, anchor=CENTER)
        self.treeview_admin.column("Customer Name", width=120, anchor=CENTER)
        self.treeview_admin.column("Pickup Address", width=150, anchor=CENTER)
        self.treeview_admin.column("Dropoff Address", width=150, anchor=CENTER)
        self.treeview_admin.column("Date", width=80, anchor=CENTER)
        self.treeview_admin.column("Time", width=50, anchor=CENTER)
        self.treeview_admin.column("Status", width=80, anchor=CENTER)

        self.populate_treeview()

        # Place the Treeview in the center of the frame
        self.treeview_admin.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Bind selection event to show buttons when a row is selected
        self.treeview_admin.bind("<<TreeviewSelect>>", self.on_row_select)

        # Create buttons (Assign driver)
        self.create_action_buttons()

    def create_refresh_button(self):
        """Create a Refresh button to reload the booking list."""
        self.refresh_button = Button(self, text="Refresh", command=self.refresh_list, width=10, height=1, bg="green",
                                     fg="white")
        self.refresh_button.place(relx=0.5, rely=0.8, anchor=CENTER)

    def refresh_list(self):
        """Refresh the list of bookings."""
        self.populate_treeview()
        print("Refresh list")

    def populate_treeview(self):
        """Populate the Treeview with bookings."""
        # Clear the existing data in the Treeview
        for item in self.treeview_admin.get_children():
            self.treeview_admin.delete(item)

        # Fetch new bookings
        bookings = self.get_bookings_from_db()

        if bookings:
            filtered_bookings = [
                booking for booking in bookings
                if booking['status'] in ['pending']
            ]
        else:
            filtered_bookings = []

        sorted_bookings = sorted(filtered_bookings, key=lambda x: x['booking_id'], reverse=True)

        # Insert the fetched data into the Treeview
        if sorted_bookings is not None:
            for booking in sorted_bookings:
                self.treeview_admin.insert("", "end", values=(

                    booking["booking_id"], booking["customer_id"], booking["customer_first_name"],
                    booking["pickup_location"], booking["dropoff_location"],
                    booking["date"], booking["time"], booking["status"]
                ))

    def create_action_buttons(self):

        # Assign Driver button
        self.assign_job_button = Button(self, text="Assign Driver", bg="#4CAF50", command=self.assign_driver_booking,
                                        width=15,
                                        height=2)
        self.assign_job_button.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.assign_job_button.place_forget()

    def on_row_select(self, event):
        selected_item = self.treeview_admin.selection()
        if selected_item:
            # Show the buttons with more space between them
            self.assign_job_button.place(relx=0.5, rely=0.9, anchor=CENTER)  # Increase rely for more space
        else:
            # Hide buttons if no row is selected
            self.assign_job_button.place_forget()

    def configure_user(self, user_data):
        self.user_data = user_data

    def assign_driver_booking(self):
        """Handle the Assign Driver action."""
        selected_item = self.treeview_admin.selection()
        if selected_item:
            # Retrieve booking details
            booking_details = self.treeview_admin.item(selected_item, "values")
            details = {
                "booking_id": booking_details[0],
                "customer_id": booking_details[1],
                "customer_first_name": booking_details[2],
                "pickup_location": booking_details[3],
                "dropoff_location": booking_details[4],
                "date": booking_details[5],
                "time": booking_details[6],
                "status": booking_details[7]
            }

            # Open the Assign Driver Frame and pass Treeview and selected item
            AssignDriverFrame(self.master, details, self.treeview_admin, selected_item[0], self.admin_service)
