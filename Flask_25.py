import random
import cv2
import numpy as np
import time
from datetime import datetime
import csv
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO

# Configuration
PORT = 5000
static_folder = 'static'
LIVE_file_path = os.path.join(static_folder, 'flight_data.csv')

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_file('redirect.html')
        elif self.path == '/home':
            self.serve_file('datapage.html')
        elif self.path == '/random_number':
            self.serve_json_data()
        elif self.path == '/video':
            self.serve_video_stream()
        else:
            self.serve_static()

    def serve_file(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(os.path.join(static_folder, filename), 'rb') as f:
            self.wfile.write(f.read())

    def serve_static(self):
        try:
            filepath = os.path.join(static_folder, self.path[1:])
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-type', self.guess_mime_type(filepath))
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        except:
            self.send_error(500)

    def serve_json_data(self):
        altitude, airspeed, lat, lon = self.sensor_input_data()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(f'{{"altitude": {altitude}, "airspeed": {airspeed}, "lat": {lat}, "lon": {lon}}}'.encode())

    def serve_video_stream(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        camera = cv2.VideoCapture(0)
        try:
            while True:
                success, frame = camera.read()
                if not success: break
                ret, buffer = cv2.imencode('.jpg', frame)
                self.wfile.write(b'--frame\r\n')
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', len(buffer))
                self.end_headers()
                self.wfile.write(buffer.tobytes())
        finally:
            camera.release()

    def guess_mime_type(self, filepath):
        return {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.jpg': 'image/jpeg',
            '.png': 'image/png'
        }.get(os.path.splitext(filepath)[1], 'application/octet-stream')

    def sensor_input_data(self):
        return (
            random.randint(40, 45),
            random.randint(10, 20),
            round(11.650227 - (random.randint(-1, 1)*0.0005), 6),
            round(76.166992 + (random.randint(-1, 1)*0.0005), 6)
        )

if __name__ == '__main__':
    with open(LIVE_file_path, 'w') as f:
        f.write('timestamp,value,status,longitude,latitude\n')

    server = HTTPServer(('localhost', PORT), ServerHandler)
    print(f"Server running on port {PORT}")
    server.serve_forever()
