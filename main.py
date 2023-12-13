# in case script stoped for an hour its recommended to close apex.
import threading
import time
import requests
import subprocess
import pyautogui
import keyboard
import pydirectinput
import cv2
import numpy as np
import os
import sys
import random
import io
import GPUtil
import ctypes
import math
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
pc_username = os.getlogin()
print(pc_username)
for i in range(5):
    print(f'Time left: {5-i} seconds', end='\r')
    time.sleep(1)
print(' ' * 20, end='\r')
print('Done!')




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
                    if level == 'wrong_pass':
                        continue
                    elif int(level) <= 19:
                        # Print the first username and password
                        return user[0].split("\t")
                        # username, password = line.strip().split("\t")
        except Exception as e:
            print("no txt file found")
            try:
                user = subprocess.run(
                    ["python", "user.py", 'get', mode_to_play], capture_output=True, check=True, timeout=300000)
                result = user.stdout.decode("utf-8").strip().split(" ")
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
                print(
                    f"Level of username {username_to_update} is updated to {level}.")
        except:
            print("Error while updating level of username.")
            result = subprocess.run(["python", "user.py", 'push',
                                    username_to_update[0], username_to_update[1], level], capture_output=True, check=True, timeout=3000000)
            print(result)


class TimeoutError(Exception):
    pass


def delay_multiplier():
    print('rnning function delay_multiplier')
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            vram_total = gpu.memoryTotal
            print('vram: ', vram_total)
            if vram_total <= 2049:
                print('2gb ram')
                return 2.5
            elif vram_total <= 4100:
                print('4gb ram')
                return 1
            else:
                print('4+gb ram')
                return 1
    except:
        print('error')
        return 1
    print('error2')
    return 1


def error_handling1():
   # return
    print('error handling start')
    old_times = 0
    click_count = 0
    global common_var
    if old_times == 0:
        # while True:
        # if common_var == 1:
        start_time = time.time()
        while time.time() - start_time < 15*DelayMultiplier:
            # times = int(30 - (time.time() - start_time))
            # if old_times != times:
            # print(f'error handling remaining time: {times} secs')
            # old_times = times
            if common_var == 1:
                # y
                # print('error handling timer rest')
                start_time = time.time()
                common_var = None
            if image('continue_afk.png', (0, 0, 1920, 1080), 0.94, True):
                start_time2 = time.time()
                while time.time() - start_time2 < 10:
                    if image('continue_afk.png', (0, 0, 1920, 1080), 0.84, True) or image('startmanu.png', (810, 599, 300, 103), 0.93, True):
                        click_count = click_count+1
                        print('click_count: ', click_count)
                        if click_count >= 10:
                            print('needs restart')
                            sys.exit("continue click count exceeded")
                            # send_screen('needs restart')
            # after temp trio challaenge completed comes
            if image('news_windnow.png', (813, 22, 93, 42), 0.94) or image('space_to_skip_matchsummary.png', (875, 900, 51, 112), 0.84):
                pydirectinput.keyDown('esc')
                time.sleep(.05)
                pydirectinput.keyUp('esc')
                time.sleep(.05*DelayMultiplier)
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


common_var = None
thread = threading.Thread(target=error_handling1)


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
        raise TimeoutError(
            f"{func.__name__} exceeded time limit of {time_limit:.2f}s")

    return wrapper


def send_screen(message='Hi'):
    # fearbot
    bot_token = ''
    chat_id = ''
    # pclogs
    bot_token = ''
    chat_id = ''

    def upload_screenshot():
        # take a screenshot of the current screen
        screen = pyautogui.screenshot()
        # create an in-memory file object to store the screenshot
        screen_buffer = io.BytesIO()
        screen.save(screen_buffer, 'PNG')
        # rewind the buffer to the beginning
        screen_buffer.seek(0)

        # upload the screenshot file to Telegram and send it as a photo
        url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
        response = requests.post(
            url, data={'chat_id': chat_id, 'caption': message + " " + os.environ['USERNAME']}, files={'photo': ('screenshot.png', screen_buffer, 'image/png')})
        # close the buffer and delete the contents to free up memory
        screen_buffer.close()
        del screen_buffer

    # create a new thread to upload the screenshot
    t = threading.Thread(target=upload_screenshot)
    t.start()

    # don't wait for the thread to complete
    return


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
            pass
        except OSError as e:
            print("Error: Screen grab failed -", e)
        if time.time() - start_time > (max_wait_time*DelayMultiplier) and already_sent == None:
            send_screen("cant find in " + str(max_wait_time *
                        DelayMultiplier) + " sec " + image_file)
            already_sent = 1
            return
    if click == True:
        long_click(img[0], img[1])
    return img


