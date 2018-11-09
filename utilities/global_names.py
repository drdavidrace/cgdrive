'''
Object to support common informational messages
'''
import os, sys
from pprint import pprint, pformat

import utilities.file_utilities as flu
#
class names:
  def __init__(self):
    self.source_path = os.path.split(flu.clean_path(sys.argv[0]))[0]
    self.current_pid = os.getpid()
    self.program_name = sys.argv[0]
    self.home = os.environ['HOME']
    self.info_dir = ".gdrive"
    self.cred_file_name = "mycreds.txt"
    self.client_secrets_name = "client_secrets.json"
    self.global_lock_name = "global_lock"
    self.process_lock_name = "process_lock"
    self.gwd_file_name = "gwd" #google drive working directory info
    self.session_file_name = "session" #session information
    self.max_lock_retries = 1
    self.max_session_time = 180 #minutes
  #Get for common names
  def info_dir_name(self):
    return flu.create_file_name(self.home,self.info_dir)
  def info_file_dir(self):
    return flu.create_dir(self.info_dir_name())
  def process_lock_file(self):
    return flu.create_process_lockfile_name(
      self.info_file_dir(), self.process_lock_name, self.current_pid, create_dir=True)
  def cred_file(self):
    return flu.create_file_name(self.info_file_dir(),self.cred_file_name, create_dir=True)
  def global_lock_file(self):
    return flu.create_file_name(self.info_file_dir(),self.global_lock_name, create_dir=True)
  def session_file(self):
    return flu.create_file_name(self.info_file_dir(), self.session_file_name, create_dir=True)
  def gwd_file(self):
    return flu.create_file_name(self.info_file_dir(), self.gwd_file_name, create_dir=True)
  def client_secrets_file(self):
    return flu.create_file_name(self.source_path, self.client_secrets_name)
  #messages
  def _info_dir_m_(self):
    return "Information Directory is {:s}".format(self.info_file_dir())
  def _subcommand_m_(self):
    sc_message = ''.join(['The valid subcommands are session, ...',
    '\n    There is only one subcommand allowed per call.',
    '\n    This is designed to be single threaded and does not queue subcommands.'])
    return sc_message
  def _action_m_(self):
    sca_message = ''.join(["The valid arguments for each subcommand are:",
    "\n    session:  clean, superclean, init"])
    return sca_message
  #get messages
  def get_subcommand_message(self):
    return self._subcommand_m_()
  def get_action_message(self):
    return self._action_m_()
  #prints of messages
  def print_info_dir(self):
    print(self._info_dir_m_())
  def print_subcommand_message(self):
    print(self.get_subcommand_message())
  def print_action_message(self):
    print(self._action_m_())
