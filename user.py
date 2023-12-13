import gspread
import sys
import json
import os
import subprocess
import datetime
import base64
import requests


client_id = ''
headers = {'Authorization': 'Client-ID ' + client_id}
'''''
# download sheets if we made changes in reference sheet
sa = gspread.service_account(filename="aigsheetkey.json")
sh = sa.open("ready_to_boost")
worksheet = sh.worksheet("reference")
enitiresheet = worksheet.get_all_values()
with open("sheet.json", "w") as f:
    json.dump(enitiresheet, f)
'''


with open('sheet.json', 'r') as f:
    coloumn = json.load(f)
header = coloumn[0]
accounts_current_state = header.index("status")
lvl_column = header.index("lvl")
error_column = header.index("error")
email_column = header.index("email id")
email_pass_column = header.index("email pass")
eapass_column = header.index("ea password")
pc_name_column = header.index("boosted pc name")
pc_username = os.getlogin()
#pc_username = "a13"
image_column = 9
cooldown_column = 10
start_boost_column = header.index("date boosted start")
end_boost_column = header.index("date boosted end")
last_accessed_column = header.index("last_accessed")
time_past_sincelast_accessed_column = header.index(
    "time past since last accessed")


try:
    arg = sys.argv[1]
    if arg == 'push':
        username = sys.argv[2]
        password = sys.argv[3]
        level_or_error = sys.argv[4]
    else:
        which_accounts = sys.argv[2]
except:
    print('Error: Invalid arguments.')
    #sys.exit()
    arg = 'push'
    which_accounts = 'find_tdm.png'
    username = '@hotmail.com'
    password = '7N7ax2m1Uy'
    level_or_error = 'wrong_pass'
    pass


def current_time():
    now = datetime.datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")
try:
    sa = gspread.service_account(filename="aigsheetkey.json")
    sh = sa.open("ready_to_boost")
    worksheet = sh.worksheet("apex 3-2-2023")
    enitiresheet = worksheet.get_all_values()
except:
    sys.exit('change date and time')

if len(enitiresheet[0]) < 16:
    worksheet.update('Q1', 'Bingo!')
    enitiresheet = worksheet.get_all_values()
    
def get_image():
    screenshot_path = os.path.join("extra", pc_username + "_lvl_pic.png")
    with open(screenshot_path, 'rb') as image_file:
        image_data = image_file.read()
        b64_image = base64.b64encode(image_data)

    url = 'https://api.imgur.com/3/image'
    data = {'image': b64_image}
    response = requests.post(url, headers=headers, data=data)
    response_data = json.loads(response.text)
    image_url = response_data['data']['link']
    #image_url ='https://i.imgur.com/LzcCj7j.png'

    # Use the image_url in the IMAGE function in Google Sheets
    formula = '=IMAGE("' + image_url + '", 1)'
    return formula

def error_check_passed(first_empty_row,which_accounts):
    # check if ea password is present becaue no ea pass means acc bnea hi ni
    # check if account status column is either training_done or already boosting because if empty then it means traing is not done 
    if first_empty_row[eapass_column] and (first_empty_row[accounts_current_state]== 'training_done' or first_empty_row[accounts_current_state]== 'Boosting'):
        return 1
    elif which_accounts == 'training.png' and not first_empty_row[accounts_current_state] and first_empty_row[eapass_column]:
        return 1 # if mode to play is traning then we will allow
    elif first_empty_row[accounts_current_state] == 'cooldown ' and int(first_empty_row[16]) < 21600: 
        return #check if account is on cooldown check if we 6 hrs are passed because only those acc can run 
    elif not first_empty_row[accounts_current_state] and first_empty_row[eapass_column]:
        return 1 # if mode to play is anything and ea pass exist then we will allow and its not cooldown


# data like first login last login etc etc
def its_first_time_running(first_empty_row):
    if first_empty_row[start_boost_column] is None or first_empty_row[start_boost_column] == '':
        return 1