def long_click(x, y):
    # Move the mouse cursor slowly to a specified position (x, y)
    start_x, start_y = pydirectinput.position()
    end_x, end_y = x, y
    distance = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
    steps = int(distance / 25) + 1  # 5 pixels per step
    duration = random.uniform(0.01, .05)
    for i in range(steps):
        t = i / steps
        px = int(start_x + (end_x - start_x) * t)
        py = int(start_y + (end_y - start_y) * t)
        pydirectinput.moveTo(px, py)
        #time.sleep(duration / steps)
    
    pydirectinput.mouseDown(x, y)
    time.sleep(hold_click_time)
    pydirectinput.mouseUp()


def image(image_file, region, confidence, click=False, debug_msg=True):
    img = None
    # time.sleep(universal_delay)
    try:
        x1, y1, x2, y2 = region
        y1 = max(y1 - 30, 0)
        y2 = min(y2 + 30, 1070)
        region = x1, y1, x2, y2
    except Exception as e:
        print(e)
    if img is None:
        try:
            img = pyautogui.center(pyautogui.locateOnScreen(
                image_file, grayscale=True, region=region, confidence=confidence))
        except TypeError:
            return None
        except OSError as e:
            print("Error: Screen grab failed -", e)
            return None
        if click == True:
            long_click(img[0], img[1])
            print("clicked: " + image_file)
            return img
        if debug_msg == True:
            print("located: " + image_file)
        return img
    return None


def what_is_on_screen():
    print(f"Running function: what_is_on_screen")
    if image('in_mainmenu.png', (1807, 962, 70, 66), 0.94):
        return 'in_mainmenu'
    if image('InGame.png', (500, 1031, 30, 27), 0.94, False) != None:
        return 'InGame'
    else:
        return 'desktop'


def openaccounts(mode_to_play):
    if platform == 'ea':
        print('running ea platform')
        # get username passowrd
        username, password = account_handle.get_acc_details(mode_to_play)
        # run ea app
        subprocess.run(
            ['C:\\Program Files\\Electronic Arts\\EA Desktop\\EA Desktop\\EALauncher.exe'], shell=True)
        # open ea account
        run_ea(username, password)  # return pid or none
        return username, password
    elif platform == 'steam':
        # get username passowrd
        username, password = account_handle.get_acc_details(mode_to_play)
        # open steam account
        run_steam(username, password)  # return pid or none
        return username, password

    else:
        print('wrong platform selected')


def run_steam(username, password):
    print(f"Running function: run_steam")
    subprocess.run(
        ['C:\\Program Files (x86)\\steam\\steam.exe app -novid -dev applaunch - login ', username, password, '-fps 20'], shell=True)
    return "in_game"


