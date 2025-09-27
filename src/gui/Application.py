from tkinter import *
from tkinter import messagebox
from gui.AdminFrame import AdminFrame
from gui.CustomerFrame import CustomerFrame
from gui.DriverFrame import DriverFrame
from gui.LoginFrame import LoginFrame
from gui.RegisterFrame import RegisterFrame


class Application:
    def __init__(self, master, customer_service, driver_service, administrator_service):
        self.master = master
        self.customer_service = customer_service
        self.driver_service = driver_service
        self.administrator_service = administrator_service

        # Initialize frames
        self.customer_frame = None
        self.register_frame = None
        self.login_frame = None
        self.admin_frame = None
        self.driver_frame = None

        # Perform setup after services are initialized
        self.setup_window()
        self.create_frames()

    def setup_window(self):
        window_width = 1000
        window_height = 800
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.master.configure(bg="#771F1F")
        self.master.title("Crown-Cab")

        icon = PhotoImage(file="src/gui/assets/taxi.png")
        self.master.iconphoto(True, icon)
        self.master.resizable(False, False)

    def create_frames(self):
        self.login_frame = LoginFrame(self.master, 800, 600, self.handle_login, self.show_register_frame,
                                      self.customer_service, self.driver_service, self.administrator_service)
        self.register_frame = RegisterFrame(self.master, self.show_login_frame)
        self.customer_frame = CustomerFrame(self.master, 800, 600, self.show_login_frame,
                                            customer_service=self.customer_service)
        self.admin_frame = AdminFrame(self.master, 800, 600, self.show_login_frame,
                                      admin_service=self.administrator_service)
        self.driver_frame = DriverFrame(self.master, 800, 600, self.show_login_frame, self.driver_service)
        self.show_login_frame()

    def show_login_frame(self):
        """Show the login frame."""
        self.hide_all_frames()
        self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_register_frame(self):
        """Show the register frame."""
        self.hide_all_frames()
        self.register_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_customer_frame(self, user_data=None):
        """Show the customer frame."""
        self.hide_all_frames()
        if user_data:
            self.customer_frame.configure_user(user_data)  # Dynamically configure frame
        self.customer_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_admin_frame(self, user_data=None):
        """Show the admin frame."""
        self.hide_all_frames()
        if user_data:
            self.admin_frame.configure_user(user_data)  # Dynamically configure frame
        self.admin_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_driver_frame(self, user_data=None):
        """Show the driver frame."""
        self.hide_all_frames()
        if user_data:
            self.driver_frame.configure_user(user_data)  # Dynamically configure frame
        self.driver_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def hide_all_frames(self):
        """Hide all frames."""
        self.login_frame.place_forget()
        self.register_frame.place_forget()
        self.customer_frame.place_forget()
        self.admin_frame.place_forget()
        self.driver_frame.place_forget()

    def handle_login(self, user_type, user_data):

        if user_type == 'admin':
            self.show_admin_frame(user_data)
        elif user_type == 'driver':
            self.show_driver_frame(user_data)
        elif user_type == 'customer':
            self.show_customer_frame(user_data)
        else:
            messagebox.showerror("Login Error", "Invalid user type.", parent=self.master)

    def run(self):
        """Run the application by showing the login frame initially."""
        self.show_login_frame()
