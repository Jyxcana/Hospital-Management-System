'''
import json
import uuid

def load_data():
    try:
        with open('hospital_data.txt', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": [], "doctors": [], "appointments": []}

def save_data(data):
    with open('hospital_data.txt', 'w') as file:
        json.dump(data, file)

def find_user(data, username):
    for user in data['users']:
        if user['username'] == username:
            return user

def sign_up(as_admin=False):
    data = load_data()
    if as_admin:
        secret_key = input("Please enter the admin secret key: ")
        correct_key = "jyx666"
        if secret_key != correct_key:
            print("Incorrect secret key. You do not have permission to create an admin account.")
            return
        user_type = "admin"
        print("    Sign Up as Admin")
    else:
        user_type = "patient"
        print("    Sign Up as Patient")

    username = input("Enter username: ")

    # Check if the username already exists
    if any(user['username'] == username for user in data['users']):
        print("Username already exists. Please try a different username.")
        return sign_up(as_admin)  # Restart the sign-up process

    password = input("Enter password: ")
    if as_admin:
        email = None
        phone_number = None
        medical_history = None
    else:
        email = input("Enter email: ")
        phone_number = input("Enter phone number: ")
        medical_history = input("Enter medical history: ")

    user = {
        "username": username,
        "password": password,
        "email": email,
        "phone_number": phone_number,
        "medical_history": medical_history,
        "type": user_type
    }
    data["users"].append(user)
    save_data(data)
    print("Sign up successful. Please log in to continue.")

def log_in():
    data = load_data()
    print("    Log In")
    username = input("Enter username: ")
    password = input("Enter password: ")
    for user in data['users']:
        if user['username'] == username and user['password'] == password:
            print(f"Log in successful. Welcome, {user['username']}.")
            if 'admin' in user.get('type', ''):
                admin_menu()
            else:
                patient_menu(user)
            return
    print("Login failed. Username or password is incorrect.")

def admin_menu():

    options = """
    1. Add Doctor
    2. Update Doctor
    3. Remove Doctor
    4. View Appointments
    5. View Patient Records
    6. Log Out
    """
    while True:
        print("    Admin Menu")
        print(options)
        choice = input("Please choose an option (1-6): ")
        if choice == '1':
            add_doctor()
        elif choice == '2':
            update_doctor()
        elif choice == '3':
            remove_doctor()
        elif choice == '4':
            view_appointments()
        elif choice == '5':
            view_patient_records()
        elif choice == '6':
            break
        else:
            print("Invalid option. Please try again.")

def patient_menu(user):
    options = """
    1. View Doctors
    2. Book Appointment
    3. View Appointments
    4. View Medical Records
    5. Log Out
    """
    while True:
        print("    Patient Menu")
        print(options)
        choice = input("Please choose an option (1-5): ")
        if choice == '1':
            view_doctors()
        elif choice == '2':
            book_appointment(user)
        elif choice == '3':
            view_my_appointments(user)
        elif choice == '4':
            view_my_records(user)
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

def add_doctor():
    data = load_data()
    name = input("Enter doctor's name: ")
    specialty = input("Enter specialty: ")
    start_date = input("Enter available start date (YYYY-MM-DD): ")
    start_time = input("Enter available start time (HH:MM): ")
    end_date = input("Enter available end date (YYYY-MM-DD): ")
    end_time = input("Enter available end time (HH:MM): ")
    doctor_id = str(uuid.uuid4())
    doctor = {
        "id": doctor_id,
        "name": name,
        "specialty": specialty,
        "available_slots": {
            "start": f"{start_date} {start_time}",
            "end": f"{end_date} {end_time}"
        }
    }
    data["doctors"].append(doctor)
    save_data(data)
    print(f"Doctor {name} added successfully with ID {doctor_id}.")

def update_doctor():
    data = load_data()
    doctor_id = input("Enter Doctor ID: ")
    for doctor in data['doctors']:
        if doctor['id'] == doctor_id:
            doctor['name'] = input("Enter new name: ")
            doctor['specialty'] = input("Enter new specialty: ")
            start_date = input("Enter new available start date (YYYY-MM-DD): ")
            start_time = input("Enter new available start time (HH:MM): ")
            end_date = input("Enter new available end date (YYYY-MM-DD): ")
            end_time = input("Enter new available end time (HH:MM): ")
            doctor['available_slots'] = {
                "start": f"{start_date} {start_time}",
                "end": f"{end_date} {end_time}"
            }
            save_data(data)
            print(f"Doctor {doctor['name']} updated successfully.")
            return
    print("Doctor not found.")

def remove_doctor():
    data = load_data()
    doctor_id = input("Enter Doctor ID: ")
    for i, doctor in enumerate(data['doctors']):
        if doctor['id'] == doctor_id:
            del data['doctors'][i]
            save_data(data)
            print(f"Doctor {doctor['name']} removed successfully.")
            return
    print("Doctor not found.")

def view_appointments():
    data = load_data()
    print("List of Appointments:")
    for appointment in data['appointments']:
        print(f"Appointment ID: {appointment['id']}, Patient: {appointment['patient_username']}, Doctor: {appointment['doctor_name']}, Date: {appointment['date']}, Time: {appointment['time']}")

def view_patient_records():
    data = load_data()
    patient_username = input("Enter patient username: ")
    user = find_user(data, patient_username)
    if not user:
        print("Patient not found.")
        return
    print("List of Medical Records:")
    for record in user.get('medical_records', []):
        print(f"Record ID: {record['id']}, Date: {record['date']}, Diagnosis: {record['diagnosis']}, Treatment: {record['treatment']}")

# Patient actions
def view_doctors():
    data = load_data()
    print("List of Doctors:")
    for doctor in data['doctors']:
        print(f"ID: {doctor['id']}, Name: {doctor['name']}, Specialty: {doctor['specialty']}, Available Slots: {doctor['available_slots']}")

def book_appointment(user):
    data = load_data()
    view_doctors()
    doctor_id = input("Enter Doctor ID: ")
    desired_date = input("Enter desired date (YYYY-MM-DD): ")
    desired_time = input("Enter desired time (HH:MM): ")
    desired_datetime = f"{desired_date} {desired_time}"
    for doctor in data['doctors']:
        if doctor['id'] == doctor_id:
            slots = doctor['available_slots']
            if slots['start'] <= desired_datetime <= slots['end']:
                appointment_id = str(uuid.uuid4())
                appointment = {
                    "id": appointment_id,
                    "patient_username": user['username'],
                    "doctor_name": doctor['name'],
                    "date": desired_date,
                    "time": desired_time
                }
                data['appointments'].append(appointment)
                save_data(data)
                print(f"Appointment booked with Dr. {doctor['name']} on {desired_datetime}.")
                return
    print("Invalid slot. Please choose from the available slots.")

def view_my_appointments(user):
    data = load_data()
    print("List of Appointments:")
    for appointment in data['appointments']:
        if appointment['patient_username'] == user['username']:
            print(f"Appointment ID: {appointment['id']}, Doctor: {appointment['doctor_name']}, Date: {appointment['date']}, Time: {appointment['time']}")

def view_my_records(user):
    print("List of Medical Records:")
    for record in user.get('medical_records', []):
        print(f"Record ID: {record['id']}, Date: {record['date']}, Diagnosis: {record['diagnosis']}, Treatment: {record['treatment']}")

def main_menu():
    options = """
    Welcome to the Hospital Management System
    1. Sign Up as Patient
    2. Sign Up as Admin
    3. Log In
    4. Exit
    """
    while True:
        print(options)
        choice = input("Please choose an option (1-4): ")
        if choice == '1':
            sign_up(as_admin=False)
        elif choice == '2':
            sign_up(as_admin=True)
        elif choice == '3':
            log_in()
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
'''
import json
import uuid
import tkinter as tk
from tkinter import messagebox, simpledialog

