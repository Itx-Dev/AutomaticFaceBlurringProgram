import cv2


class RenderBlur:
    def __init__(self, videoFilePath, progressBar, mainFrame):
        # Get Display Elements
        self.progressBar = progressBar
        self.mainFrame = mainFrame

        self.progressPercent = 0

        self.videoCapture = cv2.VideoCapture(videoFilePath)  # Get Video
        self.totalFrames = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))  # Find total frames of video
        self.frameWidth = int(self.videoCapture.get(3))  # Find Video Width
        self.frameHeight = int(self.videoCapture.get(4))  # Find Video Height
        self.fps = self.videoCapture.get(5)  # Find FPS
        self.codec = cv2.VideoWriter_fourcc(*'XVID')  # Define Codec
        self.outputVideo = cv2.VideoWriter('output_video.avi', self.codec, self.fps,
                                           (self.frameWidth, self.frameHeight))  # Define Output Video Name

    def updateProgressBar(self, percent):
        # If task completes delete progress bar
        if percent >= 99:
            self.progressBar.pack_forget()
        self.progressBar["value"] = percent
        self.mainFrame.update_idletasks()

    def renderBlur(self):

        # Define front face and side face classifiers
        frontalFaceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        sideFaceClassifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

        while True:
            # Read a frame from the video capture
            ret, frame = self.videoCapture.read()

            # If the frame is not read successfully, break the loop
            if not ret:
                print("Video Over")
                return 0

            # Check for the 'q' key to quit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return -1

            # Convert the frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect frontal faces in the grayscale frame
            faces = frontalFaceClassifier.detectMultiScale(gray_frame, scaleFactor=1.05, minNeighbors=5,
                                                           minSize=(40, 40))

            # Detect side faces in the grayscale frame
            profile_faces = sideFaceClassifier.detectMultiScale(gray_frame, scaleFactor=1.05, minNeighbors=5,
                                                                minSize=(40, 40))

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
            self.outputVideo.write(frame)

            # Calculate and print the progress
            current_frame = int(self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES))
            self.progressPercent = (current_frame / self.totalFrames) * 100
            self.updateProgressBar(self.progressPercent)

