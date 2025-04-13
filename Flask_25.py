import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time
from datetime import datetime
import random
from threading import Thread

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = []
if 'camera' not in st.session_state:
    st.session_state.camera = None
if 'running' not in st.session_state:
    st.session_state.running = False

def sensor_input_data():
    """Simulated sensor data with more realistic values"""
    return {
        'timestamp': datetime.now().strftime("%H:%M:%S.%f")[:-3],
        'altitude': random.uniform(40.0, 45.0),
        'airspeed': random.uniform(150.0, 200.0),
        'latitude': 11.650227 + random.uniform(-0.001, 0.001),
        'longitude': 76.166992 + random.uniform(-0.001, 0.001),
        'temperature': random.uniform(20.0, 25.0),
        'pressure': random.uniform(950.0, 1013.25)
    }

def camera_thread():
    """Camera capture thread"""
    st.session_state.camera = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    
    while st.session_state.running:
        success, frame = st.session_state.camera.read()
        if not success:
            st.error("Failed to read camera feed")
            break
        
        # Convert to grayscale and detect circles
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(
            cv2.GaussianBlur(gray, (9, 9), 2,
            cv2.HOUGH_GRADIENT, dp=1, minDist=330,
            param1=50, param2=30, minRadius=10, maxRadius=270
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
        
        frame_placeholder.image(frame, channels="BGR")
        time.sleep(0.03)  # ~30 FPS

def start_camera():
    """Start camera capture"""
    if not st.session_state.running:
        st.session_state.running = True
        Thread(target=camera_thread, daemon=True).start()

def stop_camera():
    """Stop camera capture"""
    if st.session_state.running:
        st.session_state.running = False
        if st.session_state.camera is not None:
            st.session_state.camera.release()

# Main UI
st.title("Flight Data Monitoring System")

# Camera control
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Camera"):
        start_camera()
with col2:
    if st.button("Stop Camera"):
        stop_camera()

# Sensor data display
if st.button("Get Sensor Data"):
    new_data = sensor_input_data()
    st.session_state.data.append(new_data)
    
    # Display latest data
    st.subheader("Latest Sensor Readings")
    st.json(new_data)

# Data visualization
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    
    st.subheader("Altitude Trend")
    st.line_chart(df.set_index('timestamp')['altitude'])
    
    st.subheader("Position Tracking")
    st.map(df[['latitude', 'longitude']])
    
    st.subheader("Raw Data")
    st.dataframe(df.sort_index(ascending=False))

# Cleanup when app stops
def on_app_close():
    stop_camera()

import atexit
atexit.register(on_app_close)
