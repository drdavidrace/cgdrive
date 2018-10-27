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
#defaults
current_pid = os.getpid()
home = os.environ['HOME']
info_dir = ".gdrive"
cred_file_name = "mycreds.txt"
global_lock_name = "global_lock"
process_lock = "process_lock"
gwd_file_name = "gwd"
session_file_name = "session"
info_file_dir = os.path.join(home,*[info_dir])
process_lock_file = os.path.join(,''.join(["{:d}".format(current_pid),".",process_lock]))
max_lock_retries = 10
#  Check the cred file path
if not os.path.isdir(info_file_dir):
    try:
        path = Path(info_file_dir)
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), info_file_dir)
#define info_file_dir
cred_file = os.path.join(info_file_dir,cred_file_name)
# Check the global lock file
global_lock_file = os.path.join(info_file_dir,*[global_lock_name])

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
    parser = argparse.ArgumentParser(description='Manage the data transfer between the local VM and a Google Drive')
    parser.add_argument('subcommand',type=str,metavar='subcommand')
    parser.add_argument('subcommand_arg',type=str,default=None,metavar='subcommand argument')
    args = parser.parse_args()
    pprint(subcommand)
    pprint(subcommand_arg)
