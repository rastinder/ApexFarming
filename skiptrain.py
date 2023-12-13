import mss.tools
import mss
import pynput
import time
import pydirectinput
import pyautogui
import ctypes
import os
import requests
from PIL import ImageGrab
import clipboard
import subprocess
import sys
import keyboard


def move_mouse(x, y):
    MOUSEEVENTF_MOVE = 0x0001
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, x, y, 0, 0)


def long_click(x, y):
    pydirectinput.mouseDown(x, y)
    time.sleep(0.01)
    pydirectinput.mouseUp()


def send_screen(message='Hi'):
    bot_token = '1331062094:AAEsirbmiJk1RsPLsbHxa2Kh5KjF6jtmMjc'
    chat_id = '706316494'

    # take a screenshot of the current screen
    screen = pyautogui.screenshot()
    # save the screenshot as a temporary file
    screen_file = 'screen.png'
    screen.save(screen_file)

    # upload the screenshot file to Telegram and send it as a photo
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    with open(screen_file, 'rb') as f:
        response = requests.post(
            url, data={'chat_id': chat_id, 'caption': message}, files={'photo': f})

    # delete the temporary file
    if response.status_code == 200:
        os.remove(screen_file)


def wait_and_click_on_image(image_file, region, confidence, click=True, max_wait_time=60):
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
        try:
            img = pyautogui.center(pyautogui.locateOnScreen(
                image_file, grayscale=True, region=region, confidence=confidence))
        except TypeError:
            continue
        if time.time() - start_time > max_wait_time and already_sent == None:
            send_screen("cant find in 10 sec " + image_file)
            already_sent = 1
    if click == True:
        long_click(img[0], img[1])
    return img


def image(image_file, region, confidence, click=False):
    img = None
    try:
        x1, y1, x2, y2 = region
        y1 = max(y1 - 30, 0)
        y2 = min(y2 + 30, 1060)
        region = x1, y1, x2, y2
    except Exception as e:
        print(e)
    if img is None:
        try:
            img = pyautogui.center(pyautogui.locateOnScreen(
                image_file, grayscale=True, region=region, confidence=confidence))
        except TypeError:
            return None
        if click == True:
            long_click(img[0], img[1])
            print("clicked: " + image_file)
            return img
        print("located: " + image_file)
        return img
    return None


def wait_and_click_on_image_color(image_file, region, confidence, click=True, max_wait_time=20):
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
        try:
            img = pyautogui.center(pyautogui.locateOnScreen(
                image_file, grayscale=False, region=region, confidence=confidence))
        except TypeError:
            continue
        if time.time() - start_time > max_wait_time and already_sent == None:
            send_screen("cant find in 10 sec " + image_file)
            already_sent = 1
    if click == True:
        long_click(img[0], img[1])
    return img


def image_color(image_file, region, confidence, click=False):
    img = None
    try:
        x1, y1, x2, y2 = region
        y1 = max(y1 - 30, 0)
        y2 = min(y2 + 30, 1060)
        region = x1, y1, x2, y2
    except Exception as e:
        print(e)
    if img is None:
        try:
            img = pyautogui.center(pyautogui.locateOnScreen(
                image_file, grayscale=False, region=region, confidence=confidence))
        except TypeError:
            return None
        if click == True:
            long_click(img[0], img[1])
            print("clicked: " + image_file)
            return img
        print("located: " + image_file)
        return img
    return None


script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def yellow_target(what='yellow'):
    subprocess.run(f'cmd /c skiptrain.ahk {what} ', check=True)
    try:
        return [int(x) for x in clipboard.paste().split(',')]
    except:
        return None


def wasd():
    pydirectinput.keyDown('w')
    time.sleep(1)
    pydirectinput.press('shift')
    time.sleep(.1)
    pydirectinput.keyDown('ctrlleft')
    time.sleep(4)
    pydirectinput.keyUp('w')
    pydirectinput.keyUp('ctrlleft')
    time.sleep(.5)
    pydirectinput.keyDown('space')
    time.sleep(.5)
    pydirectinput.keyUp('space')
    time.sleep(.3)
    pydirectinput.keyDown('ctrlleft')
    time.sleep(.5)
    pydirectinput.keyUp('ctrlleft')


