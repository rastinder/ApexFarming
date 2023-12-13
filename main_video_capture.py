# in case script stoped for an hour its recommended to close apex.
import threading
import time
import requests
import subprocess
import pyautogui
from PIL import Image

# import keyboard
#import pydirectinput
import cv2
import numpy as np
import os
import sys
import random
import io
import GPUtil
import ctypes
import math
from tcp_client import TCPClient
import asyncio
import multiprocessing
import val_full
import recieve_frame_class as ndi
from multiprocessing import Value
from yolov5_frameprocess import YoloAimbot


class MouseInputs:
    def __init__(self, qt):
        self.qt = qt
        self.user = os.environ["USERNAME"]

    def moveTo(self, x, y):
        self.qt.put(f"{self.user},4,{x}, {y}")

    def mouseClick(self, x=0, y=0):
        self.qt.put(f"{self.user},2,{x}, {y}")

    def mouseDown(self, x=0, y=0):
        self.qt.put(f"{self.user},5,{x}, {y}")

    def mouseUp(self, x=0, y=0):
        self.qt.put(f"{self.user},1,{x}, {y}")


class KeyboardInputs:
    def __init__(self, qt):
        self.qt = qt

    def press_and_release(self, key):
        # Press and release the specified key
        key = f"key,{key},0"
        val_full.wasd(key, val_full.aimbot, self.qt)

    def press(self, key):
        # Press the specified key
        key = f"key,{key},down"
        val_full.wasd(key, val_full.aimbot, self.qt)

    def release(self, key):
        # Release the specified key
        key = f"key,{key},up"
        val_full.wasd(key, val_full.aimbot, self.qt)


class WebcamCapture_SHIT:
    def __init__(self):
        self.video_sources = self.get_video_sources()
        self.frame = None
        self.is_running = False
        self.lock = threading.Lock()

    def start(self):
        self.is_running = True
        threading.Thread(target=self._capture_frames, daemon=True).start()

    def stop(self):
        self.is_running = False

    def _capture_frames(self):
        for source in self.video_sources:
            video_capture = cv2.VideoCapture(source)
            start_time = time.time()

            while time.time() - start_time < 5:
                ret, frame = video_capture.read()
                if ret and not self.is_blank_or_black(frame):
                    # if frame.shape[1] == 1920 and frame.shape[0] == 1080:
                    with self.lock:
                        self.frame = frame
                    print(f"Non-blank frame found from video source: {source}")
                    return

            video_capture.release()

        print("Timeout: No non-blank frame found from any video source")

    def get_frame(self):
        with self.lock:
            return self.frame

    @staticmethod
    def get_video_sources():
        video_sources = []
        for i in range(5):  # Check up to 10 video sources (modify if needed)
            video_capture = cv2.VideoCapture(i)
            if video_capture.isOpened():
                video_sources.append(i)
                video_capture.release()
        return video_sources

    @staticmethod
    def is_blank_or_black(frame):
        # Check if the frame is blank or black (modify the condition if needed)
        return frame.mean() < 5


class WebcamCapture:
    def __init__(self, source=0):
        self.video_capture = cv2.VideoCapture(source)
        self.frame = None
        self.is_running = False
        self.lock = threading.Lock()

    def start(self):
        self.is_running = True
        threading.Thread(target=self._capture_frames, daemon=True).start()

    def stop(self):
        self.is_running = False

    def _capture_frames(self):
        while self.is_running:
            ret, frame = self.video_capture.read()
            if ret:
                with self.lock:
                    self.frame = frame

    def get_frame(self):
        with self.lock:
            return self.frame


class account_handle:
    @staticmethod
    def get_acc_details(mode_to_play):
        try:
            with open("username.txt", "r") as file:
                # Read all lines in the file
                lines = file.readlines()
                # Loop through all lines
                for line in lines:
                    # Split the line into username and password
                    try:
                        user, level = line.strip().split(",")
                        print(user + " : " + level)
                    except:
                        user = line.strip("\n").split(",")
                        level = 0
                    print(line)
                    # Check if "20" is not written after a comma and value is below or equal to 21
                    if level == "wrong_pass":
                        continue
                    elif int(level) <= 19:
                        # Print the first username and password
                        return user[0].split("\t")
                        # username, password = line.strip().split("\t")
        except Exception as e:
            print("no txt file found")
            try:
                user = subprocess.run(
                    ["python", "user.py", "get", mode_to_play],
                    capture_output=True,
                    check=True,
                    timeout=300000,
                )
                result = user.stdout.decode("utf-8").strip().split(" ")
                # user = ["guggumuggu537@gmail.com", "GUGGUmuggu3"]
                print(result)
                return result
            except Exception as e:
                print("lets exit")
                print(e)
                sys.exit("lets exit")

    @staticmethod
    def push_acc_details(username_to_update, level):
        try:
            with open("username.txt", "r") as file:
                # Read all lines in the file
                lines = file.readlines()
            with open("username.txt", "w") as file:
                # Loop through all lines
                for line in lines:
                    # Split the line into username, level, and password
                    user = line.strip().split(",")
                    # Check if the username matches the username_to_update
                    if username_to_update[0] in user[0]:
                        # Update the level of the username
                        file.write(f"{user[0]},{level}\n")
                    else:
                        # Write the line back to the file
                        file.write(line)
                print(f"Level of username {username_to_update} is updated to {level}.")
        except:
            print("Error while updating level of username.")
            result = subprocess.run(
                [
                    "python",
                    "user.py",
                    "push",
                    username_to_update[0],
                    username_to_update[1],
                    level,
                ],
                capture_output=True,
                check=True,
                timeout=3000000,
            )
            print(result)


class TimeoutError(Exception):
    pass


def delay_multiplier():
    print("rnning function delay_multiplier")
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            vram_total = gpu.memoryTotal
            print("vram: ", vram_total)
            if vram_total <= 2049:
                print("2gb ram")
                return 2.5
            elif vram_total <= 4100:
                print("4gb ram")
                return 1
            else:
                print("4+gb ram")
                return 1
    except:
        print("error")
        return 1
    print("error2")
    return 1


