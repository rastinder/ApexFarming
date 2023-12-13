import keyboard
import pynput.mouse
import torch
import mss
import numpy as np
import cv2
#import win32con
#import win32gui
import os


class YoloAimbot:
    def __init__(self):
        self.model = torch.hub.load(r'yolo_aimbot\\yolov5-master', 'custom', path=r'yolo_aimbot\\apexSt1.pt', source='local')


    def capture_screen(self):
        sct = mss.mss()
        screen_width = 1920
        screen_height = 1080
        GAME_LEFT, GAME_TOP, GAME_WIDTH, GAME_HEIGHT = screen_width // 3, screen_height // 3, screen_width // 3, screen_height // 3  # 游戏内截图区域
        monitor = {
            'left': GAME_LEFT,
            'top': GAME_TOP,
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT
        }
        img = np.array(sct.grab(monitor))
        return img

    def detect_objects(self, img):
        results = self.model(img, size=640)
        df = results.pandas().xyxy[0]
        return df

    def draw_objects(self, img, df):
        try:
            xmin = int(df.iloc[0, 0])
            ymin = int(df.iloc[0, 1])
            xmax = int(df.iloc[0, 2])
            ymax = int(df.iloc[0, 3])
            head_level = (int(xmin + (xmax - xmin) / 2), int(ymin + (ymax - ymin) / 8))
            cv2.circle(img, head_level, 4, (0, 255, 0), thickness=-1)
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            distance = (head_level[0] - 320, head_level[1] - 320)
            return img, distance
        except:
            return img, None

    def display_image(self, img, window_name='test', resize_width=480, resize_height=270):
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, resize_width, resize_height)
        cv2.imshow(window_name, img)
        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC
            cv2.destroyAllWindows()
            exit('ESC ...')

    def print_box_coordinates(self, df):
        try:
            xmin = int(df.iloc[0, 0])
            ymin = int(df.iloc[0, 1])
            xmax = int(df.iloc[0, 2])
            ymax = int(df.iloc[0, 3])
            print("Box Coordinates:")
            print(f"Top-left: ({xmin}, {ymin})")
            print(f"Bottom-right: ({xmax}, {ymax})")
        except:
            pass
            #print("No objects detected.")

    def print_center_coordinates(self, df):
        try:
            xmin = int(df.iloc[0, 0])
            ymin = int(df.iloc[0, 1])
            xmax = int(df.iloc[0, 2])
            ymax = int(df.iloc[0, 3])
            center_x = int(xmin + (xmax - xmin) / 2)
            center_y = int(ymin + (ymax - ymin) / 2)
            print("Center Coordinates:")
            print(f"Center: ({center_x}, {center_y})")
        except:
            pass
            #print("No objects detected.")

    def return_box_coordinates(self, df):
        try:
            xmin = int(df.iloc[0, 0])
            ymin = int(df.iloc[0, 1])
            xmax = int(df.iloc[0, 2])
            ymax = int(df.iloc[0, 3])
            print("Box Coordinates:")
            print(f"Top-left: ({xmin}, {ymin})")
            print(f"Bottom-right: ({xmax}, {ymax})")
        except:
            pass
            #print("No objects detected.")

    def return_center_coordinates(self, df):
        try:
            xmin = int(df.iloc[0, 0])
            ymin = int(df.iloc[0, 1])
            xmax = int(df.iloc[0, 2])
            ymax = int(df.iloc[0, 3])
            center_x = int(xmin + (xmax - xmin) / 2)
            center_y = int(ymin + (ymax - ymin) / 2)
            return center_x, center_y
        except:
            pass
            #print("No objects detected.")

    def yolo_full(self, frame):
        df = self.detect_objects(frame)
        #img, distance = self.draw_objects(frame, df)
        #self.display_image(img)
        return self.return_center_coordinates(df)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__)) #+ "\\yolo_aimbot"
    os.chdir(script_dir)
    yolo = YoloAimbot()
    while True:
        img = yolo.capture_screen()
        df = yolo.detect_objects(img)
        img, distance = yolo.draw_objects(img, df)
        yolo.display_image(img)