def run_ea(username, password):
    skip_video = False  # if we are  playing first time then we need to skip video but its irrelevent as we have to  play tut manually
    print(f"Running function: run_ea")
    wait_and_click_on_image('ea_login.png',
                            (753, 430, 64, 22), 0.80)

    pyautogui.typewrite(username)
    wait_and_click_on_image('enter_pass.png', (755, 516, 89, 22), 0.94, False)
    pyautogui.press("tab")
    pyautogui.typewrite(password)
    image('keep_sign_in_check.png', (748, 604, 46, 43), 0.94, True)
    time.sleep(.3)
    pyautogui.press("enter")
    time.sleep(3)  # remove if you dont want
    start_time = time.time()
    while time.time() - start_time < 30*DelayMultiplier:
        if image('wrong_pass.png', (879, 588, 75, 25), 0.94):
            print("wrong pass")
            account_handle.push_acc_details(
                account_handle.get_acc_details(mode_to_play), 'wrong_pass')
            kill_ea()
            openaccounts(mode_to_play)
            return "in_game"
        elif image('technical_diffcuilty.png', (975, 591, 77, 23), 0.94):
            print("technical_diffcuilty pass")
            account_handle.push_acc_details(
                account_handle.get_acc_details(mode_to_play), 'technical_diffcuilty')
            kill_ea()
            send_screen('techincal diffcuilty '+username+ " "+ password)
            time.sleep(86400) # full day
            os.system("reboot")
            #openaccounts(mode_to_play)
            return "in_game"
        elif image('apex_icon_afterlogin.png', (293, 305, 77, 151), 0.94):
            break
        elif image('ban.png', (1007, 392, 99, 35), 0.94):
            print('ban')
            account_handle.push_acc_details(
                account_handle.get_acc_details(mode_to_play), 'ban')
            kill_ea()
            openaccounts(mode_to_play)
            return "in_game"
        elif image('ok_loginfailed.png', (1128, 517, 147, 129), 0.94):
            send_screen('some kind of error')
            kill_ea()
            openaccounts(mode_to_play)
            return "in_game"
        elif (image('new_acc_cross.png', (0, 240, 1920, 270), 0.94)) or (image('ea_afterlogon_window.png', (940, 108, 39, 31), 0.94) and time.time() - start_time > 25):
            cross_check_timer = time.time()

            print('we will be insalling apex now time =',
                  time.time() - start_time)
            while time.time() - cross_check_timer < 6*DelayMultiplier:
                if image('new_acc_cross.png', (0, 240, 1920, 270), 0.94, True):
                    skip_video = True
                    break
            print('type apex')
            image('searchbox.png', (658, 173, 58, 25), 0.94, True)
            pyautogui.typewrite('apex')
            pyautogui.keyDown("enter")
            time.sleep(.03)
            pyautogui.keyUp("enter")
            # click on install_apex_in_lib.png
            img = wait_and_click_on_image(
                'install_apex_in_lib.png', (483, 431, 92, 27), 0.94, False)
            long_click(img[0]+60, img[1]+60)
            # wait_and_click_on_image('download.png', (978, 743, 102, 29), 0.94)
            while image('next.png', (1064, 696, 67, 33), 0.94, False) == None:
                image('download.png', (978, 743, 102, 51), 0.94, True)
                if image('network_error.png', (1238, 166, 75, 32), 0.94):
                    send_screen('network_error, sad')
                    os.system("shutdown /r /t 1")
                    sys.exit()
                if image('play_button.png', (976, 752, 122, 54), 0.92):
                    break
            while image('play_button.png', (976, 752, 122, 54), 0.92) is None:
                # missing next button
                # its a hiidden next button
                img = image(
                    'next.png', (1064, 696, 67, 33), 0.94, False)
                if image('manage.png', (874, 752, 114, 54), 0.80):
                    break
                while image('next.png', (1064, 696, 67, 33), 0.94, True):
                    time.sleep(1)  # its a hiidden next button
                if image('play_button.png', (976, 752, 122, 54), 0.92):
                    break
                try:
                    long_click(img[0], img[1])
                    break
                except:
                    print('IMG next not found')
    else:
        print('different kind of problem')
        # send_screen("looking for: apex screen that is now found")

    # click on apex_icon_afterlogin.png
    wait_and_click_on_image('apex_icon_afterlogin.png',
                            (293, 305, 77, 151), 0.94)
    while image('play_button.png', (976, 752, 122, 54), 0.92) is None:
        if image('update_game.png', (966, 759, 128, 42), 0.83, True):
            print("updating")
            # click on continue_update.png
            wait_and_click_on_image(
                'continue_update.png', (1015, 679, 123, 41), 0.83)
            time.sleep(5)
        elif image('manage.png', (874, 752, 114, 54), 0.80):
            break

    # click on viewproperties.png
    while image('viewproperties.png', (887, 790, 153, 50), 0.94, True) is None:
        # click on manage.png
        wait_and_click_on_image('manage.png', (874, 752, 114, 54), 0.80)
        time.sleep(.26)

    # click on properties.png
    wait_and_click_on_image('properties.png', (737, 307, 111, 30), 0.94, False)
    if image('typearg.png', (675, 551, 573, 150), 0.94, True):
        time.sleep(.02)
        pyautogui.typewrite("-dev -novid")
        time.sleep(.05)
    # click on save_arg.png
    wait_and_click_on_image('save_arg.png', (1051, 743, 93, 55), 0.91)
    time.sleep(.06)
    # click on play_button.png
    wait_and_click_on_image('play_button.png', (976, 752, 122, 54), 0.92)
    cloudsync_Fix()

    wait_and_click_on_image('loading_screen.png',
                            (0, 0, 1920, 1080), 0.91, False)
    # click on startmanu.png
    wait_and_click_on_image(
        'startmanu.png', (810, 599, 300, 103), 0.93, True, 160)  # change pic so retry te v click kre
    image('startmanu.png', (810, 599, 300, 103), 0.93, True)
    while image('video_skip.png', (825, 417, 271, 76), 0.86):
        time.sleep(0)
    if skip_video == False:
        start_time = time.time()
        while time.time() - start_time < (3*DelayMultiplier):
            if image('black_screen_loading.png', (1770, 949, 26, 52), 0.94):
                break
        else:
            skip_video = True
    '''''
    if skip_video == False:
        start_time = time.time()
        while image('in_mainmenu.png', (1807, 962, 70, 66), 0.94, False) is None:
            if time.time() - start_time > (5*DelayMultiplier):
                skip_video = True
                break
        else:
            print('main menu yeeeeeee')
    '''
    if skip_video == True:
        print(time.time() - start_time)
        print('skip video')
        pyautogui.keyDown('alt')
        time.sleep(.01)
        pyautogui.keyDown('F4')
        time.sleep(.015)
        pyautogui.keyUp('F4')
        pyautogui.keyUp('alt')
        wait_and_click_on_image('play_button.png', (976, 752, 122, 54), 0.92)
        start_time = time.time()
        while time.time() - start_time < 2*DelayMultiplier:
            if image('launch_game.png', (992, 590, 124, 28), 0.94, True):
                break
            if image('cloud_save.png', (691, 497, 45, 42), 0.94, True):
                wait_and_click_on_image(
                    'confirm_cloudsave_window.png', (1040, 685, 92, 29), 0.94)
                wait_and_click_on_image(
                    'yes_cloud_save.png', (988, 590, 123, 30), 0.94)
        wait_and_click_on_image(
            'startmanu.png', (810, 599, 300, 103), 0.93, True, 160)
        time.sleep(.21)
        image('startmanu.png', (810, 599, 300, 103), 0.93, True)
        while image('video_skip.png', (825, 417, 271, 76), 0.86):
            time.sleep(0)
        start_time = time.time()
        while time.time() - start_time < (3*DelayMultiplier):
            if image('black_screen_loading.png', (1770, 949, 26, 52), 0.94):
                start_time = time.time()
    print("in game")
    return "in_game"