def error_handling1():
    # return
    print("error handling start")
    old_times = 0
    click_count = 0
    global common_var
    if old_times == 0:
        # while True:
        # if common_var == 1:
        start_time = time.time()
        while time.time() - start_time < 15 * DelayMultiplier:
            # times = int(30 - (time.time() - start_time))
            # if old_times != times:
            # print(f'error handling remaining time: {times} secs')
            # old_times = times
            if common_var == 1:
                # y
                # print('error handling timer rest')
                start_time = time.time()
                common_var = None
            if image("continue_afk.png", (0, 0, 1920, 1080), 0.94, True):
                start_time2 = time.time()
                while time.time() - start_time2 < 10:
                    if image(
                        "continue_afk.png", (0, 0, 1920, 1080), 0.84, True
                    ) or image("startmanu.png", (810, 599, 300, 103), 0.93, True):
                        click_count = click_count + 1
                        print("click_count: ", click_count)
                        if click_count >= 10:
                            print("needs restart")
                            sys.exit("continue click count exceeded")
                            # send_screen('needs restart')
            # after temp trio challaenge completed comes
            if image("news_windnow.png", (813, 22, 93, 42), 0.94) or image(
                "space_to_skip_matchsummary.png", (875, 900, 51, 112), 0.84
            ):
                keyboard.press("esc")    
                time.sleep(0.05)
                keyboard.release("esc")
                time.sleep(0.05 * DelayMultiplier)
            # click on play_button.png
            if image("play_button.png", (1027, 768, 54, 25), 0.94, True):
                time.sleep(5)
                #wait_and_click_on_image("startmanu.png", (810, 599, 300, 103), 0.93, True, 160)
                start_time = time.time()
        # else:
        # common_var = None


def error_handling():
    global common_var, thread
    # common_var = 1
    # return
    try:
        if not thread.is_alive():
            common_var = None
            thread.start()
        else:
            common_var = 1
    except Exception as e:
        thread = threading.Thread(target=error_handling1)
        thread.start()
        # print(thread.is_alive())
        # print(e)
        # time.sleep(3)


def enforce_time_limit(func, time_limit=5):
    if time_limit is None:
        return func

    def wrapper(*args, **kwargs):
        def inner():
            result = func(*args, **kwargs)
            timer.cancel()
            return result

        timer = threading.Timer(time_limit, raise_timeout)
        timer.start()
        result = inner()
        timer.cancel()
        return result

    def raise_timeout():
        raise TimeoutError(f"{func.__name__} exceeded time limit of {time_limit:.2f}s")

    return wrapper


def send_screen(message="Hi"):
    # fearbot
    bot_token = ""
    chat_id = ""
    # pclogs
    bot_token = ""
    chat_id = ""

    def upload_screenshot():
        # take a screenshot of the current screen
        # screen = pyautogui.screenshot()
        screen = capture_frame()
        #screen = ndicapturefunctions()
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
        image = Image.fromarray(screen)
        # create an in-memory file object to store the screenshot
        screen_buffer = io.BytesIO()
        image.save(screen_buffer, "PNG")
        # rewind the buffer to the beginning
        screen_buffer.seek(0)

        # upload the screenshot file to Telegram and send it as a photo
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        response = requests.post(
            url,
            data={
                "chat_id": chat_id,
                "caption": message + " " + os.environ["USERNAME"],
            },
            files={"photo": ("screenshot.png", screen_buffer, "image/png")},
        )
        # close the buffer and delete the contents to free up memory
        screen_buffer.close()
        del screen_buffer

    # create a new thread to upload the screenshot
    t = threading.Thread(target=upload_screenshot)
    t.start()

    # don't wait for the thread to complete
    return

def get_mouse_position():
    data = display.Display().screen().root.query_pointer()._data
    return data["root_x"], data["root_y"]

def wait_and_click_on_image(
    image_file, region, confidence, click=True, max_wait_time=60
):
    img = None
    already_sent = None
    # confidence = confidence - 0.36
    try:
        x1, y1, x2, y2 = region
        y1 = max(y1 - 30, 0)
        y2 = max(y2 + 30, 1080)
        region = x1, y1, x2, y2
    except Exception as e:
        print(e)
    print("looking for: " + image_file)
    start_time = time.time()
    while img is None:
        frame = capture_frame()
        #frame = ndicapturefunctions()
        # img = yolo.yolo_full(frame)
        try:
            img = pyautogui.center(
                pyautogui.locate(
                    image_file,
                    frame,
                    grayscale=True,
                    region=region,
                    confidence=confidence,
                )
            )
        except TypeError:
            pass
        if (
            time.time() - start_time > (max_wait_time * DelayMultiplier)
            and already_sent == None
        ):
            send_screen(
                "cant find in "
                + str(max_wait_time * DelayMultiplier)
                + " sec "
                + image_file
            )
            already_sent = 1
            return
    if click == True:
        long_click(img[0], img[1])
    return img


def long_click(x, y):
    start_x, start_y = get_mouse_position()
    end_x, end_y = x - start_x, y - start_y
    # wind_mouse(int(end_x), int(end_y))
    # return
    # time.sleep(2)
    # Move the mouse cursor slowly to a specified position (x, y)
    start_x, start_y = get_mouse_position()
    while (x < start_x - 5 or x > start_x + 5) or (y < start_y - 5 or y > start_y + 5):  #x != start_x or y != start_y:
        end_x, end_y = x - start_x, y - start_y

        mouse.moveTo(int(end_x), int(end_y))
        i = 0
        while True:
            time.sleep(0.01)  # Adjust the sleep duration as needed
            new_x, new_y = get_mouse_position()
            if new_x == start_x and new_y == start_y:
                i = i + 1
            else: i = 0
            if i == 30:
                break
            start_x, start_y = get_mouse_position()
    mouse.mouseDown()
    time.sleep(hold_click_time)
    mouse.mouseUp()


def wind_mouse(end_x, end_y):
    start_x, start_y = 0, 0
    x, y = 0, 0
    distance = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)

    # Calculate the maximum distance that the curve can go beyond the end point
    max_excess = distance * 0.02

    # Calculate the number of steps needed to move the mouse along the line
    num_steps = int(distance / 10)

    # Loop through each step and move the mouse
    for i in range(num_steps):
        # Calculate the current position of the mouse along the line
        x = start_x + (end_x - start_x) * (i / num_steps) - x
        y = start_y + (end_y - start_y) * (i / num_steps) - y

        # Add a random offset to the current position
        x += random.uniform(-5, 5)
        y += random.uniform(-5, 5)

        # If the current position is beyond the end point, adjust it
        if i == num_steps - 1:
            excess = math.sqrt((x - end_x) ** 2 + (y - end_y) ** 2)
            if excess > max_excess:
                x -= (excess - max_excess) * (x - end_x) / excess
                y -= (excess - max_excess) * (y - end_y) / excess
        mouse.moveTo(int(x), int(y))
        time.sleep(0.01)


