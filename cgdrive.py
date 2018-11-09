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
line utility.  The included locking mechanism only works within a single computer/VM; therefore, 
using the utility on multiple VMs concurrently will likely produce unstable results. 

'''
#General Imports
import os, sys
import time
import errno
import warnings
from pprint import pprint, pformat
from pathlib import Path
import argparse

#Code specific Imports
import utilities.file_utilities as flu 
import utilities.lock_mgmt as lm
import utilities.authentication_mgmt as am
import commands.arg_parse as ap
import commands.command_mgr as cmgr
#defaults
source_path, _ = os.path.split(flu.clean_path(sys.argv[0]))
current_pid = os.getpid()
program_name = sys.argv[0]
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
verbose = False
subcommand = None
action = None
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
#
def print_info_dir():
    global info_dir
    print("Information Directory is {:s}".format(info_dir))
def subcommand_message():
    sc_message = ''.join(['The valid subcommands are session, ...',
    '\n    There is only one subcommand allowed per call.',
    '\n    This is designed to be single threaded and does not queue subcommands.'])
    return sc_message

def action_message():
    sca_message = ''.join(
        ["The valid arguments for each subcommand are:",
        "\n    session:  clean, superclean, init"])
    return sca_message



if __name__ == "__main__":
    am.check_authentication(_cred_file_)
    ab = "ab"

    a_parser = argparse.ArgumentParser(
      description='Manage the data transfer between the local VM and a Google Drive',
      formatter_class=argparse.RawTextHelpFormatter)
    a_parser.add_argument(
      'subcommand',nargs='?',type=str,metavar='subcommand',default=None,
      help="{:s}".format(subcommand_message()))
    a_parser.add_argument(
      'action',nargs='?',type=str,default=None,
      metavar='action', help=action_message())
    a_parser.add_argument(
      '-v','--verbose',action='store_true',default=False,
      help="{:s}".format("Turn on the verbose information")
    )
    args = a_parser.parse_args()
    if(args.subcommand is None):
      a_parser.print_help()
      print("There must be a subcommand, exitting!")
      exit(1)
    subcommand = args.subcommand
    action = args.action
    verbose = args.verbose
    #Initialize session
    valid_command, scommand, saction = ap.are_valid_args(
      subcommand=subcommand, action=action,verbose=True)
    if verbose:
      pprint(args)
      print("File {}".format('gdrive_connect.py'))
      print("Valid Command ? {}".format(valid_command))
      print("Command Status {}".format(scommand))
      print("Action Status {}".format(saction))

    if valid_command:
      found_valid, command_status = cmgr.exe(
        subcommand = scommand, action=saction,
        info_file_dir=_info_file_dir_,
        session_file=_session_file_,max_time=max_session_time,
        verbose=verbose)
    # is_valid_session = sm.check_valid_session(info_file_dir=_info_file_dir_,
    # cred_file=_cred_file_, 
    # session_file=_session_file_)
