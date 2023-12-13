from pynput.keyboard import Key, Controller
import time

# the file to read the events from
events_file = "events.txt"
# replay the events
print("Replaying...")
keyboard = Controller()
# Read the keystroke data from the file
with open('events.txt', 'r') as file:
    events = file.readlines()

# Initialize a variable to store the previous time
previous_time = 0

# Loop through the events
for event in events:
    # Split the event into key, action, and time
    action,keys, time1 = event.strip().split(',')
  
    #    converting string to float
    Float = float(time1)  
  
    # Calculate the delay as the difference between the current and previous times
    delay = Float - previous_time
    subtract_Float = lambda Float, previous_time : Float - previous_time

    previous_time = float(Float)

    # Sleep for the delay
    print(subtract_Float(Float, previous_time))
    time.sleep(subtract_Float(Float, previous_time))

    # Press or release the key
    keys.strip('"')
    if action == 'press':
        print(keys)
        keyboard.press(keys)
    elif action == 'release':
        keyboard.release(keys)

# Stop the keyboard controller
#keyboard.stop()


# wait for the replay to finish
time.sleep(1)
# reset the keyboard