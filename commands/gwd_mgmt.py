'''
gwd commands - gwd stands for google drive working directory

This functionality is similar to the current working directory capability in Linux (i.e. the local VM)

Since this functionality is between the current working directory in the local VM 
and the google drive, we need a method to track the folder on the 
google drive that is used for the transfers.  This is the functionality
for tracking that information within a session.
'''
import os
from pprint import pprint, pformat
#
from pydrive.drive import GoogleDrive
import utilities.authentication_mgmt as am

def getgwd(global_names=None,verbose=False):
  '''
  Purpose:  Get the google directory information for the google
  current working directory.

  Inputs: global_names - the object of global names

  Outputs:  the directory information, including
    name, ...
  '''
  assert global_names is not None
  gwd_name = _getgwd_(global_names=global_names)
  #Check the google drive
  myGDrive = _get_drive_(global_names=global_names)
  global_names.myDrive = myGDrive
  isConnected = _is_connected_(global_names)
  if verbose:
    print("The google drive connection status {}".format(isConnected))
  file_info = None
  file_info = _get_file_metadata_(global_names=global_names,file_str=gwd_name)
  if verbose:
    pprint(file_info)
  return file_info
def chdir(global_names=None, new_dir=None, verbose=False):
  '''
  Purpose:  Change the google working directory

  Inputs:
  global_names - the global names object

  new_dir - the change of directory.  This can be relative or absolute
    NOTE:  We don't really expect the user to know the 'root' convention 
    Google Drive
    NOTE:  If new_dir is empty or '', then this is set back to root

  Outputs:
  The full path of the new working directory is written to ~/.gdrive/gwd
  '''
  assert global_names is not None
  if new_dir == '' or new_dir is None:
    new_dir = 'root'
  if _isdir_(global_names=global_names, dir_name=new_dir):
    work_file_info = _ls_(name)
    if(len(work_file_info['file_result']) == 1 and 'folder' in work_file_info['file_result'][0]['mimeType']):
      self.cur_dir = work_file_info['full_name']
    elif work_file_info['full_name'] == 'root':
      self.cur_dir = work_file_info['full_name']
  return self.getcwd()
  return_value = False
  return return_value
#
#  Private commands
#
def _isdir_(global_names=None, dir_name=None, verbose=False):
  '''
  Test if a string is a file name
  Parameters:
  ===========
  in_str:  The path name for a directory of interest
  Results:
  ========
  True is a file
  False otherwise
  '''
  ret_val = False
  f_info = _get_file_metadata_(global_names=global_names, file_str=dir_name)
  if f_info['mimeType']:
    if 'folder' in f_info['mimeType']:
      ret_val = True
  return ret_val
#
def  _is_connected_(global_names=None):
  '''
  This returns True if it is connected and False otherwise.
  #
  Inputs:
  -----------
  global_names - the global information for this function
  #
  Returns:
  --------
  True if connected and False otherwise
  '''
  assert global_names is not None
  return True if(_drive_about_(myDrive=global_names.myDrive)['kind'] == 'drive#about') else False
#
def _getgwd_(global_names=None,verbose=False):
  '''
  Purpose:  get the google working directory from the gwd_file

  Inputs:  global_names - the global names object

  Outputs:  The first line of the file gwd_file
  '''
  assert global_names is not None
  gwd_file = global_names.gwd_file()
  gwd_name = None
  with open(gwd_file,"r") as f:
    gwd_name = f.readline()
    gwd_name = gwd_name.strip()
    f.close()
  return gwd_name
def _get_file_metadata_(global_names=None, file_str=None):
  '''
  Purpose:
    Obtains the file meta data for a file pointed to by file_str.

  Inputs:
  ===========
  global_names - the object with the gobal data for this capability
  myDrive - the google drive object
  file_str:  The path name for the file of interest
  Outputs:
  ========
  None if there is an issue with the touching the file
  The entire metadata if the file is found
  '''
  assert global_names is not None
  assert file_str is not None
  ret_val = None
  file_info = _find_file_id_(global_names=global_names,file_str=file_str)
  if file_info:
    drive_file = global_names.myDrive.CreateFile({'id': '{:s}'.format(file_info['id'])})
    if file_info['id'] == 'root':
      ret_val =  file_info
    else:
      ret_val = drive_file.FetchMetadata(fetch_all=True)
  return ret_val
def _get_drive_(global_names=None, verbose=True):
  '''
  Purpose:  Return the pydrive.drive information

  Inputs:  The credential file (if any)

  Outputs:  The drive object

  NOTE:  This doesn't use an object approach since the command line
  doesn't support maintaining objects.  Not overly efficient but okay
  '''
  assert global_names is not None
  gauth = None
  if global_names.authentication is not None:
    gauth = global_names.authentication
  else:
    gauth = am.check_authentication(cred_file=global_names.cred_file())
  myGDrive = GoogleDrive(gauth)
  return myGDrive
#
def _drive_about_(myDrive=None, verbose=True):
  '''
  Purpose:  Get the About information for a drive

  Inputs:  The pydrive definition of a drive

  Outputs:  The About information from GetAbout
  '''
  assert myDrive is not None
  assert isinstance(myDrive,GoogleDrive)
  return myDrive.GetAbout()

