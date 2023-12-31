#!/bin/python
import os
import json
import subprocess
import argparse
from random import choice as rchoice
from sys import argv
import time
start_time = time.time()

#Constants
HOME_DIR = os.path.expanduser('~')
PROGRAM_ID = "wallpaperswitcher"
CONFIG_DIR = f"{HOME_DIR}/.config/{PROGRAM_ID}/"
STATE_FILE = f"{CONFIG_DIR}state"
CONFIG_FILE = f"{CONFIG_DIR}wallpaperswitcher.json"
ERROR_MESSAGE_PREFIX = "Ayoo, something went wrong: "
STATE = {
    "current_wallpaper" : None, 
    "prev_wallpaper" : None,
    "current_wallpaper_folder" : None
    }
DEFAULT_CONFIG = {
    "wallpaper_dir" : f"{HOME_DIR}/Pictures/wallpapers",
    "wallpaper_change_prefix" : "feh --bg-scale ",
    "show_errors" : False,
    }

config = {}
state = {}
#Check operating system, if not linux, exit 
if os.name != "posix":

    send_error_message(ERROR_MESSAGE_PREFIX + "This program only works on linux")
    exit(1)

#Check if feh is installed
try:
    subprocess.check_output("feh --version".split())
except Exception as e:
    send_error_message("feh is not installed")
    raise e
#Check if rofi is installed
try:
    subprocess.check_output("rofi -v".split())
except Exception as e:
    send_error_message("rofi is not installed")
    raise e
#initializes the config and state file
if not os.path.exists(CONFIG_DIR):
    try:
        os.mkdir(CONFIG_DIR)
    except Exception as e:
        send_error_message("Could not create config directory")
        raise e
if not os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE,"w") as config_file_handle:
            json.dump(DEFAULT_CONFIG,config_file_handle, skipkeys= True, allow_nan= True, indent = 4)
    except Exception as e:
        send_error_message("Could not create config file")
        raise e
if not os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE,"w") as state_file_handle:
            json.dump(STATE,state_file_handle)
    except Exception as e:
        send_error_message("Could not create state file")
        raise e

#Loads file data
with open(CONFIG_FILE) as config_file_handle:
    file_contents = config_file_handle.read()
    config = json.loads(file_contents)
with open(STATE_FILE) as state_file_handle:
    file_contents = state_file_handle.read()
    state = json.loads(file_contents)

def send_error_message(message, display_with_rofi = True): 
    error_message = f"'{ERROR_MESSAGE_PREFIX} {message}'"

    rofi_prefix = "rofi -dmenu -mesg".split()
    rofi_options = "-hide-scrollbar -timeout 5".split()
    rofi_input = []
    rofi_input.extend(rofi_prefix)
    rofi_input.append(error_message)
    rofi_input.extend(rofi_options)
    if(display_with_rofi and config["show_errors"]):
        #Display message that times out after 5 seconds
        subprocess.check_output(rofi_input)

    print(error_message)


def select_wallpaper_folder(folder):
    try:
        files = os.listdir(folder)
    except Exception as e:
        send_error_message(f"Could not open wallpaper directory at {folder}")
        raise e
    
    if(files.__len__() == 0):
        send_error_message(f"No files in wallpaper directory, make sure you that you have subfolders in your wallpaper directory at {folder}")
        raise Exception("No files in wallpaper directory")
    rofi_string = '\n'.join(files)

    rofi_list_input = ["echo", rofi_string]
    process_rofi_input = subprocess.Popen(rofi_list_input, stdout=subprocess.PIPE)
    process_rofi_open = subprocess.check_output("rofi -dmenu".split(),stdin=process_rofi_input.stdout)
    process_rofi_input.wait()
    return process_rofi_open.decode('utf-8').strip()
def select_wallpaper(file_name, sub_folder):
    command_args = config['wallpaper_change_prefix'].split()
    command_args.append(f"{config['wallpaper_dir']}/{sub_folder}/{file_name}")
    state["prev_wallpaper"] = f'{state["current_wallpaper_folder"]}/{state["current_wallpaper"]}'
    try:
        subprocess.check_output(command_args)
    except Exception as e:
        state["current_wallpaper"] = file_name
        state["current_wallpaper_folder"] = sub_folder
        update_state()
        send_error_message(f"Could not change wallpaper might have a corupt file at {config['wallpaper_dir']}/{sub_folder}/{file_name}")
        select_next_wallpaper()
        raise e
    state["current_wallpaper"] = file_name
    state["current_wallpaper_folder"] = sub_folder
    update_state()
    return
