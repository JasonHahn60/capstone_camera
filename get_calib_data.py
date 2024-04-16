import numpy as np

# Path to your calibration data
calib_data_path = r"C:\Users\jason\Documents\UT\Camera\openCV\calib_data\MultiMatrix.npz"

# Load the calibration data
calib_data = np.load(calib_data_path)

# Accessing the camera matrix
cam_matrix = calib_data["camMatrix"]
print("Camera Matrix:\n", cam_matrix)

# Accessing the distortion coefficients
dist_coef = calib_data["distCoef"]
print("\nDistortion Coefficients:\n", dist_coef)

# Optionally, accessing the rotation and translation vectors
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]
print("\nRotation Vectors:\n", r_vectors)
print("\nTranslation Vectors:\n", t_vectors)
