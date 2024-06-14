import json
import uuid
import tkinter as tk
from tkinter import messagebox, simpledialog
import re
from datetime import datetime
from Admin import Admin
from Patient import Patient


class System:
    def __init__(self):
        self.data = self.load_data()
        self.root = tk.Tk()
        self.root.withdraw()
        self.main_menu()

    # Generate a 6-digit unique ID
    def generate_id(self):
        return str(uuid.uuid4().int)[:6]

    # Load data from the 'hospital_data.txt' file
    def load_data(self):
        try:
            with open('hospital_data.txt', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"users": [], "doctors": [], "appointments": []}

    # Save data to the 'hospital_data.txt' file
    def save_data(self):
        with open('hospital_data.txt', 'w') as file:
            json.dump(self.data, file)

    # Find a user by their username
    def find_user(self, username):
        for user in self.data['users']:
            if user['username'] == username:
                return user

    # No space allowed in username
    def is_valid_username(self, username):
        return ' ' not in username

    # Main menu function for initial options
    def main_menu(self):
        options = """
        Welcome to the Hospital Management System
        1. Sign Up as Patient
        2. Sign Up as Admin
        3. Log In
        4. Exit
        """
        while True:
            choice = simpledialog.askstring("Main Menu", options)
            if choice == '1':
                self.sign_up(as_admin=False)
            elif choice == '2':
                self.sign_up(as_admin=True)
            elif choice == '3':
                self.log_in()
            elif choice == '4':
                break
            else:
                messagebox.showerror("Error", "Invalid option. Please try again.")

    # Sign up function for both patients and admins
    def sign_up(self, as_admin=False):
        # Admin sign-up requires a secret key
        if as_admin:
            secret_key = simpledialog.askstring("Admin Sign Up", "Please enter the admin secret key:")
            correct_key = "jyx666"
            if secret_key != correct_key:
                messagebox.showerror("Error", "Incorrect secret key. You do not have permission to create an admin account.")
                return
            user_type = "admin"
        else:
            user_type = "patient"

        # Collect name and check if it contains only letters
        while True:
            name = simpledialog.askstring("Sign Up", "Enter your name:")
            if name == None:
                return
            if ' ' in name:
                messagebox.showerror("Error", "No space allowed. Please try again.")
                return
            if name and name.isalpha():
                break
            else:
                messagebox.showerror("Error", "Name must contain only letters and can't be empty. Please try again.")

        # Collect username and check if it already exists
        while True:
            username = simpledialog.askstring("Sign Up", "Enter username:")
            if username == None:
                return
            if ' ' in username:
                messagebox.showerror("Error", "Username cannot contain spaces. Please try a different username.")
            elif any(user['username'] == username for user in self.data['users']):
                messagebox.showerror("Error", "Username already exists. Please try a different username.")
            elif username == '':
                messagebox.showerror("Error", "Username can't be empty")
            else:
                break

        # Collect password
        while True:
            password = simpledialog.askstring("Sign Up", "Enter password:", show='*')
            if password == None:
                return
            else:
                break

        # Collect additional details for patients
        if as_admin:
            email = None
            phone_number = None
            medical_records = None
        else:
            email = simpledialog.askstring("Sign Up", "Enter email:")
            if email == None:
                return
            phone_number = simpledialog.askstring("Sign Up", "Enter phone number:")
            if phone_number == None:
                return
            medical_history = simpledialog.askstring("Sign Up", "Enter medical history:")
            if medical_history == None:
                return
            medical_records = [{"id": self.generate_id(), "date": datetime.now().strftime("%Y-%m-%d"), "details": medical_history}]

        # Create user dictionary and append to users list
        user = {
            "id": self.generate_id(),
            "name": name,
            "username": username,
            "password": password,
            "email": email,
            "phone_number": phone_number,
            "medical_records": medical_records,
            "type": user_type
        }
        self.data["users"].append(user)
        self.save_data()
        messagebox.showinfo("Success", "Sign up successful. Please log in to continue.")

    # Log in function for both patients and admins
    def log_in(self):
        while True:
            username = simpledialog.askstring("Log In", "Enter username:")
            if username == None:
                return
            else:
                break

        while True:
            password = simpledialog.askstring("Log In", "Enter password:", show='*')
            if password == None:
                return
            else:
                break

        # Validate user credentials
        for user in self.data['users']:
            if user['username'] == username and user['password'] == password:
                messagebox.showinfo("Success", f"Log in successful. Welcome, {user['username']}.")
                if 'admin' in user.get('type', ''):
                    Admin(self, user)
                else:
                    Patient(self, user)
                return
        messagebox.showerror("Error", "Login failed. Username or password is incorrect.")