#
#  Find the file id for a file on GoogleDrive
#
def _find_file_id_(global_names=None, file_str=None):
  '''
  This finds a file id for a file sent in by in_str
  Parameters
  ==========
  in_str:  The assumed path to a file or directory
  Results
  =======
  A file id for a path or None
  '''
  assert global_names is not None
  assert file_str is not None
  w_str = _build_full_path_(global_names=global_names, in_str=file_str)
  file_struct = _build_path_structure_(global_names=global_names,in_str=w_str)
  r_val = _traverse_structure_list_(global_names=global_names, in_struct=file_struct['path_array'])
  p_val = r_val['file_result']
  ret_val = None
  if p_val:
    if len(p_val) > 1:
      raise FileNotFoundError('_find_file_id found too many files' + pformat(p_val))
    ret_val = {'full_name':r_val['full_name'], 'id': p_val[0]['id']}
  return ret_val
#
def _build_full_path_(global_names=None, in_str=None):
  '''
  This builds a theoretical absolute GoogleDrive path

  Parameters:
  ----------

  in_str:  The proposed directory string

  Result:
  ------
  An absolute path starting at 'root'
  '''
  assert global_names is not None
  assert in_str is not None
  ret_val = None
  if not in_str.strip():
    ret_val = _getgwd_(global_names=global_names)
  else:
    work_file_name = os.path.normpath(in_str.strip())
    if work_file_name[0] == '/':
      work_file_name = work_file_name[1:]
    work_file_struct = _build_path_structure_(global_names=global_names,in_str=work_file_name)
    if work_file_struct['path_array'][0] != 'root':
      work_file_name = os.path.join(_getgwd_(global_names=global_names),work_file_name)
    work_file_struct = _build_path_structure_(global_names=global_names,in_str=work_file_name)
    if work_file_struct['path_array'][0] != 'root':
      raise FileNotFoundError('_build_full_path_ ' + 'path must begin with root ' + work_file_name)
    else:
      ret_val = os.path.normpath(work_file_name)
  return ret_val
#
def _build_path_structure_(global_names=None, in_str=None):
  '''
  This provides a consistent path build mechanism

  Parameters:
  ----------

  in_str:  This is assumed to be an absolute path

  Result: a dictionary with the full name and the path array
    These are called full_path and path_array

  WARNING:  The full name does not contain the following ending * if that is the last entry

  '''
  assert global_names is not None
  assert in_str is not None
  work_str = os.path.normpath(in_str)
  in_struct = []
  while work_str != '':
    work_str, last = os.path.split(work_str)
    in_struct.append(last)
  in_struct.reverse()
  #house cleaning for edge cases
  if not in_struct:
    in_struct.append('*')
  t_struct = None
  if in_struct[-1] == '*':
    t_struct = in_struct[:-1]
  else:
    t_struct = in_struct
  if not t_struct:
    t_struct = _build_path_structure_(global_names=global_names,in_str=_getgwd_(global_names))
  full_name = os.path.join(*t_struct)
  return {'full_name':full_name, 'path_array':in_struct}
def _traverse_structure_list_(global_names=None, in_struct=None):
  '''
  Traverses a structure of folders to the last one and returns the information on the last element of the lsit

  Parameters:
  ===========
  global_names - the object with the global names
  in_struct:  The array with the list of directories that ends in a directory or file (as appropriate)

  Result:
  =======
  A dictionary with the full name and the information from the search

  '''
  assert global_names is not None
  assert in_struct is not None
  if (not in_struct) or (in_struct[0] != 'root'):
    raise FileNotFoundError('_traverse_struct_list_ expects a path array starting at root ' + pformat(in_struct))
  myDrive = global_names.myDrive
  file_id = 'root'
  file_path = []
  file_path.append(file_id)
  for cur_name in in_struct[1:-1]:
    file_result = []
    file_list = myDrive.ListFile({'q': "title contains '{:s}' and '{:s}' in parents and trashed=false".format(cur_name, file_id)}).GetList()
    if not file_list:
      break
    else:
      if len(file_list) > 1:
        raise FileExistsError('_list_file_dict_ only supports a single parent of the same name, GoogleDrive allows this but this does not')
      file_name = file_list[0]['title']
      file_id = file_list[0]['id']
      file_path.append(file_name)
  else:
    file_result = []
    c_name = in_struct[-1]
    if len(in_struct) > 1:
      file_list = myDrive.ListFile({'q': "title contains '{:s}' and '{:s}' in parents and trashed=false".format(c_name, file_id)}).GetList()
      if file_list:
        for file_info in file_list:
          file_name = file_info['title']
          file_id = file_info['id']
          file_type = file_info['mimeType']
          t_dict = {"title" : file_name, "id":  file_id, 'mimeType':file_type}
          try:
            t_dict['fileSize'] = file_info['fileSize']
          except KeyError:
            pass
          file_result.append(t_dict)
        if len(file_list) == 1:
          file_path.append(file_name)
    else:
      drive_file = myDrive.CreateFile({'id': '{:s}'.format(c_name)})
      t_dict = {'id': drive_file['id']}
      file_result.append(t_dict)
  return {'full_name': os.path.join(*file_path), 'file_result':file_result}