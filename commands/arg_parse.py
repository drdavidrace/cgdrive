'''
Process the subcommand and subcommand argument, then pass back the appropriate subroutine to call
'''
import utilities.file_utilities as flu 
import utilities.lock_mgmt as lm
import utilities.authentication_mgmt as am
import commands.session_mgmt as sm
from pprint import pprint
#
sess_command = 'SESS'
sess_args = ['CL','SU','IN']
subcommands = [sess_command]
def arg_parse(
    subcommand = None, subcommand_arg=None,
    infor_file_dir=None,
    session_file=None,max_time=None,
    debug=False):
    assert subcommand is not None
    assert subcommand_arg is not None
    assert isinstance(subcommand,str)
    assert isinstance(subcommand,str)
    global subcommands
    found_valid = False
    command_success = False
    found_sess = False
    found_sess_arg = False
    subcommand = subcommand.upper()
    subcommand_arg = subcommand_arg.upper()
    if sess_command in subcommand:
        found_sess = True
        found_valid = True
    if found_sess:
        for sc in sess_args:
            if sc in subcommand_arg:
                found_sess_arg = True
                break
        if not found_sess_arg:
            found_sess = False
            found_valid = False
    if found_valid:
        if found_sess:
            assert session_file is not None
            assert max_time is not None
            assert isinstance(session_file,str)
            assert isinstance(max_time,int)
            assert max_time > 0
            if debug:
                print("Subcommand {:s}".format(subcommand))
                print("Subcommand Arg {:s}".format(subcommand_arg))
            command_success = sm.init_session(session_file=session_file,max_time=max_time)
    return found_valid, command_success

