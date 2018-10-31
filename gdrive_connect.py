#!/usr/bin/env python3
'''
This is a stand-alone python3 script to support copying to/from a local directory_dictionary
and a user's Google Drive.  This makes extensive use of PyDrive.
This is not overly efficient because it assumes are are focused on a single user
moving data between a VM and their own Google Drive.

Comment on naming conventions:
(1)  For files, use <file name>_name for the short name and <file name> for the full path name
(2)  _<variable name>_ is used for the variables within a file that are passed and used else where

Threads support:  The threads support is designed to be single threaded since this is a command
line utility 
'''
#General Imports
import os, sys
import time
import errno
import warnings
from pprint import pprint, pformat
from pathlib import Path
import argparse
import pydrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#Code specific Imports
import utilities.file_utilities as flu 
import utilities.lock_mgmt as lm
import commands.session_mgmt as sm
#defaults
source_path, _ = os.path.split(flu.clean_path(sys.argv[0]))
current_pid = os.getpid()
home = os.environ['HOME']
info_dir = ".gdrive"
cred_file_name = "mycreds.txt"
client_secrets_name = "client_secrets.json"
global_lock_name = "global_lock"
process_lock_name = "process_lock"
gwd_file_name = "gwd" #google drive working directory info
session_file_name = "session" #session information
max_lock_retries = 1
max_session_time = 180 #minutes
subcommand = None
subcommand_arg = None
#create information directory file names
_info_dir_name_ = flu.create_file_name(home,info_dir)
_info_file_dir_ = flu.create_dir(_info_dir_name_)
_process_lock_file_ = flu.create_process_lockfile_name(_info_file_dir_, process_lock_name, current_pid, create_dir=True)
_cred_file_ = flu.create_file_name(_info_file_dir_,cred_file_name, create_dir=True)
_global_lock_file_ = flu.create_file_name(_info_file_dir_,global_lock_name, create_dir=True)
# Session Information
_session_file_ = flu.create_file_name(_info_file_dir_, session_file_name, create_dir=True)
#File for google drive working directory information
_gwd_file_ = flu.create_file_name(_info_file_dir_, gwd_file_name, create_dir=True)
_client_secrets_file_ = flu.create_file_name(source_path, client_secrets_name)

def check_authentication():
    global _cred_file_
    gauth = GoogleAuth()
    # Try to load saved client credentials
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        gauth.LoadCredentialsFile(_cred_file_)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(_cred_file_)


if __name__ == "__main__":
    check_authentication()
    a_parser = argparse.ArgumentParser(description='Manage the data transfer between the local VM and a Google Drive')
    a_parser.add_argument('subcommand',nargs='?',type=str,metavar='subcommand')
    a_parser.add_argument('subcommand_arg',nargs='?',type=str,default=None,metavar='subcommand argument')
    args = a_parser.parse_args()
    pprint(args)
    pprint(subcommand)
    pprint(subcommand_arg)
    #Initialize session
    pprint(type(max_session_time))
    res = sm.init_session(session_file=_session_file_,max_time=max_session_time)
    pprint(res)
    is_valid_session = sm.check_valid_session(info_file_dir=_info_file_dir_,
    cred_file=_cred_file_, 
    session_file=_session_file_)

    if not is_valid_session:
        pprint("Invalid session - Run clean and init")
