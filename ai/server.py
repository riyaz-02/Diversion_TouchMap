from flask import Flask, render_template, request, send_from_directory
import pickle
import cv2
import numpy as np

app = Flask('my_app')  # Change this line to: app = Flask('my_app')

# Load points from map.p file
with open("map.p", "rb") as f:
    points = pickle.load(f)

# Define a function to warp the image
def warp_image(img, points, size=[1920, 1080]):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [size[0], 0], [0, size[1]], [size[0], size[1]]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (size[0], size[1]))
    return imgOutput, matrix

# Define a route to serve the warped image
@app.route('/')
def index():
    # Capture image from webcam
    cap = cv2.VideoCapture(1)
    success, img = cap.read()
    cap.release()

    # Warp the image
    imgOutput, matrix = warp_image(img, points)

    # Save warped image to file
    cv2.imwrite("warped_image.jpg", imgOutput)

    # Return the warped image
    return send_from_directory('', 'warped_image.jpg')

if __name__ == '_main_':
    app.run(debug=True)
    logging.debug("Running")