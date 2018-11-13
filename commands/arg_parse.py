'''
Process the subcommand and subcommand argument, then pass back the appropriate subroutine to call
'''
import sys
import utilities.file_utilities as flu 
import utilities.lock_mgmt as lm
import utilities.authentication_mgmt as am
import commands.session_mgmt as sm
import commands.command_const as cc
from pprint import pprint
#
def _find_subcommand_(subcommand=None, verbose=False):
  '''
  Purpose:  find the subcommand

  Inputs:
  subcommand - The proposed subcommand
  verbose - a flag to output more information

  Outputs -
  True/False if valid subcommand
  scommand - The uppercase version of the subcommand, None if invalid

  Warning:  Only check the leading characters
  '''
  assert subcommand is not None
  assert isinstance(subcommand,str)
  found_valid = False
  scommand = None
  subcommand = subcommand.upper()
  for cmd in cc.subcommands:
    if cmd in subcommand:
      found_valid = True
      scommand = cmd
      break
  return found_valid, scommand
#
def _find_action_(subcommand=None, action=None, verbose=False):
  '''
  Purpose:  Find the session action

  Inputs:
  subcommand - The uppercase version of the subcommand, not checked on input
  action -  The proposed session action
  verbose -  a flag to output more information

  Outputs:
  True/False if valid action
  saction - the uppercase version of the action, None if invalid
  '''
  assert subcommand is not None
  assert action is not None
  assert isinstance(subcommand, str)
  assert isinstance(action, str)
  found_valid = False
  saction = None
  pactions = None
  valid_command = True if subcommand in cc.subcommands else False
  if valid_command:
    if subcommand == cc.sess_command:
      pactions = cc.sess_acts
    elif subcommand == cc.gwd_command:
      pactions = cc.gwd_acts
    else:
      return found_valid, saction
  else:
    return found_valid, saction
  #
  action = action.upper()
  for a in pactions:
    if a in action:
      found_valid = True
      saction = a
      break
  return found_valid, saction
#  check arg parse
def are_valid_args(
  subcommand=None, action=None,
  verbose=False):
  '''
  Purpose:  Check that the combination of subcommand and subcommand arg are valid.
  These will likely change as the code matures; therefore, this is centralized.

  Inputs:
  subcommand - The subcommand that will be attempted.  The valid subcommands are:
    session
  action - The subcommand action that will be attempted.  The actions
    vary with the subcommand
  verbose - a flag to output more information.  If true the output is to stderr

  Outputs:
  True/False for validity of the subcommand, subcommand_action
  subcommand - the uppercase version of the full subcommand, None if invalid combination
  action - the uppercase version of the full action, None if invalid combination
  '''
  assert subcommand is not None
  assert action is not None
  assert isinstance(subcommand, str)
  assert isinstance(action, str)
  action = action.upper()
  found_valid = False
  scommand = None
  saction = None
  #Check Command
  found_valid, scommand = _find_subcommand_(subcommand = subcommand)
  if not found_valid:
    return found_valid, scommand, saction
  else:
    #Check action
    found_valid, saction = _find_action_(subcommand=scommand, action=action)
    if not found_valid:
      scommand = False
  return found_valid, scommand, saction