# Load data from the 'hospital_data.txt' file
def load_data():
    try:
        with open('hospital_data.txt', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": [], "doctors": [], "appointments": []}

# Save data to the 'hospital_data.txt' file
def save_data(data):
    with open('hospital_data.txt', 'w') as file:
        json.dump(data, file)

# Find a user by their username
def find_user(data, username):
    for user in data['users']:
        if user['username'] == username:
            return user

# Sign up function for both patients and admins
def sign_up(as_admin=False):
    data = load_data()

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

    # Collect username and check if it already exists
    username = simpledialog.askstring("Sign Up", "Enter username:")
    if any(user['username'] == username for user in data['users']):
        messagebox.showerror("Error", "Username already exists. Please try a different username.")
        sign_up(as_admin)
        return

    # Collect password
    password = simpledialog.askstring("Sign Up", "Enter password:", show='*')

    # Collect additional details for patients
    if as_admin:
        email = None
        phone_number = None
        medical_history = None
    else:
        email = simpledialog.askstring("Sign Up", "Enter email:")
        phone_number = simpledialog.askstring("Sign Up", "Enter phone number:")
        medical_history = simpledialog.askstring("Sign Up", "Enter medical history:")

    # Create user dictionary and append to users list
    user = {
        "username": username,
        "password": password,
        "email": email,
        "phone_number": phone_number,
        "medical_history": medical_history,
        "type": user_type
    }
    data["users"].append(user)
    save_data(data)
    messagebox.showinfo("Success", "Sign up successful. Please log in to continue.")

# Log in function for both patients and admins
def log_in():
    data = load_data()
    username = simpledialog.askstring("Log In", "Enter username:")
    password = simpledialog.askstring("Log In", "Enter password:", show='*')

    # Validate user credentials
    for user in data['users']:
        if user['username'] == username and user['password'] == password:
            messagebox.showinfo("Success", f"Log in successful. Welcome, {user['username']}.")
            if 'admin' in user.get('type', ''):
                admin_menu()
            else:
                patient_menu(user)
            return
    messagebox.showerror("Error", "Login failed. Username or password is incorrect.")

# Admin menu with options to manage doctors and view data
def admin_menu():
    options = """
    1. Add Doctor
    2. Update Doctor
    3. Remove Doctor
    4. View Appointments
    5. View Patient Records
    6. Log Out
    """
    while True:
        choice = simpledialog.askstring("Admin Menu", options)
        if choice == '1':
            add_doctor()
        elif choice == '2':
            update_doctor()
        elif choice == '3':
            remove_doctor()
        elif choice == '4':
            view_appointments()
        elif choice == '5':
            view_patient_records()
        elif choice == '6':
            break
        else:
            messagebox.showerror("Error", "Invalid option. Please try again.")

# Patient menu with options to view doctors, book appointments, and view records
def patient_menu(user):
    options = """
    1. View Doctors
    2. Book Appointment
    3. View Appointments
    4. View Medical Records
    5. Log Out
    """
    while True:
        choice = simpledialog.askstring("Patient Menu", options)
        if choice == '1':
            view_doctors()
        elif choice == '2':
            book_appointment(user)
        elif choice == '3':
            view_my_appointments(user)
        elif choice == '4':
            view_my_records(user)
        elif choice == '5':
            break
        else:
            messagebox.showerror("Error", "Invalid option. Please try again.")

# Function to add a doctor
def add_doctor():
    data = load_data()
    name = simpledialog.askstring("Add Doctor", "Enter doctor's name:")
    specialty = simpledialog.askstring("Add Doctor", "Enter specialty:")
    start_date = simpledialog.askstring("Add Doctor", "Enter available start date (YYYY-MM-DD):")
    start_time = simpledialog.askstring("Add Doctor", "Enter available start time (HH:MM):")
    end_date = simpledialog.askstring("Add Doctor", "Enter available end date (YYYY-MM-DD):")
    end_time = simpledialog.askstring("Add Doctor", "Enter available end time (HH:MM):")
    doctor_id = str(uuid.uuid4())
    doctor = {
        "id": doctor_id,
        "name": name,
        "specialty": specialty,
        "available_slots": {
            "start": f"{start_date} {start_time}",
            "end": f"{end_date} {end_time}"
        }
    }
    data["doctors"].append(doctor)
    save_data(data)
    messagebox.showinfo("Success", f"Doctor {name} added successfully with ID {doctor_id}.")

# Function to update a doctor's information
def update_doctor():
    data = load_data()
    doctor_id = simpledialog.askstring("Update Doctor", "Enter Doctor ID:")
    for doctor in data['doctors']:
        if doctor['id'] == doctor_id:
            doctor['name'] = simpledialog.askstring("Update Doctor", "Enter new name:")
            doctor['specialty'] = simpledialog.askstring("Update Doctor", "Enter new specialty:")
            start_date = simpledialog.askstring("Update Doctor", "Enter new available start date (YYYY-MM-DD):")
            start_time = simpledialog.askstring("Update Doctor", "Enter new available start time (HH:MM):")
            end_date = simpledialog.askstring("Update Doctor", "Enter new available end date (YYYY-MM-DD):")
            end_time = simpledialog.askstring("Update Doctor", "Enter new available end time (HH:MM):")
            doctor['available_slots'] = {
                "start": f"{start_date} {start_time}",
                "end": f"{end_date} {end_time}"
            }
            save_data(data)
            messagebox.showinfo("Success", f"Doctor {doctor['name']} updated successfully.")
            return
    messagebox.showerror("Error", "Doctor not found.")

# Function to remove a doctor
def remove_doctor():
    data = load_data()
    doctor_id = simpledialog.askstring("Remove Doctor", "Enter Doctor ID:")
    for i, doctor in enumerate(data['doctors']):
        if doctor['id'] == doctor_id:
            del data['doctors'][i]
            save_data(data)
            messagebox.showinfo("Success", f"Doctor {doctor['name']} removed successfully.")
            return
    messagebox.showerror("Error", "Doctor not found.")

# Function to view all appointments
def view_appointments():
    data = load_data()
    appointments = "\n".join([f"Appointment ID: {a['id']}, Patient: {a['patient_username']}, Doctor: {a['doctor_name']}, Date: {a['date']}, Time: {a['time']}" for a in data['appointments']])
    messagebox.showinfo("Appointments", appointments)

# Function to view patient records
def view_patient_records():
    data = load_data()
    patient_username = simpledialog.askstring("View Patient Records", "Enter patient username:")
    user = find_user(data, patient_username)
    if not user:
        messagebox.showerror("Error", "Patient not found.")
        return
    records = "\n".join([f"Record ID: {r['id']}, Date: {r['date']}, Diagnosis: {r['diagnosis']}, Treatment: {r['treatment']}" for r in user.get('medical_records', [])])
    messagebox.showinfo("Medical Records", records)

# Function to view all doctors
def view_doctors():
    data = load_data()
    doctors = "\n".join([f"ID: {d['id']}, Name: {d['name']}, Specialty: {d['specialty']}, Available Slots: {d['available_slots']}" for d in data['doctors']])
    messagebox.showinfo("Doctors", doctors)

# Function to book an appointment for a patient
def book_appointment(user):
    data = load_data()
    view_doctors()
    doctor_id = simpledialog.askstring("Book Appointment", "Enter Doctor ID:")
    desired_date = simpledialog.askstring("Book Appointment", "Enter desired date (YYYY-MM-DD):")
    desired_time = simpledialog.askstring("Book Appointment", "Enter desired time (HH:MM):")
    desired_datetime = f"{desired_date} {desired_time}"
    for doctor in data['doctors']:
        if doctor['id'] == doctor_id:
            slots = doctor['available_slots']
            if slots['start'] <= desired_datetime <= slots['end']:
                appointment_id = str(uuid.uuid4())
                appointment = {
                    "id": appointment_id,
                    "patient_username": user['username'],
                    "doctor_name": doctor['name'],
                    "date": desired_date,
                    "time": desired_time
                }
                data['appointments'].append(appointment)
                save_data(data)
                messagebox.showinfo("Success", f"Appointment booked with Dr. {doctor['name']} on {desired_datetime}.")
                return
    messagebox.showerror("Error", "Invalid slot. Please choose from the available slots.")

# Function to view patient's own appointments
def view_my_appointments(user):
    data = load_data()
    appointments = "\n".join([f"Appointment ID: {a['id']}, Doctor: {a['doctor_name']}, Date: {a['date']}, Time: {a['time']}" for a in data['appointments'] if a['patient_username'] == user['username']])
    messagebox.showinfo("My Appointments", appointments)

# Function to view patient's own medical records
def view_my_records(user):
    records = "\n".join([f"Record ID: {r['id']}, Date: {r['date']}, Diagnosis: {r['diagnosis']}, Treatment: {r['treatment']}" for r in user.get('medical_records', [])])
    messagebox.showinfo("My Medical Records", records)

# Main menu function for initial options
def main_menu():
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
            sign_up(as_admin=False)
        elif choice == '2':
            sign_up(as_admin=True)
        elif choice == '3':
            log_in()
        elif choice == '4':
            break
        else:
            messagebox.showerror("Error", "Invalid option. Please try again.")

# Entry point of the application
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    main_menu()
