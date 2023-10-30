import cv2
import mediapipe as mp
import serial

ser = serial.Serial('/dev/cu.usbmodem141301', 9600)

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
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            is_left_hand = landmarks.landmark[0].x < landmarks.landmark[5].x

            finger_count = 0
            for finger, landmark_indices in finger_landmarks.items():
                base_landmark = landmarks.landmark[landmark_indices[0]]
                tip_landmark = landmarks.landmark[landmark_indices[-1]]

                if finger == "thumb":
                    if is_left_hand:
                        relative_x_displacement = tip_landmark.x - base_landmark.x
                        if relative_x_displacement > 0.02:
                            finger_count += 1
                    else:
                        relative_x_displacement = base_landmark.x - tip_landmark.x
                        if relative_x_displacement > 0.02:
                            finger_count += 1
                else:
                    relative_y_displacement = tip_landmark.y - base_landmark.y
                    threshold_y_displacement = -0.05

                    if relative_y_displacement < threshold_y_displacement:
                        finger_count += 1

            for connection in connections:
                start_point = landmarks.landmark[connection[0]]
                end_point = landmarks.landmark[connection[1]]
                start_x, start_y = int(start_point.x * img.shape[1]), int(start_point.y * img.shape[0])
                end_x, end_y = int(end_point.x * img.shape[1]), int(end_point.y * img.shape[0])
                cv2.line(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        
            ser.write(bytes([finger_count]))

            # Decide where to put the text based on which hand is detected
            text_position = (50, 50) if is_left_hand else (img.shape[1] - 200, 50)
            cv2.putText(img, f'Fingers: {finger_count}', text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()