def lpress(key, time1=.1):
    pydirectinput.keyDown(key)
    time.sleep(time1)
    pydirectinput.keyUp(key)


def genrade():
    pydirectinput.keyDown('w')


for i in range(1):
    print(f'Time left: {1-i} seconds', end='\r')
    time.sleep(1)
print(' ' * 20, end='\r')


'''''
i = 0
while True:
    move_mouse(1, 0)
    i=i+1
    print(i)
    time.sleep(.1)
'''''


while not image('tut_wasd_lshift.png', (1448, 322, 75, 40), 0.94):
    time.sleep(1)
wasd()
time.sleep(5)
# locate target
wasd()  # go forward
time.sleep(1)
lpress('w', 1)
# press a to go extreme left
lpress('a', 3.5)


while True:
    img = yellow_target()
    if img:
        img[0] = img[0] - 960
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
            # print(img[0])
        else:
            break
    else:
        print('guess')
        move_mouse(5, 0)

while image('e_open.png', (0, 400, 1920, 1080), 0.87, False) is None:
    pydirectinput.press('w')
pydirectinput.press('e')
pydirectinput.press('w')
pydirectinput.press('w')
pydirectinput.press('w')
pydirectinput.press('w')
pydirectinput.press('w')
print('Done!')

while image('tut_e_pickup_syringe.png', (0, 400, 1920, 1080), 0.87, False) is None:
    move_mouse(-5, 0)
pydirectinput.press('e')

while image('tut_e_pickup_frag.png', (0, 400, 1920, 1080), 0.87, False) is None:
    move_mouse(25, 0)
    pydirectinput.press('e')
    if image('tut_g_forgenrade.png', (0, 0, 1920, 1080), 0.88):
        break
pydirectinput.press('e')
# throw frag etc etc
print('throw frag etc etc')
# click on tut_g_forgenrade.png
wait_and_click_on_image('tut_g_forgenrade.png',
                        (1483, 419, 43, 39), 0.88, False)
if image('tut_g_forgenrade.png', (1483, 419, 43, 39), 0.88):
    time.sleep(2)
    pydirectinput.keyDown('4')
    start_time = time.time()
    time.sleep(.01)
    pydirectinput.keyUp('4')
    pydirectinput.keyDown('g')
    time.sleep(6.66)
    # while time.time() - start_time < 5.2:
    move_mouse(0, -50)
    pydirectinput.keyUp('g')
    time.sleep(.503)
    move_mouse(600, 0)
    pynput.mouse.Controller().click(pynput.mouse.Button.left)
    time.sleep(2)
    while image('tut_throw_grande.png', (1484, 323, 37, 39), 0.94):
        pynput.mouse.Controller().click(pynput.mouse.Button.left)
        time.sleep(.01)
    pynput.mouse.Controller().click(pynput.mouse.Button.left)
    move_mouse(-600, 0)
    time.sleep(.2)

# pick wepon and ammo
print('pick wepon and ammo')
print('yellow target look')
while not yellow_target():
    time.sleep(1)
print('target found')

for i in range(2):
    while True:
        img = yellow_target()
        if img:
            img[0] = img[0] - 960
            while abs(img[0]) > 500:
                img[0] = int(img[0] * .5)
            if abs(img[0]) > 5:
                move_mouse(img[0], 0)
            else:
                break

pydirectinput.keyDown('ctrl')
while not image('tut_e_picked_gun.png', (1844, 284, 28, 21), 0.93):
    pydirectinput.press('w')
    pydirectinput.press('e')
pydirectinput.press('w')
pydirectinput.keyUp('ctrl')

move_mouse(-400, 0)
move_mouse(-400, 0)
move_mouse(-200, 0)

start_time = time.time()
# while time.time() - start_time < 10:
while not image('tut_equip_weapon.png', (0, 0, 1920, 1080), 0.80) or time.time() - start_time < 8:
    pydirectinput.press('w')
