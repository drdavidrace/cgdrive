'''
These are the commands to manage the session
The session is controlled by two time elements, the start of the session and the amount of timeself.
These two values are stored in the session file within .gdrive
'''
from datetime import datetime
from datetime import timedelta
from dateutil import parser
#
from utilities.file_utilities import create_file

def init_session(session_file=None, max_time=None):
    '''
    Purpose:  Initialize the session time for managing a sessionself.

    Inputs:
    session_file - the name of the session files
    max_time - maximum time for the session #in seconds
    '''
    assert session_file is not None
    assert max_time is not None
    assert isinstance(session_file, str)
    assert isinstance(max_time,int)
    assert max_time > 0
    sess_file = create_file(session_file, overwrite=True, create_dir=True)
    cur_time = str(datetime.now())
    with open(sess_file,'w+') as f:
        f.write("{:s}\n".format(cur_time))
        f.write("{:d}\n".format(max_time))
        f.close()
    return sess_file