def cloudsync_Fix():
    # wait for loading screen or launch_game error due to sync
    start_time = time.time()
    while time.time() - start_time < 4:
        print('launch game or cloud save')
        if image('launch_game.png', (992, 590, 124, 28), 0.94, True):
            break
        if image('cloud_save.png', (691, 497, 45, 42), 0.94, True):
            wait_and_click_on_image(
                'confirm_cloudsave_window.png', (1040, 685, 92, 29), 0.94)
            wait_and_click_on_image(
                'yes_cloud_save.png', (988, 590, 123, 30), 0.94)


def find_lvl(shape_tolerance=0.1):
    region = (792, 117, 83, 83)

    while True:
        screen = np.array(pyautogui.screenshot(region=region))
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 200, 500)
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            largest_contour = max(contours, key=cv2.contourArea)
        except:
            print('rect bot found')
            return
        try:
            rect = cv2.minAreaRect(largest_contour)
            if abs(1 - rect[1][0] / rect[1][1]) < shape_tolerance:
                area = int(rect[1][0] * rect[1][1])
                if 2800 <= area <= 2960:
                    #image send function here
                    return 1
                print('lvl not found', area)
        except:
            print('rect is not square')
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
    while image(
            'in_mainmenu.png', (1807, 962, 70, 66), 0.94, False) is None:  # esc or continue
        error_handling()
        if image('exit_to_desktop.png', (860, 606, 198, 35), 0.94):
            keyboard.press_and_release("esc")
    error_handling()

    start_time = time.time()
    # need something robust; lvl 19 di pic lelo te odo hi activate hove jdo lvl 19 disse
    while time.time() - start_time < 8*DelayMultiplier:
        if find_lvl():
            print('lvl found')
            time.sleep(.1)
            break
        if image('training.png', (58, 834, 128, 31), 0.94):
            checks.append("lvl_ok")
            checks.append('training.png')
            checks.append("ready_state")
            return checks
    else:
        print('lvl not found in time')

    if image('lvl_20.png', (809, 139, 50, 35), 0.94) or image('select_button.png', (100, 935, 302, 78), 0.94):
        lvl_pic()
        return 'lvl_20'
    else:
        checks.append("lvl_ok")
    # check if its first game as TDM is available after 3 matches
    # assuming we will only play arena or tdm if we desided to play other modes permanently then we need to make another check where we will check if trios is present as well
    # we think it doesnt find match and fill.png isnt visible even though it is supposed to so we added canceled match count to skip this
    if image('training.png', (58, 834, 128, 31), 0.94):
        checks.append('training.png')
        checks.append("ready_state")
        return checks
    elif image('fill.png', (83, 662, 60, 34), 0.94, False) is None and cant_find_match < 2 and image('trios.png', (55, 833, 84, 31), 0.94):
        checks.append('temp_trio')
    elif image('fill.png', (83, 662, 60, 34), 0.94, False) is None and mode_to_play != 'training.png' and cant_find_match < 2:
        checks.append('find_tdm.png')
    elif mode_to_play != 'training.png':
        print("changing mode")
        # click on changemode.png
        # some times a pop up window appear so we need to fix thatand cant_find_match < 2
        wait_and_click_on_image(
            'changemode.png', (348, 833, 63, 61), 0.92, True)
        wait_and_click_on_image(
            'select_a_game_mode_window.png', (702, 27, 114, 36), 0.94, False)
        time.sleep(0.01*DelayMultiplier)
        long_click(1031, 500)
        start_time = time.time()
        while time.time() - start_time < 5:
            if image('playlist_unavailable.png', (1000, 632, 126, 30), 0.94):
                return 'False'
            if image('ready_state.png', (161, 951, 141, 41), 0.94):
                checks.append('find_tdm.png')
                checks.append("ready_state")
                return checks
        else:
            long_click(1031, 500)
            time.sleep(.2*DelayMultiplier)
            if image('ready_state.png', (161, 951, 141, 41), 0.94):
                checks.append('find_tdm.png')
                checks.append("ready_state")
                return checks
    elif mode_to_play == 'training.png':
        # if mode_to_play is traing then we only do traing and so we return , in future we can do traingin on the go then checks.append('training.png') will pe present
        return 'training_done'

    if image('ready_state.png', (161, 951, 141, 41), 0.94):
        checks.append("ready_state")
    else:
        print("ready state not found take a ss")
        return 'False'
    return checks


