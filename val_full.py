import asyncio
import requests
import websockets
import socket
import cv2
from mss import mss
import numpy as np
import time
import timeit
import os
import math
import clipboard
import imutils
import multiprocessing
from multiprocessing import Value
import configparser
#import bezier
import random



# user = "intel"
user = "Administrator"

if __name__ == '__main__':
    time.sleep(5)

sct = mss()
scst = mss()

host = "192.168.1.100"
#host = "192.168.1.100"
port = 4455
addr = (host, port)
mid = 0
if __name__ == '__main__':
    print('controlling ' + user + ' host=' + host)


ortakare = 200
fovlimit = 200
breadth = 960
length = 540

boyutlar = sct.monitors[1]
boyutlar['left'] = int(breadth - (ortakare*3.2))
boyutlar['top'] = int(length - ortakare)
boyutlar['width'] = int(ortakare*6.4)
boyutlar['height'] = int(ortakare*2)

minimap = scst.monitors[1]
minimap['left'] = 172
minimap['top'] = 100
minimap['width'] = 112
minimap['height'] = 144


lower_map = np.array([0, 0, 176])
upper_map = np.array([131, 4, 190])
lower_map2 = np.array([26, 24, 185])
upper_map2 = np.array([34, 47, 196])


# aim trainer
lower = np.array([0, 156, 210])
upper = np.array([4, 255, 243])
# SIGHT
lower = np.array([173, 100, 182])
upper = np.array([179, 173, 193])
# purple
lower = np.array([143, 132, 164])
upper = np.array([156, 211, 255])


