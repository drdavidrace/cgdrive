#Get the mgmt directory lock
def get_process_lock(global_lock_file=None, process_lock_file=None, current_pid=None, max_lock_retries=1):
    '''
    Purpose:  This creates a process lock file and tries to link the global lock file
    to the process lock file.  This ensures that only a single process is doing a taskself.
    This should be wrapped with the release_process_lock inside each gdrive_connect functions
    that manages the gdrive files.
    '''
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
            pprint(e)
            pass
        if not lock_acquired:
            current_count += 1
            time.sleep(5)
    return lock_acquired

def release_process_lock(global_lock_file=None, process_lock_file=None, current_pid=None, max_lock_retries=1):
    '''
    Purpose:  This is the pair for the get_process_lock that ensure that only a single process
    is working on the gdrive at a time.
    '''
    os.unlink(global_lock_file)
    os.remove(process_lock_file)
    return True