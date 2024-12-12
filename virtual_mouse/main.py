import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe Hands and drawing utility
capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils

# Get screen width and height for PyAutoGUI
screen_width, screen_height = pyautogui.size()

# Initialize the camera
camera = cv2.VideoCapture(0)

# Initialize variables for mouse control
x1 = y1 = x2 = y2 = 0

while True:
    _, image = camera.read()
    image_height, image_width, _ = image.shape
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print("Mediapipe imported successfully")
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks
    
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                # print(x, y)
                if id == 8:  # Index finger tip
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    cv2.circle(image, (x, y), 10, (0, 255, 255), -1)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1 = x
                    y1 = y
                if id == 4:  # Thumb tip
                    x2 = x
                    y2 = y
                    cv2.circle(image, (x, y), 10, (0, 255, 255), -1)
                    
        dist = y2 - y1
        print(dist)
        if dist < 20:
            pyautogui.click()
            
    cv2.imshow("Hand movement video capture", image)
    key = cv2.waitKey(1)  # Fixed delay to 1ms for smoother video capture
    if key == 27:  # Press 'ESC' to exit
        break

camera.release()
cv2.destroyAllWindows()