def webcapturefunctions():
    if webcam_capture is not None:
        return webcam_capture.get_frame()
def ndicapturefunctions():
    return ndi_receiver.receive_frames()
def capture_frame():
    return ndicapturefunctions()
    return
    while True:

                cap = cv2.VideoCapture(4)
                check,frame = cap.read()
                frame = cv2.resize(frame, (1920, 1080))
                print("Frame resolution:", frame.shape)
                cv2.imshow('Webcam', frame)
                cv2
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to find the next source
                        break
                #return frame
    #webcapturefunctions()
    #ndicapturefunctions()



def image(image_file, region, confidence, click=False, debug_msg=True):
    img = None

    try:
        # x1 y1 , x1+ length, y1 + breadth
        x1, y1, x2, y2 = region
        y1 = max(y1 - 30, 0)
        y2 = min(y2 + 30, 1070)
        region = (x1, y1, x2, y2)
    except Exception as e:
        print(e)
    frame = capture_frame()
    #frame = ndicapturefunctions()
    # img = yolo.yolo_full(frame)
    print("looking for: " + image_file)
    try:
        img = pyautogui.center(
            pyautogui.locate(
                image_file, frame, grayscale=True, region=region, confidence=confidence
            )
        )
    except TypeError:
        return None
    if img is not None:
        if click:
            long_click(img[0], img[1])
            print("clicked: " + image_file)
        if debug_msg:
            print("located: " + image_file)
        return img

    return None


def what_is_on_screen():
    print(f"Running function: what_is_on_screen")
    if image("in_mainmenu.png", (1807, 962, 70, 66), 0.94):
        return "in_mainmenu"
    if image("InGame.png", (500, 1031, 30, 27), 0.94, False) != None:
        return "InGame"
    else:
        return "desktop"


def openaccounts(mode_to_play):
    if platform == "ea":
        print("running ea platform")
        # get username passowrd
        username, password = account_handle.get_acc_details(mode_to_play)
        # run ea app
        subprocess.run(
            [
                "C:\\Program Files\\Electronic Arts\\EA Desktop\\EA Desktop\\EALauncher.exe"
            ],
            shell=True,
        )
        # open ea account
        run_ea(username, password)  # return pid or none
        return username, password
    elif platform == "steam":
        # get username passowrd
        username, password = account_handle.get_acc_details(mode_to_play)
        # open steam account
        run_steam(username, password)  # return pid or none
        return username, password

    else:
        print("wrong platform selected")


def run_steam(username, password):
    print(f"Running function: run_steam")
    subprocess.run(
        [
            "C:\\Program Files (x86)\\steam\\steam.exe app -novid -dev applaunch - login ",
            username,
            password,
            "-fps 20",
        ],
        shell=True,
    )
    return "in_game"


