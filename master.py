import sys
import traceback
import time
import threading
import requests
import pyautogui
import io
import json
import cv2
import numpy as np
import pydirectinput
import os
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# fearbot
bot_token = ""
chat_id = ""
# pclogs
bot_token = ""
chat_id = ""
printed_message_ids = set()
last_message_timestamp = 0
text, caption = "", ""


def long_click(x, y):
    pydirectinput.mouseDown(x, y)
    time.sleep(0.08)
    pydirectinput.mouseUp()

def chrom_chk():
    chrome_path1 =r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    # Check if the Chrome executable file exists
    if os.path.exists(chrome_path) or os.path.exists(chrome_path1):
        print("Google Chrome is installed.")
    else:
        print("Google Chrome is not installed.")
        send_screen('chrome not installed')

def perform_actions(action_name):
    command, *args = action_name.split()
    if command in commands:
        function_name = commands[command]
        function = globals().get(function_name)
        if function:
            function(*args)
    else:
        send_screen("uknown command" + action_name)
 

def get_latest_non_bot_message():
    global printed_message_ids, last_message_timestamp
    while True:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates?offset=-1&chat_id={chat_id}&allowed_updates=message&fields=message,from"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content.decode("utf-8"))
            if data["ok"]:
                for message in data["result"]:
                    if (
                        "message" in message
                        and not message["message"]["from"]["is_bot"]
                    ):
                        message_id = message["message"]["message_id"]
                        if message_id not in printed_message_ids:
                            message_timestamp = message["message"]["date"]
                            if message_timestamp > last_message_timestamp - 60:
                                text = message["message"].get("text")
                                photo = message["message"].get("photo", [])
                                caption = message["message"].get("caption")
                                if not text:
                                    text = ""
                                elif not caption:
                                    caption = ""
                                if (
                                    os.environ["USERNAME"] in text
                                    or "all" in text
                                    or os.environ["USERNAME"] in caption
                                    or "all" in caption
                                ):
                                    if photo:
                                        # Get the largest red contour and its center
                                        photo_url = photo[-1]["file_id"]
                                        file_url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={photo_url}"
                                        file_response = requests.get(file_url)
                                        file_data = json.loads(
                                            file_response.content.decode("utf-8")
                                        )
                                        if file_data["ok"]:
                                            file_path = file_data["result"]["file_path"]
                                            photo_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
                                            photo_response = requests.get(photo_url)
                                            nparr = np.frombuffer(
                                                photo_response.content, np.uint8
                                            )
                                            img_np = cv2.imdecode(
                                                nparr, cv2.IMREAD_COLOR
                                            )
                                            hsv = cv2.cvtColor(
                                                img_np, cv2.COLOR_BGR2HSV
                                            )
                                            lower_red = np.array([0, 50, 50])
                                            upper_red = np.array([10, 255, 255])
                                            mask1 = cv2.inRange(
                                                hsv, lower_red, upper_red
                                            )
                                            lower_red = np.array([170, 50, 50])
                                            upper_red = np.array([180, 255, 255])
                                            mask2 = cv2.inRange(
                                                hsv, lower_red, upper_red
                                            )
                                            mask = mask1 + mask2
                                            contours, hierarchy = cv2.findContours(
                                                mask,
                                                cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE,
                                            )
                                            largest_contour = max(
                                                contours, key=cv2.contourArea
                                            )
                                            moments = cv2.moments(largest_contour)
                                            center_x = int(
                                                moments["m10"] / moments["m00"]
                                            )
                                            center_y = int(
                                                moments["m01"] / moments["m00"]
                                            )
                                            long_click(center_x, center_y)
                                    elif text is not None:
                                        print(text)
                                        if "screen" in text:
                                            send_screen("is looking at ")
                                        else:
                                            perform_actions(text)
                                printed_message_ids.add(message_id)
                                last_message_timestamp = message_timestamp
                                text, caption = "", ""


def send_screen(message="Hi"):
    def upload_screenshot():
        # take a screenshot of the current screen
        screen = pyautogui.screenshot()
        # create an in-memory file object to store the screenshot
        screen_buffer = io.BytesIO()
        screen.save(screen_buffer, "PNG")
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


def force_update(value=0):
    # stop main.py wait for 5 sec and run main.py again
    pass


def list_commands(value=0):
    send_screen(commands)


def softupdate(value=0):
    # wait till last print output in main.py has lvl_ok then close main.py and rerun it
    pass


def pause(value=0):
    #pause the script
    global is_paused
    is_paused = True
    pass

def unpause(value=0):
    # if telegram sends unpause then unpause the script
    global is_paused
    is_paused = False

def stop(value=0):
    # stop the main.py immidiately
    os.system("pkill main.py") # stop main.py
    pass

def exec_main():
    message_counts = {}
    last_reset_time = time.time()

    while True:
        try:
            # Start the subprocess
            print("opening main.py")
            process = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE)

            # Read the output of the subprocess line by line in real time
            while True:
                output = process.stdout.readline()
                if output == b'' and process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode('utf-8'))

            # Wait for 5 seconds before restarting the subprocess
            time.sleep(5)
        except Exception as e:
            # Print the error message and line number
            exc_type, exc_value, exc_traceback = sys.exc_info()
            p = "Error on line " + str(exc_traceback.tb_lineno) + ": " + str(e)

            msg = traceback.format_exc()
            if msg in message_counts:
                message_counts[msg] += 1
            else:
                message_counts[msg] = 1

            # Check if any messages have exceeded the limit
            if time.time() - last_reset_time >= 600:
                for message, count in message_counts.items():
                    if count > 5:
                        print(
                            "Pausing for a day due to repeated errors: {}".format(
                                message
                            )
                        )
                        send_screen('Pausing for a day due to repeated errors')
                        start_time = time.time()
                        is_paused = True
                        while True:
                            if is_paused:
                                print('Resuming...')
                                send_screen('Resuming...')
                                break
                            elif time.time() - start_time >= 86400:
                                print('Timeout: Resuming...')
                                send_screen('Timeout: Resuming...')
                                break
                            else:
                                time.sleep(1)  # check every minute
                        message_counts.clear()
                        last_reset_time = time.time()
                        break
                else:
                    message_counts.clear()
                    last_reset_time = time.time()

            # Print the full traceback
            print(p)
            traceback.print_exc()
            send_screen(msg)

            # Wait for 5 seconds before retrying
            time.sleep(5)


if __name__ == "__main__":
    commands = {
        "force update": "force_update",
        "list commands": "list_commands",
        "update": "softupdate",
        "stop": "stop",
        "unpause": "unpause",
        "pause": "pause"
    }
    chrom_chk()
    is_paused = False
    telerhread = threading.Thread(target=get_latest_non_bot_message)
    telerhread.start()
    telerhread = threading.Thread(target=exec_main)
    telerhread.start()