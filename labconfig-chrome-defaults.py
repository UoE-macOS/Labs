#!/usr/bin/env python

# Created by Amsys
#
# Use at your own risk.  Amsys will accept
# no responsibility for loss or damage
# caused by this script.
# DW - Amsys - 2016.01.25

# Name the Casper Parameters:
# 4 URL to set homepage to
# 5 behaviour to adopt if preference file exists (UPDATE, UPDATEONCE, SKIP)

# Script setup ########################################
# Importing Libraries
import json
import sys
from SystemConfiguration import SCDynamicStoreCopyConsoleUser
import os
import subprocess

print("STARTING: Google Chrome Setup Script")

username = (SCDynamicStoreCopyConsoleUser(None, None, None) or [None])[0]; username = [username,""][username in [u"loginwindow", None, u""]]; sys.stdout.write(username + "\n")

homepage = "https://www.ed.ac.uk"
behaviour = "UPDATE"

# Work out the user's home folder location
userhome = os.path.expanduser("~" + username)
if len(userhome) < 1:
	print("User Home not successfully discovered")
	exit(1)

firstrundirectory = userhome + "/Library/Application Support/Google/Chrome"
firstrunfile = userhome + "/Library/Application Support/Google/Chrome/First Run"
firstruntopdirectory = userhome + "/Library/Application Support/Google"
preferencesdirectory = userhome + "/Library/Application Support/Google/Chrome/Default"
preferencesfile = userhome + "/Library/Application Support/Google/Chrome/Default/Preferences"
runoncefile = userhome + "/Library/Application Support/Google/Chrome/Default/PreferencesSetOnce"

# Print out found variables
print("Username: " + username)
print("Homepage: " + homepage)
print("Behaviour: " + behaviour)
print("Userhome: " + userhome)

# First Run file creation ########################

# Check if first run directory exists and create it if needed
if not os.path.exists(firstrundirectory):
    os.makedirs(firstrundirectory)

# Try and create the first run file
try:
    open(firstrunfile, 'a').close()
except:
    print("Failed to create first run file")
    exit(2)

# Fix any permissions with this bit
try:
    subprocess.call(['chown', '-R', username, firstruntopdirectory])
except:
    print("Failed to permission the first run file directory")
    exit(3)

# Preference file creation ########################

# Create the Preference file directory
if not os.path.exists(preferencesdirectory):
    try:
        os.makedirs(preferencesdirectory)
    except:
        print("Failed to create User's Preference file directory")
        exit(4)

if os.path.isfile(preferencesfile):
    if behaviour.upper() == "SKIP":
        print("Preference file exists and script is set to skip")
        exit(0)
    elif behaviour.upper() == "UPDATEONCE":
        if os.path.isfile(runoncefile):
            print("Preference file exists and has been updated once already")
            exit(0)
        else:
            open(runoncefile, 'a').close()
    elif behaviour.upper() == "UPDATE":
        print("Preference file exists and script is set to update, continuing...")
else:
    try:
        open(preferencesfile, 'a').close()
 #       os.system("echo " + "{}" ">" + preferencesfile)
    except:
        print("Failed to create the preference file")
        exit(5)

print("Writing content to preference file")

# Read the file
with open(preferencesfile) as json_file:
    try:
        json_decoded = json.load(json_file)
    except ValueError:
        json_decoded = {}

# Set the Values
# browser section
json_decoded["browser"] = {}
json_decoded["browser"]["check_default_browser"] = False
json_decoded["browser"]["show_home_button"] = True
json_decoded["browser"]["show_update_promotion_info_bar"] = False

# distribution section
json_decoded["distribution"] = {}
json_decoded["distribution"]["import_bookmarks"] = False
json_decoded["distribution"]["import_history"] = False
json_decoded["distribution"]["import_home_page"] = False
json_decoded["distribution"]["import_search_engine"] = False
json_decoded["distribution"]["make_chrome_default"] = False
json_decoded["distribution"]["make_chrome_default_for_user"] = False
json_decoded["distribution"]["show_welcome_page"] = False
json_decoded["distribution"]["skip_first_run_ui"] = True
json_decoded["distribution"]["suppress_first_run_bubble"] = True
json_decoded["distribution"]["suppress_first_run_default_browser_prompt"] = True

# top level section
json_decoded["first_run_tabs"] = {}
json_decoded["first_run_tabs"] = homepage
json_decoded["homepage"] = homepage
json_decoded["homepage_is_newtabpage"] = False

# Proxy section
json_decoded["proxy"] = {}
json_decoded["proxy"]["bypass_list"] = ""
json_decoded["proxy"]["mode"] = "system"
json_decoded["proxy"]["server"] = ""

# sync_promo section
json_decoded["sync_promo"] = {}
json_decoded["sync_promo"]["user_skipped"] = True

# session section
json_decoded["session"] = {}
json_decoded["session"]["restore_on_startup"] = 4
json_decoded["session"]["startup_urls"] = [homepage]

# Save changes
with open(preferencesfile, 'w+') as json_file:
    json.dump(json_decoded, json_file)

# Re-permission directories
try:
    subprocess.call(['chown', '-R', username, preferencesdirectory])
except:
    print("Failed to permission the preference file directory")
    exit(6)

print("Script Completed")
exit(0)