move_mouse(200, 0)
pydirectinput.press('w')
pydirectinput.press('w')
pydirectinput.press('w')
pydirectinput.press('w')


print('look equip')
'''''
for i in range(4):
    start_time = time.time()
    while time.time() - start_time < 2:
        img = image('tut_equip_weapon.png', (0, 0, 1920, 1080), 0.80)
        if img:

            x = int(img[0] - 960)
            if abs(x) > 5:
                if x < 1:
                    x = 1
                print(img[0], x)
                move_mouse(x, 0)
            else:
                break
        else:
            print('equip not found')
    if image('tut_equip_weapon.png', (0, 0, 1920, 1080), 0.80):
        pydirectinput.press('w')
'''''
print('look center')

lpress('a', 0.6)
while not image('tut_equip_weapon.png', (0, 0, 1920, 1080), 0.80):
    keyboard.press('d')
    time.sleep(.005)
    keyboard.release('d')
    time.sleep(.4)
# slide lil more
keyboard.press('d')
time.sleep(.02)  # find weapon to ping
keyboard.release('d')
time.sleep(.4)

pydirectinput.press('e')
time.sleep(1)
pynput.mouse.Controller().scroll(0, 1)
time.sleep(1)
lpress('e', 1)


print('ping check')
while True:
    if image('tut_ping_location.png', (1486, 273, 34, 39), 0.92) or image('tut_ping_location.png', (1486, 417, 34, 39), 0.92):
        break
    lpress('e', 1)
time.sleep(2)

pynput.mouse.Controller().click(pynput.mouse.Button.middle)
time.sleep(.07)
pynput.mouse.Controller().click(pynput.mouse.Button.middle)
time.sleep(.07)
pynput.mouse.Controller().click(pynput.mouse.Button.middle)
time.sleep(.07)
pynput.mouse.Controller().click(pynput.mouse.Button.middle)
time.sleep(.07)
pynput.mouse.Controller().click(pynput.mouse.Button.middle)
time.sleep(.07)
pynput.mouse.Controller().click(pynput.mouse.Button.middle)
pynput.mouse.Controller().click(pynput.mouse.Button.middle)
pynput.mouse.Controller().click(pynput.mouse.Button.middle)
time.sleep(1)

i = 0
pydirectinput.keyDown('ctrl')
while not image('tut_e_pickup_ammo_ping1.png', (0, 0, 1920, 1080), 0.85):
    move_mouse(-25, 25)
    i = i+25
move_mouse(-25, 25)
time.sleep(.02)
pynput.mouse.Controller().click(pynput.mouse.Button.middle)
time.sleep(.02)
move_mouse(25, -25)
i = i+5
move_mouse(-400, 900)
move_mouse(0, -600)
move_mouse(0, -300)
move_mouse(-400, -i)
move_mouse(-400, 0)
move_mouse(-400, 0)
time.sleep(1)
print('hold mmb')
pynput.mouse.Controller().press(pynput.mouse.Button.middle)
time.sleep(1)
pynput.mouse.Controller().release(pynput.mouse.Button.middle)
time.sleep(1)
pydirectinput.keyUp('ctrl')

print('ping finish')
'''''
time.sleep(12)
while True:
    img = yellow_target()
    if img:
        img[0] = img[0] - 960
        # print(img)
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
        else:
            break
print('double sure target XD')
move_mouse(6, 0)
time.sleep(.12)
while True:
    img = yellow_target()
    if img:
        img[0] = img[0] - 960
        # print(img)
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
        else:
            break

# look at rope
print('rope')
move_mouse(442, 0)
'''''
while True:
    img = yellow_target('rope')
    if img:
        img[0] = img[0] - 960
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
        else:
            break
    else:
        move_mouse(20, 0)
# look at rope second time
while True:
    img = yellow_target('rope')
    if img:
        img[0] = img[0] - 960
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
        else:
            break
    else:
        move_mouse(20, 0)
# reach at rope
lpress('d', 1.25)
time.sleep(.5)
lpress('w', 15)

# look target
while True:
    img = yellow_target()
    if img:
        img[0] = img[0] - 960
        # print(img)
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
        else:
            break