def click_ready():
    if image('ready_state.png', (161, 951, 141, 41), 0.94, True):
        start_time = time.time()
        while True:
            if time.time() - start_time < DelayMultiplier*2:
                if image('cancel_means_searching_for_match.png', (147, 951, 171, 43), 0.90, False):
                    break
            else:
                print("cant find cancel_means_searching_for_match")
                error_handling()
                time.sleep(.5*DelayMultiplier)
                image('ready_state.png', (161, 951, 141, 41), 0.94, True)
                start_time = time.time()


def search_match():
    print(f"Running function: search_match")
    if image('fill.png', (83, 662, 60, 34), 0.94):
        return 'False'

    # click on ready_state.png
    lvl_pic()
    click_ready()

    start_time = time.time()
    while image('cancel_means_searching_for_match.png', (147, 951, 171, 43), 0.90, False, False) != None:
        if (time.time() - start_time) > 1800:
            send_screen('no match found in 30 mins possible ban')
            start_time = time.time()
    print('cancel button gone so either in match or got auto canceled')
    time.sleep(2*DelayMultiplier)
    global cant_find_match
    if image('ready_state.png', (161, 951, 141, 41), 0.9, False):
        # increase 1 num each time match isnt found contiuely
        cant_find_match = cant_find_match + 1
        print(F"cant_find_match count = {cant_find_match}")
        return 'False'  # ek war trios mode lag gea so false return kita because dubara arena select krna c
    cant_find_match = 0
    update_status('active')
    error_handling()
    return 'match_found'


