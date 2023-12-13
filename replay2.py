import keyboard
import time

# Read the events from the text file
events = []
with open('events.txt', 'r') as file:
    for line in file:
        event = line.strip().split(',')
        key = event[1].strip("'")
        events.append((event[0], key, float(event[2])))

# Replay the events
for event in events:
    action, key, timestamp = event
    delay = timestamp - time.time()
    
ab    if delay > 0:
        time.sleep(delay)
    if action == 'press':
        keyboard.press(key)
    else:
        keyboard.release(key)
