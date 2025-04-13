import serial

ser = serial.Serial('COM5', 57600) 
while True:
    if ser.in_waiting > 0:
        received_data = ser.readline().decode('utf-8').strip()
        print(received_data)