def run_ea(username, password):
    skip_video = False  # if we are  playing first time then we need to skip video but its irrelevent as we have to  play tut manually
    print(f"Running function: run_ea")
    wait_and_click_on_image("ea_login.png", (754, 432, 56, 26), 0.80)
    time.sleep(1)
    keyboard.press_and_release(username)
    wait_and_click_on_image("enter_pass.png", (755, 516, 89, 22), 0.94, False)
    keyboard.press_and_release("tab")
    keyboard.press_and_release(password)
    image("keep_sign_in_check.png", (748, 604, 46, 43), 0.94, True)
    time.sleep(0.3)

    keyboard.press_and_release("enter")
    time.sleep(3)  # remove if you dont want
    start_time = time.time()
    while time.time() - start_time < 300 * DelayMultiplier:
        if image("wrong_pass.png", (879, 588, 75, 25), 0.94):
            print("wrong pass")
            account_handle.push_acc_details(
                account_handle.get_acc_details(mode_to_play), "wrong_pass"
            )
            kill_ea()
            openaccounts(mode_to_play)
            return "in_game"
        elif image("technical_diffcuilty.png", (975, 591, 77, 23), 0.94):
            print("technical_diffcuilty pass")
            account_handle.push_acc_details(
                account_handle.get_acc_details(mode_to_play), "technical_diffcuilty"
            )
            kill_ea()
            send_screen("techincal diffcuilty " + username + " " + password)
            time.sleep(86400)  # full day
            os.system("reboot")
            # openaccounts(mode_to_play)
            return "in_game"
        elif image("apex_icon_afterlogin.png", (293, 305, 77, 251), 0.9):
                break
        elif image("ban.png", (1007, 392, 99, 35), 0.94):
            print("ban")
            account_handle.push_acc_details(
                account_handle.get_acc_details(mode_to_play), "ban"
            )
            kill_ea()
            openaccounts(mode_to_play)
            return "in_game"
        elif image("ok_loginfailed.png", (1128, 517, 147, 129), 0.94):
            send_screen("some kind of error")
            kill_ea()
            openaccounts(mode_to_play)
            return "in_game"
        elif (image("new_acc_cross.png", (0, 240, 1920, 270), 0.94)) or (image("ea_afterlogon_window.png", (940, 108, 39, 31), 0.94) and time.time() - start_time > 25):
            cross_check_timer = time.time()

            print("we will be insalling apex now time =", time.time() - start_time)
            while time.time() - cross_check_timer < 6 * DelayMultiplier:
                if image("new_acc_cross.png", (0, 240, 1920, 270), 0.94, True):
                    skip_video = True
                    break
            print("type apex")
            image("searchbox.png", (658, 173, 58, 25), 0.94, True)
            keyboard.press_and_release("apex")
            keyboard.press("enter")
            time.sleep(0.03)
            keyboard.release("enter")
            # click on install_apex_in_lib.png
            img = wait_and_click_on_image(
                "install_apex_in_lib.png", (483, 431, 92, 27), 0.94, False
            )
            long_click(img[0] + 60, img[1] + 60)
            # wait_and_click_on_image('download.png', (978, 743, 102, 29), 0.94)
            while image("next.png", (1064, 696, 67, 33), 0.94, False) == None:
                image("download.png", (978, 743, 102, 51), 0.94, True)
                if image("network_error.png", (1238, 166, 75, 32), 0.94):
                    send_screen("network_error, sad")
                    time.sleep(5)
                    os.system("shutdown /r /t 1")
                    sys.exit()
                if image("play_button.png", (976, 752, 122, 54), 0.92):
                    break
            while image("play_button.png", (976, 752, 122, 54), 0.92) is None:
                # missing next button
                # its a hiidden next button
                img = image("next.png", (1064, 696, 67, 33), 0.94, False)
                if image("manage.png", (874, 752, 114, 54), 0.80):
                    break
                while image("next.png", (1064, 696, 67, 33), 0.94, True):
                    time.sleep(1)  # its a hiidden next button
                if image("play_button.png", (976, 752, 122, 54), 0.92):
                    break
                try:
                    long_click(img[0], img[1])
                    break
                except:
                    print("IMG next not found")
    else:
        print("different kind of problem")
        # send_screen("looking for: apex screen that is now found")

    # click on apex_icon_afterlogin.png
    wait_and_click_on_image("apex_icon_afterlogin.png", (293, 305, 77, 151), 0.94)
    while image("play_button.png", (976, 752, 122, 54), 0.92) is None:
        if image("update_game.png", (966, 759, 128, 42), 0.83, True):
            print("updating")
            # click on continue_update.png
            wait_and_click_on_image("continue_update.png", (1015, 679, 123, 41), 0.83)
            time.sleep(5)
        elif image("manage.png", (874, 752, 114, 54), 0.80):
            break
    '''''
    # click on viewproperties.png
    while image("viewproperties.png", (887, 790, 153, 50), 0.94, True) is None:
        # click on manage.png
        wait_and_click_on_image("manage.png", (874, 752, 114, 54), 0.80)
        time.sleep(0.36)
    '''''
    print('start manage')
    while image("properties.png", (737, 307, 111, 34), 0.94, False) is None:
        if image("viewproperties.png", (887, 790, 153, 50), 0.94, True) is None:
            time.sleep(.2)
            image("manage.png", (874, 752, 114, 54), 0.80,True)
            time.sleep(.5)
        time.sleep(.5)
        
    # click on properties.png
    wait_and_click_on_image("properties.png", (737, 307, 111, 34), 0.94, False)
    if image("typearg.png", (675, 551, 573, 150), 0.94, True):
        time.sleep(0.02)
        keyboard.press_and_release("-dev -novid")
        time.sleep(0.05)
    # click on save_arg.png
    wait_and_click_on_image("save_arg.png", (1051, 743, 93, 55), 0.91)
    time.sleep(0.06)
    # click on play_button.png
    wait_and_click_on_image("play_button.png", (976, 752, 122, 54), 0.92)
    cloudsync_Fix()

    wait_and_click_on_image("loading_screen.png", (0, 0, 1920, 1080), 0.91, False)
    # click on startmanu.png
    wait_and_click_on_image(
        "startmanu.png", (810, 599, 300, 103), 0.93, True, 160
    )  # change pic so retry te v click kre
    image("startmanu.png", (810, 599, 300, 103), 0.93, True)
    while image("video_skip.png", (825, 417, 271, 76), 0.86):
        time.sleep(0)
    if skip_video == False:
        start_time = time.time()
        while time.time() - start_time < (3 * DelayMultiplier):
            if image("black_screen_loading.png", (1770, 949, 26, 52), 0.94):
                break
        else:
            skip_video = True
    """''
    if skip_video == False:
        start_time = time.time()
        while image('in_mainmenu.png', (1807, 962, 70, 66), 0.94, False) is None:
            if time.time() - start_time > (5*DelayMultiplier):
                skip_video = True
                break
        else:
            print('main menu yeeeeeee')
    """
    if skip_video == True:
        print(time.time() - start_time)
        print("skip video")
        pyautogui.keyDown("alt")
        time.sleep(0.01)
        pyautogui.keyDown("F4")
        time.sleep(0.015)
        pyautogui.keyUp("F4")
        pyautogui.keyUp("alt")
        wait_and_click_on_image("play_button.png", (976, 752, 122, 54), 0.92)
        start_time = time.time()
        while time.time() - start_time < 2 * DelayMultiplier:
            if image("launch_game.png", (992, 590, 124, 28), 0.94, True):
                break
            if image("cloud_save.png", (691, 497, 45, 42), 0.94, True):
                wait_and_click_on_image(
                    "confirm_cloudsave_window.png", (1040, 685, 92, 29), 0.94
                )
                wait_and_click_on_image("yes_cloud_save.png", (988, 590, 123, 30), 0.94)
        wait_and_click_on_image("startmanu.png", (810, 599, 300, 103), 0.93, True, 160)
        time.sleep(0.21)
        image("startmanu.png", (810, 599, 300, 103), 0.93, True)
        while image("video_skip.png", (825, 417, 271, 76), 0.86):
            time.sleep(0)
        start_time = time.time()
        while time.time() - start_time < (3 * DelayMultiplier):
            if image("black_screen_loading.png", (1770, 949, 26, 52), 0.94):
                start_time = time.time()
    print("in game")
    return "in_game"

def clcckonmanage():
    return
        
def cloudsync_Fix():
    # wait for loading screen or launch_game error due to sync
    start_time = time.time()
    while time.time() - start_time < 4:
        print("launch game or cloud save")
        if image("launch_game.png", (992, 590, 124, 28), 0.94, True):
            break
        if image("cloud_save.png", (691, 497, 45, 42), 0.94, True):
            wait_and_click_on_image(
                "confirm_cloudsave_window.png", (1040, 685, 92, 29), 0.94
            )
            wait_and_click_on_image("yes_cloud_save.png", (988, 590, 123, 30), 0.94)


def find_lvl(shape_tolerance=0.1):
    region = (792, 117, 83, 83)

    while True:
        frame = capture_frame()
        #frame = ndicapturefunctions()
        screen = frame[
            region[1] : region[1] + region[3], region[0] : region[0] + region[2]
        ]
        # cv2.imshow('jatt', screen)
        # cv2.waitKey(0)
        # screen = np.array(pyautogui.screenshot(region=region))
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 200, 500)
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        try:
            largest_contour = max(contours, key=cv2.contourArea)
        except:
            print("rect bot found")
            return
        try:
            rect = cv2.minAreaRect(largest_contour)
            if abs(1 - rect[1][0] / rect[1][1]) < shape_tolerance:
                area = int(rect[1][0] * rect[1][1])
                if 2800 <= area <= 2960:
                    # image send function here
                    return 1
                print("lvl not found", area)
        except:
            print("rect is not square")
        return


