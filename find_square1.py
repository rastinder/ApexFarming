import cv2
import numpy as np
import pyautogui

def find_lvl(shape_tolerance=0.1):
    region = (792, 117, 83, 83)

    while True:
        try:
            # Capture the region of the screen
            screen = np.array(pyautogui.screenshot(region=region))
            #screen = np.array(screen)

            # Convert the captured image to grayscale
            gray = cv2.cvtColor(screen,cv2.COLOR_BGR2GRAY)

            # Detect edges in the grayscale image
            #edges = cv2.Canny(gray,50,150)
            edges = cv2.Canny(gray,200,500)

            # Find contours in edge image
            contours,_=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

            # Find contour with largest area
            largest_contour=max(contours,key=cv2.contourArea)

            # Find minimum area rectangle that fits contour
            rect=cv2.minAreaRect(largest_contour)

            # Check if rectangle is square based on shape_tolerance value 
            if abs(1 - rect[1][0] / rect[1][1]) < shape_tolerance:
                #print("Square")
                area = int(rect[1][0] * rect[1][1])
                if 2800 <= area <= 2960:
                    #return 1
                    print(f"Area: {area}")
            #else:
                #print("Rectangle")

            # Find four corner points of rectangle 
            box=cv2.boxPoints(rect)
            box=np.int0(box)

            # Draw rectangle on original image 
            cv2.drawContours(screen,[box],0,(0,0,255),2)

            # Open window at (-100, 0) and auto update
            cv2.imshow("Largest Square", screen)
            cv2.moveWindow("Largest Square", -140, 0)
            cv2.imshow("edges", edges)
            cv2.moveWindow("edges", -280, 0)
            cv2.waitKey(1)

        except ValueError:
            print("No rectangle visible.")
            #break

    cv2.destroyAllWindows()



find_lvl()