print('way')
move_mouse(220, 0)

print('sleep')
time.sleep(2)
pydirectinput.keyDown('space')
pydirectinput.keyDown('shift')
lpress('w', 10.6)
pydirectinput.keyUp('shift')
pydirectinput.keyUp('space')

while image('m.png', (0, 0, 1920, 1080), 0.7):
    move_mouse(-20, 0)

pydirectinput.keyDown('shift')
lpress('w', 3.44)
pydirectinput.keyUp('shift')
move_mouse(-300, 0)
lpress('w', 1)


print('revive dummy')

# click on tut_press_e_to_revive.png
wait_and_click_on_image('tut_press_e_to_revive.png',
                        (1489, 274, 31, 38), 0.80, False,30)
# look dummy
while True:
    img = yellow_target()
    if img:
        img[0] = img[0] - 960
        # print(img)
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
        else:
            break
# click on tut_hold_e_to_revive.png
while not image('tut_hold_e_to_revive.png', (0, 0, 1920, 1080), 0.94, False):
    lpress('w', .3)
lpress('e', 7)
time.sleep(16)
lpress('s', .3)
pydirectinput.press('q')
time.sleep(19)

print('pick dummy')

pydirectinput.press('w')
pydirectinput.press('w')
pydirectinput.press('w')

pydirectinput.keyDown('ctrl')
time.sleep(4)
pydirectinput.press('e')
time.sleep(4)
pydirectinput.keyUp('ctrl')
time.sleep(4)
print('go ro revive')
while True:
    img = yellow_target()
    if img:
        img[0] = img[0] - 960
        # print(img)
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
        else:
            break
lpress('w', 3.5)
lpress('e', 7)
time.sleep(28)
pydirectinput.press('z')
move_mouse(0, 400)
lpress('s', 1)
time.sleep(.2)
pynput.mouse.Controller().click(pynput.mouse.Button.left)
time.sleep(20)
lpress('w', 1)
pydirectinput.press('e')
time.sleep(3)
pydirectinput.press('e')
wait_and_click_on_image('tut_end.png', (768, 722, 131, 37), 0.94, False)
keyboard.press('alt')
keyboard.press('F4')
time.sleep(1)
keyboard.release('F4')
keyboard.release('alt')
time.sleep(5)
# click on notification.png
wait_and_click_on_image('notification.png', (1691, 167, 33, 31), 0.94)
# click on logout.png
wait_and_click_on_image('logout.png', (1515, 535, 74, 29), 0.94)
# click on skip_sync.png
wait_and_click_on_image('skip_sync.png', (0, 0, 1920, 1080), 0.94, False)
while image('skip_sync.png', (0, 0, 1920, 1080), 0.90, False):
    time.sleep(.1)
print('@@')
print('done')
sys.exit()

while True:
    img = yellow_target('rope')
    if img:
        img[0] = img[0] - 960
        print(img)
        while abs(img[0]) > 500:
            img[0] = int(img[0] * .5)
        print(img)
        if abs(img[0]) > 5:
            move_mouse(img[0], 0)
        else:
            break
    else:
        move_mouse(-20, 0)


