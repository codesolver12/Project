# app.py
import streamlit as st
import cv2
import numpy as np
import time
from datetime import datetime
import pandas as pd
import random

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = []

# Sensor data simulation
def sensor_input_data():
    return (
        random.randint(40, 45),
        random.randint(10, 20),
        round(11.650227 - random.uniform(-0.0005, 0.0005), 6),
        round(76.166992 + random.uniform(-0.0005, 0.0005), 6)
    )

# Video streamer
def video_stream():
    camera = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    
    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        
        # Convert to grayscale and detect circles
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, 
                                 minDist=330, param1=50, param2=30,
                                 minRadius=10, maxRadius=270)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
        
        frame_placeholder.image(frame, channels="BGR")
    
    camera.release()

# Main app
def main():
    st.title("Flight Data Dashboard")
    
    # Start video stream in a thread
    if st.button("Start Video Stream"):
        video_stream()
    
    # Data display
    if st.button("Get Sensor Data"):
        altitude, airspeed, lat, lon = sensor_input_data()
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        st.session_state.data.append({
            'timestamp': timestamp,
            'altitude': altitude,
            'airspeed': airspeed,
            'latitude': lat,
            'longitude': lon
        })
        
        st.line_chart(pd.DataFrame(st.session_state.data).set_index('timestamp'))
    
    # Show raw data
    st.dataframe(pd.DataFrame(st.session_state.data))

if __name__ == "__main__":
    main()
