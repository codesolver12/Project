from flask import Flask, render_template
import serial

app = Flask(__name__)
ser = serial.Serial('COM5', 57600)

@app.route('/')
def index():
    if ser.in_waiting > 0:
        received_data = ser.readline().decode('utf-8').strip()
        return render_template('telemetry_test.html', data=received_data)
    else:
        return render_template('telemetry_test.html', data='No data received')

if __name__ == '__main__':
    # You may need to run the script with elevated privileges or use a virtual environment
    app.run(debug=False)