def lvl_pic():
    screenshot_path = os.path.join("extra", pc_username + "_lvl_pic.png")
    pyautogui.screenshot(region=(806, 140, 54, 30)).save(screenshot_path)


# mode_to_play = 'find_arenas_match.png' / 'must_play_trios.png' / 'find_tdm.png' / control.png
# if image('select_control.png', (950, 777, 147, 35), 0.94):
# if image('control.png', (59, 833, 112, 32), 0.94):
# if image('gunrun.png', (62, 836, 109, 27), 0.94):
# if image('select_gunrun.png', (957, 777, 133, 34), 0.94):


def set_everything_before_match(q=None):
    print(f"Running function: set_everything_before_match")
    checks = []
    global mode_to_play
    while (
        image("in_mainmenu.png", (1807, 962, 70, 66), 0.94, False) is None
    ):  # esc or continue
        error_handling()
        if image("exit_to_desktop.png", (860, 606, 198, 35), 0.94):
            keyboard.press_and_release("esc")
    error_handling()

    start_time = time.time()
    # need something robust; lvl 19 di pic lelo te odo hi activate hove jdo lvl 19 disse
    while time.time() - start_time < 8 * DelayMultiplier:
        if find_lvl():
            print("lvl found")
            time.sleep(0.1)
            break
        if image("training.png", (58, 834, 128, 31), 0.94):
            checks.append("lvl_ok")
            checks.append("training.png")
            checks.append("ready_state")
            return checks
    else:
        print("lvl not found in time")

    if image("tut_press_e_to_revive.png", (809, 139, 50, 35), 0.94) or image(
        "select_button.png", (100, 935, 302, 78), 0.94
    ): #  replace tut_press_e_to_revive with lvl_50 testing
        lvl_pic()
        return "lvl_20"
    else:
        checks.append("lvl_ok")
    # check if its first game as TDM is available after 3 matches
    # assuming we will only play arena or tdm if we desided to play other modes permanently then we need to make another check where we will check if trios is present as well
    # we think it doesnt find match and fill.png isnt visible even though it is supposed to so we added canceled match count to skip this
    if image("training.png", (58, 834, 128, 31), 0.94):
        checks.append("training.png")
        checks.append("ready_state")
        return checks
    elif (
        image("fill.png", (83, 662, 60, 34), 0.94, False) is None
        and cant_find_match < 2
        and image("trios.png", (55, 833, 84, 31), 0.94)
    ):
        checks.append("temp_trio")
    elif (
        image("fill.png", (83, 662, 60, 34), 0.94, False) is None
        and mode_to_play != "training.png"
        and cant_find_match < 2
    ):
        checks.append("find_tdm.png")
    elif mode_to_play != "training.png":
        print("changing mode")
        # click on changemode.png
        # some times a pop up window appear so we need to fix thatand cant_find_match < 2
        wait_and_click_on_image("changemode.png", (348, 833, 63, 61), 0.92, True)
        wait_and_click_on_image(
            "select_a_game_mode_window.png", (702, 27, 114, 36), 0.94, False
        )
        time.sleep(0.01 * DelayMultiplier)
        long_click(1031, 500)
        start_time = time.time()
        while time.time() - start_time < 5:
            if image("playlist_unavailable.png", (1000, 632, 126, 30), 0.94):
                return "False"
            if image("ready_state.png", (161, 951, 141, 41), 0.94):
                checks.append("find_tdm.png")
                checks.append("ready_state")
                return checks
        else:
            long_click(1031, 500)
            time.sleep(0.2 * DelayMultiplier)
            if image("ready_state.png", (161, 951, 141, 41), 0.94):
                checks.append("find_tdm.png")
                checks.append("ready_state")
                return checks
    elif mode_to_play == "training.png":
        # if mode_to_play is traing then we only do traing and so we return , in future we can do traingin on the go then checks.append('training.png') will pe present
        return "training_done"

    if image("ready_state.png", (161, 951, 141, 41), 0.94):
        checks.append("ready_state")
    else:
        print("ready state not found take a ss")
        return "False"
    return checks


def click_ready():
    if image("ready_state.png", (161, 951, 141, 41), 0.94, True):
        start_time = time.time()
        while True:
            if time.time() - start_time < DelayMultiplier * 2:
                if image(
                    "cancel_means_searching_for_match.png",
                    (147, 951, 171, 43),
                    0.90,
                    False,
                ):
                    break
            else:
                print("cant find cancel_means_searching_for_match")
                error_handling()
                time.sleep(0.5 * DelayMultiplier)
                image("ready_state.png", (161, 951, 141, 41), 0.94, True)
                start_time = time.time()


def search_match():
    print(f"Running function: search_match")
    if image("fill.png", (83, 662, 60, 34), 0.94):
        return "False"

    # click on ready_state.png
    lvl_pic()
    click_ready()

    start_time = time.time()
    while (
        image(
            "cancel_means_searching_for_match.png",
            (147, 951, 171, 43),
            0.90,
            False,
            False,
        )
        != None
    ):
        if (time.time() - start_time) > 1800:
            send_screen("no match found in 30 mins possible ban")
            start_time = time.time()
    print("cancel button gone so either in match or got auto canceled")
    time.sleep(2 * DelayMultiplier)
    global cant_find_match
    if image("ready_state.png", (161, 951, 141, 41), 0.9, False):
        # increase 1 num each time match isnt found contiuely
        cant_find_match = cant_find_match + 1
        print(f"cant_find_match count = {cant_find_match}")
        return "False"  # ek war trios mode lag gea so false return kita because dubara arena select krna c
    cant_find_match = 0
    update_status("active")
    error_handling()
    return "match_found"


def wasd(action=1):
    def sub_wasd():
        keyboard.press("w")
        time.sleep(0.6)
        keyboard.press_and_release("shift")
        time.sleep(0.1)
        keyboard.press("ctrl")
        time.sleep(1)
        keyboard.release("w")
        keyboard.release("ctrl")

    if action == 1:
        t = threading.Thread(target=sub_wasd)
        t.start()


