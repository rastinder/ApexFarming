import pynput.keyboard
import time

# the file to save the events
events_file = "events.txt"

# a list to store the current pressed keys
pressed_keys = []

# a listener to record keyboard events


def on_press(key):
    global pressed_keys
    pressed_keys.append(key)
    with open(events_file, "a") as f:
        try:
            f.write("press,{},{}\n".format(key.char, time.time()))
        except:
            f.write("press,{},{}\n".format(key, time.time()))
            


def on_release(key):
    global pressed_keys
    pressed_keys.remove(key)
    with open(events_file, "a") as f:
        try:
            f.write("release,{},{}\n".format(key.char, time.time()))
        except:
            f.write("release,{},{}\n".format(key, time.time()))


# start the keyboard listener
keyboard_listener = pynput.keyboard.Listener(
    on_press=on_press, on_release=on_release)
keyboard_listener.start()
try:
    print("Recording... Press 'esc' to stop.")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
# stop recording
keyboard_listener.stop()