def wasd(action=1):

    def sub_wasd():
        pydirectinput.keyDown('w')
        time.sleep(.6)
        pydirectinput.press('shift')
        time.sleep(.1)
        pydirectinput.keyDown('ctrlleft')
        time.sleep(1)
        pydirectinput.keyUp('w')
        pydirectinput.keyUp('ctrlleft')

    if action == 1:
        t = threading.Thread(target=sub_wasd)
        t.start()

def move_mouse():
    def sub_move_mouse():
        start_time = time.time()
        sec_run = random.uniform(1.1, 2)
        while (time.time() - start_time) < sec_run:
            ctypes.windll.user32.mouse_event(0x0001, random.choice([random.randint(-20, -10), random.randint(10, 20)]), random.choice([random.randint(-3, -0), random.randint(0, 3)]), 0, 0)
    t = threading.Thread(target=sub_move_mouse)
    t.start()


def long_click_random():
    def sub_long_click():
        sec_run = random.uniform(.5, 2)
        pydirectinput.mouseDown()
        time.sleep(sec_run)
        pydirectinput.mouseUp()
    t = threading.Thread(target=sub_long_click)
    t.start() 
def run_walkbot():
    print(f"Running function: run_walkbot")
    loadout_selection = 1
    in_game = False
    key_press = False
    start_time = time.time()
    kkeys = ['w', long_click_random, move_mouse, 'a', 's', 'd', 'space', 'ctrl', 'shift', wasd]
    while True:  # add server error etc etc
        while image('InGame.png', (500, 1031, 30, 27), 0.94, False, False) != None:
            # circumfrence
            in_game = True
            if key_press == False:
                kkey = random.choice(kkeys)
                if callable(kkey):
                    try:
                        kkey()
                    except:
                        print(kkeys)
                else:
                    keyboard.press(kkey)
                start_time = time.time()
                key_press = True
            elif time.time() - start_time >= 3 and key_press == True:
                if not callable(kkey):
                    keyboard.release(kkey)
                key_press = False
        else:
            if key_press == True:
                if not callable(kkey):
                    keyboard.release(kkey)
                key_press = False
            if in_game == False:
                image('esc_before_first_tdm.png',
                      (904, 886, 48, 33), 0.8, True)
            if image('select_spawn_window.png', (1080, 948, 28, 25), 0.94):
                image('click_for_control.png', (0, 0, 1920, 1080), 0.84, True)
            error_handling()
        # or image('match_quality_survey_yes.png', (0, 0, 1920, 1080), 0.94):
        if image('match_summary.png', (609, 16, 800, 70), 0.94) or image('space_to_skip_matchsummary.png', (875, 980, 51, 22), 0.85):  # 875, 980, 51, 21
            # press_esc_to_leave_match()
            return 'match_finished'
        # if mode_to_play == 'find_tdm.png':
        if 1 > 0:  # always true check
            if image('game_over_tdm_trio.png', (902, 1019, 112, 53), 0.94, False):
                press_esc_to_leave_match()
                return 'match_finished'
            if loadout_selection:
                if image('select_loadout_in_dm.png', (254, 316, 40, 27), 0.94, True):
                    image('select_loadout_in_dm.png',
                          (254, 316, 40, 27), 0.94, True)
                    loadout_selection = 0

        if image('ready_state.png', (161, 951, 141, 41), 0.9, False):
            print("run function wich ready show ho gea strange")
            return 'False'  # ek war trios mode lag gea so false return kita because dubara arena select krna c


def press_esc_to_leave_match():
    print(f"Running function: press_esc_to_leave_match")
    pydirectinput.keyDown('esc')
    time.sleep(.05)
    pydirectinput.keyUp('esc')
    print("esc pressed")
    start_time = time.time()
    while True:
        if time.time() - start_time < (1.5*DelayMultiplier):
            # click on leave_match.png
            if image('leave_match.png', (881, 610, 159, 27), 0.86, True):
                wait_and_click_on_image(
                    'Yes_leave.png', (821, 660, 56, 74), 0.94, True, 2)
                image('Yes_leave.png', (821, 660, 56, 74), 0.94, True)
                time.sleep(5*DelayMultiplier)
                print("sleep end so break")
                break
        else:
            if image('in_mainmenu.png', (1807, 962, 70, 66), 0.93, False):
                return
            pydirectinput.keyDown('esc')
            time.sleep(.05)
            pydirectinput.keyUp('esc')
            start_time = time.time()
            print("esc pressed again")
            if image('in_mainmenu.png', (1807, 962, 70, 66), 0.93, False):
                return
            error_handling()
            if image('in_mainmenu.png', (1807, 962, 70, 66), 0.93, False):
                return


