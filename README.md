
# Hand Gesture Media Control (Streamlit + OpenCV + MediaPipe)

A real-time desktop application that enables you to control your system media player (play/pause, volume up/down) using hand gestures, powered by webcam input, computer vision, and gesture recognition.

## Features

- Real-time hand gesture recognition via webcam
- Control media playback: play/pause, volume up, volume down
- Start/stop webcam stream directly from the web UI
- Uses Streamlit for UI, OpenCV and MediaPipe for hand tracking, PyAutoGUI for simulating media key presses

## Technologies Used

- Python 3.x
- [Streamlit](https://streamlit.io/)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)
- NumPy

## How It Works

- The Streamlit app captures frames from your webcam.
- MediaPipe detects hand landmarks and the app classifies specific finger patterns as:
  - **Volume Up:** Index and middle fingers up
  - **Volume Down:** Only index finger up
  - **Pause:** Fist (all fingers down)
  - **Play:** Default
- When a gesture is detected, PyAutoGUI sends the corresponding media key press to your system.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/pranavyedla/mediacontrol.git
cd mediacontrol
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
*You may need to install additional dependencies depending on your OS (see [PyAutoGUI OS requirements](https://pyautogui.readthedocs.io/en/latest/install.html)).*

### 3. Run the Application

```bash
streamlit run mediacontrol.py
```

- Open the provided local Streamlit URL in your browser.
- Click the **"Start Camera"** checkbox to start webcam detection.
- Show one of the supported gestures in front of your camera.
- Uncheck the box to stop the camera.

## Limitations

- **This app is intended to be run locally**. It cannot control your system media when deployed online due to browser/cloud sandboxing.
- Some systems may require additional permissions for webcam access and for PyAutoGUI to control media keys.
- The app supports one hand at a time and basic gestures.

## Acknowledgements

- [MediaPipe Hand Detection](https://mediapipe.dev/)
- [OpenCV Library](https://opencv.org/)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/en/latest/)
- [Streamlit](https://streamlit.io/)
