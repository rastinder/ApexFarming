import cv2
import time

def capture_webcam():
    for source_index in range(4):
        video_capture = cv2.VideoCapture(source_index)
        if video_capture.isOpened():
            print("Webcam source {}: {}".format(source_index, video_capture.getBackendName()))
            video_capture.release()
    
    selected_source = int(input("Enter the source index to use: "))
    
    video_capture = cv2.VideoCapture(selected_source)
    
    if not video_capture.isOpened():
        print("Failed to open the selected webcam")
        return
    
    source_name = video_capture.getBackendName()
    print("Capture Source: {}".format(source_name))
    
    start_time = time.time()
    num_frames = 0
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        cv2.imshow(source_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        num_frames += 1
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    fps = num_frames / elapsed_time
    
    print("Frames per second: {:.2f}".format(fps))
    
    video_capture.release()
    cv2.destroyAllWindows()

capture_webcam()