keyboardkeys = {
    "a": "0x04",
    "b": "0x05",
    "c": "0x06",
    "d": "0x07",
    "e": "0x08",
    "f": "0x09",
    "g": "0x0a",
    "h": "0x0b",
    "i": "0x0c",
    "j": "0x0d",
    "k": "0x0e",
    "l": "0x0f",
    "m": "0x10",
    "n": "0x11",
    "o": "0x12",
    "p": "0x13",
    "q": "0x14",
    "r": "0x15",
    "s": "0x16",
    "t": "0x17",
    "u": "0x18",
    "v": "0x19",
    "w": "0x1a",
    "x": "0x1b",
    "y": "0x1c",
    "z": "0x1d",
    "1": "0x1e",
    "2": "0x1f",
    "3": "0x20",
    "4": "0x21",
    "5": "0x22",
    "6": "0x23",
    "7": "0x24",
    "8": "0x25",
    "9": "0x26",
    "0": "0x27",
    "A": "0x04",
    "B": "0x05",
    "C": "0x06",
    "D": "0x07",
    "E": "0x08",
    "F": "0x09",
    "G": "0x0A",
    "H": "0x0B",
    "I": "0x0C",
    "J": "0x0D",
    "K": "0x0E",
    "L": "0x0F",
    "M": "0x10",
    "N": "0x11",
    "O": "0x12",
    "P": "0x13",
    "Q": "0x14",
    "R": "0x15",
    "S": "0x16",
    "T": "0x17",
    "U": "0x18",
    "V": "0x19",
    "W": "0x1A",
    "X": "0x1B",
    "Y": "0x1C",
    "Z": "0x1D",
    "ctrl": "0xE0",
    "alt": "0xE2",
    "shift":  "0xE1",
    "enter": "0x28",
    "win": "0xE3",
    "Return": "0x28",
    "Escape": "0x29",
    "Backspace": "0x2A",
    "Tab": "0x2B",
    "Spacebar": "0x2C",
    "Space": "0x2C",
    "@":"0x1f",
    ".":"0x37",
    "_":"0x2D",
    "Minus": "0x2D",
    "Equals": "0x2E",
    "LeftSquareBracket": "0x2F",
    "RightSquareBracket": "0x30",
    "Backslash": "0x31",
    "NonUsHash": "0x32",
    "Semicolon": "0x33",
    "Quote": "0x34",
    "GraveAccent": "0x35",
    "Comma": "0x36",
    "Period": "0x37",
    "Slash": "0x38",
    "CapsLock": "0x39",
    "F1": "0x3A",
    "F2": "0x3B",
    "F3": "0x3C",
    "F4": "0x3D",
    "F5": "0x3E",
    "F6": "0x3F",
    "F7": "0x40",
    "F8": "0x41",
    "F9": "0x42",
    "F10": "0x43",
    "F11": "0x44",
    "F12": "0x45",
    "PrintScreen": "0x46",
    "ScrollLock": "0x47",
    "Pause": "0x48",
    "Insert": "0x49",
    "Home": "0x4A",
    "PageUp": "0x4B",
    "Delete": "0x4C",
    "End": "0x4D",
    "PageDown": "0x4E",
    "RightArrow": "0x4F",
    "LeftArrow": "0x50",
    "DownArrow": "0x51",
    "UpArrow": "0x52",
    "KeypadNumLock": "0x53",
    "KeypadDivide": "0x54",
    "KeypadMultiply": "0x55",
    "KeypadAdd": "0x56",
    "KeypadSubtrace": "0x57",
    "KeypadReturn": "0x58",
    "Keypad1": "0x59",
    "Keypad2": "0x5A",
    "Keypad3": "0x5B",
    "Keypad4": "0x5C",
    "Keypad5": "0x5D",
    "Keypad6": "0x5E",
    "Keypad7": "0x5F",
    "Keypad8": "0x60",
    "Keypad9": "0x61",
    "Keypad0": "0x62",
    "enter": "0x28",
    "escape": "0x29",
    "esc": "0x29",
    "backspace": "0x2a",
    "tab": "0x2b",
    "spacebar": "0x2c",
    "space": "0x2C",
    "minus": "0x2d",
    "equals": "0x2e",
    "left_bracket": "0x2f",
    "right_bracket": "0x30",
    "backslash": "0x31",
    "pound": "0x32",
    "semicolon": "0x33",
    "quote": "0x34",
    "grave_accent": "0x35",
    "comma": "0x36",
    "period": "0x37",
    "forward_slash": "0x38",
    "caps_lock": "0x39",
    "f1": "0x3a",
    "f2": "0x3b",
    "f3": "0x3c",
    "f4": "0x3d",
    "f5": "0x3e",
    "f6": "0x3f",
    "f7": "0x40",
    "f8": "0x41",
    "f9": "0x42",
    "f10": "0x43",
    "f11": "0x44",
    "f12": "0x45",
    "print_screen": "0x46",
    "scroll_lock": "0x47",
    "pause": "0x48",
    "insert": "0x49",
    "home": "0x4a",
    "page_up": "0x4b",
    "delete": "0x4c",
    "end": "0x4d",
    "page_down": "0x4e",
    "right_arrow": "0x4f",
    "left_arrow": "0x50",
    "down_arrow": "0x51",
    "up_arrow": "0x52",
    "keypad_numlock": "0x53",
    "keypad_forward_slash": "0x54"
}
inputkeys = {
    "mmcal": 8,
    "mccal": 9,
    "mm": 4,
    "mc": 2,
    "mp": 5,
    "mr": 1,
    "key": 3,
    "up": 7,
    "down": 6
}
keystate = {
    "0": 0,
    "up": 7,
    "down": 6
}

def send_message(message = 'Hi'):
    bot_token = ''
    chat_id = ''
    requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={user,message}')


def senddata(q, walkmsg, walkbotloop, aimbotloop, qt):
    """ Creating the tcp socket """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reconnect_attempts = 0
    max_reconnect_attempts = 15
    while True:
        try:
            if reconnect_attempts == 0:
                send_message(user + " trying 2 connect to " + host)
                client.connect(addr)
                #client.settimeout(0.4)
                send_message(user + "connected to " + host)
            while True:
                if (q.empty() is False) and (aimbotloop.value >= 1):
                    data = q.get() + "|"
                    aimbotloop.value = 2
                    #print('aim ' + str(data))
                    client.sendall(data.encode("utf-8"))
                    aimbotloop.value = 1
                else:
                    while not q.empty():
                        q.get()
                if (not walkmsg.empty()) and (walkbotloop.value == 1):
                    data = walkmsg.get() + "|"
                    # print('walk ' + str(data))
                    client.sendall(data.encode("utf-8"))
                else:
                    while not walkmsg.empty():
                        walkmsg.get()
                if qt.empty() is False:
                    data = qt.get() + "|"
                    #print(data)
                    client.sendall(data.encode("utf-8"))
        except (socket.timeout, socket.error) as e:
            #send_message(user + str(e))
            reconnect_attempts = 0
            while reconnect_attempts < max_reconnect_attempts:
                try:
                    client.connect(addr)
                    #send_message(f'{user} reconnected to server after {reconnect_attempts+1} attempt(s)')
                    reconnect_attempts = 1
                    break
                except (socket.timeout, socket.error) as e:
                    client.close()
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    reconnect_attempts += 1
                    time.sleep(1)
                    continue
            if reconnect_attempts == max_reconnect_attempts:
                #send_message(f'{user} failed to reconnect after {max_reconnect_attempts} attempts')
                aimbotloop.value = 0
                walkbotloop.value = 0
        except Exception as e:
            send_message(user +", exception cant br handeled \n"+ str(e))

