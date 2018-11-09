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
  assert g_names is not None
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
      assert isinstance(session_file,str)
      if verbose:
        print("Subcommand {:s}".format(scommand))
        print("Subcommand Arg {:s}".format(saction))
      if saction == 'IN':
        max_time = g_names.max_session_time
        assert isinstance(max_time,int)
        assert max_time > 0
        cred_file = g_names.cred_file()
        assert isinstance(cred_file,str)
        am.check_authentication(cred_file)
        gwd_file = g_names.gwd_file()
        command_success = sm.init_session(
          session_file=session_file,gwd_file=gwd_file, max_time=max_time)
      elif saction == 'CL':
        gwd_file = g_names.gwd_file()
        assert isinstance(gwd_file, str)
        command_success = sm.clean_session(
          session_file=session_file, gwd_file=gwd_file, are_you_sure=True)
      elif saction == 'SU':
        gwd_file = g_names.gwd_file()
        cred_file = g_names.cred_file()
        assert isinstance(gwd_file, str)
        assert isinstance(cred_file, str)
        try:
          choice = str(input("Are you sure you want to superclean your session.\nThis removes the creditial file [y|n]:"))
          m_choice = choice.upper()[0]
          if m_choice not in 'NY':
            raise ValueError("Choice must be in [n|y|N|Y]")
        except ValueError:
          raise ValueError("Choice must be in [n|y|N|Y]")
        if m_choice in 'yY':
          command_success = sm.super_clean_session(
            cred_file=cred_file, session_file=session_file, gwd_file=gwd_file,
            are_you_sure=True
          )
      elif saction == 'PR':
        command_success = sm.print_session_information(global_names=g_names)
      else:
        command_success = False
  return found_valid, command_success