import numpy as np

# Load the calibration data
calib_data_path = "calib_data/4k/MultiMatrix.npz"  # Update this path if needed
data = np.load(calib_data_path)

# Extract the camera matrix and distortion coefficients
camMatrix = data["camMatrix"]
distCoeffs = data["distCoef"]

# Print the camera matrix
print("Camera Matrix (K):")
print(camMatrix)

# Extracting and printing focal lengths and principal point coordinates from the camera matrix
fx = camMatrix[0, 0]  # Focal length in pixel coordinates along the x-axis
fy = camMatrix[1, 1]  # Focal length in pixel coordinates along the y-axis
cx = camMatrix[0, 2]  # Principal point x-coordinate
cy = camMatrix[1, 2]  # Principal point y-coordinate

print(f"\nFocal Lengths (fx, fy) in pixels: ({fx}, {fy})")
print(f"Principal Point Coordinates (cx, cy) in pixels: ({cx}, {cy})")

# Print the distortion coefficients
print("\nDistortion Coefficients:")
print(distCoeffs)
