'''
Tools to manage the google drive authentication process
'''
import warnings
import pydrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
def check_authentication(cred_file=None):
    '''
    Purpose:  This checks to verify that the creditionals file exists and that it is valid.

    Inputs:
    cred_file - The full path to the creditional file

    Outputs:
    None
    '''
    assert cred_file is not None
    assert isinstance(cred_file,str)
    gauth = GoogleAuth()
    # Try to load saved client credentials
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        gauth.LoadCredentialsFile(cred_file)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(cred_file)
#