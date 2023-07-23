import cv2
import keyboard
import datetime

def select_camera():
    num_cameras = 0
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            num_cameras += 1
            cap.release()
        else:
            break

    if num_cameras == 0:
        print("No cameras found.")
        return None

    print("Available cameras:")
    for i in range(num_cameras):
        print(f"{i + 1}. Camera {i + 1}")

    while True:
        try:
            camera_choice = int(input("Select the camera number (1, 2, ...): "))
            if 1 <= camera_choice <= num_cameras:
                return camera_choice - 1
            else:
                print("Invalid camera choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def record_video(output_file, camera_index, fps=20.0, duration=10):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Error: Camera {camera_index + 1} could not be opened.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()

        if ret:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Video Stream', frame)

            out.write(frame)

        if keyboard.is_pressed('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    output_file = "recorded_video.avi"
    fps = 20.0
    duration = 10  

    camera_index = select_camera()
    if camera_index is not None:
        print(f"Using Camera {camera_index + 1}")
        print("Press 'r' to start recording...")
        while True:
            if keyboard.is_pressed('r'):
                print("Recording started...")
                record_video(output_file, camera_index, fps, duration)
                print(f"Video recorded and saved to '{output_file}'.")
                break

            cv2.waitKey(1)

        print("Press 'q' to exit.")
        while True:
            if keyboard.is_pressed('q'):
                break