def end_match(playing=None):
    ban_check = 0
    if playing == 'temp_trio':
        print(f"Running function: end_match")
        wait_and_click_on_image('waitingforplayers.png',
                                (801, 362, 306, 28), 0.94, False)
        press_esc_to_leave_match()
        while image('in_mainmenu.png', (1807, 962, 70, 66), 0.93, False) == None:
            pydirectinput.keyDown('esc')
            time.sleep(.05)
            pydirectinput.keyUp('esc')
            time.sleep(.01)
        return 'in_mainmenu'
    else:
        # if playing == 'find_tdm.png':
        while image('in_mainmenu.png', (1807, 962, 70, 66), 0.93, False) == None:
            pydirectinput.keyDown('esc')
            time.sleep(.05)
            pydirectinput.keyUp('esc')
            time.sleep(.1)
            image('leave_match.png', (881, 610, 159, 27), 0.94, True)
            if image('Yes_leave.png', (821, 660, 56, 74), 0.94, True):
                image('Yes_leave.png', (821, 660, 56, 74), 0.94, True)
                time.sleep(5)
            if image('play_button.png', (976, 752, 122, 54), 0.92, True):
                while True:
                    if image('startmanu.png', (810, 599, 300, 103), 0.93, True):
                        time.sleep(10*DelayMultiplier)
                        if not image('video_skip.png', (825, 417, 271, 76), 0.86):
                            break
                        else:
                            keyboard.press('alt')
                            keyboard.press('F4')
                            time.sleep(1)
                            keyboard.release('F4')
                            keyboard.release('alt')
                            ban_check = ban_check + 1
                            if ban_check == 3:
                                print('ban')
                                send_screen('chai k sath mathhi')
                                account_handle.push_acc_details(
                                    account_handle.get_acc_details(mode_to_play), 'ban')
                                kill_ea()
                                openaccounts(mode_to_play)
                                return 'False'
                            break
        return 'in_mainmenu'

    # arena
    while image('in_mainmenu.png', (1807, 962, 70, 66), 0.93, False) == None:
        print("esc")
        pydirectinput.press('esc')
        image('esc_aftermatch.png', (1691, 1031, 50, 32), 0.94, True)
        # image('esc_aftermatch.png', (0, 880, 1920, 200), 0.94, True)
        if image('space_return_to_lobby.png', (1594, 1028, 238, 42), 0.94) or image('space_return_to_lobby.png', (0, 300, 1920, 780), 0.94, False):
            keyboard.press_and_release("esc")
        # click on leave_match.png
        image('leave_match.png', (881, 610, 159, 27), 0.94, True)
        # click on Yes_leave.png
        if image('Yes_leave.png', (821, 702, 56, 32), 0.94, True):
            time.sleep(5)
    else:
        return 'in_mainmenu'


def changeip():
    return
    commands = ['adb shell cmd connectivity airplane-mode enable',
                'adb shell cmd connectivity airplane-mode disable']
    [subprocess.run(cmd, shell=True) and time.sleep(3) for cmd in commands]
    time.sleep(2)
    return
    subprocess.run("warp-cli disconnect",
                   cwd=r"C:\Program Files\Cloudflare\Cloudflare WARP")
    time.sleep(.5)
    subprocess.run("warp-cli connect",
                   cwd=r"C:\Program Files\Cloudflare\Cloudflare WARP")


def kill_ea():
    print('kill ea')
    try:
        subprocess.run(
            ["taskkill", "/FI", f"USERNAME eq {os.environ['USERNAME']}", "/IM", "r5apex.exe", "/F"])
        subprocess.run(
            ["taskkill", "/FI", f"USERNAME eq {os.environ['USERNAME']}", "/IM", "EALocalHostSvc.exe", "/F"])
        subprocess.run(
            ["taskkill", "/FI", f"USERNAME eq {os.environ['USERNAME']}", "/IM", "EABackgroundService.exe", "/F"])
        subprocess.run(
            ["taskkill", "/FI", f"USERNAME eq {os.environ['USERNAME']}", "/IM", "EADesktop.exe", "/F"])
        subprocess.run(
            ["taskkill", "/FI", f"USERNAME eq {os.environ['USERNAME']}", "/IM", "EADesktop.exe", "/F"])
    except:
        pass
    changeip()


