#!/usr/bin/env python3
'''
This is a stand-alone python3 script to support copying to/from a local directory_dictionary
and a user's Google Drive.  This makes extensive use of PyDrive.
This is not overly efficient because it assumes are are focused on a single user
moving data between a VM and their own Google Drive.

Comment on naming conventions:
(1)  For files, this code uses <file name>_name for the short name and <file name> for the full path name
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
import argparse

#Code specific Imports
import utilities.global_names as gn
import utilities.lock_mgmt as lm
import utilities.authentication_mgmt as am
import commands.arg_parse as ap
import commands.command_mgr as cmgr
#defaults
gnames = gn.names()
verbose = False
subcommand = None
action = None
#
if __name__ == "__main__":
  '''
  This is the main driver for cgdrive.
  '''
  am.check_authentication(gnames.cred_file())

  a_parser = argparse.ArgumentParser(
    description='Manage the data transfer between the local VM and a Google Drive',
    formatter_class=argparse.RawTextHelpFormatter)
  a_parser.add_argument(
    'subcommand',nargs='?',type=str,metavar='subcommand',default=None,
    help=gnames.get_subcommand_message())
  a_parser.add_argument(
    'action',nargs='?',type=str,default=None,
    metavar='action', help=gnames.get_action_message())
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
      g_names = gnames, verbose=verbose)
