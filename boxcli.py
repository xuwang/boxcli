import os, sys, click
from boxsdk import JWTAuth
from boxsdk import Client
from boxsdk import LoggingClient
from boxsdk.exception import *

@click.group()
def boxcli():
    """box command line tool"""
    pass

@boxcli.group()
def folder():
    """sub-commands for manage box folders."""
    pass

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.option('--parent_id', '-p', default='0', help='parent id')
def list(user, limit, offset, parent_id):
    """List folder."""
    client = user_client(user)
    root_folder = client.folder(folder_id=parent_id).get()
    #owner = root_folder.owned_by
    #print('The root folder is owned by: {0} (id: {1})'.format(owner['name'], owner['id']))

    items = root_folder.get_items(limit=limit, offset=offset)
    if len(items) > 0:
        #print('This is the first {0} items in the root folder:'.format(limit))
        for item in items:
            print(repr(item))
    else:
        print "No items found."

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.option('--parent_id', '-p', default='0', help='parent id')
@click.argument('item_name')
def find(user, item_name, limit, offset, parent_id):
    """Find folders by name."""
    client=user_client(user)
    results = find_items(client, user, item_name, limit, offset, parent_id)
    if len(results) > 0:
        for item in results:
            print(repr(item))
    else:
        print('no matching items')

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent_id', '-p', default='0', help='parent id')
@click.argument('item_name')
def get(user, item_name, parent_id):
    """Get a folder by name."""
    client=user_client(user)
    results = find_items(client, user, item_name, 1, 0, parent_id,)
    if len(results) > 0:
        print results[0]
    else:
        print('no matching items')

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent_id', '-p', default='0', help='parent id')
@click.argument('folder_name')
def create(user, folder_name, parent_id):
    """Create a folder."""
    client=user_client(user)
    try:
        parent = client.folder(folder_id=parent_id)
        parent.create_subfolder(folder_name)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.argument('folder_id')
def delete(user, folder_id):
    """Delete a folder."""
    client=user_client(user)
    try:
        forder = client.folder(folder_id=folder_id)
        forder.delete()
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))     

@boxcli.group()
def file():
    """sub-commands for manage box files."""
    pass

@file.command()
def list():
    """list files"""
    click.echo('Hello World!')

@boxcli.group()
def user():
    """sub-commands for manage box app users."""
    pass

@user.command()
def list():
    """List app users."""
    client = instance_client()
    users = client.users()
    for u in users:
        print repr(u)

@user.command()
@click.argument('user_name')
def create(user_name):
    """Create new app user."""
    client = instance_client()
    user = get_first_user_by_name(client, user_name)
    if user is None:
        try:    
            user = client.create_user(user_name)
            print "Created: " + repr(user)
        except BoxAPIException as err:
            print("Box api error: {0}".format(err)) 
    else:
        print "Error: {0} already exist".format(name)

@user.command()
@click.argument('user_name')
def byname(user_name):
    """Get app users by name."""
    client = instance_client()
    users = client.users()

    for user in client.users():
        if user.name == user_name:
            exit(repr(user))
    exit("No app user by name '{0}' found".format(user_name))

@user.command()
@click.argument('user_id')
def byid(user_id):
    """Get app user by id."""
    client = instance_client()
    user = get_user_by_id(client, user_id)
    if user is None:
        print "Error: user with user id {0} is not exist".format(id)
    else:
        print repr(user)

@user.command()
@click.option('--user_name', '-u', help='app user name.')
@click.option('--user_id', '-i', help='app user id.')
def get(user_name, user_id):
    """Get app users by name or id."""
    if user_name is None and user_id is None:
        raise click.BadParameter('please give either user name or id to get user', param_hint=['--user_name', '--user_id'])

    client = instance_client()
    if user_id is not None:
        user = get_user_by_id(client, user_id)
        if user is None:
            print "Error: user with user id {0} is not exist".format(id)
        else:
            print repr(user)
    else:
        for user in client.users():
            if user.name == user_name:
                print repr(user)

@user.command()
@click.argument('user_id')
def delete(user_id):
    """Delete app user by id."""
    client = instance_client()
    user = get_user_by_id(client, user_id)
    if user is None:
        print "Error: user with user id {0} is not exist".format(id)
    else:
        try:
            user.delete()
            print ("Deleted: {0}".format(repr(user)))
        except BoxAPIException as err:
            print("Box api error: {0}".format(err)) 

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

def find_items(client, user, item_name, limit, offset, parent_id):
    """Find items by name."""
    try:
        return client.search(
            item_name,
            limit=limit,
            offset=offset,
            ancestor_folders=[client.folder(folder_id=parent_id)],
        )
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
