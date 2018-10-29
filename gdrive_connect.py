#!/usr/bin/env python3
'''
This is a stand-alone python3 script to support copying to/from a local directory_dictionary
and a user's Google Drive.  This makes extensive use of PyDrive.
This is not overly efficient because it assumes are are focused on a single user
moving data between a VM and their own Google Drive.
'''
#General Imports
import os, sys
import time
import errno
import warnings
from pprint import pprint, pformat
from pathlib import Path
import argparse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#Code specific Imports
from utilities.file_utilities import *
from commands import session_mgmt
#defaults
source_path, _ = os.path.split(clean_path(sys.argv[0]))
current_pid = os.getpid()
home = os.environ['HOME']
info_dir = ".gdrive"
cred_file_name = "mycreds.txt"
client_secrets_name = "client_secrets.json"
global_lock_name = "global_lock"
process_lock = "process_lock"
gwd_file_name = "gwd" #google drive working directory info
session_file_name = "session" #session information
max_lock_retries = 1
max_session_time = 180 #minutes
subcommand = None
subcommand_arg = None
#create information directory file names
info_dir_name = create_file_name(home,info_dir)
info_file_dir = create_dir(info_dir_name)
process_lock_file = create_process_lockfile_name(info_file_dir, process_lock, current_pid, create_dir=True)
cred_file = create_file_name(info_file_dir,cred_file_name, create_dir=True)
global_lock_file = create_file_name(info_file_dir,global_lock_name, create_dir=True)
session_file = create_file_name(info_file_dir, session_file_name, create_dir=True)
gwd_file = create_file_name(info_file_dir, gwd_file_name, create_dir=True)
client_secrets_file = create_file_name(source_path, client_secrets_name)
# clean and init session information
def clean_session(are_you_sure=False):
    global info_file_dir, cred_file, session_file, gwd_file
    if not are_you_sure:
        return False
    else:
        if os.path.isfile(session_file):
            os.remove(session_file)
        if os.path.isfile(gwd_file):
            os.remove(gwd_file)
        return True
def super_clean_session(are_you_sure=False):
    global info_file_dir, cred_file, session_file, gwd_file
    if not are_you_sure:
        return False
    else:
        clean_session(are_you_sure=True)
        if os.path.isfile(cred_file):
            os.remove(cred_file)
        #maybe remove the directory at some point
        return True
def init_session():
    global info_file_dir, cred_file, session_file, gwd_file
    create_dir(info_file_dir)
    init_session(session_file, max_session_time)
    init_gwd(gwd_file)

def check_valid_session():
    global info_file_dir, cred_file, session_file, gwd_file
    valid_session = True
    if not os.path.isdir(info_file_dir):
        raise FileNotFoundError("Missing information directory {:s}".format(info_file_dir))
    if not os.path.isfile(cred_file):
        raise FileNotFoundError("Missing credentials file {:s}".format(cred_file))
    if not os.path.isfile(session_file):
        raise FileNotFoundError("Missing session file {:s}.  Run init to create this file automatically".format(session_file))
    return True
#
def check_authentication():
    global cred_file
    gauth = GoogleAuth()
    # Try to load saved client credentials
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        gauth.LoadCredentialsFile(cred_file)
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
    gauth.SaveCredentialsFile(cred_file)
#Get the mgmt directory lock
def get_process_lock():
    '''
    Purpose:  This creates a process lock file and tries to link the global lock file
    to the process lock file.  This ensures that only a single process is doing a taskself.
    This should be wrapped with the release_process_lock inside each gdrive_connect functions
    that manages the gdrive files.
    '''
    global current_pid, global_lock_file, process_lock_file, max_lock_retries
    with open(process_lock_file, 'w+') as f:
        f.write("{:d}\n".format(current_pid))
    f.close()
    current_count = 0
    lock_acquired = False
    while not lock_acquired and current_count < max_lock_retries:
        try:
            os.link(process_lock_file, global_lock_file)
            lock_acquired = True
        except Exception as e:
            result = os.stat(process_lock_file)
            lock_acquired = (result.st_nlink == 2)
            pass
        if not lock_acquired:
            current_count += 1
            time.sleep(5)
    return lock_acquired
def release_process_lock():
    '''
    Purpose:  This is the pair for the get_process_lock that ensure that only a single process
    is working on the gdrive at a time.
    '''
    global current_pid, global_lock_file, process_lock_file, max_lock_retries
    os.unlink(global_lock_file)
    os.remove(process_lock_file)
    return True

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
    res = session_mgmt.init_session(session_file=session_file,max_time=max_session_time)
    pprint(res)
    is_valid_session = check_valid_session()

    if not is_valid_session:
        pprint("Invalid session - Run clean and init")
