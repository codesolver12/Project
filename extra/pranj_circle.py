import cv2
import numpy as np
import time

# Function to detect circles using Hough transforms
def detect_circles(image, min_radius, max_radius, param1, param2):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect circles in the original color image
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=100,
                               param1=param1, param2=param2, minRadius=min_radius, maxRadius=max_radius)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # Sort circles based on radius in descending order
        circles = sorted(circles[0], key=lambda x: x[2], reverse=True)[:1]
        return circles
    else:
        return None

# Function to draw a green circle around the detected circle and display text
def draw_circle_text(image, circle, color, text):
    center = (circle[0], circle[1])
    radius = circle[2]
    
    # Draw the circle
    cv2.circle(image, center, radius, color, 2)
    
    # Display text
    text_position = (center[0] - radius, center[1] - radius - 10)
    cv2.putText(image, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)

# Main function
def main():
    # Open the video capture
    cap = cv2.VideoCapture(0)

    # Set video frame width and height
    cap.set(3, 640)
    cap.set(4, 480)

    # Parameters for HoughCircles
    min_radius = 10
    max_radius = 100
    param1 = 50
    param2 = 30

    # Initialize variables for FPS calculation
    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect circles
        circles = detect_circles(frame, min_radius, max_radius, param1, param2)

        # Draw circles and text
        if circles is not None:
            for circle in circles:
                color = (0, 255, 0)  # Green color
                text = f"Circle Detected"
                draw_circle_text(frame, circle, color, text)

        # Calculate and display FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

        # Show the frame
        cv2.imshow('Circle Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture
    cap.release()

    # Destroy all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == "_main_":
    main()