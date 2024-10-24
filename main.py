import cv2
import numpy as np


def main():
    # Define lower and upper range for the laser pointer color (in HSV)
    # Adjust these values according to your laser pointer color
    # Note: This example uses a typical red laser pointer
    lower_red = np.array([150,60, 245])  # Lower bound in HSV
    upper_red = np.array([170, 80, 265])  # Upper bound in HSV

    # Capture video from the webcam (typically the first camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Convert the frame from BGR to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask for the red color (laser pointer)
        mask = cv2.inRange(hsv_frame, lower_red, upper_red)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Process contours
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Draw rectangle around the detected laser pointer
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calculate the center of the bounding box
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)

            # Display the center point of the detected laser pointer
            cv2.circle(frame, (center_x, center_y), 3, (255, 0, 0), -1)

            # Optionally display distance estimation (this could be improved)
            distance = estimate_distance(h)
            cv2.putText(frame, f'Distance: {distance:.2f} m', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display the original frame and the mask
        cv2.imshow('Laser Pointer Detection', frame)
        cv2.imshow('Mask', mask)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


def estimate_distance(h):
    """
    Dummy function to estimate distance based on the height of the contour (bounding box).
    This function can be improved with more accurate distance calculations.
    """
    # Assume that a laser pointer will create a bounding box of a certain size at a given distance.
    base_height_at_2m = 50
    if h > 0:  # Prevent division by zero
        distance = base_height_at_2m / h
    else:
        distance = float('inf')  # Infinite distance if height is zero
    return round(distance, 2)


if __name__ == '__main__':
    main()
