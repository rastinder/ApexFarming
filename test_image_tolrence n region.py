import pyautogui
import cv2
import numpy as np
import clipboard
import time
import sys

time.sleep(0)
# locate the image
image = 'ea_login.png'
#image = 'download.png'
tolerance = 1
ea_login = pyautogui.locateOnScreen(image, grayscale=True, confidence=tolerance)

# increase tolerance by 0.05 and search again if the image is not found
while ea_login is None:
    tolerance -= 0.01
    if tolerance < 0.2:
        break
    ea_login = pyautogui.locateOnScreen(image, grayscale=True, confidence=tolerance)
tolerance -= 0.05
tolerance = round(tolerance, 2)
if tolerance < 0.2:
    print("error")
    sys.exit(0)
# print the area with a 5-pixel margin where the image is found
if ea_login is not None:
    x, y, w, h = ea_login
    print("Area with 50 pixel margin:", x-50,",", y-50,",", w+100,",", h+100)
    
    # print the center of the found image n cofidence
    center = (x + w//2, y + h//2)
    print("Center:", center)
    print("cofidence:", tolerance)
    # print code to copy
    if pyautogui.locateOnScreen(image, grayscale=True,region=(x-5, y-5, w+10, h+10), confidence=tolerance)  != None:
        cc = f"#click on {image}\nwait_and_click_on_image('{image}', ({x-5}, {y-5}, {w+10}, {h+10}), {tolerance})\n"
        print(f"if image('{image}', ({x-5}, {y-5}, {w+10}, {h+10}), {tolerance}):\n")
        #print( f"pyautogui.locateOnScreen('{image}', grayscale=True,region=({x-5}, {y-5}, {w+10}, {h+10}), confidence={tolerance})  != None:\n")
        print(f"pyautogui.locateOnScreen('{image}', grayscale=True,region=(0, 0, 1920, 1080), confidence={tolerance})  != None:")
        print(cc)
        
        clipboard.copy(cc)
    else:
        print("not working")
    # display the area in cv2.imshow
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    cv2.imshow("EA Login", screenshot[y-5:y+h+5, x-5:x+w+5])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # move mouse to center of found image
    pyautogui.click(center)
else:
    print("Image not found on screen")