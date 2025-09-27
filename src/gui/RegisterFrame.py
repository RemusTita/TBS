import tkinter.font as tkFont
from tkinter import *
from tkinter import messagebox
from database.db_manager import DatabaseManager
from services.booking_service import BookingService
from services.customer_service import CustomerService


class RegisterFrame(Frame):
    def __init__(self, master, show_login_callback):
        super().__init__(master, bg="#771F1F")
        self.master = master
        self.show_login_callback = show_login_callback
        self.input_fields = {}
        self.create_widgets()

    def create_widgets(self):
        custom_font = tkFont.Font(family="Helvetica", size=14)
        input_font = tkFont.Font(family="Helvetica", size=14)
        link_font = tkFont.Font(family="Helvetica", size=12, underline=True)
        register_font = tkFont.Font(family="Helvetica", size=10)

        fields = ['First Name', 'Last Name', 'Address', 'Postcode', 'Phone Number', 'Email', 'Password']
        for i, field in enumerate(fields):
            label = Label(self, text=f"{field}:", bg="#771F1F", fg="white", font=register_font)
            label.grid(row=i * 2, column=0, pady=(0, 5), sticky="w")

            entry = Entry(self, font=input_font, width=20, show="*" if field == 'Password' else '')
            entry.grid(row=i * 2 + 1, column=0, columnspan=2, pady=(0, 15), padx=(0, 0))

            # Store entry in dictionary
            self.input_fields[field] = entry

        register_button = Button(self, text="Register", bg="#4CAF50", fg="white", font=custom_font,
                                 width=20, height=1, command=self.register_action)
        register_button.grid(row=len(fields) * 2 + 1, column=0, columnspan=2, pady=(20, 10))

        back_to_login = Label(self, text="Already have an account? Login", bg="#771F1F", fg="white",
                              font=link_font, cursor="hand2")
        back_to_login.grid(row=len(fields) * 2 + 2, column=0, columnspan=2)
        back_to_login.bind("<Button-1>", lambda e: self.show_login_callback())
        back_to_login.bind("<ButtonRelease-1>", lambda e: self.clear_fields())

    def register_action(self):
        db_manager = DatabaseManager("taxi_booking_system.db")
        booking_service = BookingService(db_manager)
        # Retrieve field values
        user_data = {field: entry.get().strip() for field, entry in self.input_fields.items()}

        # Perform validation
        errors = self.validate_fields(user_data)

        if errors:
            messagebox.showerror("Invalid Input", "\n".join(errors), parent=self.master)
        else:
            messagebox.showinfo("Success", "Registration successful!", parent=self.master)
            customers_service = CustomerService(db_manager, booking_service)
            customers_service.register(
                first_name=user_data['First Name'],
                last_name=user_data['Last Name'],
                address=user_data['Address'],
                postcode=user_data['Postcode'],
                email=user_data['Email'],
                phone_number=user_data['Phone Number'],
                password=user_data['Password']
            )
            self.clear_fields()
            self.show_login_callback()

    def validate_fields(self, user_data):
        """Validate input fields and return a list of error messages if invalid."""
        errors = []

        # Check if all fields are filled
        for field, value in user_data.items():
            if not value:
                errors.append(f"{field} is required.")

        # Validate specific fields
        if 'Email' in user_data:
            if '@' not in user_data['Email'] or '.' not in user_data['Email']:
                errors.append("Invalid email format.")

        if 'Password' in user_data:
            if len(user_data['Password']) < 8:
                errors.append("Password must be at least 8 characters long.")

        return errors

    def clear_fields(self):
        """Clear all input fields in the form."""
        for entry in self.input_fields.values():
            entry.delete(0, END)