def move_mouse():
    def sub_move_mouse():
        start_time = time.time()
        sec_run = random.uniform(1.1, 2)
        while (time.time() - start_time) < sec_run:
            ctypes.windll.user32.mouse_event(
                0x0001,
                random.choice([random.randint(-20, -10), random.randint(10, 20)]),
                random.choice([random.randint(-3, -0), random.randint(0, 3)]),
                0,
                0,
            )

    t = threading.Thread(target=sub_move_mouse)
    t.start()


def long_click_random():
    def sub_long_click():
        sec_run = random.uniform(0.5, 2)
        mouse.mouseDown()
        time.sleep(sec_run)
        mouse.mouseUp()

    t = threading.Thread(target=sub_long_click)
    t.start()


def aimEnemy(x, mouse):
    x, y = x[0] - 960, x[1] - 530  # x,y = int(x[0] - 960), int(x[1] -530)
    if x < 15:
        mouse.mouseClick(x, 0)
    else:
        mouse.moveTo(x,0)


def run_aimbot(apexaimloop, mouse):
    yolo = YoloAimbot()
    # ndi.start_capture()
    computer_name = os.environ["COMPUTERNAME"]
    # computer_name = "HOG"
    ndi_receiver = ndi.NDIReceiver(computer_name)
    if ndi_receiver.initialize():
        print("connection found")
    print("find frame")
    '''''
    while True:
        try:
            tframe = ndi_receiver.receive_frames()
            if tframe.shape:
                break
                print(tframe.shape)
                tframe = tframe[340:740, 80:1840]
                cv2.imshow("frame", tframe)
                cv2.waitKey(1)
        except:
            pass
    '''''
    while True:
        if apexaimloop.value == 1:
            frame = capture_frame()
            #frame = ndi_receiver.receive_frames()
            try:
                screen = frame[340:740, 80:1840]
                img = yolo.yolo_full(screen)
                if img:
                    print("enemy found")
                    aimEnemy(img, mouse)
            except:
                pass
            time.sleep(0.15)


def run_walkbot(apexaimloop=0):
    print(f"Running function: run_walkbot")
    loadout_selection = 1
    in_game = False
    key_press = False
    start_time = time.time()
    kkeys = [
        "w",
        "w",
        "w",
        # long_click_random,
        # move_mouse,
        "a",
        # "s",
        "d",
        "Spacebar",
        "ctrl",
        "shift",
        "2",
        "1",
        "q",
        "r",
        "e",
        "z",
        wasd,
    ]
    while True:  # add server error etc etc
        while image("InGame.png", (500, 1031, 30, 27), 0.94, False, False) != None:
            # circumfrence
            in_game = True
            apexaimloop.value = 1  # testing
            if key_press == False:
                kkey = random.choice(kkeys)
                if callable(kkey):
                    try:
                        kkey()
                    except:
                        print(kkeys)
                else:
                    if kkey == "Spacebar" or kkey == "ctrl":
                        keyboard.press_and_release(kkey)
                    keyboard.press(kkey)
                start_time = time.time()
                key_press = True
            elif time.time() - start_time >= 3 and key_press == True:
                if not callable(kkey):
                    keyboard.release(kkey)
                key_press = False
                apexaimloop.value = 0
        else:
            apexaimloop.value = 0
            if key_press == True:
                if not callable(kkey):
                    keyboard.release(kkey)
                key_press = False
            if in_game == False:
                image("esc_before_first_tdm.png", (904, 886, 48, 33), 0.8, True)
            if image('joined_match_in_progress.png', (771, 993, 91, 38), 0.9):
                image('chick_char.png', (433, 710, 69, 77), 0.9, True)
                time.sleep(.2)
                image('elephant_char.png', (715, 846, 82, 84), 0.89, True)
                time.sleep(.2)
            if image("select_spawn_window.png", (1080, 948, 28, 25), 0.94):
                image("click_for_control.png", (0, 0, 1920, 1080), 0.84, True)
                time.sleep(10)
            error_handling()
        # or image('match_quality_survey_yes.png', (0, 0, 1920, 1080), 0.94):
        if image("match_summary.png", (609, 16, 800, 70), 0.94) or image(
            "space_to_skip_matchsummary.png", (875, 980, 51, 22), 0.85
        ):  # 875, 980, 51, 21
            # press_esc_to_leave_match()
            return "match_finished"
        # if mode_to_play == 'find_tdm.png':
        if 1 > 0:  # always true check
            if image("game_over_tdm_trio.png", (902, 1019, 112, 53), 0.94, False):
                press_esc_to_leave_match()
                return "match_finished"
            if loadout_selection:
                if image("select_loadout_in_dm.png", (254, 316, 40, 27), 0.94, True):
                    #image("select_loadout_in_dm.png", (254, 316, 40, 27), 0.94, True)
                    loadout_selection = 0

        if image("ready_state.png", (161, 951, 141, 41), 0.9, False):
            print("run function wich ready show ho gea strange")
            return "False"  # ek war trios mode lag gea so false return kita because dubara arena select krna c


def press_esc_to_leave_match():
    print(f"Running function: press_esc_to_leave_match")
    keyboard.press("esc")
    time.sleep(0.05)
    keyboard.release("esc")
    print("esc pressed")
    start_time = time.time()
    while True:
        if time.time() - start_time < (1.5 * DelayMultiplier):
            # click on leave_match.png
            if image("leave_match.png", (881, 610, 159, 27), 0.86, True):
                wait_and_click_on_image(
                    "Yes_leave.png", (821, 660, 56, 74), 0.94, True, 2
                )
                image("Yes_leave.png", (821, 660, 56, 74), 0.94, True)
                time.sleep(5 * DelayMultiplier)
                print("sleep end so break")
                break
        else:
            if image("in_mainmenu.png", (1807, 962, 70, 66), 0.93, False):
                return
            keyboard.press("esc")
            time.sleep(0.05)
            keyboard.release("esc")
            start_time = time.time()
            print("esc pressed again")
            if image("in_mainmenu.png", (1807, 962, 70, 66), 0.93, False):
                return
            error_handling()
            if image("in_mainmenu.png", (1807, 962, 70, 66), 0.93, False):
                return


