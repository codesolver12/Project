from flask import Flask, render_template, jsonify, send_from_directory, request, Response
import random
import cv2
import numpy as np
import time
from datetime import datetime
import csv
import shutil
import os
import serial 


static_folder = 'static'
LIVE_file_path = os.path.join(static_folder, 'flight_data.csv')
STORED_file_path = os.path.join(static_folder, 'flight_data_copy.csv')
ZONE_file_path = os.path.join(static_folder, 'flight_data_zonecopy.csv')

app = Flask(__name__, static_folder='static')

app.config['DEBUG']=False
camera = cv2.VideoCapture(1)



#================================================================
# USE WHEN ARDUINO NOT CONNECTED
#================================================================
def sensor_input_data():
    altitude = random.randint(40, 45)
    airspeed = random.randint(10, 20)
    lat = round(11.650227 - (random.randint(-1, 1)*0.0005),6)
    lon = round(76.166992 + (random.randint(-1, 1)*0.0005),6)
    pong = "t"



    return(altitude,airspeed,lat,lon,pong)
#================================================================
#================================================================


#================================================================
# USE WHEN ARDUINO CONNECTED
#================================================================    

# ser = serial.Serial('COM5', 57600)  # Change 'COM3' to the appropriate port for your Arduino
# def sensor_input_data():
#     try:
#         while True:
#             if ser.in_waiting > 0:
#                 received_data = ser.readline().decode('utf-8').strip()  # Read data from the serial port
#                 Sensor_data = received_data.split(',')

#                     # Assign each substring to a separate variable
#                 altitude, airspeed, lat, lon, pong= Sensor_data
#                 print(altitude, airspeed, lat, lon, pong)

#                 return(altitude,airspeed,lat,lon,pong)
    
#     except Exception as e:
#         print("ERROR OCCURED !!!")

#================================================================
#================================================================
def dataAcquire(status):
    altitude,airspeed,lat,lon = sensor_input_data()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    
    time.sleep(1)  # Simulate some work

    with open(LIVE_file_path, mode='a', newline='') as file:
        fieldnames = ['timestamp', 'value','status','longitude','latitude']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        

    writer.writerow({'timestamp': formatted_time, 'value': altitude, 'status':status, 'longitude':lat, 'latitude':lon})

    return jsonify(altitude=altitude,airspeed=airspeed,lat=lat,lon=lon)
#================================================================
def convert_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #return(frame)

def detect_circles(frame):
    # Apply GaussianBlur to reduce noise and help circle detection
    blurred_frame = cv2.GaussianBlur(frame, (9, 9), 2)

    # Use Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(
        blurred_frame,
        cv2.HOUGH_GRADIENT,
        dp=1,  # inverse ratio of accumulator resolution
        minDist=330,  # minimum distance between centers of detected circles
        param1=50,  # upper threshold for the internal Canny edge detector
        param2=30,  # threshold for center detection
        minRadius=10,  # minimum radius of the circles
        maxRadius=270  # maximum radius of the circles
    )

    if circles is not None:
        # Convert the circle coordinates to integers
        circles = np.uint16(np.around(circles))
        
        # Draw the circles on the frame
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

    return frame

def generate_frames():
    while True:
        # read the camera frame
        success, frame = camera.read()

        if not success:
            break
        else:
            # convert the frame to grayscale
            gray_frame = convert_to_grayscale(frame)

            # detect circles in the grayscale frame
            frame_with_circles = detect_circles(gray_frame)

            # encode the frame with circles to JPEG
            ret, buffer = cv2.imencode('.jpg', frame_with_circles)
            frame_bytes = buffer.tobytes()

            # yield the frame with circles and appropriate boundaries for multipart streaming
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#================================================================

@app.route('/')
def re_direct():
    with open(LIVE_file_path, mode='w', newline='') as file:
        fieldnames = fieldnames = ['timestamp', 'value','status','longitude','latitude']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
                writer.writeheader()

    with open(LIVE_file_path, mode='w', newline='') as copy_file:
        fieldnames = ['timestamp', 'value','status','longitude','latitude']
        writer = csv.DictWriter(copy_file, fieldnames=fieldnames)
        if copy_file.tell() == 0:
                writer.writeheader()

    return render_template('redirect.html')

@app.route('/home')
def datapage():
    shutil.copy(LIVE_file_path,ZONE_file_path)
    return render_template('datapage.html')

@app.route('/random_number', methods=['GET'])
def get_random_number():

        altitude,airspeed,lat,lon,pong = sensor_input_data()
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        
        time.sleep(1)  # Simulate some work

        with open(LIVE_file_path, mode='a', newline='') as file:
            fieldnames = fieldnames = ['timestamp', 'value','status','longitude','latitude']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            

            writer.writerow({'timestamp': formatted_time, 'value': altitude, 'status':'ARMED', 'longitude':lat, 'latitude':lon})

        return jsonify(altitude=altitude,airspeed=airspeed,lat=lat,lon=lon)



@app.route('/random_number_deployed', methods=['GET'])
def get_random_number_deployed():

        altitude,airspeed,lat,lon,pong = sensor_input_data()
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")

        time.sleep(1)  # Simulate some work

        with open(LIVE_file_path, mode='a', newline='') as file:
            fieldnames = ['timestamp', 'value','status','longitude','latitude']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            

            writer.writerow({'timestamp': formatted_time, 'value': altitude, 'status':"DEPLOYED", 'longitude':lat, 'latitude':lon})

        return jsonify(altitude=altitude,airspeed=airspeed,lat=lat,lon=lon)

        



@app.route('/playback_static')  
def secondpage_static():
    shutil.copy(LIVE_file_path,STORED_file_path)
    return render_template('playback_static.html')

@app.route('/playback_live')  
def secondpage_live():
    return render_template('playback_live.html')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)