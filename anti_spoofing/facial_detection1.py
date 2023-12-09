import face_recognition
import cv2
import numpy as np
import mysql.connector
from collections import defaultdict
from fake_detect import testing
from collections import Counter
import datetime
import sys
from playsound import playsound
date=datetime.datetime.now().time()
current_time_str = f"{date.hour:02d}:{date.minute:02d}"


def get_most_common_names(name_list,threshold=1):
    name_counts = Counter(name_list)
    most_common_names = [name for name, count in name_counts.items() if count >= threshold]
    return most_common_names

def insert_attendance(names):
    if names == "Unknown":
        pass
    else:    
        try:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            check_column_query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'log' AND COLUMN_NAME = '{current_date}'"
            cursor.execute(check_column_query)

            if cursor.fetchone():
                # Column already exists, update the attendance
                update_query = f"UPDATE log SET `{current_date}` = %s WHERE names = %s;"
                values = ("present({})".format(current_time_str), names)
                cursor.execute(update_query, values)
                print("attendance updated successfully for " + names)
            else:
                # Column doesn't exist, create it and insert attendance
                create_column_query = f"ALTER TABLE log ADD COLUMN `{current_date}` VARCHAR(20);"
                cursor.execute(create_column_query)

                # Insert attendance for the current date
                insert_query = f"UPDATE log SET `{current_date}` = %s WHERE names = %s;"
                values = ("present", names)
                cursor.execute(insert_query, values)
                print("attendance updated successfully for " + names)

        except Exception as e:
            print("Error occurred:", str(e))

connection = mysql.connector.connect(host="localhost", user="root", password="CH@rms12345", database="attendence")
cursor = connection.cursor()
cursor.execute("use attendence")
cursor.execute("select face_encodings from student_details")
rows = cursor.fetchall()
cursor1 = connection.cursor()
cursor1.execute('use attendence')
cursor1.execute('select name from student_details')
names = cursor1.fetchall()

known_face_encodings = []
for row in rows:
    encoding_string = row[0]
    encoding = np.fromstring(encoding_string, dtype=np.float64)
    known_face_encodings.append(encoding.tolist())

known_face_names = [name[0] for name in names]

with open('/home/rupesh_pabba/rupeshpabba/IKSHANA/YOLO-3-OpenCV/yolo-coco-data/coco.names') as f:
    labels = [line.strip() for line in f]


network = cv2.dnn.readNetFromDarknet('/home/rupesh_pabba/rupeshpabba/IKSHANA/YOLO-3-OpenCV/yolo-coco-data/yolov3.cfg',
                                     '/home/rupesh_pabba/rupeshpabba/IKSHANA/YOLO-3-OpenCV/yolo-coco-data/yolov3.weights')

layers_names_all = network.getLayerNames()

layers_names_output = \
    [layers_names_all[i - 1] for i in network.getUnconnectedOutLayers()]


probability_minimum = 0.5

threshold1 = 0.3

colours = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

video_capture = cv2.VideoCapture(0)
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
recognized_counts = defaultdict(int) 
spoofed_faces_in_past_frames = []  
h, w = None, None

while True:
    ret, frame = video_capture.read()

    if process_this_frame:
        if w is None or h is None:
        # Slicing from tuple only first two elements
            h, w = frame.shape[:2]
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
        network.setInput(blob)
        output_from_network = network.forward(layers_names_output)
        bounding_boxes = []
        confidences = []
        class_numbers = []
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    
    for result in output_from_network:
        for detected_objects in result:
            scores = detected_objects[5:]
            class_current = np.argmax(scores)
            confidence_current = scores[class_current]
            if confidence_current > probability_minimum:

                box_current = detected_objects[0:4] * np.array([w, h, w, h])

                x_center, y_center, box_width, box_height = box_current
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))

                bounding_boxes.append([x_min, y_min,
                                       int(box_width), int(box_height)])
                confidences.append(float(confidence_current))
                class_numbers.append(class_current)

    results = cv2.dnn.NMSBoxes(bounding_boxes, confidences,
                               probability_minimum, threshold1)
    texts = []
    if len(results) > 0:
        for i in results.flatten():
            colour_box_current = colours[class_numbers[i]].tolist() 
            texts.append(labels[class_numbers[i]])
    cell=False
    for i in texts:
        if i =='cell phone':
            cell=True

    label = testing(frame,
                    model_dir='/home/rupesh_pabba/Desktop/attendance/anti_spoofing/resources/anti_spoof_models',
                    device_id=1)

    if label == 0 or cell==True:
        spoofed_faces_in_past_frames.append(face_names)

        print('Spoofing Detected!'+"for",end=' ')
        print(spoofed_faces_in_past_frames)
        playsound('beep-warning-6387.mp3')
        sys.exit()
    

    else:
        recognized_counts.clear()  
        
        for name in face_names:
            recognized_counts[name] += 1
        
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            box_color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            label_text = "Unknown" if name == "Unknown" else name

            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, label_text, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        
        cv2.imshow('Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


final_attendance=get_most_common_names(face_names,threshold=1)
print(final_attendance)
for i in final_attendance:
    insert_attendance(i)

connection.commit()
cursor.close()
connection.close()
video_capture.release()
cv2.destroyAllWindows()

