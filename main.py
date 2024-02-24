import cv2

video_capture = cv2.VideoCapture('videos/testFace.mp4')

# Check if the video capture object is successfully opened
if not video_capture.isOpened():
    print("Error: Unable to open the video source.")
    exit()

# Get the total number of frames in the video
total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

# Get the video's frame width, height, and frames per second
frame_width = int(video_capture.get(3))
frame_height = int(video_capture.get(4))
fps = video_capture.get(5)

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('output_video.avi', fourcc, fps, (frame_width, frame_height))

# Define front face and side face classifiers
frontalFaceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
sideFaceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

while True:
    # Read a frame from the video capture
    ret, frame = video_capture.read()

    # If the frame is not read successfully, break the loop
    if not ret:
        print("Video Over")
        break

    # Check for the 'q' key to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect frontal faces in the grayscale frame
    faces = frontalFaceClassifier.detectMultiScale(gray_frame, scaleFactor=1.05, minNeighbors=5, minSize=(40, 40))

    # Detect side faces in the grayscale frame
    profile_faces = sideFaceClassifier.detectMultiScale(gray_frame, scaleFactor=1.05, minNeighbors=5, minSize=(40, 40))

    # Draw ellipses around the detected frontal faces and apply Gaussian blur
    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        axes = (w // 2, h // 2)
        angle = 0  # You can set the angle as per your preference
        cv2.ellipse(frame, center, axes, angle, 0, 360, (0, 255, 0), 4)

        # Calculate ROI for applying Gaussian blur
        roi = frame[y:y + h, x:x + w]
        blurred_roi = cv2.GaussianBlur(roi, (101, 101), 0)

        # Replace the original ROI with the blurred one
        frame[y:y + h, x:x + w] = blurred_roi

    # Draw ellipses around the detected profile faces and apply Gaussian blur
    for (x, y, w, h) in profile_faces:
        center = (x + w // 2, y + h // 2)
        axes = (w // 2, h // 2)
        angle = 0  # You can set the angle as per your preference
        cv2.ellipse(frame, center, axes, angle, 0, 360, (255, 0, 0), 4)

        # Calculate ROI for applying Gaussian blur
        roi = frame[y:y + h, x:x + w]
        blurred_roi = cv2.GaussianBlur(roi, (101, 101), 0)  # Adjust kernel size if needed

        # Replace the original ROI with the blurred one
        frame[y:y + h, x:x + w] = blurred_roi

    # Write the frame to the output video file
    output_video.write(frame)

    # Calculate and print the progress
    current_frame = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))
    progress = (current_frame / total_frames) * 100
    print(f"Progress: {progress:.2f}%")

# Release the video capture and output video writer objects, and close all windows
video_capture.release()
output_video.release()
cv2.destroyAllWindows()