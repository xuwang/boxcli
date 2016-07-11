import os, sys, click
from boxsdk import JWTAuth
from boxsdk import Client
from boxsdk import LoggingClient
from boxsdk.exception import *


def get_first_user_by_name(client, name):
    """ Get the first app user by name. Note: user name is NOT unique """
    for user in client.users():
        if user.name == name:
            return user
    return  None

def get_user_by_id(client, id):
    """ get app user by id """
    try:
        return client.user(user_id=id).get()
    except BoxAPIException as err:
        exit("Box api error: {0}".format(err))
        
def user_client(app_user_name):
    """ authenticate the app user by name and return the box user client """
    client = instance_client()
    user = get_first_user_by_name(client, app_user_name)
    if user is None:
        exit ("Error: app user {0} is not exist.".format(app_user_name))
    try:
        client.auth.authenticate_app_user(user)
    except BoxAPIException as err:
        exit("Box api error: {0}".format(err))
    return client

def instance_client():
    """ authenticate the app and return the box instance client """
    oauth=auth()
    return Client(oauth)

def store_tokens(access_token, refresh_token):
    pass
    # store the tokens at secure storage (e.g. Keychain)
    # tokens will be stored in memory for the duration of the Python script run,
    # so we don't always need to pass store_tokens.

def auth():
    # check auth conf
    for k in ["BOX_CLIENT_ID", "BOX_CLIENT_SECRET", "BOX_ENTERPRISE_ID", "BOX_JWT_KEY_ID", "BOX_PRIVATE_KEY_FILE" ]:
        if os.environ.get(k) is None:
            exit("ERROR: {0} is not defined!".format(k))
    # get oauth token
    oauth = JWTAuth(
        client_id = os.environ.get('BOX_CLIENT_ID'),
        client_secret = os.environ.get('BOX_CLIENT_SECRET'),
        enterprise_id = os.environ.get('BOX_ENTERPRISE_ID'),
        jwt_key_id = os.environ.get('BOX_JWT_KEY_ID'),
        rsa_private_key_file_sys_path = os.environ.get('BOX_PRIVATE_KEY_FILE'),
        #store_tokens=store_tokens,
    )
    try:
        oauth.authenticate_instance()
    except BoxAPIException as err:
        exit("Box api error: {0}".format(err))
    return oauth
