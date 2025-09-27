import tkinter.font as tkFont
from tkinter import *
from tkinter import messagebox


class LoginFrame(Frame):
    def __init__(self, master, window_width, window_height, handle_login_callback, show_register_callback,
                 customer_service, driver_service, administrator_service):
        super().__init__(master, bg="#771F1F", width=window_width, height=window_height)
        self.customer_service = customer_service
        self.driver_service = driver_service
        self.administrator_service = administrator_service
        self.password_entry = None
        self.email_entry = None
        self.master = master
        self.window_width = window_width
        self.window_height = window_height
        self.show_register_callback = show_register_callback
        self.handle_login_callback = handle_login_callback
        self.create_widgets()

    def create_widgets(self):
        custom_font = tkFont.Font(family="Helvetica", size=14)
        input_font = tkFont.Font(family="Helvetica", size=14)
        link_font = tkFont.Font(family="Helvetica", size=12, underline=True)

        email_label = Label(self, text="Email:", bg="#771F1F", fg="white", font=custom_font)
        email_label.grid(row=0, column=0, pady=(0, 5), sticky="w")
        self.email_entry = Entry(self, font=input_font, width=20)
        self.email_entry.grid(row=1, column=0, columnspan=2, pady=(0, 15), padx=(0, 0))

        password_label = Label(self, text="Password:", bg="#771F1F", fg="white", font=custom_font)
        password_label.grid(row=2, column=0, pady=(0, 5), sticky="w")
        self.password_entry = Entry(self, show="*", font=input_font, width=20)
        self.password_entry.grid(row=3, column=0, columnspan=2, pady=(0, 15), padx=(0, 0))

        signin_button = Button(self, text="Sign In", bg="#4CAF50", fg="white", font=custom_font, width=20, height=1,
                               command=self.login)
        signin_button.grid(row=4, column=0, columnspan=2, pady=(20, 10))

        # Register Link
        register_link = Label(self, text="Don't have an account? Register", bg="#771F1F", fg="white",
                              font=link_font, cursor="hand2")
        register_link.grid(row=5, column=0, pady=(10, 5))
        register_link.bind("<Button-1>", lambda e: self.show_register_callback())

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Login Error", "Email and password cannot be empty.", parent=self.master)
            return

        # Attempt to log in the user in the following order: admin, driver, customer
        # Attempt to log in the user in the following order: admin, driver, customer
        user_data = None
        user_type = None

        # Try logging in as an administrator
        user_data = self.administrator_service.login(email, password)
        if user_data:
            user_type = "admin"
        else:
            # Try logging in as a driver
            user_data = self.driver_service.login(email, password)
            if user_data:
                user_type = "driver"
            else:
                # Try logging in as a customer
                user_data = self.customer_service.login(email, password)
                if user_data:
                    user_type = "customer"

        # Handle successful or failed login
        if user_data:
            # Successful login
            self.handle_login_callback(user_type, user_data)
            self.clear_inputs()
            self.place_forget()
        else:
            # All login attempts failed
            messagebox.showerror("Login", "Invalid email or password. Please try again.")

    def clear_inputs(self):
        """Clear the login input fields."""
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)
