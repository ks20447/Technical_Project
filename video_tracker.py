import cv2
import numpy as np
import csv


cap = cv2.VideoCapture("Videos/run_and_tumble_test.mp4")

# Initialize object tracker
tracker = cv2.TrackerCSRT_create()

# Open CSV files for writing trajectory data
output_csv_path = 'Data/KB_output_trajectories.csv'
x_csv_path = 'Data/x.csv'
y_csv_path = 'Data/y.csv'

with open(output_csv_path, 'w', newline='') as csvfile, \
        open(x_csv_path, 'w', newline='') as x_csvfile, \
        open(y_csv_path, 'w', newline='') as y_csvfile:

    csv_writer = csv.writer(csvfile)
    x_csv_writer = csv.writer(x_csvfile)
    y_csv_writer = csv.writer(y_csvfile)

    csv_writer.writerow(['ObjectID', 'Frame', 'X', 'Y'])


    # List to store selected regions
    regions_to_track = []

    while True:
        # Read the first frame from the video
        ret, frame = cap.read()
        if not ret:
            break
        # Resize the frame (optional, depending on your model)
        # frame = cv2.resize(frame, (original_width, original_height))
        # Select region of interest (ROI) for tracking
        bbox = cv2.selectROI("Select Object to Track", frame, fromCenter=False, showCrosshair=True)
        if not any(bbox):  # If the user presses 'Esc', break the loop
            break

        regions_to_track.append(bbox)

    # Initialize trackers for all selected regions
    trackers = [cv2.TrackerCSRT_create() for _ in range(len(regions_to_track))]
    for i, bbox in enumerate(regions_to_track):
        trackers[i].init(frame, bbox)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        x_values = []  # List to store X values for each robot
        y_values = []  # List to store Y values for each robot

        for i, tracker in enumerate(trackers):
            # Update tracker
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(coord) for coord in bbox]

                x_values.append(x + w / 2)
                y_values.append(y + h / 2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save X values to the CSV file
        x_csv_writer.writerow(x_values)
        # Save Y values to the CSV file
        y_csv_writer.writerow(y_values)
        # Save general trajectories to the CSV file
        csv_writer.writerow([i + 1, frame_count, x_values, y_values])


        cv2.imshow("Tracking", frame)
        if cv2.waitKey(30) & 0xFF == 27:  # Press 'Esc' to stop tracking
            break

        frame_count += 1

cap.release()
cv2.destroyAllWindows()