import pynput
import time
import pydirectinput
import ctypes

def on_press(key):
    try: 
        if key == pynput.keyboard.Key.right:
            # Move the mouse to the right
            print("right")
            move_mouse(1, 0)
            pydirectinput
        elif key == pynput.keyboard.Key.left:
            print("left")
            # Move the mouse to the left
            move_mouse(-1, 0)
            #pydirectinput.moveRel(1, 0)
            #pynput.mouse.Controller().move(-5, 0)
        elif key == pynput.keyboard.Key.up:
            # Move the mouse up
            move_mouse(0, -1)
        elif key == pynput.keyboard.Key.down:
            # Move the mouse down
            move_mouse(0, 1)
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
