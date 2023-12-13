import cv2
'''''
# Iterate through available video sources
for i in range(0, 10):
    cap = cv2.VideoCapture(i)

    # Get the video source name
    frameframe, frame = cap.read()

    # Check if the video source contains 'usb' in its name
    if frameframe == True:
        print('i: ', i)
        cap.release()
        cv2.destroyAllWindows()
        break

# Check if no webcam with 'usb' in the name was found
if frameframe == False:
    print("Unable to find a webcam with 'usb' in the name.")
    exit()
'''''
cap = cv2.VideoCapture(4)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS , 120)
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    print("CAP_PROP_FPS : '{}'".format(cap.get(cv2.CAP_PROP_FPS)))

    # Check if the frame was successfully captured
    if not ret:
        print("Failed to capture frame from the webcam.")
        break

    # Display the frame in a window named 'Webcam'
    cv2.imshow('Webcam', frame)

    # Wait for the 'q' key to be pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close the window
cap.release()
cv2.destroyAllWindows()