def end_match(playing=None):
    ban_check = 0
    if playing == "temp_trio":
        print(f"Running function: end_match")
        wait_and_click_on_image(
            "waitingforplayers.png", (801, 362, 306, 28), 0.94, False
        )
        press_esc_to_leave_match()
        while image("in_mainmenu.png", (1807, 962, 70, 66), 0.93, False) == None:
            keyboard.press("esc")
            time.sleep(0.05)
            keyboard.release("esc")
            time.sleep(0.01)
        return "in_mainmenu"
    else:
        # if playing == 'find_tdm.png':
        while image("in_mainmenu.png", (1807, 962, 70, 66), 0.93, False) == None:
            keyboard.press("esc")
            time.sleep(0.05)
            keyboard.release("esc")
            time.sleep(0.1)
            image("leave_match.png", (881, 610, 159, 27), 0.94, True)
            if image("Yes_leave.png", (821, 660, 56, 74), 0.94, True):
                image("Yes_leave.png", (821, 660, 56, 74), 0.94, True)
                time.sleep(5)
            if image("play_button.png", (976, 752, 122, 54), 0.92, True):
                while True:
                    if image("startmanu.png", (810, 599, 300, 103), 0.93, True):
                        time.sleep(10 * DelayMultiplier)
                        if not image("video_skip.png", (825, 417, 271, 76), 0.86):
                            break
                        else:
                            keyboard.press("alt")
                            keyboard.press("F4")
                            time.sleep(1)
                            keyboard.release("F4")
                            keyboard.release("alt")
                            ban_check = ban_check + 1
                            if ban_check == 3:
                                print("ban")
                                send_screen("chai k sath mathhi")
                                account_handle.push_acc_details(
                                    account_handle.get_acc_details(mode_to_play), "ban"
                                )
                                kill_ea()
                                openaccounts(mode_to_play)
                                return "False"
                            break
        return "in_mainmenu"

    # arena
    while image("in_mainmenu.png", (1807, 962, 70, 66), 0.93, False) == None:
        print("esc")
        pydirectinput.press("esc")
        image("esc_aftermatch.png", (1691, 1031, 50, 32), 0.94, True)
        # image('esc_aftermatch.png', (0, 880, 1920, 200), 0.94, True)
        if image("space_return_to_lobby.png", (1594, 1028, 238, 42), 0.94) or image(
            "space_return_to_lobby.png", (0, 300, 1920, 780), 0.94, False
        ):
            keyboard.press_and_release("esc")
        # click on leave_match.png
        image("leave_match.png", (881, 610, 159, 27), 0.94, True)
        # click on Yes_leave.png
        if image("Yes_leave.png", (821, 702, 56, 32), 0.94, True):
            time.sleep(5)
    else:
        return "in_mainmenu"


def changeip():
    return
    commands = [
        "adb shell cmd connectivity airplane-mode enable",
        "adb shell cmd connectivity airplane-mode disable",
    ]
    [subprocess.run(cmd, shell=True) and time.sleep(3) for cmd in commands]
    time.sleep(2)
    return
    subprocess.run(
        "warp-cli disconnect", cwd=r"C:\Program Files\Cloudflare\Cloudflare WARP"
    )
    time.sleep(0.5)
    subprocess.run(
        "warp-cli connect", cwd=r"C:\Program Files\Cloudflare\Cloudflare WARP"
    )


def kill_ea():
    return
    print("kill ea")
    try:
        subprocess.run(
            [
                "taskkill",
                "/FI",
                f"USERNAME eq {os.environ['USERNAME']}",
                "/IM",
                "r5apex.exe",
                "/F",
            ]
        )
        subprocess.run(
            [
                "taskkill",
                "/FI",
                f"USERNAME eq {os.environ['USERNAME']}",
                "/IM",
                "EALocalHostSvc.exe",
                "/F",
            ]
        )
        subprocess.run(
            [
                "taskkill",
                "/FI",
                f"USERNAME eq {os.environ['USERNAME']}",
                "/IM",
                "EABackgroundService.exe",
                "/F",
            ]
        )
        subprocess.run(
            [
                "taskkill",
                "/FI",
                f"USERNAME eq {os.environ['USERNAME']}",
                "/IM",
                "EADesktop.exe",
                "/F",
            ]
        )
        subprocess.run(
            [
                "taskkill",
                "/FI",
                f"USERNAME eq {os.environ['USERNAME']}",
                "/IM",
                "EADesktop.exe",
                "/F",
            ]
        )
    except:
        pass
    changeip()


def skip_training():
    print("in functionskip_training")
    # skip training copde
    while True:
        try:
            user = subprocess.run(
                ["python", "skiptrain.py"], capture_output=True, check=True, timeout=600
            )
            user = user.stdout.decode("utf-8").strip().split("@@", 1)[1].lstrip()
            print("line 923 recieved: ", user)
            if "done" in user:
                print("train finished")
                account_handle.push_acc_details(
                    account_handle.get_acc_details(mode_to_play), "training_done"
                )
                return
        except:
            print("press alt f4")
            keyboard.press("alt")
            keyboard.press("F4")
            time.sleep(1)
            keyboard.release("F4")
            keyboard.release("alt")
            wait_and_click_on_image("play_button.png", (976, 752, 122, 54), 0.92)
            while image("startmanu.png", (810, 599, 300, 103), 0.93, True, 160) == None:
                cloudsync_Fix()
            time.sleep(0.21)
            image("startmanu.png", (810, 599, 300, 103), 0.93, True)
            click_ready()


def run_with_time_limit_and_error_handeling(func, time_limit=None):
    # return_value = queue.Queue()
    try:
        return run_with_time_limit(func, True, time_limit=None)
    except TimeoutError as e:
        pass


def run_with_time_limit(func, raise_error, time_limit=None, q=None):
    print(f"Running function: {func.__name__} with time_limit: {time_limit}")
    enforced_function = enforce_time_limit(func, time_limit)
    thread = threading.Thread(target=enforced_function)
    thread.start()
    thread.join(time_limit)
    if thread.is_alive():
        print(f"{func.__name__} exceeded time limit of {time_limit:.2f}s")
        if raise_error:
            raise TimeoutError(
                f"{func.__name__} exceeded time limit of {time_limit:.2f}s"
            )
        return f"{func.__name__} exceeded time limit of {time_limit:.2f}s"
    else:
        return thread.result


def update_status(status):
    def thread_function():
        print("updating ", status)
        account_handle.push_acc_details(
            account_handle.get_acc_details(mode_to_play), status
        )
        print("updating done")

    thread1 = threading.Thread(target=thread_function)
    thread1.start()
    # thread.join()  # Wait for the thread to complete
    return


