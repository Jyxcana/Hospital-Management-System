from tkinter import simpledialog, messagebox

class Patient:
    def __init__(self, system, user):
        self.system = system
        self.user = user
        self.patient_menu()

    # Patient menu with options to view doctors, book appointments, and view records
    def patient_menu(self):
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
                self.view_doctors()
            elif choice == '2':
                self.book_appointment()
            elif choice == '3':
                self.view_my_appointments()
            elif choice == '4':
                self.view_my_records()
            elif choice == '5':
                break
            else:
                messagebox.showerror("Error", "Invalid option. Please try again.")

    # Function to book an appointment for a patient
    def book_appointment(self):
        self.view_doctors()
        while True:
            doctor_id = simpledialog.askstring("Book Appointment", "Enter Doctor ID:")
            if doctor_id == None:
                messagebox.showerror("Error", "Doctor ID can't be skipped. Try again.")
            else:
                break
        desired_date = simpledialog.askstring("Book Appointment", "Enter desired date (YYYY-MM-DD):")
        desired_time = simpledialog.askstring("Book Appointment", "Enter desired time (HH:MM):")

        # Validate date format
        try:
            desired_datetime = datetime.strptime(f"{desired_date} {desired_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format. Please enter a valid date (YYYY-MM-DD) and time (HH:MM).")
            return

        for doctor in self.system.data['doctors']:
            if doctor['id'] == doctor_id:
                slots = doctor['available_slots']
                slot_start = datetime.strptime(slots['start'], "%Y-%m-%d %H:%M")
                slot_end = datetime.strptime(slots['end'], "%Y-%m-%d %H:%M")
                if slot_start <= desired_datetime <= slot_end:
                    appointment_id = self.system.generate_id()
                    appointment = {
                        "id": appointment_id,
                        "patient_username": self.user['username'],
                        "doctor_name": doctor['name'],
                        "date": desired_date,
                        "time": desired_time
                    }
                    self.system.data['appointments'].append(appointment)
                    self.system.save_data()
                    messagebox.showinfo("Success", f"Appointment booked with Dr. {doctor['name']} on {desired_datetime}.")
                    return
        messagebox.showerror("Error", "Invalid slot. Please choose from the available slots.")

    # Function to view patient's own appointments
    def view_my_appointments(self):
        appointments = "\n".join([f"Appointment ID: {a['id']}, Doctor: {a['doctor_name']}, Date: {a['date']}, Time: {a['time']}" for a in self.system.data['appointments'] if a['patient_username'] == self.user['username']])
        messagebox.showinfo("My Appointments", appointments)

    # Function to view patient's own medical records
    def view_my_records(self):
        records = self.user.get('medical_records', [])
        if not records:
            messagebox.showinfo("My Medical Records", "No medical records found.")
            return

        record_list = "\n".join([f"Record ID: {r['id']}, Date: {r['date']}, Details: {r['details']}" for r in records])
        messagebox.showinfo("My Medical Records", record_list)

    # Function to view all doctors
    def view_doctors(self):
        if not self.system.data['doctors']:
            messagebox.showinfo("All Doctors", "No doctors for now.")
            return
        doctors = "\n".join([f"ID: {d['id']}, Name: {d['name']}, Specialty: {d['specialty']}, Available Slots: {d['available_slots']}" for d in self.system.data['doctors']])
        messagebox.showinfo("All Doctors", doctors)
