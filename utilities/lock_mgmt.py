import os
import glob
from pprint import pprint
import utilities.file_utilities as flu
import time
#Get the application lock
def get_process_lock(
    gnames=None, 
    verbose=False):
    '''
    Purpose:  This creates a process lock file and tries to link the global lock file
    to the process lock file.  This ensures that only a single process is doing a task.
    This should be wrapped with the release_process_lock inside each gdrive_connect functions
    that manages the gdrive files.

    Inputs:
    gnames - the object that contains the global names used by this application
    verbose - option to output verbose information to stdout

    Outputs:
    process lock file linked to the global lock file - if successful
    True/False regarding the ability to create the link
    '''
    assert gnames is not None
    process_lock_file = gnames.process_lock_file()
    global_lock_file = gnames.global_lock_file()
    max_lock_retries = gnames.max_lock_retries
    current_pid = gnames.current_pid
    if verbose:
        dir_list = os.listdir(gnames.info_dir_name())
        for f in dir_list:
            pprint(f)
    with open(process_lock_file, 'w+') as f:
        f.write("{:d}\n".format(current_pid))
    f.close()
    current_count = 0
    lock_acquired = False
    while not lock_acquired and current_count < max_lock_retries:
        try:
            os.link(process_lock_file, global_lock_file)
            lock_acquired = True
        except Exception as e:
            result = os.stat(process_lock_file)
            lock_acquired = (result.st_nlink == 2)
            if verbose:
                pprint(e)
            pass
        if not lock_acquired:
            current_count += 1
            time.sleep(5)
    if not lock_acquired:
        os.remove(process_lock_file)
    if verbose:
        dir_list = os.listdir(gnames.info_dir_name())
        for f in dir_list:
            pprint(f)
    return lock_acquired

def release_process_lock(
    gnames=None,
    verbose=False):
    '''
    Purpose:  This is the pair for the get_process_lock that ensure that only a single process
    is working on the gdrive at a time.
    '''
    process_lock_file = gnames.process_lock_file()
    global_lock_file = gnames.global_lock_file()
    if verbose:
        pprint(process_lock_file)
        pprint(global_lock_file)
    os.unlink(global_lock_file)
    p_lock_file=flu.create_process_lockfile_name(
        dir_name=gnames.info_dir_name(), file_name=gnames.process_lock_name, 
        pid='*', create_dir=False)
    for f in glob.glob(p_lock_file):
        os.remove(f)
    return True