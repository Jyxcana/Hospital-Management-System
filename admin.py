from datetime import datetime
from tkinter import simpledialog, messagebox

class Admin:
    def __init__(self, system, user):
        self.system = system
        self.user = user
        self.admin_menu()

    # Admin menu with options to manage doctors and view data
    def admin_menu(self):
        options = """
        1. Add Doctor
        2. Update Doctor
        3. Remove Doctor
        4. View Appointments
        5. View Patient Records
        6. View All Doctors
        7. Log Out
        """
        while True:
            choice = simpledialog.askstring("Admin Menu", options)
            if choice == '1':
                self.add_doctor()
            elif choice == '2':
                self.update_doctor()
            elif choice == '3':
                self.remove_doctor()
            elif choice == '4':
                self.view_appointments()
            elif choice == '5':
                self.view_patient_records()
            elif choice == '6':
                self.view_all_doctors()
            elif choice == '7':
                break
            else:
                messagebox.showerror("Error", "Invalid option. Please try again.")

    # Function to check valid date
    def is_valid_datetime(self, datetime_str):
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    # Function to add a doctor
    def add_doctor(self):
        while True:
            name = simpledialog.askstring("Add Doctor", "Enter doctor's name:")
            if name == None:
                messagebox.showerror("Error", "Name can't be skipped.")
            else:
                break
        if not name.isalpha():
            messagebox.showerror("Error", "Name must contain only letters.")
            return
        specialty = simpledialog.askstring("Add Doctor", "Enter specialty:")
        start_date = simpledialog.askstring("Add Doctor", "Enter available start date (YYYY-MM-DD):")
        start_time = simpledialog.askstring("Add Doctor", "Enter available start time (HH:MM):")
        end_date = simpledialog.askstring("Add Doctor", "Enter available end date (YYYY-MM-DD):")
        end_time = simpledialog.askstring("Add Doctor", "Enter available end time (HH:MM):")

        # Ensure no fields are left blank
        if not all([name, specialty, start_date, start_time, end_date, end_time]):
            messagebox.showerror("Error", "All fields are required.")
            return

        # Check if start date/time is before end date/time
        start_datetime = f"{start_date} {start_time}"
        end_datetime = f"{end_date} {end_time}"
        if not self.is_valid_datetime(start_datetime) or not self.is_valid_datetime(end_datetime):
            messagebox.showerror("Error", "Invalid date or time format. Please enter a valid date (YYYY-MM-DD) and time (HH:MM).")
            return
        if start_datetime >= end_datetime:
            messagebox.showerror("Error", "Start date/time must be before end date/time.")
            return

        doctor_id = self.system.generate_id()
        doctor = {
            "id": doctor_id,
            "name": name,
            "specialty": specialty,
            "available_slots": {
                "start": start_datetime,
                "end": end_datetime
            }
        }
        self.system.data["doctors"].append(doctor)
        self.system.save_data()
        messagebox.showinfo("Success", f"Doctor {name} added successfully with ID {doctor_id}.")

    # Function to update a doctor's information
    def update_doctor(self):
        doctor_id = simpledialog.askstring("Update Doctor", "Enter Doctor ID:")
        for doctor in self.system.data['doctors']:
            if doctor['id'] == doctor_id:
                doctor['name'] = simpledialog.askstring("Update Doctor", "Enter new name:")
                doctor['specialty'] = simpledialog.askstring("Update Doctor", "Enter new specialty:")
                start_date = simpledialog.askstring("Update Doctor", "Enter new available start date (YYYY-MM-DD):")
                start_time = simpledialog.askstring("Update Doctor", "Enter new available start time (HH:MM):")
                end_date = simpledialog.askstring("Update Doctor", "Enter new available end date (YYYY-MM-DD):")
                end_time = simpledialog.askstring("Update Doctor", "Enter new available end time (HH:MM):")

                # Ensure no fields are left blank
                if not all([doctor['name'], doctor['specialty'], start_date, start_time, end_date, end_time]):
                    messagebox.showerror("Error", "All fields are required.")
                    return

                # Check if start date/time is before end date/time
                start_datetime = f"{start_date} {start_time}"
                end_datetime = f"{end_date} {end_time}"
                if not self.is_valid_datetime(start_datetime) or not self.is_valid_datetime(end_datetime):
                    messagebox.showerror("Error", "Invalid date or time format. Please enter a valid date (YYYY-MM-DD) and time (HH:MM).")
                    return
                if start_datetime >= end_datetime:
                    messagebox.showerror("Error", "Start date/time must be before end date/time.")
                    return

                doctor['available_slots'] = {
                    "start": start_datetime,
                    "end": end_datetime
                }
                self.system.save_data()
                messagebox.showinfo("Success", f"Doctor {doctor['name']} updated successfully.")
                return
        messagebox.showerror("Error", "Doctor not found.")

    # Function to remove a doctor
    def remove_doctor(self):
        doctor_id = simpledialog.askstring("Remove Doctor", "Enter Doctor ID:")
        for i, doctor in enumerate(self.system.data['doctors']):
            if doctor['id'] == doctor_id:
                del self.system.data['doctors'][i]
                self.system.save_data()
                messagebox.showinfo("Success", f"Doctor {doctor['name']} removed successfully.")
                return
        messagebox.showerror("Error", "Doctor not found.")

    # Function to view all appointments
    def view_appointments(self):
        appointments = "\n".join([f"Appointment ID: {a['id']}, Patient: {a['patient_username']}, Doctor: {a['doctor_name']}, Date: {a['date']}, Time: {a['time']}" for a in self.system.data['appointments']])
        messagebox.showinfo("Appointments", appointments)

    # Function to view patient records
    def view_patient_records(self):
        patient_username = simpledialog.askstring("View Patient Records", "Enter patient username:")
        user = self.system.find_user(patient_username)
        if not user:
            messagebox.showerror("Error", "Patient not found.")
            return
        records = "\n".join([f"Record ID: {r['id']}, Date: {r['date']}, Details: {r['details']}" for r in user.get('medical_records', [])])
        messagebox.showinfo("Medical Records", records)

    # Function to view all doctors
    def view_all_doctors(self):
        if not self.system.data['doctors']:
            messagebox.showinfo("All Doctors", "No doctors for now.")
            return
        doctors = "\n".join([f"ID: {d['id']}, Name: {d['name']}, Specialty: {d['specialty']}, Available Slots: {d['available_slots']}" for d in self.system.data['doctors']])
        messagebox.showinfo("All Doctors", doctors)
