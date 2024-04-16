import cv2
import numpy as np
import os
import glob

# Define the dimensions of checkerboard
CHECKERBOARD = (6, 6)

# Stop the iteration when specified accuracy, epsilon, is reached or specified number of iterations are completed.
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 3D points real world coordinates
objectp3d = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objectp3d[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
threedpoints = []  # 3D point in real world space
twodpoints = []  # 2D points in image plane

# Path to the directory containing calibration images
image_dir_path = './calibration_images'
if not os.path.exists(image_dir_path):
    print(f"Error: The specified directory does not exist: {image_dir_path}")
    exit()

images = glob.glob(f'{image_dir_path}/*.jpg')
if not images:
    print(f"No images found in the directory: {image_dir_path}")
    exit()

for filename in images:
    image = cv2.imread(filename)
    if image is None:
        print(f"Failed to load image: {filename}")
        continue

    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(grayColor, CHECKERBOARD,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK +
                                             cv2.CALIB_CB_NORMALIZE_IMAGE)
    if not ret:
        print(f"Chessboard corners not found in image: {filename}")
        continue

    print(f"Chessboard corners detected in image: {filename}")
    threedpoints.append(objectp3d)
    corners2 = cv2.cornerSubPix(grayColor, corners, (11, 11), (-1, -1), criteria)
    twodpoints.append(corners2)

# Perform calibration only if points have been collected
if not threedpoints or not twodpoints:
    print("No valid points collected from images for calibration.")
else:
    ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(threedpoints, twodpoints, grayColor.shape[::-1], None, None)
    print("Camera calibration successful.")
    # Add code to save and load calibration data as shown in the previous example.
