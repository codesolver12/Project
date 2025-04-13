from flask import Flask, render_template, jsonify
import random
import time


from flask import Flask, render_template
import serial

app = Flask(__name__)

# ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the appropriate port for your Arduino

# def sensor_input_data():
#     try:
#         generated_data = ser.readline().decode().strip()  # Read data from the serial port
#         return (generated_data)
    
#     except Exception as e:
#         print("ERROR OCCURED !!!")

def sensor_input_data():
     random_number = random.randint(1, 100)
     return(random_number)

@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/random_number', methods=['GET'])
def get_random_number():
    random_number = sensor_input_data()
    return jsonify(random_number=random_number)


if __name__ == '__main__':
    app.run(debug=True)