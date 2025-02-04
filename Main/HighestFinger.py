# Perform relevant imports
import cv2
import mediapipe as mp

# Initialize the MediaPipe Hands model
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
    "thumb": [0, 1, 2, 3, 4],
    "index": [0, 5, 6, 7, 8],
    "middle": [0, 9, 10, 11, 12],
    "ring": [0, 13, 14, 15, 16],
    "pinky": [0, 17, 18, 19, 20]
}

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Run the loop infinitely
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
        # Initialise
        highest_finger = None
        highest_y = float("inf")  # Initialize with negative infinity

        for landmarks in results.multi_hand_landmarks:

            # Iterate through each finger's landmarks
            for finger, landmark_indices in finger_landmarks.items():
                finger_tip_landmark = landmarks.landmark[landmark_indices[-1]]
                finger_tip_x, finger_tip_y = int(finger_tip_landmark.x * img.shape[1]), int(finger_tip_landmark.y * img.shape[0])

                # Check if this finger's tip is higher than the current highest
                if finger_tip_y < highest_y:
                    highest_y = finger_tip_y
                    highest_finger = finger

                # Draw circles at the finger tips
                cv2.circle(img, (finger_tip_x, finger_tip_y), 5, (0, 255, 0), -1)
                cv2.putText(img, str(finger), (finger_tip_x - 10, finger_tip_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # Draw lines between landmarks
            for connection in connections:
                start_point = landmarks.landmark[connection[0]]
                end_point = landmarks.landmark[connection[1]]
                start_x, start_y = int(start_point.x * img.shape[1]), int(start_point.y * img.shape[0])
                end_x, end_y = int(end_point.x * img.shape[1]), int(end_point.y * img.shape[0])
                cv2.line(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        
        # Display the highest finger in text
        cv2.putText(img, f'Highest Finger: {highest_finger}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display Video and when 'q' is entered, destroy the window
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