lastsign = 0


def walkbot(q, walkbotloop, key_w, key_s):
    while True:
        if walkbotloop.value == 1:  # 1 value kro
            walkbot1(q, key_w, key_s, walkbotloop)
            time.sleep(0.01)


def walkbot_screen_coordinates():
    img = np.array(sct.grab(minimap))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_map, upper_map)
    mask1 = cv2.inRange(hsv, lower_map2, upper_map2)
    mask = mask + mask1
    kernel = np.ones((2, 2), np.uint8)
    erode = cv2.erode(mask, kernel, iterations=2)
    dilated = cv2.dilate(erode, kernel, iterations=5)
    # cv2.imshow("raw", img)
    # cv2.imshow("dilated", dilated)
    # cv2.destroyAllWindows()

    # find contours in thresholded image
    cnts = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) != 0:  # j lab gea  tan
        extLeft, extRight, extTop, extBot = 1e9, -1e9, 1e9, -1e9   # values jali likho
        for cc in cnts:   # extreme points labbo
            extLeft = min(cc[:, :, 0].min(), extLeft)
            extRight = max(cc[:, :, 0].max(), extRight)
            extTop = min(cc[:, :, 1].min(), extTop)
            extBot = max(cc[:, :, 1].max(), extBot)
        # print(extBot, extTop)
        if (extBot > 85) and extLeft < 70 and extRight > 40:  # error value na chk lai es lai
            return extLeft, extRight, extTop
    return -1, -1, -1


def walkbot1(q, key_w, key_s, walkbotloop):
    extLeft, extRight, extTop, extBot = 1e9, -1e9, 1e9, -1e9   # values jali likho
    try:
        extLeft, extRight, extTop = walkbot_screen_coordinates()
    except:
        pass
    if extRight in range(1, 200):     # thr is a way
        if walkbotloop.value == 0:
            return
        q.put(str(user+','+'3'+','+str("s") + ','+str('7')))
        q.put(str(user+','+'3'+','+str("w") + ','+str('6')))

        value = (extRight - 57) if (extRight -
                                    57) > (57 - extLeft) else (extLeft - 57)
        q.put(f"{user},8,{math.floor(value*1.19)},0")

        return

    q.put(str(user+','+'3'+','+str("w") + ','+str('7')))
    key_w.value = 0
    q.put(str(user+','+'3'+','+str("s") + ','+str('6')))
    key_s.value = 1
    time.sleep(1)
    q.put(str(user+','+'3'+','+str("s") + ','+str('7')))
    key_s.value = 0

    extTop = 1e9
    toppoint = -90
    # print(timeit.default_timer() - last)
    last = timeit.default_timer()
    turnwhere = random.choice(
        [random.randint(-500, -100), random.randint(100, 500)])
    # find way loop
    while walkbotloop.value == 1 and toppoint <= extTop and (timeit.default_timer() - last) < 4:
        extLeft, extRight, extTop = walkbot_screen_coordinates()  # chking if we have way
        if extTop == 1e9 or extTop == 0:  # no path found
            q.put(str(user+','+'8'+','+str(turnwhere) + ','+str('0')))
            time.sleep(0.5)
        else:  # path found so turning lil bit till longest straight path found
            if int(toppoint) < int(extTop):  # store longest path
                toppoint = extTop
                turnwhere = (extRight - 57) if (extRight -
                                                57) > (57 - extLeft) else (extLeft - 57)
            q.put(f"{user},8,{math.floor(turnwhere*1.59)},0")


