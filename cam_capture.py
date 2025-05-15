import cv2
import time
import socket

from collections import deque

ROBOT_IP_ADDRESS = "192.168.56.2"
PORT = 29999
buffer_size = 1024

## For testing
def robot_unlock_protective_stop_and_play(client_socket):
    message = "Unlock Protective Stop" + "\n"
    client_socket.sendall(message.encode())
    time.sleep(2)
    message = "play" + "\n"
    client_socket.sendall(message.encode())

def robot_status_polling_cbseries(client_socket):
    try:
        message = "safetymode" + "\n"
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)

        print(f"Received from server: {data.decode()}")
        current_robot_status = data.decode().strip()
        print(current_robot_status)

        if current_robot_status == "Safetymode: NORMAL":
            return False
        
        elif current_robot_status == "Safetymode: PROTECTIVE_STOP":
            return True
        
        else:
            print("Status invalid")
        
        
    except socket.error as e:
        print(f"Connection error: {e}")

def robot_status_polling_eseries(client_socket):
    try:
        message = "safetystatus" + "\n"
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)

        # print(f"Received from server: {data.decode()}")
        current_robot_status = data.decode().strip()

        if current_robot_status == "Safetystatus: NORMAL":
            return False
        
        elif current_robot_status == "Safetystatus: PROTECTIVE_STOP":
            return True
        
        else:
            print("Status invalid")
        
        
    except socket.error as e:
        print(f"Connection error: {e}")

def robot_ip_connection():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ROBOT_IP_ADDRESS, PORT))
        print(f"Connected to server at {ROBOT_IP_ADDRESS}:{PORT}")
        
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

        return client_socket
        
    except socket.error as e:
        print(f"Connection error: {e}")

def query_robot_generation(client_socket):
    try:
        message = "get serial number" + "\n"
        client_socket.sendall(message.encode())
        
        data_robot_serial_no_temp = client_socket.recv(1024)
        data_robot_serial_no = data_robot_serial_no_temp.decode().strip() 
        print(f"Robot serial number: {data_robot_serial_no}")
        data_curr_robot_gen = data_robot_serial_no[4] 

        return data_curr_robot_gen

    except socket.error as e:
        print(f"Connection error: {e}")

# def get_current_date_and_time():
#     current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
#     return

def add_timestamp(frame):
    # Get the current time as a string
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Add the timestamp text to the frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_corner = (10, 30)
    font_scale = 1
    font_color = (0, 255, 0)  # Green color
    line_type = 2
    cv2.putText(frame, current_time, bottom_left_corner, font, font_scale, font_color, line_type)

def save_buffer_video(buffer_frames, output_file, fps):
    if len(buffer_frames) == 0:
        print("Error: Buffer is empty. Unable to save buffer video.")
        return

    height, width, _ = buffer_frames[0][1].shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Write the frames from the buffer to the video
    for _, frame in buffer_frames:
        output_video.write(frame)

    # Release the video writer
    output_video.release()

def stream_video_to_buffer(buffer_duration, additional_duration, sock, robot_gen):
    # Set the desired frame rate for the buffer duration
    buffer_fps = 30  # Adjust this value if needed
    additional_frame_count = 0
    capturing_post_key_frames = False
    capture_once = False 
    
    
    # Open the default camera (usually the built-in webcam)
    # TODO Consider if there's multiple cameras on the PC (Webcam + External)
    
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        print("Error: Unable to access the webcam.")
        return
    
    # Robot Generation Polling functions. Dashboard commands are different on the CB and e-series
    if robot_gen == "3":
        polling_function = robot_status_polling_cbseries
        print("Robot generation: cb-series")
    elif robot_gen == "5":
        polling_function = robot_status_polling_eseries
        type
        print("Robot generation: e-series")
    else:
        raise ValueError(f"Unknown Robot generation: {robot_gen}")


    # Calculate the number of frames to capture for the specified buffer duration
    buffer_frames_to_capture = int(buffer_fps * buffer_duration)
    additional_frames_to_capture = int(buffer_fps * additional_duration)

    # Use a deque to create a circular buffer to store frames with timestamps
    frame_buffer = deque(maxlen=buffer_frames_to_capture + additional_frames_to_capture)

    # Start the streaming and buffer loop
    print("Streaming webcam video to buffer...")
    while True:
        isRobotStopped = polling_function(sock)
        
        ret, frame = capture.read()

        # Check if frame was successfully read
        if not ret:
            print("Error: Unable to read frame.")
            break

        # Get the current timestamp
        current_time = time.time()
        
        # Add timestamp to the frame
        add_timestamp(frame)

        # Append the frame with the timestamp to the buffer
        frame_buffer.append((current_time, frame))

        # Display the frame
        cv2.imshow("Webcam", frame)

        # Press 'q' to quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        # TEMP For testing
        if key == ord('c'):
            robot_unlock_protective_stop_and_play(sock)

        if isRobotStopped is True and capturing_post_key_frames is False and capture_once is False:
            capturing_post_key_frames = True

            keypress_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
            print(f"Start of camera recording:{keypress_time}")
            print("Please wait white we capture additional frames after keypress...")

        
            # If capturing post-key frames, count the frames
        if capturing_post_key_frames:
            additional_frame_count += 1

            # Once we've captured the required additional frames, save the video
            if additional_frame_count >= additional_frames_to_capture:
                # This if statement extends the frame_buffer to overwrite previous frame buffer and add the next X seconds. 
                # Save the buffer video with timestamps
                output_file = f"Recording_{keypress_time}.avi" 
                
                save_buffer_video(list(frame_buffer), output_file, buffer_fps)
                print(f"Buffer video saved as '{output_file}'")

                end_recording = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())

                print(f"End of camera recording:{end_recording}")

                # Reset the capture state (or stop the loop if done)
                capturing_post_key_frames = False
                capture_once = True
                additional_frame_count = 0
                
        if isRobotStopped is False and capture_once is True:
            capture_once = False

    # Release the capture and close the window
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    buffer_duration = 10  # Buffer duration in seconds (e.g., 10 seconds)
    additional_duration = 5  # Additional recording duration after 'c' is pressed (e.g., 5 seconds)
    
    initialTimecheck_val = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Program started at {initialTimecheck_val}")
    
    sock = robot_ip_connection()
    robot_gen = query_robot_generation(sock)

    time.sleep(0.5)

    while True:
        stream_video_to_buffer(buffer_duration, additional_duration, sock, robot_gen)
