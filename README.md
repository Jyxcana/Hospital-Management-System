# Hospital Management System

This is a simple hospital management system implemented using Python and Tkinter. The system allows users to sign up as patients or admins, log in, and perform various tasks such as booking appointments, viewing medical records, and managing doctors. The data is stored in a JSON file (`hospital_data.txt`).

## Features

- **User Types**: Patients and Admins.
- **Sign Up**: Separate sign-up processes for patients and admins.
- **Log In**: Users can log in using their username and password.
- **Admin Functions**:
  - Add, update, and remove doctors.
  - View all appointments.
  - View patient records.
  - View all doctors.
- **Patient Functions**:
  - View available doctors.
  - Book appointments with doctors.
  - View own appointments.
  - View own medical records.

## Installation and Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Jyxcana/Hospital-Management-System.git
    cd <repository_directory>
    ```

2. **Install Dependencies**:
    Ensure you have Python and Tkinter installed. Tkinter usually comes pre-installed with Python.

3. **Run the Application**:
    ```bash
    python main.py
    ```

## Usage

### Main Menu

Upon starting the application, you will see the main menu with the following options:

1. **Sign Up as Patient**: Register as a patient.
2. **Sign Up as Admin**: Register as an admin (requires a secret key).
3. **Log In**: Log in to the system.
4. **Exit**: Exit the application.

### Sign Up

- **Patient Sign Up**:
  - Enter your name (only letters, no spaces).
  - Choose a username (no spaces).
  - Set a password.
  - Provide your email and phone number.
  - Enter your medical history.

- **Admin Sign Up**:
  - Enter the admin secret key (`jyx666`).
  - Enter your name (only letters, no spaces).
  - Choose a username (no spaces).
  - Set a password.

### Log In

- Enter your username and password to log in.
- If the credentials are correct, you will be directed to either the admin or patient menu based on your account type.

### Admin Menu

Admins have the following options:

1. **Add Doctor**: Add a new doctor by providing their name, specialty, and available slots.
2. **Update Doctor**: Update the information of an existing doctor.
3. **Remove Doctor**: Remove a doctor using their ID.
4. **View Appointments**: View all appointments.
5. **View Patient Records**: View medical records of a specific patient.
6. **View All Doctors**: View all registered doctors.
7. **Log Out**: Log out from the admin account.

### Patient Menu

Patients have the following options:

1. **View Doctors**: View all available doctors.
2. **Book Appointment**: Book an appointment with a doctor by providing the doctor's ID, desired date, and time.
3. **View Appointments**: View all your appointments.
4. **View Medical Records**: View your medical records.
5. **Log Out**: Log out from the patient account.

## Data Storage

All data is stored in a JSON file named `hospital_data.txt` located in the same directory as the script. The data includes user information, doctor information, and appointments.

## License

This project is licensed under the MIT License.

## Contact

For any questions or issues, please contact jyxcana@gmail.com.
