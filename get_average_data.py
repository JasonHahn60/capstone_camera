import csv
from collections import defaultdict

distances = defaultdict(list)
with open("marker_distances.csv", mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        marker_id = row["Marker ID"]
        distance = float(row["Distance"])
        distances[marker_id].append(distance)

averages = {marker_id: sum(dist_list) / len(dist_list) for marker_id, dist_list in distances.items()}
for marker_id, avg_distance in averages.items():
    print(f"Marker ID: {marker_id}, Average Distance: {avg_distance/1000:.3f}")



print("----------------------\n")

# Set a new, higher threshold that's appropriate for your measurements
threshold_upper = 15000  # Example upper limit threshold, adjust as needed
threshold_lower = 4000   # Example lower limit threshold, adjust as needed

filtered_distances = []
with open("marker_distances.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        distance = float(row["Distance"])
        # Only include distances within the specified range
        if threshold_lower < distance < threshold_upper:
            filtered_distances.append(distance)

# Check if the list has enough data to proceed
if filtered_distances:
    filtered_distances.sort()
    n = len(filtered_distances)
    if n % 2 == 0:  # Even number of distances
        median_distance = (filtered_distances[n//2 - 1] + filtered_distances[n//2]) / 2
    else:  # Odd number of distances
        median_distance = filtered_distances[n//2]
    average_distance = sum(filtered_distances) / n

    print(f"Average Distance (excluding outliers): {average_distance:.2f}")
    print(f"Median Distance (excluding outliers): {median_distance:.2f}")
else:
    print("No distances within the specified range were found. Check your data and threshold values.")
