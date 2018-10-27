'''
This contains a set of simple utilities that are used to keep the code
simple but also check the quality of the implementation as it proceeds
'''
import os
from pathlib import Path
import errno
#
def create_file_name(dir_name=None, file_name=None, create_dir=False):
    '''
    Purpose:  Create a file name from a directory name.  This will eliminate the
    need for using globals outside of the main routine.  The create_dir flag is
    used to create the directory if necessary.

    NOTE:  This only creates the file name.  The creation of the actual file is
    a different function.

    Inputs:
    dir_name - The name of a directory.  This is checked for existance.
    file_name - The name of the file
    check_dir - Check if the dirctory is a real directory
    create_dir - The directory is created if it doesn't exist if this is True

    Outputs:
    None if the directory doesn't exist and create_dir == True

    full path name in other cases
    '''
    assert dir_name is not None
    assert file_name is not None

    file_name = os.path.join(dir_name, file_name)
    if not create_dir:
        normpath = os.path.normpath(file_name)
        full_path = os.path.realpath(normpath)
        return full_path
    else:
        dir_exists = os.path.isdir(dir_name)
        normpath = os.path.normpath(file_name)
        full_path = os.path.realpath(normpath)
        if dir_exists:
            return full_path
        else:
            try:
                mkpath = os.path.dirname(full_path)
                os.makedirs(mkpath,exist_ok=True)
            except Exception as e:
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), full_path)
            return full_path
#
def create_file(file_name=None, overwrite=False, create_dir=False):
    '''
    Purpose:  This creates a file using the given file name.  It checks to verify if the
    path is relative to the cwd or a full path

    Inputs:
    file_name:  This is the file name to create, must be a full file name
    overwrite:  If True overwrite an existing file if it exists; otherwise, do not
    overwrite
    create_dir:  If True, create any directory leaves as necessary; otherwise
    do not create the directory tree

    Outputs:
    None if the file was not able to be created
    file_name if the file was created or overwritten

    Side Effects:  A file is created with the given name if able
    '''
    assert file_name is not None
    work_file_name = os.path.normpath(file_name)
    dir_name, f_name = os.split(work_file_name)
    dir_name = dir_name if os.path.isabs(dir_name) else os.path.join(os.getcwd(),dir_name)
    if not create_dir and not os.path.isdir(dir_name):
        return None
    if create_dir and not os.path.isdir(dir_name):
        try:
            path = Path(dir_name)
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), dir_name)
    real_file_name = os.path.join(dir_name, f_name)
    if not overwrite:
        if os.path.isfile(real_file_name):
            return real_file_name
        else:
            try:
                os.close(os.open(real_file_name,'x'))
            except Exception as e:
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), dir_name)
            return real_file_name
    else:
        if os.path.isfile(real_file_name):
            with open(real_file_name, 'w+') as f:
                f.seek(0)
                f.truncate()
                f.close()
            return real_file_name
        else:
            try:
                os.close(os.open(real_file_name,'x'))
            except Exception as e:
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), dir_name)
            return real_file_name
