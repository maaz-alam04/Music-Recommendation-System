from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import webbrowser
import threading
import signal
import sys

app = Flask(__name__)

# Load the pre-trained model and labels
model = load_model("model.h5")
label = np.load("labels.npy")

# Setup MediaPipe
holistic = mp.solutions.holistic
holis = holistic.Holistic()
drawing = mp.solutions.drawing_utils

emotion_detected = ""
cap = None
cap_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global cap
    while True:
        with cap_lock:
            if cap is None:
                break
            ret, frame = cap.read()
            if not ret:
                break
        
        frm = cv2.flip(frame, 1)  # Flip for mirror image
        res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
        lst = []

        if res.face_landmarks:
            for i in res.face_landmarks.landmark:
                lst.append(i.x - res.face_landmarks.landmark[1].x)
                lst.append(i.y - res.face_landmarks.landmark[1].y)

            if res.left_hand_landmarks:
                for i in res.left_hand_landmarks.landmark:
                    lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
            else:
                for _ in range(42):
                    lst.append(0.0)

            if res.right_hand_landmarks:
                for i in res.right_hand_landmarks.landmark:
                    lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
            else:
                for _ in range(42):
                    lst.append(0.0)

            lst = np.array(lst).reshape(1, -1)
            pred = label[np.argmax(model.predict(lst))]
            global emotion_detected
            emotion_detected = pred
            cv2.putText(frm, pred, (50, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

        drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_TESSELATION,
                               landmark_drawing_spec=drawing.DrawingSpec(color=(0, 0, 255), thickness=-1, circle_radius=1),
                               connection_drawing_spec=drawing.DrawingSpec(thickness=1))
        drawing.draw_landmarks(frm, res.left_hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
        drawing.draw_landmarks(frm, res.right_hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

        ret, buffer = cv2.imencode('.jpg', frm)
        frm = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frm + b'\r\n')

@app.route('/video_feed')
def video_feed():
    global cap
    with cap_lock:
        if cap is None:
            cap = cv2.VideoCapture(0)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_video')
def stop_video():
    global cap
    with cap_lock:
        if cap is not None:
            cap.release()
            cap = None
    return "Video stopped", 200

@app.route('/recommend', methods=['POST'])
def recommend():
    lang = request.form['lang']
    singer = request.form['singer']
    if emotion_detected in ["sad", "fear"]:
        query = f"{lang} uplifting motivational song {singer}"
    else:
        query = f"{lang} {emotion_detected} song {singer}"
    
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    return redirect(url_for('index'))

def release_camera_on_exit():
    global cap
    with cap_lock:
        if cap is not None:
            cap.release()
            cap = None

def signal_handler(sig, frame):
    release_camera_on_exit()
    sys.exit(0)

if __name__ == "__main__":
    # Set up the signal handler to release the camera on exit
    signal.signal(signal.SIGINT, signal_handler)
    app.run(debug=True)