def pixel(q, boyutlar, ortakare, walkbotloop, aimbotloop, key_w, key_s, qt):
    lastfov = 200
    freez = 0
    scale = 1
    start = -8888
    x_last = 78
    y_last = 0
    break_now = 0
    #cv2.imshow("thresh", cv2.WINDOW_NORMAL)
    #cv2.moveWindow('thresh', -1920, 0)

    while True:
        if aimbotloop.value >= 1:
            img = np.array(sct.grab(boyutlar))
            # cv2.imshow("Open", img)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(mask, kernel, iterations=5)
            thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
            # print(thresh)
            #cv2.imshow("thresh", thresh)
            contours, hierarchy = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            if len(contours) >= 1 and aimbotloop.value == 1:  # testing 5 as 0 giving problems
                contours = sorted(
                    contours, key=lambda c: cv2.boundingRect(c)[1])
                x, y, w, h = cv2.boundingRect(contours[0])
                #M = cv2.moments(thresh)
                #cX = int(M["m10"] / M["m00"])
                #cY = int(M["m01"] / M["m00"])
                x = int(x + boyutlar['left'] - 960 + (w/2))
                y = y + boyutlar['top'] - 530  # 540
                #y_last += y

                freez = freez + 1
                if freez == 1:
                    start = timeit.default_timer()
                    walkbotloop.value = 2
                    print("stop walkbot by aim")
                    qt.put(f"{user},3,w,7")
                    qt.put(f"{user},3,s,7")
                    q.put(f"{user},9,{x},{y}")
                    time.sleep(.45)  # .35
                # to counter any false +ve we implemented this it will shoot at flowers for 5 sec then it will skip
                elif freez >= 2 and (timeit.default_timer() - start > 5):
                    if walkbotloop.value == 2 and aimbotloop.value == 1:
                        print("start walkbot freez aim seems false +ve")
                        freez, walkbotloop.value = 0, 1
                        #y_last = -(y_last)
                        # q.put(f"{user},8,0,{y_last}")
                        #y_last = 0
                        time.sleep(5)
                q.put(f"{user},9,{x},{y}")
                #wind_mouse(q, user, x, y, '8')
                time.sleep(.22)  # .18
            elif freez >= 1:
                stop = timeit.default_timer()
                # print('Time: ', stop - start)
                if int(stop - start) >= 3:
                    freez = 0
                    #y_last = -(y_last)
                    # if abs(y_last) > 600
                    # q.put(f"{user},8,0,{y_last}")
                    #y_last = 0
                    if walkbotloop.value == 2 and aimbotloop.value == 1:
                        print("start walkbot")
                        walkbotloop.value = 1


def wind_mouse(q, user, end_x, end_y, device):
    start_x, start_y = 0, 0
    end_x, end_y = cal_angle(end_x), cal_angle(end_y)
    # Calculate the distance between the starting and ending points
    distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)

    # Calculate the maximum distance that the curve can go beyond the end point
    max_excess = distance * 0.02

    # Calculate the number of steps needed to move the mouse along the line
    num_steps = int(distance / 10)

    # Loop through each step and move the mouse
    for i in range(num_steps):
        # Calculate the current position of the mouse along the line
        x = start_x + (end_x - start_x) * (i / num_steps)
        y = start_y + (end_y - start_y) * (i / num_steps)

        # Add a random offset to the current position
        x += random.uniform(-5, 5)
        y += random.uniform(-5, 5)

        # If the current position is beyond the end point, adjust it
        if i == num_steps - 1:
            excess = math.sqrt((x - end_x)**2 + (y - end_y)**2)
            if excess > max_excess:
                x -= (excess - max_excess) * (x - end_x) / excess
                y -= (excess - max_excess) * (y - end_y) / excess

        # Move the mouse to the adjusted position
        q.put(f"{user},8,{int(x)},{int(y)}")
    # time.sleep(.28)
    q.put(f"{user},9,0,2")


angle_table = [1.146666667, 1.104, 1.08, 1.066964286, 1.047272727, 1.027692308, 0.9947089947,
               0.9835294118, 0.9620253165, 0.9190207156, 0.9050966608, 0.8817891374, 0.8624260355, 0.844137931]


def cal_angle(newX):
    stroke = newX // 50
    if stroke < len(angle_table):
        return newX * angle_table[stroke]
    else:
        return newX * 0.8036144578


def togglekeys(key, state, key_w, key_s):
    if key == "w":
        if state == "0":
            key_w.value = 0
            q.put(str(user+','+'3'+','+str("w") + ','+str('7')))
            print("w released")
        else:
            key_w.value = "1"
            q.put(str(user+','+'3'+','+str("w") + ','+str('6')))
            print("w pressed")
    elif key == "s":
        if state == "0":
            key_s.value = 0
            q.put(str(user+','+'3'+','+str("s") + ','+str('7')))
            print("s released")
        else:
            key_s.value = 1
            q.put(str(user+','+'3'+','+str("s") + ','+str('6')))
            print("s pressed")