image('m.png', (0, 0, 1920, 1080), 0.80)
while True:
    if image('tut_wasd_lshift.png', (1448, 322, 75, 40), 0.94):
        wasd()
        while True:
            if image('tut_open_box.png', (1526, 280, 188, 29), 0.62):
                pydirectinput.keyDown('e')
                time.sleep(.01)
                pydirectinput.keyUp('e')
                if image('tut_prees_e_quick_suplly.png', (0, 0, 1920, 1080), 0.94):
                    start_time = time.time()
                    while time.time() - start_time < 4:
                        pydirectinput.keyDown('e')
                        time.sleep(.01)
                        pydirectinput.keyUp('e')
                        time.sleep(.001)
                        if image('tut_g_forgenrade.png', (1483, 275, 43, 39), 0.94):
                            break
                    pydirectinput.keyDown('4')
                    start_time = time.time()
                    time.sleep(.01)
                    pydirectinput.keyUp('4')
                    pydirectinput.keyDown('g')
                    time.sleep(6.66)
                    # while time.time() - start_time < 5.2:
                    move_mouse(0, -50)
                    pydirectinput.keyUp('g')
                    time.sleep(.503)
                    pynput.mouse.Controller().click(pynput.mouse.Button.left)
                    while image('tut_throw_grande.png', (1484, 323, 37, 39), 0.94):
                        pynput.mouse.Controller().click(pynput.mouse.Button.left)
                        time.sleep(.01)
                    time.sleep(3)
                    while image('tut_e_preess_pick_weapon.png', (1483, 274, 43, 40), 0.94):
                        pydirectinput.keyDown('e')
                        time.sleep(.01)
                        pydirectinput.keyUp('e')
                        time.sleep(.01)
                    break
    # wepaon
    if image('tut_pickweapon_swap_etc.png', (1481, 273, 42, 40), 0.94):
        print('wepon pick')
        pydirectinput.keyDown('e')
        time.sleep(.1)
        pydirectinput.keyUp('e')
        while True:
            while image('tut_tick_pick_weapon.png', (1842, 277, 32, 31), 0.94) is None:
                time.sleep(.1)
            time.sleep(.5)
            # cycle weapon
            pynput.mouse.Controller().scroll(0, 1)
            time.sleep(.8)
            pydirectinput.keyDown('e')
            time.sleep(.15)
            pydirectinput.keyUp('e')
            break
    # ping
    if image('tut_ping_location.png', (1486, 273, 34, 39), 0.92) or image('tut_ping_location.png', (1486, 417, 34, 39), 0.92):
        pynput.mouse.Controller().click(pynput.mouse.Button.middle)
        time.sleep(0.02)
        pynput.mouse.Controller().click(pynput.mouse.Button.middle)
        time.sleep(0.02)
        pynput.mouse.Controller().click(pynput.mouse.Button.middle)
        pynput.mouse.Controller().click(pynput.mouse.Button.middle)
        pynput.mouse.Controller().click(pynput.mouse.Button.middle)
        time.sleep(0.02)
        while image('tut_e_pickup_ammo_ping.png', (915, 380, 211, 130), 0.94) is None:
            time.sleep(0.02)
        pynput.mouse.Controller().click(pynput.mouse.Button.middle)
        move_mouse(-30, -30)
        move_mouse(-35, -40)
        pynput.mouse.Controller().press(pynput.mouse.Button.middle)
        move_mouse(-30, -30)
        pynput.mouse.Controller().release(pynput.mouse.Button.middle)


def on_press(key):
    try:
        if key == pynput.keyboard.Key.right:
            # Move the mouse to the right
            print("right")
            # move_mouse(10, 0)
            wasd()
        elif key == pynput.keyboard.Key.left:
            print("left")
            # Move the mouse to the left
            move_mouse(-10, 0)
            # pydirectinput.moveRel(1, 0)
            # pynput.mouse.Controller().move(-5, 0)
        elif key == pynput.keyboard.Key.up:
            # Move the mouse up
            move_mouse(0, -10)
        elif key == pynput.keyboard.Key.down:
            # Move the mouse down
            move_mouse(0, 10)
        elif key.vk and key.vk == 97:
            # Perform left mouse click
            pynput.mouse.Controller().click(pynput.mouse.Button.left)
        elif key.vk and key.vk == 98:
            # Perform right mouse click1
            pynput.mouse.Controller().click(pynput.mouse.Button.right)
        elif key.vk and key.vk == 99:
            # Perform middle mouse click
            pynput.mouse.Controller().press(pynput.mouse.Button.middle)
            time.sleep(0.02)
            print("press")
        elif key.vk and key.vk == 101:
            # Scroll down using the mouse wheel
            pynput.mouse.Controller().scroll(0, 1)
    except AttributeError:
        pass


def on_release(key):
    try:
        if key.vk and key.vk == 99:
            pynput.mouse.Controller().release(pynput.mouse.Button.middle)
            print("release")
    except AttributeError:
        pass


def move_mouse(x, y):
    MOUSEEVENTF_MOVE = 0x0001
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, x, y, 0, 0)


with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
