import string
import os
import sys
from time import sleep
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from twocaptcha import TwoCaptcha
import random
import re
import time
import subprocess
from datetime import datetime
# from pytz import timezone
solver = TwoCaptcha('ab64599f9baded9ee06e9ba8d21c5e71')

driver = Chrome(use_subprocess=True)
first_names = ['Aiyden', 'Bexley', 'Cayleb', 'Daxx', 'Ellyot', 'Fynlee',    'Graesyn', 'Huxston', 'Izayiah', 'Jaxxyn', 'Kaedn', 'Lisbeth',    'Maksym', 'Nylah', 'Oaklyn', 'Prinz', 'Quillan', 'Ravynn',    'Santanna', 'Thorn', 'Ulrick', 'Vaelen', 'Wyll', 'Xzander',    'Ysrael', 'Zael', 'Aarik', 'Brynnlee', 'Cyler', 'Dael',    'Eirik', 'Fynnegan', 'Gryffin', 'Huxleigh', 'Izael', 'Jaxsten',    'Kashtyn', 'Landynn', 'Makiah', 'Nyxen', 'Owynn', 'Pryor',    'Quinnten', 'Rael', 'Stryder', 'Thorrin', 'Urie', 'Vail',    'Wylder', 'Xael', 'Yarrow',
               'Zayvion', 'Aarush', 'Brixtyn',    'Cedar', 'Dreyden', 'Elyas', 'Fintan', 'Gaelen', 'Haidyn',    'Iziah', 'Jaxtyn', 'Kamdyn', 'Landry', 'Maddoxx', 'Navi',    'Oden', 'Paxon', 'Qays', 'Rorik', 'Sylas', 'Tavian',    'Urien', 'Viggo', 'Weylyn', 'Xaden', 'Yorick', 'Zadok',    'Abrielle', 'Briar', 'Chesney', 'Daela', 'Ellyana', 'Feryn',    'Gwendolynn', 'Haisley', 'Ilysse', 'Jordis', 'Kynzleigh', 'Lilou',    'Maelle', 'Niamh', 'Olyviah', 'Pryce', 'Quill', 'Rielle',    'Saria', 'Taisley', 'Uriah', 'Vaeda', 'Wylde', 'Xaela',    'Ysadora', 'Zailey']


def changeip():
    return
    subprocess.run("warp-cli disconnect",
                   cwd=r"C:\Program Files\Cloudflare\Cloudflare WARP")
    sleep(.5)
    subprocess.run("warp-cli connect",
                   cwd=r"C:\Program Files\Cloudflare\Cloudflare WARP")


def num_of_emails():
    num_emails = 0
    while num_emails == 0:
        table = driver.find_element(By.ID, 'messagelist')

    # find all the rows in the table
        rows = table.find_elements(By.TAG_NAME, 'tr')

    # get the number of rows excluding the header row
        num_emails = len(rows) - 1

    # print the number of emails
    print(f'Number of emails: {num_emails}')
    return num_emails


def get_email_subject_of_latest_email():
    # find the latest email row and click on it
    latest_email = driver.find_element(
        By.CSS_SELECTOR, 'tr.message:first-child a')
    latest_email.click()
    # Locate the email element that contains the subject
    email_subject_element = driver.find_element(
        By.XPATH, "//span[contains(@class, 'subject')]")

    # Get the text of the email subject
    email_subject = email_subject_element.text

    # Print the email subject
    print(email_subject)


def open_roundcube(email, password):

    # wait for the inbox page to load
    lets_return = False
    driver.get(email_site)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, '_user'))).send_keys(email)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
        (By.NAME, '_pass'))).send_keys(password + "\n")
    for i in range(0, 3):
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'messagelist')))
            lets_return = True
            break
        except:
            driver.get(email_site)
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.NAME, '_user'))).send_keys(email)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                (By.NAME, '_pass'))).send_keys(password + "\n")
    if lets_return == True:
        return
    else:
        return 'wrong_pass_email'


def last_mail_time():
    utc = timezone('UTC')
    span_elements = driver.find_elements(By.CLASS_NAME, 'date.skip-on-drag')
    now = datetime.now()

    for span in span_elements:
        # Extract the date/time string from the span element using the 'text' property
        date_string = span.text

        # Extract the time string using regular expressions
        match = re.search(r'\d{1,2}:\d{2}', date_string)
        if match:
            time_string = match.group()
            if len(time_string) == 5:
                time_string = '0' + time_string

            # Convert the time string to a datetime object
            date_object = datetime.strptime(
                time_string, '%H:%M' if len(time_string) == 5 else '0%H:%M')

            # If the date string also contains the date, extract and use it
            match = re.search(r'\d{4}-\d{2}-\d{2}', date_string)
            if match:
                date_string = match.group()
                date_object = datetime.strptime(
                    date_string + ' ' + time_string, '%Y-%m-%d %H:%M')
            else:
                # If the date string does not contain the date, use the current date
                date_object = datetime.combine(
                    datetime.now().date(), date_object.time())

            # Calculate the time difference in minutes
            time_difference = (now - date_object).total_seconds() / 60

            # Print the time difference
            print(
                f'Time difference for {date_string}: {time_difference:.2f} minutes')