def skip_training():
    print('in functionskip_training')
    # skip training copde
    while True:
        try:
            user = subprocess.run(
                ["python", "skiptrain.py"], capture_output=True, check=True, timeout=600)
            user = user.stdout.decode(
                "utf-8").strip().split('@@', 1)[1].lstrip()
            print("line 923 recieved: ", user)
            if "done" in user:
                print('train finished')
                account_handle.push_acc_details(
                    account_handle.get_acc_details(mode_to_play), 'training_done')
                return
        except:
            print("press alt f4")
            keyboard.press('alt')
            keyboard.press('F4')
            time.sleep(1)
            keyboard.release('F4')
            keyboard.release('alt')
            wait_and_click_on_image(
                'play_button.png', (976, 752, 122, 54), 0.92)
            while image(
                    'startmanu.png', (810, 599, 300, 103), 0.93, True, 160) == None:
                cloudsync_Fix()
            time.sleep(.21)
            image('startmanu.png', (810, 599, 300, 103), 0.93, True)
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
                f"{func.__name__} exceeded time limit of {time_limit:.2f}s")
        return f"{func.__name__} exceeded time limit of {time_limit:.2f}s"
    else:
        return thread.result


def update_status(status):
    def thread_function():
        print('updating ', status)
        account_handle.push_acc_details(
            account_handle.get_acc_details(mode_to_play), status)
        print('updating done')
    thread1 = threading.Thread(target=thread_function)
    thread1.start()
    # thread.join()  # Wait for the thread to complete
    return


# ....................testing start
platform = 'ea'  # ea /steam
debugging = True  # set this to True if in debugging mode
DelayMultiplier = delay_multiplier()
universal_delay = 0.2*DelayMultiplier
hold_click_time = 0.05*DelayMultiplier
try:
    mode_to_play = sys.argv[1]
except:
    mode_to_play = 'find_tdm.png'  # find_arenas_match.png # training.png 'find_tdm.png'
playing = None
cant_find_match = 0  # if match got cancelled too many times we need to do something
print('we are going to train or boost? \n ans: ', mode_to_play)
play_time = time.time()
state = what_is_on_screen()  # desktop, in_menu
print("state: ", state)
if state == 'desktop':
    kill_ea()
    user = openaccounts(mode_to_play)
    play_time = time.time()
if state == 'InGame':
    if run_walkbot() == 'match_finished':
        end_match()
state = 'False'
while True:
    print("state: ", state)
    if len(state) == 3:
        playing = state[1]
        state = search_match()
        if playing == 'temp_trio' and state != 'False':
            state = 'match_finished'
        elif playing == 'training.png' and state != 'False':
            skip_training()
            # state = 'match_finished' # in future we auto mate doing tut
            kill_ea()
            user = openaccounts(mode_to_play)
            play_time = time.time()
            state = 'False'
    if state == 'match_found':
        state = run_walkbot()
    if state == 'match_finished':
        state = end_match(playing)
        playing = None
    if state == 'lvl_20':
        account_handle.push_acc_details(
            account_handle.get_acc_details(mode_to_play), '20')
        kill_ea()
        user = openaccounts(mode_to_play)
        play_time = time.time()
        state = 'False'
    if state == 'training_done':
        account_handle.push_acc_details(
            account_handle.get_acc_details(mode_to_play), 'training_done')
        send_screen('m assuming traing done already')
        kill_ea()
        user = openaccounts(mode_to_play)
        play_time = time.time()
        state = 'False'

    if state == 'False' or state == 'in_mainmenu':
        if (time.time() - play_time) < 21600: # 6 hrs 
            state = set_everything_before_match()
        else:
            account_handle.push_acc_details(
            account_handle.get_acc_details(mode_to_play), 'time_limit')
            kill_ea()
            user = openaccounts(mode_to_play)
            play_time = time.time()



# ....................testing end
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
