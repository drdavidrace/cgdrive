'''
Object to support common informational messages and common file names
'''
import os, sys
from pprint import pprint, pformat

# PyDrive
import pydrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials
#
import utilities.authentication_mgmt as am
import utilities.file_utilities as flu
#
class gdrive_global(GoogleDrive):
  
  def __init__(self, argv=None, pid=None, verbose=False):
    assert argv is not None
    assert argv is not None
    #Path variables
    self.is_valid = False
    self.source_path = os.path.split(flu.clean_path(argv[0]))[0]
    self.current_pid = pid
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
    self.verbose = verbose
    #Authenticate and set up the drive
    self.gauth = None
    try:
      self.gauth = self._check_authentication_()
    except Exception:
      raise ConnectionError("GoogleDrive is not authenticated")
    try:
      super().__init__(self.gauth)
    except Exception:
      raise FileNotFoundError("Root directory of the GoogleDrive was not found")
    #Set up information files
    self.info_file_dir()
    self.is_valid = True
    return None
  #Get for common names
  def info_dir_name(self):
    return flu.create_file_name(self.home,self.info_dir)
  def info_file_dir(self):
    return flu.create_dir(self.info_dir_name())
  def process_lock_file(self):
    return flu.create_process_lockfile_name(
      self.info_file_dir(), self.process_lock_name, self.current_pid, create_dir=True)
  def glob_lock_file(self):
    return flu.create_process_lockfile_name(
    self.info_file_dir(), self.process_lock_name, '*', create_dir=True)
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
  #
  #messages
  #
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
  #
  #  public methods
  #
  def getgwd(self):
    '''
    Purpose:  Get the google directory information for the google
    current working directory.

    Inputs: None

    Outputs:  the directory information, including
      name, ...
    '''
    assert self.is_valid is True
    gwd_name = self._getgwd_()
    if self.verbose:
      print("The google drive connection status {}".format(self._is_connected_())
    file_info = None
    file_info = self._get_file_metadata_(file_str=gwd_name)
    if self.verbose:
      pprint(file_info)
    return file_info
  #
  #  private methods
  #
  #
  def _getgwd_(self):
    '''
    Purpose:  get the google working directory from the gwd_file

    Inputs:  global_names - the global names object

    Outputs:  The first line of the file gwd_file
    '''
    assert self.is_valid
    gwd_file = self.gwd_file()
    gwd_name = None
    with open(gwd_file,"r") as f:
      gwd_name = f.readline()
      gwd_name = gwd_name.strip()
      f.close()
    return gwd_name

  def _check_authentication_(self):
    '''
    Purpose:  This checks to verify that the creditionals file exists and that it is valid.

    Inputs:
    cred_file - The full path to the creditional file

    Outputs:
    gauth information
    '''
    cred_file = self.cred_file()
    gauth = GoogleAuth()
    #gauth.credentials = GoogleCredentials.get_application_default()
    # Try to load saved client credentials
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        gauth.LoadCredentialsFile(cred_file)
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        if this.verbose:
          pprint("Token Expired")
        os.remove(cred_file)
        gauth.LocalWebserverAuth()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(cred_file)
    # return the gauth
    return gauth
  def  _is_connected_(self):
        '''
    This returns True if it is connected and False otherwise.
    #
    Parameters:
    -----------
    None
    #
    Returns:
    --------
    True if connected and False otherwise

    TODO:
    -----
    (1)  Just checks the local variable.  Probably should check the drive just incase it was timed out.
    '''
    return True if(self.GetAbout()['kind'] == 'drive#about') else False