async def tcp_conversation():
    while True:
        item = await tcp_queue.get()
        tcp.send_message(item)
        tcp_queue.task_done()


# ....................testing start
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    '''''
    # usb capture
    webcam_capture = WebcamCapture()
    webcam_capture.start()
    '''''

    pc_username = os.getlogin()
    print(pc_username)
    for i in range(5):
        print(f"Time left: {5-i} seconds", end="\r")
        time.sleep(1)  # testing
    print(" " * 20, end="\r")
    print("Done!")

    common_var = None
    thread = threading.Thread(target=error_handling1)

    # ndi capture
    computer_name = os.environ["COMPUTERNAME"]
    # computer_name = "HOG"
    print("Computer Name (Environment Variable):", computer_name)
    ndi.start_capture()
    ndi_receiver = ndi.NDIReceiver(computer_name)
    if ndi_receiver.initialize():
        print("connection found")
    else:
        sys.exit()

    # yolo
    # yolo = YoloAimbot()
    # yolo test
    # tframe = np.empty((0,))
    tframe = ""
    i = 5
    print("find frame")
    #'''''
    while True:
        break
        try:
                cam  = cv2.VideoCapture(5)
                result, frame = cam.read()
                #return frame
            #tframe = ndicapturefunctions()
            #if tframe.shape:
                #print(tframe.shape)
                #break
                #tframe = tframe[340:740, 80:1840]
                cv2.imshow("frame", image1)
                print(i)
                cv2.waitKey(1)
        except:
            i = i+1
            pass
    print("frame found")
    #'''''
    # cv2.imshow('frame', frame)
    # cv2.waitKey(1)
    # while True:
    #    img = yolo.yolo_full(tframe)

    # tcp = TCPClient()
    # loop = asyncio.get_event_loop()
    # tcp_queue = asyncio.Queue()
    # consumer_coroutine = tcp_conversation()
    # loop.run_until_complete(consumer_coroutine)

    # ful val script
    q = multiprocessing.Queue()  # aim pope
    qt = multiprocessing.Queue()  # main pipe
    walkmsg = multiprocessing.Queue()  # walks pipe

    aimbotloop = Value("d", 0.0)
    walkbotloop = Value("d", 0.0)
    key_w = Value("d", 0.0)
    key_s = Value("d", 0.0)
    mwalkbot = multiprocessing.Process(
        target=val_full.walkbot, args=(walkmsg, walkbotloop, key_w, key_s)
    )
    maimbot = multiprocessing.Process(
        target=val_full.pixel,
        args=(
            q,
            val_full.boyutlar,
            val_full.ortakare,
            walkbotloop,
            aimbotloop,
            key_w,
            key_s,
            qt,
        ),
    )
    msenddata = multiprocessing.Process(
        target=val_full.senddata, args=(q, walkmsg, walkbotloop, aimbotloop, qt)
    )

    msenddata.start()
    keyboard = KeyboardInputs(qt)
    mouse = MouseInputs(qt)
    """
    # mouse move test
    start_time = time.time()
    while time.time() - start_time < 5:
        x = random.randint(-5, 5)
        y = random.randint(-5, 5)
        mouse.moveTo(x, y)
        time.sleep(0.1)
    """
    apexaimloop = Value("d", 0)  # togle for apex aim
    #apexaimloop.value = 1
    mrun_walkbot = multiprocessing.Process(target=run_aimbot, args=(apexaimloop, mouse))
    mrun_walkbot.start()  # run aimbot process
    #time.sleep(91000.1)
    platform = "ea"  # ea /steam
    debugging = True  # set this to True if in debugging mode
    DelayMultiplier = delay_multiplier()
    universal_delay = 0.2 * DelayMultiplier
    hold_click_time = 0.05 * DelayMultiplier
    try:
        mode_to_play = sys.argv[1]
    except:
        mode_to_play = (
            "find_tdm.png"  # find_arenas_match.png # training.png 'find_tdm.png'
        )
    playing = None
    cant_find_match = 0  # if match got cancelled too many times we need to do something
    print("we are going to train or boost? \nans: ", mode_to_play)

    clcckonmanage()
    print(" test over")
    #time.sleep(999999999)
    play_time = time.time()
    state = what_is_on_screen()  # desktop, in_menu
    print("state: ", state)
    if state == "desktop":
        kill_ea()
        user = openaccounts(mode_to_play)
        play_time = time.time()
    if state == "InGame":
        if run_walkbot(apexaimloop) == "match_finished":
            end_match()
    state = "False"
    while True:
        print("state: ", state)
        if len(state) == 3:
            playing = state[1]
            state = search_match()
            if playing == "temp_trio" and state != "False":
                state = "match_finished"
            elif playing == "training.png" and state != "False":
                skip_training()
                # state = 'match_finished' # in future we auto mate doing tut
                kill_ea()
                user = openaccounts(mode_to_play)
                play_time = time.time()
                state = "False"
        if state == "match_found":
            state = run_walkbot(apexaimloop)
        if state == "match_finished":
            state = end_match(playing)
            playing = None
        if state == "lvl_20":
            account_handle.push_acc_details(
                account_handle.get_acc_details(mode_to_play), "20"
            )
            kill_ea()
            user = openaccounts(mode_to_play)
            play_time = time.time()
            state = "False"
        if state == "training_done":
            account_handle.push_acc_details(
                account_handle.get_acc_details(mode_to_play), "training_done"
            )
            send_screen("m assuming traing done already")
            kill_ea()
            user = openaccounts(mode_to_play)
            play_time = time.time()
            state = "False"

        if state == "False" or state == "in_mainmenu":
            if (time.time() - play_time) < 21600:  # 6 hrs
                state = set_everything_before_match()
            else:
                account_handle.push_acc_details(
                    account_handle.get_acc_details(mode_to_play), "time_limit"
                )
                kill_ea()
                user = openaccounts(mode_to_play)
                play_time = time.time()
# ....................testing end
"""
    # Stop the webcam capture
    webcam_capture.stop()
while True:
    try:
        run_with_time_limit(function_1)
        run_with_time_limit(set_everything_before_match)
        break
    except TimeoutError as e:
        print("excuption")
        if debugging:
            print(e)  # for debugging purposes
            print("excuption")
            print(e.args[0])
            break
        else:
            print("restart")
            # restart or terminate the script as desired
"""