def keyboardkey(x, y, DeviceEvent, q):
    xx = [char for char in x]
    for i in xx:
        print(i)
        if i.islower() or i.isdigit() or i == '.':
            q.put(str(user+','+str(inputkeys[DeviceEvent]) +
                      ','+str(i) + ','+str(keystate[y])))
            # time.sleep(0.3)
        else:
            q.put(str(user+','+str(inputkeys[DeviceEvent])+',' +
                      str("shift") + ','+str(keystate["down"])))
            # time.sleep(0.5)
            q.put(str(user+','+str(inputkeys[DeviceEvent]) +
                      ','+str(i) + ','+str(keystate[y])))
            # time.sleep(0.5)
            q.put(str(user+','+str(inputkeys[DeviceEvent])+',' +
                      str("shift") + ','+str(keystate["up"])))
            # time.sleep(0.5)


def DeviceEvents(DeviceEvent, x, y, q):
    if "m" in DeviceEvent:
        x = int(float(x))
        y = int(float(y))
        q.put(
            str(user+','+str(inputkeys[DeviceEvent])+','+str(x) + ','+str(y)))
        return
    try:
        zz = keyboardkeys[x]  # previously its x = keyboardkeys[x]
    except:
        keyboardkey(x, y, DeviceEvent, q)
        return
    q.put(str(user+','+str(inputkeys[DeviceEvent]
                           )+','+str(x) + ','+str(keystate[y])))


def wasd(text, aimbot, q):
    if text == "start":
        aimbot = 1
        return aimbot
    elif text == "stop":
        print("stop both")
        aimbot = 2
        return aimbot
    elif text == "walkstop":
        aimbot = 3
        return aimbot
    elif text == "aimstop":
        aimbot = 4
        return aimbot
    else:
        nn = text.split(",")
        if len(nn) != 3:
            print(f'wrong:{text}')
        else:
            DeviceEvent = nn[0]
            x = nn[1]
            y = nn[2]
            DeviceEvents(DeviceEvent, x, y, q)
        return aimbot


text1 = 0
aimbot = 0
lastfov = 0
clipboardcommands = True

if __name__ == '__main__':
    print("Ready !")

    q = multiprocessing.Queue()  # aim pope
    qt = multiprocessing.Queue()  # main pipe
    walkmsg = multiprocessing.Queue()  # walks pipe
    aimbotloop = Value('d', 0.0)
    walkbotloop = Value('d', 0.0)
    key_w = Value('d', 0.0)
    key_s = Value('d', 0.0)
    mwalkbot = multiprocessing.Process(
        target=walkbot, args=(walkmsg, walkbotloop, key_w, key_s))
    maimbot = multiprocessing.Process(target=pixel, args=(
        q, boyutlar, ortakare, walkbotloop, aimbotloop, key_w, key_s, qt))
    msenddata = multiprocessing.Process(
        target=senddata, args=(q, walkmsg, walkbotloop, aimbotloop, qt))

    mwalkbot.start()
    maimbot.start()
    msenddata.start()

    '''''
    # 366,-111
    #
    #
    #
    #
    x = 0
    y = -0
    q.put(f"{user},9,{x},{y}")
    '''''
    config = configparser.ConfigParser()
    config.sections()
    config.read('settings.ini')
    text = 0

    while True:
        if clipboardcommands == True:
            try:
                config.read('settings.ini')
                text = config['logs']['clipboards']
            except:
                pass
            if text != text1:
                print('ahk ' + text)
                text1 = text
                aimbot = wasd(text, aimbot, qt)

        if (aimbot == 1):
            print("aim + walk enabled")
            aimbot = 0
            walkbotloop.value = 1  # ethe 1 krna
            aimbotloop.value = 1
            start_time = time.time()
        elif (aimbot == 2):
            aimbotloop.value = 0
            walkbotloop.value = 0
            print("aim + walk stoped")
            aimbot = 0
        elif (aimbot == 3):
            aimbot = 0
            walkbotloop.value = 0
        elif (aimbot == 4):
            aimbot = 0
            aimbotloop.value = 0
        elif aimbotloop.value == 1 and time.time() - start_time > 600:
            aimbot = 2
            print("stoping aim n walk because 10 min is its on limit")
            
