import face_recognition
import mysql.connector
import numpy as np

cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='CH@rms12345',
    database='attendence'
)
cursor = cnx.cursor()
known_face_names=['sriya']

data = []

for i, name in enumerate(known_face_names, start=1):
    image = face_recognition.load_image_file("/home/rupesh_pabba/Desktop/attendance/known_people/" + name + ".jpeg")
    encoding = face_recognition.face_encodings(image)[0]
    encoding_string = encoding.tostring()
    data.append((12, name, encoding_string))
    print(data)

insert_query1 = "INSERT INTO student_details (roll_no, name, face_encodings,status) VALUES (%s, %s, %s,NULL)"
insert_query2 = """INSERT INTO log(names, `2023-09-10`, `2023-09-11`, `2023-09-12`, `2023-09-19`, `2023-09-20`, `2023-11-22`, `2023-12-08`, `2023-12-09`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
parameters = (known_face_names[0], None, None, None, None, None, None, None, None)
cursor.executemany(insert_query1, data)
print('yes')
cursor.execute(insert_query2, parameters)
print('done')


# Commit the changes to the database
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
