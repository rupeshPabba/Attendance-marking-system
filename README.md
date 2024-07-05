Overview

This project presents an Attendance Monitoring System leveraging Facial Recognition and Anti-Spoofing technologies. The system aims to automate the process of tracking and managing attendance in various contexts such as educational institutions and corporate environments.

Features

    Facial Recognition: Accurately identifies and verifies individuals.
    Anti-Spoofing Measures: Detects and prevents fraudulent attempts using fake images or videos.
    Real-Time Reporting: Provides real-time attendance tracking and reporting.
    User-Friendly Interface: Easy-to-use interface for administrators to manage attendance records.

Scope and Limitations

Scope:

    Supports multiple users with a comprehensive attendance database.
    Real-time monitoring through cameras and facial recognition.
    User-friendly interface for administrators.

Limitations:

    Accuracy may be affected by lighting, facial obstructions, and image quality.
    Anti-spoofing measures are not foolproof.
    Privacy concerns regarding facial data storage.
    Hardware and software requirements must be met for optimal functionality.

Usage:

1.Run "pip install -r requirements.txt".
2.run the file(facial_detection1.py) which is present in anti_spoofing directory{which starts the camera and captures faces and marks attendance for students,if nay person trying to spoof the machine he will be reported and not.}.
![image](https://github.com/rupeshPabba/Attendance-marking-system/assets/96829415/c9a63ba6-78f4-43fc-b5c2-3e3b560041cc)
![image](https://github.com/rupeshPabba/Attendance-marking-system/assets/96829415/a6f10607-51d4-418d-af5b-3bfa2f8461ac)
![image](https://github.com/rupeshPabba/Attendance-marking-system/assets/96829415/97a5ca87-438b-44d6-86ff-33aaaf57a900)

3. if you wanat to add data(i.e faces) in jpeg format you can use add_data.py{make sure you have mysql and its credentials for your database}


Results:
Database showing proof for attendance:

![image](https://github.com/rupeshPabba/Attendance-marking-system/assets/96829415/e479d14e-8585-4cf2-9c30-32664f201a90)
Detection:

![image](https://github.com/rupeshPabba/Attendance-marking-system/assets/96829415/d3211915-342f-433e-8d61-dd2d324f4144)