def wait_for_new_mail():
    previous_emails = num_of_emails()
    curent_emails = previous_emails
    # while True:
    # last_mail_time()
    # sleep(2)
    start_time = time.time()
    while time.time() - start_time < 10:
        driver.refresh()
        current_emails = num_of_emails()
        if previous_emails != current_emails:
            break


def generate_password():
    min_length = 8
    max_length = 12
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    password = ""
    while len(password) < min_length or len(password) > max_length or not any(c.islower() for c in password) or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
        password = "".join(random.choice(lowercase_letters + uppercase_letters + digits)
                           for _ in range(random.randint(min_length, max_length)))
    print('password: %s' % password)
    while len(password) > 12:
        password = generate_password()
    return password


def generate_username1():
    first_names = ['Avery', 'Bailey', 'Cameron', 'Dakota', 'Elliott', 'Frankie', 'Gray', 'Harley', 'Jordan', 'Kendall',
                   'Logan', 'Morgan', 'Parker', 'Quinn', 'Reese', 'Rowan', 'Sage', 'Spencer', 'Taylor', 'Valentine', 'Winter', 'Zephyr']
    second_names = ['Ace', 'Alpha', 'Apex', 'Berserk', 'Blaze', 'Champion', 'Cobra', 'Dragon', 'Eagle', 'Falcon', 'Glitch', 'Hawk', 'Hunter', 'Jaguar',
                    'Knight', 'Legend', 'Maverick', 'Ninja', 'Omega', 'Phoenix', 'Pirate', 'Raptor', 'Rebel', 'Samurai', 'Shadow', 'Sniper', 'Warrior', 'Wolf', 'Zombie']
    last_names = ['Black', 'Blade', 'Blaze', 'Dark', 'Death', 'Dragon', 'Fire', 'Fury', 'Ghost', 'Hunter',
                  'Knight', 'Legend', 'Ninja', 'Phoenix', 'Rebel', 'Shadow', 'Slayer', 'Storm', 'Thunder', 'Warrior']
    suffixes = ['Gaming', 'Player', 'Warrior', 'Master',
                'Legend', 'Hunter', 'Assassin', 'Champion', 'Ninja', 'Sniper']

    separator = random.choice(['_', '.', '-', ''])

    # Randomly decide whether to use a middle name
    use_middle_name = random.choice([True, False])
    if use_middle_name:
        middle_name = random.choice(second_names)
        word_choices = [random.choice(
            first_names), middle_name, random.choice(last_names)]
    else:
        word_choices = [random.choice(first_names), random.choice(last_names)]

    random.shuffle(word_choices)

    # Randomly decide whether to add a number to the username
    add_number = random.choice([True, False])
    if add_number:
        random_number = random.randint(100, 999)
        word_choices.append(str(random_number))

    # Randomly decide whether to add a suffix to the username
    add_suffix = random.choice([True, False])
    if add_suffix:
        suffix = random.choice(suffixes)
        word_choices.append(suffix)

    # Randomly choose the number of characters to remove
    num_chars_to_remove = random.randint(5, 15)

    # Randomly remove characters from the username
    username = separator.join(word_choices)
    for i in range(num_chars_to_remove):
        if len(username) <= 1:
            break
        index = random.randint(0, len(username) - 1)
        username = username[:index] + username[index+1:]
    print('username: %s' % username)
    while len(password) > 12 or len(password) <= 4:
        password = generate_password()
    return username


def click_on_reset():
    # find the tag and click it to open in a new tab
    iframe = driver.find_element(By.ID, 'messagecontframe')
    driver.switch_to.frame(iframe)
    # find the element containing the text "signin.ea.com" and print the text
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.
        XPATH, "//*[contains(text(), 'signin.ea.com')]")))
    print(element.text)
    driver.get(element.text)
    new_password = generate_password()
    print("new password= " + new_password)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'password'))).send_keys(new_password + "\n")
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'btnSubmit'))).click()
    return new_password


def open_ea_to_change_pass(email):
    driver.get('https://www.ea.com/login')
    sleep(2)
    driver.find_element(By.ID, 'forget-password').click()
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, 'email'))).send_keys(email)
    captcha_element = driver.find_element(By.ID, 'captchaImg')
    captcha_element.screenshot('captcha.png')
    while True:
        try:
            result = solver.normal('captcha.png')
            sleep(2)
            break
        except Exception as e:
            print(f'Error solving captcha: {e}')
    code = result['code']
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'recaptcha_response_field'))).send_keys(code + "\n")
    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'backToLogin')))
            break
        except:
            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'form-error-invalid-emailOrId')))
                return 'invalid_eamil'
            except:
                pass
            try:
                driver.find_element(By.CLASS_NAME, 'otkinput-errormsg')
                captcha_element = driver.find_element(By.ID, 'captchaImg')
                captcha_element.screenshot('captcha.png')
                while True:
                    try:
                        result = solver.normal('captcha.png')
                        sleep(2)
                        break
                    except Exception as e:
                        print(f'Error solving captcha: {e}')
                code = result['code']
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'recaptcha_response_field'))).send_keys(code + "\n")
            except:
                pass
    os.remove('captcha.png')


