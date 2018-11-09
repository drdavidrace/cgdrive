'''
The commands in this file execute the subcommand/subcommand action combination
'''
import sys
import utilities.file_utilities as flu 
import utilities.lock_mgmt as lm
import utilities.authentication_mgmt as am
import commands.session_mgmt as sm
import commands.arg_parse as ap
import commands.command_const as cc
from pprint import pprint
cmgr_file_name = "command_mgr.py"
def exe(
  subcommand = None, action=None,
  g_names=None, verbose=False):
  '''
  Purpose:  execute the subcommand and action

  Inputs:
  subcommand - The command to execute, this must be preprocessed through ap
  action - the action to perform, this must be preprocessed through ap

  verbose - The flag to output additional process information
  '''
  assert subcommand is not None
  assert action is not None
  assert isinstance(subcommand,str)
  assert isinstance(action,str)

  found_valid = False
  command_success = False
  found_valid, scommand, saction = ap.are_valid_args(
    subcommand=subcommand,
    action=action)
  if verbose:
    sys.stderr.write("====File {}====\n".format(cmgr_file_name))
    sys.stderr.write("Found Valid ? {}\n".format(found_valid))
    sys.stderr.write("subcommand {}\n".format(scommand))
    sys.stderr.write("action {}\n".format(saction))

  if found_valid:
    if verbose:
      sys.stderr.write("Inside valid command action\n")
    if scommand == cc.sess_command:
      session_file = g_names.session_file()
      max_time = g_names.max_session_time
      assert isinstance(session_file,str)
      assert isinstance(max_time,int)
      assert max_time > 0
      if verbose:
        print("Subcommand {:s}".format(scommand))
        print("Subcommand Arg {:s}".format(saction))
      if saction == 'IN':
        command_success = sm.init_session(session_file=session_file,max_time=max_time)
  return found_valid, command_success