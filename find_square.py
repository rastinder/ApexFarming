import cv2
import numpy as np
import pyautogui

def find_lvl(shape_tolerance=0.1):
    region = (790, 115, 85, 85)

    while True:
        screen = np.array(pyautogui.screenshot(region=region))
        gray = cv2.cvtColor(screen,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,200,500)
        contours,_=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        largest_contour=max(contours,key=cv2.contourArea)
        rect=cv2.minAreaRect(largest_contour)

        if abs(1 - rect[1][0] / rect[1][1]) < shape_tolerance:
            area = int(rect[1][0] * rect[1][1])
            if 2800 <= area <= 2960:
                return 1
find_lvl()