def ea_login(email, newpassword):
    driver.get('https://www.ea.com/login')
    sleep(2)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'email'))).send_keys(email)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'password'))).send_keys(newpassword + "\n")
    sleep(2)


def reset_ea_yogi(email, password):
    if open_ea_to_change_pass(email) == 'invalid_eamil':
        return 'invalid_eamil'
    open_roundcube(email, password)
    wait_for_new_mail()
    get_email_subject_of_latest_email()
    new_pass = click_on_reset()
    ea_login(email, new_pass)
    driver.close()
    print('@@')
    return new_pass
# new accounts functions


def open_ea_to_create_account_old(email, emailpass):
    driver.get('https://www.ea.com/register')
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'countryDobNextBtn')))
    sleep(2)
    driver.switch_to.active_element
    # day
    ActionChains(driver).send_keys(Keys.TAB*8).perform()
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    for i in range(random.randint(1, 28)):
        ActionChains(driver).send_keys(Keys.DOWN).perform()
    ActionChains(driver).send_keys(Keys.TAB).perform()
    # month
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    for i in range(random.randint(1, 12)):
        ActionChains(driver).send_keys(Keys.DOWN).perform()
    ActionChains(driver).send_keys(Keys.TAB).perform()
    # year
    ActionChains(driver).send_keys(Keys.TAB).perform()
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    for i in range(random.randint(20, 34)):
        ActionChains(driver).send_keys(Keys.DOWN).perform()
    ActionChains(driver).send_keys(Keys.TAB).perform()
    # enter
    ActionChains(driver).send_keys(Keys.ENTER).perform()

    # eA pass
    new_password = generate_password()
    ActionChains(driver).send_keys(Keys.TAB*2).perform()
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'email'))).send_keys(email)
    while True:
        # originId = random.choice(first_names) + (str(random.randint(999, 9999))
        #                                         if random.choice([True, False]) else generate_username1())
        originId = random.choice(first_names) + \
            str(random.randint(999, 9999))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
            (By.ID, 'originId'))).send_keys(originId)
        ActionChains(driver).send_keys(Keys.TAB).perform()
        sleep(2)
        try:
            error = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.ID, "form-error-eaid-invalid")))
            print(error.text)
            if not error.text:
                break
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, 'originId'))).clear()
        except:
            break
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'password'))).send_keys(new_password)  # + "\n"
    ActionChains.key_down(Keys.ENTER).pause(1).key_up(Keys.ENTER)
    sleep(2)

    # VERIFY_
    try:
        frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "challenge")))
        driver.switch_to.frame(frame)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, "home_children_button"))).click()
    except:
        print('captch fail')
        pass
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.ID, 'contact-me-container')))

    ActionChains(driver).send_keys(Keys.TAB*4).perform()
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    ActionChains(driver).send_keys(Keys.TAB*3).perform()
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()

    code = from_email(email, emailpass)
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.ID, 'emailVerifyCode'))).send_keys(code + "\n")

    # Your EA Account is verified and ready to go. Here are your account details
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'continueDoneBtn'))).click()

    return originId, new_password


def from_email(email, emailpass):
    # driver = Chrome(use_subprocess=True)
    driver.tab_new('about:blank')
    driver.switch_to.window(driver.window_handles[1])
    open_roundcube(email, emailpass)
    code = print_all_email_subjects()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return code


def get_code(code):
    if "Your EA Security Code is:" in code:
        code = code.split(": ")[-1]
        print("The security code is:", code)
        return code


def print_all_email_subjects():
    while True:
        try:
            email_rows = WebDriverWait(driver, 3).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.message a')))
            code = None
            for email_row in email_rows:
               # print(email_row.accessible_name)
                code = get_code(email_row.accessible_name)
                if code:
                    return code
            driver.refresh()
        except:
            driver.refresh()


def create_ea_yogi(email, password):
    originId, new_password = open_ea_to_create_account(email, password)
    print('@@')
    return print(originId+","+new_password)


changeip()
try:
    arg = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
except:
    print('Invalid')
    #sys.exit()
# '''''
    arg = 'change_pass'
    username = 'lukec@getgoodmail.icu'
    password = 'Bethq5454'
    level_or_error = 'wrong_pass'
# '''''
'''''
print('ras')
print('@@')
originId='Landry7133'
new_password='M6pZzGF7t'
print(originId+","+new_password)
driver.close()
sys.exit()
'''''
email_site='https://getbestmail.com/mail'
email_site='https://mail.zsthost.com/'
if arg == 'change_pass':
    print(reset_ea_yogi(username, password))
elif arg == 'create_ea_yogi':
    create_ea_yogi(username, password)
    driver.close()
sys.exit()
