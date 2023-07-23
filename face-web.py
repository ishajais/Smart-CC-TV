import face_recognition
import cv2
import os
def load_known_faces(known_faces_folder):
    known_face_encodings = []
    known_face_names = []

    for file in os.listdir(known_faces_folder):
        image = face_recognition.load_image_file(os.path.join(known_faces_folder, file))
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) == 0:
            # No face detected in the image, skip it
            continue
        
        face_encoding = face_recognition.face_encodings(image, face_locations)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(file.split('.')[0])

    return known_face_encodings, known_face_names


def main():
    known_faces_folder = "known_faces"
    video_capture = cv2.VideoCapture(0)

    known_face_encodings, known_face_names = load_known_faces(known_faces_folder)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            # Compare the face encoding with known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]

            # Draw a rectangle around the face and display the name
            top, right, bottom, left = face_recognition.face_locations(frame)[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()