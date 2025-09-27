from datetime import datetime
from tkinter import *
from tkinter import messagebox, ttk, font as tkFont
from tkcalendar import DateEntry


class CustomerFrame(Frame):
    def __init__(self, master, window_width, window_height, show_login_frame, customer_service):
        super().__init__(master, bg="#771F1F", width=window_width, height=window_height)
        self.master = master
        self.customer_service = customer_service
        self.user_data = None
        self.error_label = None
        self.dropoff_entry = None
        self.time_entry = None
        self.pickup_entry = None
        self.cancel_button = None
        self.treeview = None
        self.date_entry = None
        self.customer_data = None
        self.update_entries = None
        self.window_width = window_width
        self.window_height = window_height
        self.show_login_frame = show_login_frame

        # Fonts
        self.custom_font = tkFont.Font(family="Helvetica", size=14)
        self.form_font = tkFont.Font(family="Helvetica", size=12)

        # Initialize Frames
        self.booking_form_frame = Frame(self, bg="#771F1F")
        self.view_bookings_frame = Frame(self, bg="#771F1F")
        self.view_update_frame = Frame(self, bg="#771F1F")
        self.home_frame = Frame(self, bg="#771F1F", bd=2, relief="ridge")

        # Create UI Elements
        self.create_top_buttons()
        self.create_booking_form()
        self.create_view_bookings()
        self.create_update_form()

    def get_customer_data(self):
        """Fetch the latest customer data from the database."""
        # Example data (replace with actual database fetch logic)

        try:
            # Attempt to get the booking history using the customer_id
            return self.customer_service.get_booking_history(self.user_data['customer']['customer_id']) or None
        except Exception:
            return None

    # UI Initialization
    def create_top_buttons(self):
        """Create buttons at the top of the frame."""
        button_frame = Frame(self, bg="#771F1F")
        button_frame.place(relx=0.5, rely=0.1, anchor=CENTER)

        # Buttons
        Button(button_frame, text="Home", bg="#4CAF50", fg="white", font=self.custom_font,
               command=self.go_home).grid(row=0, column=0, padx=10)

        Button(button_frame, text="Book Taxi", bg="#4CAF50", fg="white", font=self.custom_font,
               command=self.show_booking_form).grid(row=0, column=1, padx=10)

        Button(button_frame, text="View Bookings", bg="#4CAF50", fg="white", font=self.custom_font,
               command=self.view_bookings).grid(row=0, column=2, padx=10)

        Button(button_frame, text="Update Details", bg="#4CAF50", fg="white", font=self.custom_font,
               command=self.show_update_form).grid(row=0, column=3, padx=10)

        Button(button_frame, text="Log Out", bg="#4CAF50", fg="white", font=self.custom_font,
               command=self.logout).grid(row=0, column=4, padx=10)

        self.go_home()

    # Booking Form
    def create_booking_form(self):
        # Pickup Location
        Label(self.booking_form_frame, text="Pickup Location:", font=("Helvetica", 14), bg="#771F1F", fg="white").pack(
            pady=(10, 5))
        self.pickup_entry = Entry(self.booking_form_frame, width=40,
                                  font=("Helvetica", 14))  # Increased width and font size
        self.pickup_entry.pack(pady=(10, 10))

        # Drop-off Location
        Label(self.booking_form_frame, text="Drop-off Location:", font=("Helvetica", 14), bg="#771F1F",
              fg="white").pack(pady=(10, 5))
        self.dropoff_entry = Entry(self.booking_form_frame, width=40,
                                   font=("Helvetica", 14))  # Increased width and font size
        self.dropoff_entry.pack(pady=(10, 10))

        # Date Picker
        Label(self.booking_form_frame, text="Date:", font=("Helvetica", 14), bg="#771F1F", fg="white").pack(
            pady=(10, 5))
        self.date_entry = DateEntry(self.booking_form_frame, width=40, font=("Helvetica", 14),
                                    date_pattern='dd-mm-yyyy', background='darkblue',
                                    foreground='white', borderwidth=2)  # Increased width and font size
        self.date_entry.pack(pady=(10, 10))

        # Time Selection
        Label(self.booking_form_frame, text="Time:", font=("Helvetica", 14), bg="#771F1F", fg="white").pack(
            pady=(10, 5))
        self.time_entry = ttk.Combobox(self.booking_form_frame, values=generate_time_slots(), state='readonly',
                                       width=38, font=("Helvetica", 14))  # Increased width and font size
        self.time_entry.pack(pady=(0, 10))
        self.time_entry.current(0)

        # Submit Button
        Button(self.booking_form_frame, text="Submit", bg="#4CAF50", fg="white", command=self.submit_booking, width=20,
               height=2, font=("Helvetica", 14)).pack(pady=(20, 10))  # Larger width, height, and font size

    def show_booking_form(self):
        """Display the booking form and hide other elements."""
        self.clear_frames()
        self.booking_form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def submit_booking(self):
        """Handle booking submission with validation."""
        pickup_location = self.pickup_entry.get()
        dropoff_location = self.dropoff_entry.get()
        selected_date = self.date_entry.get()
        selected_time = self.time_entry.get()
        # Validate that no fields are empty
        if not pickup_location or not dropoff_location or not selected_date or not selected_time:
            messagebox.showerror("Input Error", "All fields must be filled out. Please provide valid input.")
            return
        # If validation passes

        messagebox.showinfo("Booking Confirmation",
                            f"Your booking is pending.\n"
                            f"Pickup: {pickup_location}\n"
                            f"Drop-off: {dropoff_location}\n"
                            f"Date: {selected_date}\n"
                            f"Time: {selected_time}\n"
                            "A driver will be assigned soon.\n"
                            "Thank you for choosing Crown-Cab!",
                            parent=self.master)
        self.customer_service.book_taxi(customer_id=self.user_data['customer']['customer_id'],
                                        pickup_location=pickup_location,
                                        dropoff_location=dropoff_location, date=selected_date, time=selected_time)
        # Clear the booking form
        self.clear_booking_form()
        # Redirect to the home screen
        self.go_home()

    def clear_booking_form(self):
        """Clear the booking form entries and reset defaults."""
        self.pickup_entry.delete(0, END)
        self.dropoff_entry.delete(0, END)
        self.date_entry.set_date(datetime.now())
        self.time_entry.set('')
        self.booking_form_frame.place_forget()

    def show_update_form(self):
        """Display the booking form and hide other elements."""
        self.clear_frames()
        self.view_update_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # View Bookings
    def create_view_bookings(self):
        self.clear_frames()
        # Apply a custom style to the Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#333333",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#333333",
                        bordercolor="#555555",
                        borderwidth=0)

        self.treeview = ttk.Treeview(self.view_bookings_frame, height=10, padding=0)

        # Add 'Booking ID' as a new column
        self.treeview['columns'] = ('Booking ID', 'Pickup', 'Drop-off', 'Date', 'Time', 'Status')

        # Configure headers for each column
        self.treeview.heading('#0', text='', anchor=CENTER)  # Default empty column
        self.treeview.column('#0', width=0, stretch=False)

        # Set up headers and customize the columns
        self.treeview.heading('Booking ID', text='Booking ID', anchor=CENTER)  # Modify header for ID
        self.treeview.column('Booking ID', width=80, anchor=CENTER)  # Adjust width for ID

        self.treeview.heading('Pickup', text='Pickup Location', anchor=CENTER)  # Modify header for Pickup
        self.treeview.column('Pickup', width=160, anchor=CENTER)  # Adjust width for Pickup

        self.treeview.heading('Drop-off', text='Drop-off Location', anchor=CENTER)  # Modify header for Drop-off
        self.treeview.column('Drop-off', width=160, anchor=CENTER)  # Adjust width for Drop-off

        self.treeview.heading('Date', text='Date', anchor=CENTER)  # Modify header for Date
        self.treeview.column('Date', width=80, anchor=CENTER)  # Adjust width for Date

        self.treeview.heading('Time', text='Time', anchor=CENTER)  # Modify header for Time
        self.treeview.column('Time', width=50, anchor=CENTER)  # Adjust width for Time

        self.treeview.heading('Status', text='Status', anchor=CENTER)  # Modify header for Status
        self.treeview.column('Status', width=80, anchor=CENTER)  # Adjust width for Status

        self.treeview.pack(expand=True, fill=BOTH)

        # Bind the selection event
        self.treeview.bind("<<TreeviewSelect>>", self.handle_selection)

        # Create the "CANCEL" button (hidden by default)
        self.cancel_button = Button(self.view_bookings_frame, text="CANCEL", bg="red", fg="white",
                                    command=self.cancel_booking)
        self.cancel_button.place(relx=0.5, rely=0.9, anchor=CENTER)  # Adjust placement
        self.cancel_button.place_forget()  # Initially hidden

    def handle_selection(self, event):
        """Handle item selection in the Treeview and show the CANCEL button if applicable."""
        selected_item = self.treeview.focus()  # Get the selected item's ID
        if not selected_item:
            self.cancel_button.place_forget()
            return
        # Retrieve the values of the selected item
        item_values = self.treeview.item(selected_item, 'values')

        # Check the status column (last column in the Treeview)
        status = item_values[-1]  # Assuming 'Status' is the last column
        if status in ('pending', 'confirmed'):
            self.cancel_button.place(relx=0.5, rely=0.95, anchor=CENTER)  # Show the button
        else:
            self.cancel_button.place_forget()  # Hide the button

    def cancel_booking(self):
        """Handle the cancellation of a booking."""
        selected_item = self.treeview.focus()  # Get the selected item's ID
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a booking to cancel.",
                                   parent=self.view_bookings_frame)
            return

        # Retrieve the values of the selected item
        item_values = self.treeview.item(selected_item, 'values')

        # Confirm cancellation
        confirm = messagebox.askyesno("Cancel Booking", f"Are you sure you want to cancel this booking?\n\n"
                                                        f"Booking ID: {item_values[0]}\n"
                                                        f"Pickup: {item_values[1]}\n"
                                                        f"Drop-off: {item_values[2]}\n"
                                                        f"Date: {item_values[3]}\n"
                                                        f"Time: {item_values[4]}",
                                      parent=self.view_bookings_frame)
        if confirm:
            # Update the status (you can also send this change to your backend/database)
            self.treeview.item(selected_item, values=(
                item_values[0],  # Booking ID
                item_values[1],  # Pickup
                item_values[2],  # Drop-off
                item_values[3],  # Date
                item_values[4],  # Time
                "cancelled"  # Update Status
            ))
            self.customer_service.cancel_booking(item_values[0])
            self.cancel_button.place_forget()  # Hide the button
            messagebox.showinfo("Booking Cancelled", "The booking has been successfully cancelled.",
                                parent=self.view_bookings_frame)

    def view_bookings(self):
        """Display the customer's current bookings from a list of dictionaries."""

        if self.customer_data is None:
            self.customer_data = self.get_customer_data()

        # Clear existing data in the treeview (booking table)
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Sort bookings by 'booking_id' in descending order
        try:
            sorted_bookings = sorted(self.customer_data, key=lambda x: x['booking_id'], reverse=True)

            # Loop through the list of bookings and insert each one into the treeview
            for booking in sorted_bookings:
                self.treeview.insert('', 'end', values=(
                    booking['booking_id'],
                    booking['pickup_location'],
                    booking['dropoff_location'],
                    booking['date'],
                    booking['time'],
                    booking['status']
                ))
        except TypeError:
            print(f"No bookings found")


        # Clear frames and show the booking view
        self.clear_frames()
        self.view_bookings_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Utility Methods
    def clear_frames(self):
        """Hide all dynamic content frames."""
        self.booking_form_frame.place_forget()
        self.view_bookings_frame.place_forget()
        self.view_update_frame.place_forget()
        self.home_frame.place_forget()

    def logout(self):
        """Handle logout functionality."""
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?", parent=self.master):
            self.user_data = None
            self.clear_frames()
            self.place_forget()
            self.show_login_frame()

    # Home page
    def go_home(self):
        """Navigate back to the home (welcome screen) and display customer data."""
        self.clear_frames()

        # Fetch latest customer data from the database
        self.customer_data = self.get_customer_data()

        # Check if customer_data is empty or None
        if not self.customer_data:
            # Handle the case when there is no data available yet
            no_data_label = Label(self.home_frame, text="No bookings available.", font=("Helvetica", 12), fg="white", bg="#333333")
            no_data_label.pack(fill=X, padx=10, pady=(10, 10))
            return

        # Filter bookings with 'Pending' or 'Confirmed' status
        filtered_bookings = [booking for booking in self.customer_data if booking['status'] in ['pending', 'confirmed']]

        # If no bookings with 'Pending' or 'Confirmed' status, show a message
        if not filtered_bookings:
            print("No bookings with 'Pending' or 'Confirmed' status.")
            return

        # Update the home frame with a scrollable treeview of bookings
        self.home_frame = Frame(self, bg="#222222", bd=2, relief="ridge")
        self.home_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=800, height=400)

        # Create a Treeview widget
        columns = ('pickup', 'dropoff', 'date', 'time', 'status', 'driver_info')
        tree = ttk.Treeview(self.home_frame, columns=columns, show='headings', height=15)

        # Define column headings
        tree.heading('pickup', text='Pickup')
        tree.heading('dropoff', text='Drop-off')
        tree.heading('date', text='Date')
        tree.heading('time', text='Time')
        tree.heading('status', text='Status')
        tree.heading('driver_info', text='Driver Information')

        # Define column widths
        tree.column('pickup', width=200, anchor=CENTER)
        tree.column('dropoff', width=200, anchor=CENTER)
        tree.column('date', width=80, anchor=CENTER)
        tree.column('time', width=50, anchor=CENTER)
        tree.column('status', width=80, anchor=CENTER)
        tree.column('driver_info', width=200, anchor=W)  # Increased width for driver info

        # Add a vertical scrollbar
        vsb = ttk.Scrollbar(self.home_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        # Grid layout
        tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        # Sort the bookings by booking_id in descending order
        sorted_bookings = sorted(filtered_bookings, key=lambda x: x['booking_id'], reverse=True)

        # Populate the treeview with booking details
        for idx, booking in enumerate(sorted_bookings):
            driver_info = ""
            if booking["driver_id"]:
                driver_info = (
                    f"Driver: {booking['driver_name']}\n"
                    f"Vehicle: {booking['driver_vehicle']}\n"
                    f"Reg. Plate: {booking['driver_registration']}"
                )
            else:
                driver_info = "Driver: No driver assigned yet"

            # Insert booking details along with driver information in one row
            tree.insert('', 'end', values=(
                booking['pickup_location'],
                booking['dropoff_location'],
                booking['date'],
                booking['time'],
                booking['status'].capitalize(),
                driver_info  # Driver information in its own column
            ))

        # Apply a custom style to the Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#333333",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#333333",
                        bordercolor="#555555",
                        borderwidth=0)
        style.configure("Treeview", font=('Helvetica', 8))  # Adjust the font and size as needed
        style.configure("Treeview.Heading", font=('Helvetica', 9))  # For column headings


    def create_update_form(self):
        """Create the update form with simple validation."""
        # Dictionary to store Entry widgets for each field
        self.update_entries = {}

        # Define form fields
        fields = ['First Name', 'Last Name', 'Address', 'Postcode', 'Phone Number']

        # Font size for labels and input fields
        label_font = ("Helvetica", 14)  # Increase font size for labels
        entry_font = ("Helvetica", 12)  # Increase font size for entry fields
        button_font = ("Helvetica", 14)  # Font size for button

        # Create input fields
        for i, field in enumerate(fields):
            # Create label with increased font size
            label = Label(self.view_update_frame, text=f"{field}:", bg="#771F1F", fg="white", font=label_font)
            label.grid(row=i, column=0, pady=(10, 5), sticky="w", padx=(10, 5))

            # Create entry with increased font size
            entry = Entry(self.view_update_frame, width=30, font=entry_font)
            entry.grid(row=i, column=1, pady=(10, 5), padx=(5, 10))

            # Store the Entry widget in the dictionary using the field name as the key
            self.update_entries[field] = entry

        # Error label for showing validation messages
        self.error_label = Label(self.view_update_frame, text="", fg="red", bg="#771F1F", font=("Helvetica", 12))
        self.error_label.grid(row=len(fields), column=0, columnspan=2)

        # Submit button with increased font size
        submit_button = Button(self.view_update_frame, text="Submit", bg="#4CAF50", fg="white", font=button_font,
                               command=self.submit_update_details)
        submit_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(20, 10))

    def submit_update_details(self):
        """Submit the form after simple validation."""
        # Dictionary to store the updated values
        updated_data = {}

        # Validate and collect data
        for field, entry in self.update_entries.items():
            value = entry.get().strip()  # Get the value and remove extra whitespace
            if value == "":  # Check if the field is empty
                self.error_label.config(text=f"Error: {field} cannot be empty!")
                return  # Stop the function if any field is empty
            updated_data[field] = value  # Add the value to the updated_data dictionary

        # At this point, updated_data contains all the validated fields
        print("Updated data:", updated_data)  # Debugging: Print updated data

        # Example: Perform database update using updated_data
        try:
            # Assuming you have a method to update customer data in your database
            self.customer_service.update_details(
                customer_id=self.user_data['customer']['customer_id'],
                first_name=updated_data['First Name'],
                last_name=updated_data['Last Name'],
                address=updated_data['Address'],
                postcode=updated_data['Postcode'],
                phone_number=updated_data['Phone Number']
            )
            self.error_label.config(text="Update successful!", fg="green")
        except Exception as e:
            # Handle update errors
            self.error_label.config(text=f"Error: {str(e)}", fg="red")

        print("Form submitted successfully!")  # Replace with actual form submission logic
        self.clear_update_form()
        self.clear_frames()
        self.view_update_frame.place_forget()
        self.go_home()

    def clear_update_form(self):
        """Clear all fields in the update form."""
        for entry in self.update_entries.values():
            entry.delete(0, END)

    def configure_user(self, user_data):
        self.user_data = user_data


def generate_time_slots():
    """Generate a list of time slots in HH:MM format."""
    return [f"{hour:02}:{minute:02}" for hour in range(24) for minute in [0, 15, 30, 45]]
