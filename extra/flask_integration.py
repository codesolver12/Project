from flask import Flask, render_template, jsonify, send_from_directory, request
import random
import time
from datetime import datetime
import csv
import shutil
import os
import serial

#from flask_socketio import SocketIO

static_folder = 'static'
LIVE_file_path = os.path.join(static_folder, 'flight_data.csv')
STORED_file_path = os.path.join(static_folder, 'flight_data_copy.csv')

app = Flask(__name__, static_folder='static')

ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the appropriate port for your Arduino


#================================================================
#THIS IS THE FUNCTION THAT YOU NEED TO BE WORKING ON 
#================================================================
def sensor_input_data():
    try:
        generated_data = ser.readline().decode().strip()  # Read data from the serial port
        return (generated_data)
    
    except Exception as e:
        print("ERROR OCCURED !!!")

#================================================================
# do not change the function name "sensor_input_data" 
# unless you change it on line 54 and line 77
#================================================================

@app.route('/')
def re_direct():
    with open(LIVE_file_path, mode='w', newline='') as file:
        fieldnames = ['timestamp', 'value','status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
                writer.writeheader()

    with open(LIVE_file_path, mode='w', newline='') as copy_file:
        fieldnames = ['timestamp', 'value','status']
        writer = csv.DictWriter(copy_file, fieldnames=fieldnames)
        if copy_file.tell() == 0:
                writer.writeheader()

    return render_template('redirect.html')

@app.route('/home')
def datapage():
    return render_template('datapage.html')

@app.route('/random_number', methods=['GET'])
def get_random_number():

        #random_number = random.randint(1, 100)                  #Random number generator to be replaced by actual data received thru telemetry
        random_number = sensor_input_data()
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        
        # print(random_number)                                  #Print to see in serial port
        time.sleep(1)  # Simulate some work

        with open(LIVE_file_path, mode='a', newline='') as file:
            fieldnames = ['timestamp', 'value','status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            

            writer.writerow({'timestamp': formatted_time, 'value': random_number, 'status':"ARMED"})

        return jsonify(random_number=random_number)



@app.route('/random_number_deployed', methods=['GET'])
def get_random_number_deployed():

        #random_number = random.randint(1, 100)                  #Random number generator to be replaced by actual data received thru telemetry
        random_number = sensor_input_data()
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        
        # print(random_number)                                  #Print to see in serial port
        time.sleep(1)  # Simulate some work

        with open(LIVE_file_path, mode='a', newline='') as file:
            fieldnames = ['timestamp', 'value','status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            


            writer.writerow({'timestamp': formatted_time, 'value': random_number, 'status':"DEPLOYED"})

        return jsonify(random_number=random_number)

        



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



if __name__ == '__main__':
    #socketio.run(app, debug=True)
    app.run(host='127.0.0.1', port=5000)