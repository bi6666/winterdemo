import cv2
import numpy as np

# Initialize global variables
hue_values = []


def capture_hue(event, x, y, flags, param):
    """Capture the hue value from the mouse click."""
    global hue_values
    if event == cv2.EVENT_LBUTTONDOWN:
        # Take the pixel color in BGR format
        bgr = frame[y, x]
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)
        hue_values.append(hsv[0][0][0])
        print(f"HSV Value at ({x}, {y}): {hsv[0][0]}")  # Print the HSV value


def main():
    global frame
    # Capture video from the webcam (typically the first camera)
    cap = cv2.VideoCapture(0)

    cv2.namedWindow('Laser Pointer Detection')
    cv2.setMouseCallback('Laser Pointer Detection', capture_hue)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Display the current frame
        cv2.imshow('Laser Pointer Detection', frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()
    cv2.destroyAllWindows()

    # After collecting the hue values, you can decide on the lower and upper ranges.
    if hue_values:
        lower_hue = int(min(hue_values)) - 10  # Adjust these values accordingly
        upper_hue = int(max(hue_values)) + 10
        print(f"Suggested lower bound: {lower_hue}, upper bound: {upper_hue}")


if __name__ == '__main__':
    main()
