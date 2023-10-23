import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2)

# Define the connections between landmarks to form lines
connections = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (0, 9), (9, 10), (10, 11), (11, 12), (0, 13), (13, 14), (14, 15), (15, 16), (0, 17), (17, 18), (18, 19), (19, 20)]

# Finger landmark mapping
finger_landmarks = {
    "thumb": [1, 2, 3, 4],
    "index": [5, 6, 7, 8],
    "middle": [9, 10, 11, 12],
    "ring": [13, 14, 15, 16],
    "pinky": [17, 18, 19, 20]
}

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read video frame by frame
    success, img = cap.read()

    # Flip the image (frame)
    img = cv2.flip(img, 1)

    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the RGB image
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        # Initialize finger count, excluding the thumb
        finger_count = 0

        for landmarks in results.multi_hand_landmarks:
            # Calculate the relative Y displacement for each finger, excluding the thumb
            for finger, landmark_indices in finger_landmarks.items():
                if finger != "thumb":
                    base_landmark = landmarks.landmark[landmark_indices[0]]
                    tip_landmark = landmarks.landmark[landmark_indices[-1]]

                    relative_y_displacement = tip_landmark.y - base_landmark.y

                    # Set a relative Y displacement threshold for fingers (adjust as needed)
                    threshold_y_displacement = -0.05

                    if relative_y_displacement < threshold_y_displacement:
                        finger_count += 1

            # Draw lines between landmarks
            for connection in connections:
                start_point = landmarks.landmark[connection[0]]
                end_point = landmarks.landmark[connection[1]]
                start_x, start_y = int(start_point.x * img.shape[1]), int(start_point.y * img.shape[0])
                end_x, end_y = int(end_point.x * img.shape[1]), int(end_point.y * img.shape[0])
                cv2.line(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

            # Display the finger count
            cv2.putText(img, f'Fingers: {finger_count}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display Video and when 'q' is entered, destroy the window
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
