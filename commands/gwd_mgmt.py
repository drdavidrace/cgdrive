'''
gwd commands - gwd stands for google drive working directory

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

def getgwd(gnames=None,verbose=False):
  '''
  Purpose:  Get the google directory information for the google
  current working directory.

  Inputs: gnames - the object of global names

  Outputs:  the directory information, including
    name, ...
  '''
  assert gnames is not None
  gwd_name = _getgwd_(gnames=gnames)
  #Check the google drive
  myGDrive = _get_drive_(gnames=gnames)
  gnames.myDrive = myGDrive
  isConnected = _is_connected_(gnames)
  if verbose:
    print("The google drive connection status {}".format(isConnected))
  file_info = None
  file_info = _get_file_metadata_(gnames=gnames,file_str=gwd_name)
  if verbose:
    pprint(file_info)
  return file_info['full_name'], file_info['id']
  
#
#  Private commands
#
def  _is_connected_(gnames=None):
  '''
  This returns True if it is connected and False otherwise.
  #
  Inputs:
  -----------
  gnames - the global information for this function
  #
  Returns:
  --------
  True if connected and False otherwise
  '''
  assert gnames is not None
  return True if(_drive_about_(myDrive=gnames.myDrive)['kind'] == 'drive#about') else False
#
def _getgwd_(gnames=None,verbose=False):
  '''
  Purpose:  get the google working directory from the gwd_file

  Inputs:  gnames - the global names object

  Outputs:  The first line of the file gwd_file
  '''
  assert gnames is not None
  gwd_file = gnames.gwd_file()
  gwd_name = None
  with open(gwd_file,"r") as f:
    gwd_name = f.readline()
    gwd_name = gwd_name.strip()
    f.close()
  return gwd_name
def _get_file_metadata_(gnames=None, file_str=None):
  '''
  Purpose:
    Obtains the file meta data for a file pointed to by file_str.

  Inputs:
  ===========
  gnames - the object with the gobal data for this capability
  myDrive - the google drive object
  file_str:  The path name for the file of interest
  Outputs:
  ========
  None if there is an issue with the touching the file
  The entire metadata if the file is found
  '''
  assert gnames is not None
  assert file_str is not None
  myDrive = gnames.myDrive
  ret_val = None
  file_info = _find_file_id_(gnames=gnames,file_str=file_str)
  if file_info:
    drive_file = myDrive.CreateFile({'id': '{:s}'.format(file_info['id'])})
    ret_val = file_info
  return ret_val
def _get_drive_(gnames=None, verbose=True):
  '''
  Purpose:  Return the pydrive.drive information

  Inputs:  The credential file (if any)

  Outputs:  The drive object

  NOTE:  This doesn't use an object approach since the command line
  doesn't support maintaining objects.  Not overly efficient but okay
  '''
  assert gnames is not None
  gauth = None
  if gnames.authentication is not None:
    gauth = gnames.authentication
  else:
    gauth = am.check_authentication(cred_file=gnames.cred_file())
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
def _find_file_id_(gnames=None, file_str=None):
  '''
  This finds a file id for a file sent in by in_str
  Parameters
  ==========
  in_str:  The assumed path to a file or directory
  Results
  =======
  A file id for a path or None
  '''
  assert gnames is not None
  assert file_str is not None
  w_str = _build_full_path_(gnames=gnames, in_str=file_str)
  file_struct = _build_path_structure_(gnames=gnames,in_str=w_str)
  r_val = _traverse_structure_list_(gnames=gnames, in_struct=file_struct['path_array'])
  p_val = r_val['file_result']
  ret_val = None
  if p_val:
    if len(p_val) > 1:
      raise FileNotFoundError('_find_file_id found too many files' + pformat(p_val))
    ret_val = {'full_name':r_val['full_name'], 'id': p_val[0]['id']}
  return ret_val
#
def _build_full_path_(gnames=None, in_str=None):
  '''
  This builds a theoretical absolute GoogleDrive path

  Parameters:
  ----------

  in_str:  The proposed directory string

  Result:
  ------
  An absolute path starting at 'root'
  '''
  assert gnames is not None
  assert in_str is not None
  ret_val = None
  if not in_str.strip():
    ret_val = _getgwd_(gnames=gnames)
  else:
    work_file_name = os.path.normpath(in_str.strip())
    if work_file_name[0] == '/':
      work_file_name = work_file_name[1:]
    work_file_struct = _build_path_structure_(gnames=gnames,in_str=work_file_name)
    if work_file_struct['path_array'][0] != 'root':
      work_file_name = os.path.join(_getgwd_(gnames=gnames),work_file_name)
    work_file_struct = _build_path_structure_(gnames=gnames,in_str=work_file_name)
    if work_file_struct['path_array'][0] != 'root':
      raise FileNotFoundError('_build_full_path_ ' + 'path must begin with root ' + work_file_name)
    else:
      ret_val = os.path.normpath(work_file_name)
  return ret_val
#
def _build_path_structure_(gnames=None, in_str=None):
  '''
  This provides a consistent path build mechanism

  Parameters:
  ----------

  in_str:  This is assumed to be an absolute path

  Result: a dictionary with the full name and the path array
    These are called full_path and path_array

  WARNING:  The full name does not contain the following ending * if that is the last entry

  '''
  assert gnames is not None
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
    t_struct = _build_path_structure_(gnames=gnames,in_str=_getgwd_(gnames))
  full_name = os.path.join(*t_struct)
  return {'full_name':full_name, 'path_array':in_struct}
def _traverse_structure_list_(gnames=None, in_struct=None):
  '''
  Traverses a structure of folders to the last one and returns the information on the last element of the lsit

  Parameters:
  ===========
  gnames - the object with the global names
  in_struct:  The array with the list of directories that ends in a directory or file (as appropriate)

  Result:
  =======
  A dictionary with the full name and the information from the search

  '''
  assert gnames is not None
  assert in_struct is not None
  if (not in_struct) or (in_struct[0] != 'root'):
    raise FileNotFoundError('_traverse_struct_list_ expects a path array starting at root ' + pformat(in_struct))
  myDrive = gnames.myDrive
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
          except KeyError as e:
            pass
          file_result.append(t_dict)
        if len(file_list) == 1:
          file_path.append(file_name)
    else:
      drive_file = myDrive.CreateFile({'id': '{:s}'.format(c_name)})
      t_dict = {'id': drive_file['id']}
      file_result.append(t_dict)
  return {'full_name': os.path.join(*file_path), 'file_result':file_result}