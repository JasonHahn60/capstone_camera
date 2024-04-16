import cv2 as cv
from cv2 import aruco
import numpy as np
import csv

# Load calibration data
calib_data_path = r"C:\Users\jason\Documents\UT\Camera\openCV\calib_data\480p\MultiMatrix.npz"
calib_data = np.load(calib_data_path)
cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]

MARKER_SIZE = 46.433

# Aruco marker dictionary
marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)  # Initialize the camera

#cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

#cap.set(cv.CAP_PROP_FRAME_WIDTH, 3840)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2160)


# Initialize a list to store the distances
distance_data = []

while True:
    ret, frame = cap.read()
    #print(frame.shape)
    if not ret:
        break

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )

    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        
        for i in range(marker_IDs.size):
            # Calculate the distance
            distance = np.sqrt(tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2)
            
            # Append the marker ID and distance to the list
            distance_data.append([int(marker_IDs[i]), round(distance, 3)])
            
            # Visualization code (draws polylines, frame axes, and text on the frame)
            corners = marker_corners[i].reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            bottom_right = corners[2].ravel()

            cv.polylines(frame, [corners], True, (0, 255, 255), 4, cv.LINE_AA)
            cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            cv.putText(frame, f"id: {marker_IDs[i][0]} Dist: {round(distance, 2)}", top_right, cv.FONT_HERSHEY_PLAIN, 1.3, (0, 0, 255), 2, cv.LINE_AA)
            cv.putText(frame, f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)}", bottom_right, cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255), 2, cv.LINE_AA)

    
    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv.destroyAllWindows()

# After closing the window, write the data to a CSV file
with open("marker_distances.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Marker ID", "Distance"])
    writer.writerows(distance_data)

print("Data has been written to marker_distances.csv")
