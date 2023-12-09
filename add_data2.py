import face_recognition
import mysql.connector
import tkinter as tk
from tkinter import Label, Entry, Button

def submit_data():
    name = name_entry.get()
    
    # Load image and face encoding
    image = face_recognition.load_image_file(f"/home/rupesh_pabba/Desktop/attendance/known_people/{name}.jpeg")
    encoding = face_recognition.face_encodings(image)[0]
    encoding_string = encoding.tostring()
    
    # Insert data into the database
    cursor.execute("INSERT INTO student_details (roll_no, name, face_encodings, status) VALUES (%s, %s, %s, NULL)",
                   (17, name, encoding_string))
    insert_query2 = """INSERT INTO log(names, `2023-09-10`, `2023-09-11`, `2023-09-12`, `2023-09-19`, `2023-09-20`, `2023-11-22`, `2023-12-08`, `2023-12-09`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    parameters = (name, None, None, None, None, None, None, None, None)
    cursor.execute(insert_query2, parameters)
    print('done')


    # Commit the changes to the database
    cnx.commit()
    
    # Update the known_face_names list
    known_face_names.append(name)
    
    # Clear the entry
    name_entry.delete(0, tk.END)
    
    print(f'Data for {name} submitted successfully!')

# Connect to the database
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='CH@rms12345',
    database='attendence'
)
cursor = cnx.cursor()

# List to store known face names
known_face_names = []

# Create the main window
window = tk.Tk()
window.title("Face Recognition GUI")

# Create and place widgets in the window
label_name = Label(window, text="Enter Name:")
label_name.grid(row=0, column=0, padx=10, pady=10)

name_entry = Entry(window)
name_entry.grid(row=0, column=1, padx=10, pady=10)

submit_button = Button(window, text="Submit", command=submit_data)
submit_button.grid(row=1, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
window.mainloop()

# Close the cursor and connection
cursor.close()
cnx.close()
