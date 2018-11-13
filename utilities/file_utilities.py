'''
This contains a set of simple utilities that are used to keep the code
simple but also check the quality of the implementation as it proceeds
'''
import os
from os.path import normpath, realpath
from pathlib import Path
import errno
def clean_path(in_name=None):
    assert in_name is not None
    assert isinstance(in_name, str)
    return realpath(normpath(in_name.strip()))
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
    assert isinstance(dir_name,str)
    assert isinstance(file_name,str)
    dir_name = clean_path(dir_name)
    file_name = file_name.strip()

    file_name = os.path.join(dir_name, file_name)
    full_path = clean_path(file_name)
    if not create_dir:
        return clean_path(full_path)
    else:
        dir_exists = os.path.isdir(dir_name)
        if dir_exists:
            return full_path
        else:
            try:
                mkpath = os.path.dirname(full_path)
                os.makedirs(mkpath,exist_ok=True)
            except Exception as e:
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), ''.join([full_path,e]))
            return full_path
#
def create_process_lockfile_name(dir_name=None, file_name=None, pid=None, create_dir=False):
    '''
    Purpose:  Create a file name from a process lock file.  This will eliminate the
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
    assert pid is not None
    assert isinstance(dir_name,str)
    assert isinstance(file_name,str)

    dir_name = clean_path(dir_name)
    file_name = file_name.strip()
    if isinstance(pid,int):
        file_name = clean_path(os.path.join(dir_name, ''.join(["{:d}-".format(pid),file_name])))
    elif isinstance(pid,str):
        pid = pid.strip()
        file_name = clean_path(os.path.join(dir_name, ''.join(["{:s}-".format(pid),file_name])))
    else:
        raise TypeError("Bad type: {}".format(pid))
    full_path = clean_path(file_name)
    if not create_dir:
        return full_path
    else:
        dir_exists = os.path.isdir(dir_name)
        if dir_exists:
            return full_path
        else:
            try:
                mkpath = os.path.dirname(full_path)
                os.makedirs(mkpath,exist_ok=True)
            except Exception as e:
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), ''.join([full_path,e]))
            return full_path
#
def create_dir(dir_name=None, create_dir=True):
    '''
    Purpose:  Creates a directory with the given name

    Inputs:
    dir_name:  This is the dirctory name to create
    create_dir:  If True, create any directory leaves as necessary; otherwise
    do not create the directory tree

    Outputs:
    None if the file was not able to be created
    file_name if the file was created or overwritten

    Side Effects:  A file is created with the given name if able
    '''
    assert dir_name is not None
    assert isinstance(dir_name,str)
    dir_name = dir_name if os.path.isabs(dir_name) else os.path.join(os.getcwd(),dir_name)
    dir_name = clean_path(dir_name)
    if not create_dir:
        return None
    else:
        try:
            path = Path(dir_name)
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), ''.join([dir_name,e]))
        return dir_name
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
    assert isinstance(file_name,str)
    work_file_name = clean_path(file_name)
    dir_name, f_name = os.path.split(work_file_name)
    dir_name = dir_name if os.path.isabs(dir_name) else os.path.join(os.getcwd(),dir_name)
    if not create_dir and not os.path.isdir(dir_name):
        return None
    if create_dir and not os.path.isdir(dir_name):
        try:
            path = Path(dir_name)
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), ''.join([dir_name,e]))
    real_file_name = os.path.join(dir_name, f_name)
    if not overwrite:
        if os.path.isfile(real_file_name):
            return real_file_name
        else:
            try:
                with open(real_file_name,'w+') as f:
                    f.seek(0)
                    f.truncate()
                    f.close()
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
                with open(real_file_name,'w+') as f:
                    f.seek(0)
                    f.truncate()
                    f.close()
            except Exception as e:
                raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), dir_name)
            return real_file_name
