'''
These are the commands to manage the session
The session is controlled by two time elements, the start of the session and the amount of time.
These two values are stored in the session file within .gdrive
'''
import os
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from shutil import copy
import glob
from pprint import pprint
#
from utilities.file_utilities import create_file
def print_session_information(global_names=None):
    '''
    Purpose:  Prints all of the session information.  Very limited in scope

    Inputs:  global_names - this is the global names class

    Outputs:  This prints the current session information to stdout
    '''
    assert global_names is not None
    session_dir = global_names.info_file_dir()
    session_file = global_names.session_file()
    cred_file = global_names.cred_file()
    gwd_file = global_names.gwd_file()
    if not os.path.isdir(session_dir):
        print("The session path does not exist {:s}.  Run session init.".format(session_dir))
    else:
        print("The session path is: {:s}".format(session_dir))
        if not os.path.isfile(session_file):
            print("The session file does not exist{:s}. Run session init.".format(session_file))
        else:
            print("The session file is: {:s}".format(session_file))
            with open(session_file,"r") as f:
                for line in f:
                    print("\t{}".format(line.rstrip()))
                f.close()
        if not os.path.isfile(cred_file):
            print("The credential file does not exist{:s}. Run session init.".format(cred_file))
        else:
            print("The credential file is: {:s}".format(cred_file))
            with open(cred_file,"r") as f:
                for line in f:
                    pprint("\t{}".format(line))
                f.close()
        if not os.path.isfile(gwd_file):
            print("The google working directory file does not exist{:s}. Run session init.".format(gwd_file))
        else:
            print("The google working directory file is: {:s}".format(gwd_file))
            with open(gwd_file,"r") as f:
                for line in f:
                    print("\t{}".format(line.rstrip()))
                f.close()
    return True
    
# validation
def check_valid_session(info_file_dir=None, cred_file=None, session_file=None):
    assert info_file_dir is not None
    assert cred_file is not None
    assert session_file is not None

    if not os.path.isdir(info_file_dir):
        raise FileNotFoundError("Missing information directory {:s}.  Run init to create this file automatically".format(info_file_dir))
    if not os.path.isfile(cred_file):
        raise FileNotFoundError("Missing credentials file {:s}.  Run init to create this file automatically.".format(cred_file))
    if not os.path.isfile(session_file):
        raise FileNotFoundError("Missing session file {:s}.  Run init to create this file automatically".format(session_file))
    return True

# clean and init session information
def clean_session(session_file=None, gwd_file=None, are_you_sure=False):
    assert session_file is not None
    assert gwd_file is not None
    assert isinstance(session_file,str)
    assert isinstance(gwd_file, str)
    if not are_you_sure:
        return False
    else:
        if os.path.isfile(session_file):
            os.remove(session_file)
        if os.path.isfile(gwd_file):
            os.remove(gwd_file)
        return True

def super_clean_session(cred_file=None, session_file=None, gwd_file=None, are_you_sure=False):
    assert cred_file is not None
    assert session_file is not None
    assert gwd_file is not None
    assert isinstance(cred_file,str)
    assert isinstance(session_file, str)
    assert isinstance(gwd_file, str)
    if not are_you_sure:
        return False
    else:
        clean_session(session_file, gwd_file,are_you_sure=True)
        if os.path.isfile(cred_file):
            os.remove(cred_file)
        #maybe remove the directory at some point
        return True

def init_session(session_file=None, gwd_file=None, max_time=None):
    '''
    Purpose:  Initialize the session time for managing a sessionself.

    Inputs:
    session_file - the name of the session files
    max_time - maximum time for the session #in seconds
    '''
    assert session_file is not None
    assert gwd_file is not None
    assert max_time is not None
    assert isinstance(session_file, str)
    assert isinstance(gwd_file,str)
    assert isinstance(max_time,int)
    assert max_time > 0
    secrets_file = "./client_secrets.json"
    secrets_file_glob = ''.join([secrets_file,'.*'])
    secrets_glob = glob.glob(secrets_file_glob)
    if not secrets_glob:
        raise OSError("A base secrets file must exist.  This must be named secrets_file.json.[somthing]")
    print("Choose a base secrets file (by number):")
    for i in range(len(secrets_glob)):
        print("{:d}: {:s}\n".format(i,secrets_glob[i]))
    try:
        choice = int(input("Choose a number:"))
    except ValueError:
        raise ValueError("Choice was not a number")
    if choice >= len(secrets_glob):
        raise ValueError("Choice is not in the given range")
    #initialize session
    copy(secrets_glob[choice],secrets_file)
    sess_file = create_file(session_file, overwrite=True, create_dir=True)
    cur_time = str(datetime.now())
    with open(sess_file,'w+') as f:
        f.write("{:s}\n".format(cur_time))
        f.write("{:d}\n".format(max_time))
        f.write("{:s}\n".format(secrets_glob[choice]))
        f.close()
    #initialize gwd = google current working directory
    gwd_f = create_file(gwd_file,overwrite=True, create_dir=True)
    with open(gwd_f,'w+') as f:
        f.write("{:s}\n".format('root'))
        f.close()
    

    return True
