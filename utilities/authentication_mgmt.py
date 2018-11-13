'''
Tools to manage the google drive authentication process

'''
import os
import warnings
import pydrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pprint import pprint
def check_authentication(cred_file=None, verbose=False):
    '''
    Purpose:  This checks to verify that the creditionals file exists and that it is valid.

    Inputs:
    cred_file - The full path to the creditional file

    Outputs:
    gauth information
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
        pprint("Token Expired")
        os.remove(cred_file)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            gauth.LoadCredentialsFile(cred_file)
        gauth.LocalWebserverAuth()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(cred_file)
    # return the gauth
    return gauth