def get_wallpapers_in_current_folder():
    sub_folder = state["current_wallpaper_folder"]
    wallpaper_dir = config["wallpaper_dir"]
    files = os.listdir(f'{wallpaper_dir}/{sub_folder}' )
    for file in files:
        if not file.endswith(".png") and not file.endswith(".jpg") and not file.endswith(".jpeg"):
            files.remove(file)
    return files
def select_next_wallpaper():
    sub_folder = state["current_wallpaper_folder"]
    files = get_wallpapers_in_current_folder()  
    if(sub_folder == None):
        select_random_wallpaper()
        return
    if state["current_wallpaper"] == None:
        select_wallpaper(files[0], sub_folder)
        update_state()
        return
    if state["current_wallpaper"] not in files:
        select_wallpaper(files[0], sub_folder)
        return
    for i in range(files.__len__()):
        if state["current_wallpaper"] == files[i]:
            if i > files.__len__() - 2:
                select_wallpaper(files[0], sub_folder)
                return
            else:
                select_wallpaper(files[i+1], sub_folder)
                return

def select_random_wallpaper():
    sub_folder = state["current_wallpaper_folder"]
    files = get_wallpapers_in_current_folder()
    random_file = rchoice(files)
    select_wallpaper(random_file, sub_folder)
    return

def select_prev_wallpaper():
    sub_folder = state["current_wallpaper_folder"]
    files = get_wallpapers_in_current_folder()
    previous_wallpaper = state["prev_wallpaper"].split("/")
    if previous_wallpaper == None: 
        select_wallpaper(files[0], sub_folder)
        return
    else:
        select_wallpaper(previous_wallpaper[1], previous_wallpaper[0])
        return

def select_total_random_wallpaper():
    wallpaper_dir = config["wallpaper_dir"]
    sub_folders = os.listdir(f'{wallpaper_dir}/')
    
    random_sub_folder = rchoice(sub_folders)
    files = os.listdir(f'{wallpaper_dir}/{random_sub_folder}')
    random_file = rchoice(files)
    select_wallpaper(random_file, random_sub_folder)
    return

def update_state():
    try: 
        with open(STATE_FILE, "w" ) as state_file_handle:
            json.dump(state,state_file_handle)
    except Exception as e:
        send_error_message("Could not update state file")
        raise e





argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-sf", "--select-folder", help="Select a wallpaper folder", action="store_true")
argument_parser.add_argument("-nw", "--next-wallpaper", help="Select the next wallpaper in the current folder", action="store_true") 
argument_parser.add_argument("-pw", "--prev-wallpaper", help="Select the previous wallpaper in the current folder", action="store_true")
argument_parser.add_argument("-nr", "--next-random", help="Select a random wallpaper in the current folder", action="store_true" )
argument_parser.add_argument("-r", "--random", help="Select a random wallpaper in a random folder", action="store_true" )
argument_parser.add_argument("-c", "--current", help="Print the current wallpaper", action="store_true")
args = argument_parser.parse_args(argv[1:])



if args.select_folder:
    state["current_wallpaper_folder"] = select_wallpaper_folder(config["wallpaper_dir"])
    update_state()
    select_next_wallpaper()
elif args.next_wallpaper:
    print("next wallpaper")
    select_next_wallpaper()
elif args.prev_wallpaper:
    print("prev wallpaper")
    select_prev_wallpaper()
elif args.next_random:
    print("selecting random wallpaper in current folder")
    select_random_wallpaper()
elif args.random:
    print("selecting random wallpaper in random folder")
    select_total_random_wallpaper()
elif args.current:
    print(f'Current wallpaper: {state["current_wallpaper_folder"]}/{state["current_wallpaper"]})')
else:
    print("Setting wallpaper to last wallpaper")
    select_wallpaper(state["current_wallpaper"], state["current_wallpaper_folder"])

end_time = time.time()
print(f"Time elapsed: {end_time - start_time}")
