# Hospital-Management-System

This is a simple Hospital Management System implemented using Python and Tkinter. The system allows for user registration, login, and management of doctors and appointments. There are different roles for users (patients and admins), each with their own set of functionalities.

## Features

- **User Registration**: Patients and admins can sign up for an account.
- **User Login**: Patients and admins can log in to access their respective menus.
- **Admin Functions**:
  - Add, update, and remove doctors.
  - View all appointments.
  - View patient records.
- **Patient Functions**:
  - View doctors.
  - Book appointments.
  - View their own appointments.
  - View their own medical records.

## Prerequisites

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## Installation

1. Clone the repository or download the source code.
2. Ensure Python is installed on your system.
3. Run the `hospital_management_system.py` file.

```sh
python hospital_management_system.py
```

## Usage

1. **Launch the Application**: Run the script to start the application.
2. **Main Menu**: You will be presented with options to sign up as a patient, sign up as an admin, log in, or exit.
3. **Sign Up**: Choose to sign up as either a patient or an admin. Admin sign-up requires a secret key (`jyx666`).
4. **Log In**: Log in with your username and password.
5. **Admin Menu**: After logging in as an admin, you can add, update, or remove doctors, view all appointments, and view patient records.
6. **Patient Menu**: After logging in as a patient, you can view doctors, book appointments, view your appointments, and view your medical records.

## File Structure

- `hospital_management_system.py`: The main script file containing all the functionalities.
- `hospital_data.txt`: A JSON file used for storing user data, doctor information, and appointments.

## Code Overview

- **Data Loading and Saving**:
  - `load_data()`: Loads data from the `hospital_data.txt` file.
  - `save_data(data)`: Saves data to the `hospital_data.txt` file.

- **User Management**:
  - `sign_up(as_admin=False)`: Sign-up function for patients and admins.
  - `log_in()`: Log-in function for patients and admins.
  - `find_user(data, username)`: Finds a user by their username.

- **Admin Functions**:
  - `admin_menu()`: Displays the admin menu.
  - `add_doctor()`: Adds a new doctor.
  - `update_doctor()`: Updates an existing doctor's information.
  - `remove_doctor()`: Removes a doctor.
  - `view_appointments()`: Views all appointments.
  - `view_patient_records()`: Views patient records.

- **Patient Functions**:
  - `patient_menu(user)`: Displays the patient menu.
  - `view_doctors()`: Views all doctors.
  - `book_appointment(user)`: Books an appointment for a patient.
  - `view_my_appointments(user)`: Views the patient's own appointments.
  - `view_my_records(user)`: Views the patient's own medical records.

- **Main Menu**:
  - `main_menu()`: Displays the initial main menu with options to sign up, log in, or exit.

- **Entry Point**:
  - The script starts by hiding the root Tkinter window and displaying the main menu.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
