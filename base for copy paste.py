import threading
import time
import subprocess


class account_handle:
    @staticmethod
    def get_acc_details():
        try:
            with open("username.txt", "r") as file:
                # Read all lines in the file
                lines = file.readlines()
                # Loop through all lines
                for line in lines:
                    # Split the line into username and password
                    user, level, _ = line.strip().split(",")
                    # Check if "20" is not written after a comma and value is below or equal to 21
                    if level <= 19:
                        # Print the first username and password
                        return user.strip().split("\t")
                        #username, password = line.strip().split("\t")
        except:
            print("no txt file found")

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
                    user, cur_level = line.strip().split(",")
                    # Check if the username matches the username_to_update
                    if username_to_update in user:
                        # Update the level of the username
                        file.write(f"{user},{level}\n")
                    else:
                        # Write the line back to the file
                        file.write(line)
                print(
                    f"Level of username {username_to_update} is updated to {level}.")
        except:
            print("Error while updating level of username.")


class TimeoutError(Exception):
    pass


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


def function_1():
    # your code here
    time.sleep(1)


def function_2():
    # your code here
    time.sleep(2)


def function_3():
    # your code here
    time.sleep(11)


def openaccounts():
    # get username passowrd
    username, password = account_handle.get_acc_details()
    # open steam account
    run_steam(username, password)  # return pid or none


def run_steam(username, password):
    launch_options = [
        "--low",  # High priority
        "--no-browser",  # Don't launch the web browser
        "-login", username, " ", password,  # Login option
        "fps_max 20",
        "+exec autoexec"  # Execute autoexec configuration file
    ]

    subprocess.Popen(["steam", "-applaunch", "407530"] + launch_options)
    return


debugging = True  # set this to True if in debugging mode


def run_with_time_limit(func, time_limit=5):
    print(f"Running function: {func.__name__} with time_limit: {time_limit}")
    enforced_function = enforce_time_limit(func, time_limit)
    thread = threading.Thread(target=enforced_function)
    thread.start()
    thread.join(time_limit)
    if thread.is_alive():
        raise TimeoutError(
            f"{func.__name__} exceeded time limit of {time_limit:.2f}s")


while True:
    try:
        run_with_time_limit(function_1)
        run_with_time_limit(function_2, time_limit=None)
        run_with_time_limit(function_3, time_limit=1)
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