if arg == 'get':  # get a username and password , where pc name on sheet is empty or same as current user &&  lvl less then 20 and has no error in error_coloum
    no_user_found_to_play = True
    selected_rows = []
    for i, row in enumerate(enitiresheet):
        # if not defined then make it 0 also make it a int to compare
        lvl = int(row[lvl_column]) if row[lvl_column] else 0
        # if thr is any error likr ban wrong pass etc
        error = row[error_column]
        # tryna find ownold user or fresh user
        if lvl < 20 and not row[error_column] and (not row[pc_name_column] or pc_username == row[pc_name_column]):
            selected_row_number = str(i+1)
            if error_check_passed(row,which_accounts): # return something means passed and if status column is empty and mode is not trainig then it will return false
                # as of now it will work but if we automated traning then two accounts can access this account
                if which_accounts == 'training.png' and not row[accounts_current_state]:
                    print(row[email_column], row[eapass_column])
                    no_user_found_to_play = False
                    break
                elif which_accounts != 'training.png': #not row[accounts_current_state]:
                    if its_first_time_running(row):
                        worksheet.update("f" + selected_row_number + ":m" + selected_row_number, [["Boosting",str(
                            lvl), "", pc_username, row[image_column], "", current_time(), current_time()]])  # m da matlab till colm m
                    else:
                        worksheet.update("f" + selected_row_number + ":m" + selected_row_number, [["Boosting", str(
                            lvl), "", pc_username, row[image_column], "", row[start_boost_column], current_time()]])  # m da matlab till colm m
                    print(row[email_column],
                          row[eapass_column])
                    no_user_found_to_play = False
                    break
            #else:
                #break
        # .......store user..........of other pc who is not active since last 60 mins
        elif lvl < 20 and not row[error_column] and (not row[time_past_sincelast_accessed_column] or int(row[time_past_sincelast_accessed_column]) > 60) and error_check_passed(row,which_accounts):
                # save values here
                row.append(str(i+1))  # add selected_row_number_backup as a cell in the row
                selected_rows.append(row)
                #selected_row_number_backup = str(i+1)
                #row_backup = row
    if no_user_found_to_play == True and which_accounts != 'training.png' and selected_rows:  #if selected_rows: then......... access user........ of other pc who is not active since last 60 mins, only do this we are not looking for training
        row_backup = max(selected_rows, key=lambda r: (int(r[time_past_sincelast_accessed_column]), int(r[-1])))
        selected_row_number_backup = row_backup[-1]
        worksheet.update("f" + selected_row_number_backup + ":m" + selected_row_number_backup, [
                         ["Boosting", str(row_backup[lvl_column]), "", pc_username, row[image_column], "", row_backup[start_boost_column], current_time()]])
        print(row_backup[email_column],
              row_backup[eapass_column])
    elif no_user_found_to_play == True and which_accounts == 'training.png': # j trainig kar rahe a tan new accoiunt bnawe normal boost wich na bnawe
        arg = 'create_account'


if arg == 'push':  # push level 20 or wrong pass in error
    for i, row in enumerate(enitiresheet):
        if row[email_column] == username:
            row_number = str(i+1)

            if level_or_error == 'wrong_pass':
                #    row[email_pass_column]
                user = subprocess.run(
                    ["python", "create_account.py", 'change_pass', username,row[email_pass_column] ], capture_output=True, check=True, timeout=300)
                invalid_result = user.stdout.decode("utf-8")
                if 'invalid_eamil' in invalid_result:
                    worksheet.update("H"+row_number, 'invalid email')
                    break
                result = user.stdout.decode(
                    "utf-8").strip().split('@@', 1)[1].lstrip()
                try:
                    worksheet.update("E"+row_number, result)
                except:
                    worksheet.update("E"+row_number, result)
            elif level_or_error == 'technical_diffcuilty':
                worksheet.update("f" + row_number + ":i" + row_number, [["", "",level_or_error,pc_username]])
            elif level_or_error == 'ban':
                worksheet.update("f" + row_number + ":i" + row_number, [["", "",level_or_error,pc_username]])
            elif level_or_error == '20':

                worksheet.update("f" + row_number + ":m" + row_number,
                                 [["ready_to_sell", "20", "", pc_username, get_image(), "", row[start_boost_column], current_time()]],value_input_option="USER_ENTERED")

            elif level_or_error == 'training_done':

                worksheet.update("f" + row_number + ":m" + row_number,
                                 [["training_done", "0", "", pc_username, row[image_column], "", row[start_boost_column], current_time()]])
            elif level_or_error == 'time_limit':
                  worksheet.update("f" + row_number + ":m" + row_number,
                                 [["cooldown", "0", "", pc_username, row[image_column], "", row[start_boost_column], current_time()]])
            else:  # update last accessed as of now level_or_error = active
                print(f"unexpected arg {level_or_error}")
                lvl_pic = get_image()
                worksheet.update("f" + row_number + ":m" + row_number,
                                 [[row[accounts_current_state], row[lvl_column], "", pc_username, lvl_pic, "", row[start_boost_column], current_time()]],value_input_option="USER_ENTERED")
            print("user updated")
            sys.exit()
    else:
        print("user not found")

if arg == 'create_account':
    while True:
        for i, row in enumerate(enitiresheet):
            if not row[eapass_column]:
                row_number = str(i+1)
                user = subprocess.run(
                    ["python", "create_account.py", 'create_ea_yogi',row[email_column],row[email_pass_column]], capture_output=True, check=True, timeout=300000)
                result = user.stdout.decode(
                    "utf-8").strip().split('@@', 1)[1].lstrip().split(",")
                resultuser = result[0]
                resultpass = result[1]
                print(row[email_column],resultpass)
                while True:
                 try:
                    worksheet.update("D"+row_number +":E" + row_number, [[resultuser,resultpass]])
                    break
                 except: pass
                #sys.exit()
elif arg == 'create_hotmail_and_ea_account':
         for i, row in enumerate(enitiresheet):
            if not row[eapass_column]:
                row_number = str(i+1)
                user = subprocess.run(
                    ["python", "create_account.py", 'create_hotmail','make_ea'], capture_output=True, check=True, timeout=300000)
                result = user.stdout.decode(
                    "utf-8").strip().split('@@', 1)[1].lstrip().split(",")
                if 'upgradet' in result:
                    continue
                email = result[0]
                emailpass = result[1]
                resultuser = result[2]
                resultpass = result[3]
                print(row[email_column],resultpass)
                while True:
                 try:
                    worksheet.update("B"+row_number +":E" + row_number, [[email,emailpass,resultuser,resultpass]])
                    break
                 except:
                     try:
                        worksheet.update("B"+row_number +":E" + row_number, [[email,emailpass,resultuser,resultpass]])
                     except:
                             with open("unsaved.txt", "a+") as f:
                                    f.write(result + "\n")
