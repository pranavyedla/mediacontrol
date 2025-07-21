import streamlit as st
import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

st.title("Hand Gesture Media Control (MediaPipe + OpenCV)")

# Streamlit checkbox to start/stop camera
run = st.checkbox('Start Camera')
frame_placeholder = st.empty()
status_placeholder = st.empty()

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1
)

prev_gesture = None
gesture_last_time = 0
cooldown = 1  # seconds

def control_system(gesture):
    if gesture == "volume_up":
        pyautogui.press("volumeup")
    elif gesture == "volume_down":
        pyautogui.press("volumedown")
    elif gesture == "pause":
        pyautogui.press("playpause")

def recognize_gesture(hand_landmarks):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    # Thumb logic (can adjust for left/right hand if needed)
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    if fingers == [0, 1, 1, 0, 0]:  # Index and middle up
        return "volume_up"
    elif fingers == [0, 1, 0, 0, 0]:  # Only index up
        return "volume_down"
    elif fingers == [0, 0, 0, 0, 0]:  # Fist
        return "pause"
    return None

if run:
    cap = cv2.VideoCapture(0)
    status_placeholder.info("Press the checkbox again to stop the camera.")
    while run:
        ret, frame = cap.read()
        if not ret:
            status_placeholder.error("Failed to capture image")
            break
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = recognize_gesture(hand_landmarks)
                if gesture:
                    # Cooldown logic to avoid repeated keypresses
                    if gesture != prev_gesture or (time.time() - gesture_last_time) > cooldown:
                        control_system(gesture)
                        prev_gesture = gesture
                        gesture_last_time = time.time()
                    cv2.putText(frame, f"Gesture: {gesture}", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    status_placeholder.success(f"Gesture Detected: {gesture}")
                else:
                    prev_gesture = None
                    cv2.putText(frame, "Gesture: Neutral", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    status_placeholder.info("Gesture: Neutral")
        else:
            prev_gesture = None
            cv2.putText(frame, "Gesture: Neutral", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            status_placeholder.info("Gesture: Neutral")

        # Show webcam feed in the Streamlit app
        frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
        # Streamlit can't easily break out of the loop, so rely on the checkbox
        if not run:
            break

    cap.release()
    status_placeholder.info("Camera stopped.")
else:
    status_placeholder.info("Check the box above to start the camera.")