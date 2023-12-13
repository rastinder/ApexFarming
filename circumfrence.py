import cv2
import numpy as np
import keyboard
import mss
import time
from pyautogui import *
import pyautogui

time.sleep(2)
# Function to locate the circle in the image
def locate_circle(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use the HoughCircles function to detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

    # Check if any circles were found
    if circles is not None:
        # Get the first circle detected
        circle = circles[0][0]
        x, y, r = circle
        cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 0), 2)
        cv2.imshow("Circle Detection", img)
        cv2.waitKey(1)
        return circle
    else:
        print("Circle not found")
        return None

# Function to locate the circumference in the image
def locate_circumference(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use the Canny function to detect edges in the image
    edges = cv2.Canny(gray, 50, 150)

    # Use the HoughLinesP function to detect lines in the image
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    # Check if any lines were found
    if lines is not None:
        # Get the first line detected
        line = lines[0][0]
        x1, y1, x2, y2 = line
        circumference = np.array([[x1, y1], [x2, y2]])
        cv2.drawContours(img, [circumference], 0, (0, 255, 0), 2)
        cv2.imshow("Circumference Detection", img)
        cv2.waitKey(1)
        return line
    else:
        print("Circumference not found")
        return None

# Function to move the circle to the center of the captured image
def move_circle_to_center(circle, center):
    # Get the x and y coordinates of the center of the circle
    x, y = circle[0], circle[1]

    # Calculate the difference between the x and y coordinates of the circle and the center
    x_diff = x - center[0]
    y_diff = y - center[1]

    # Check if the x-coordinate of the circle needs to be adjusted
    if x_diff > 0:
        keyboard.press_and_release("a")
    elif x_diff < 0:
        keyboard.press_and_release("d")

    # Check if the y-coordinate of the circle needs to be adjusted
    if y_diff > 0:
        keyboard.press_and_release("w")
    elif y_diff < 0:
        keyboard.press_and_release("s")

# Function to move the circumference to the center of the captured image
def move_circumference_to_center(circumference, center):
    # Get the x and y coordinates of the first and second points of the line
    x1, y1 = circumference[0], circumference[1]
    x2, y2 = circumference[2], circumference[3]

    # Calculate the center of the line
    x = (x1 + x2) // 2
    y = (y1 + y2) // 2

    # Calculate the difference between the x and y coordinates of the line and the center
    x_diff = x - center[0]
    y_diff = y - center[1]

    # Check if the x-coordinate of the line needs to be adjusted
    if x_diff > 0:
        keyboard.press_and_release("a")
    elif x_diff < 0:
        keyboard.press_and_release("d")

    # Check if the y-coordinate of the line needs to be adjusted
    if y_diff > 0:
        keyboard.press_and_release("w")
    elif y_diff < 0:
        keyboard.press_and_release("s")

# Main loop to capture and process the image
cv2.namedWindow('Circumference Detection', cv2.WINDOW_NORMAL)
cv2.namedWindow('Circle Detection', cv2.WINDOW_NORMAL)
cv2.moveWindow('Circumference Detection', -1920, 0)
cv2.moveWindow('Circle Detection', -1920, 310)

with mss.mss() as sct:
    # Set the monitor to capture
    monitor = {"top": 49, "left": 49, "width": 242, "height": 242}
    #while True:
    while pyautogui.locateOnScreen('InGame.png', region=(10,1028,680,1080), grayscale=True, confidence=0.9) != None:
        print("in")
        # Get the raw image data
        img = np.array(sct.grab(monitor))

        # Locate the circle in the image
        circle = locate_circle(img)

        # Check if a circle was found
        if circle is not None:
            move_circle_to_center(circle, (img.shape[1] // 2, img.shape[0] // 2))
        else:
            # Locate the circumference in the image
            circumference = locate_circumference(img)

            # Check if a circumference was found
            if circumference is not None:
                move_circumference_to_center(circumference, (img.shape[1] // 2, img.shape[0] // 2))
            else:
                print("Neither circle nor circumference found")

   
