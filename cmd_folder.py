import os, sys, click
from boxsdk.exception import *
from auth import *

@click.group()
@click.pass_context
def cmd_folder(ctx):
    pass

@cmd_folder.group()
@click.pass_context
def folder(ctx):
    """commands for managing box folders."""
    pass

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.option('--parent-id', '-p', default='0', help='parent id')
def list(user, limit, offset, parent_id):
    """List folder."""
    client = user_client(user)
    root_folder = client.folder(folder_id=parent_id).get()
    #owner = root_folder.owned_by
    #print('The root folder is owned by: {0} (id: {1})'.format(owner['name'], owner['id']))

    items = root_folder.get_items(limit=limit, offset=offset)
    n = 0
    for item in items:
        if item.type == 'folder':
            n += 1
            print(repr(item))
    if n == 0:
        print "No items found."

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('folder_name')
def find(user, folder_name, limit, offset, parent_id):
    """Find folders by name."""
    client=user_client(user)
    results = find_items(client, user, folder_name, limit, offset, parent_id)
    if len(results) > 0:
        for item in results:
            if item.type == 'folder':
                print(repr(item))
    else:
        print('no matching items')

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('folder_name')
def get(user, folder_name, parent_id):
    """Get a folder by name."""
    client=user_client(user)
    item = get_folder(client, folder_name, parent_id)
    if item is not None:
        exit(repr(item))
    else:
        print "No folder found."

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
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
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('folder_name')
@click.argument('new_name')
def rename(user, folder_name, new_name, parent_id):
    """Rename a folder."""
    client=user_client(user)
    item = get_folder(client, folder_name, parent_id)
    if item is not None:
        try:
            item.rename(new_name)
        except BoxAPIException as err:
            exit("Box api error: {0}".format(err))
    else:
        print "No folder '{0}' found.".format(folder_name)

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('folder_name')
def delete(user, folder_name, parent_id):
    """Delete a folder."""
    client=user_client(user)
    try:
        folder = get_folder(client, folder_name, parent_id)
        if folder is not None:
            folder.delete()
            print ("Folder {0} deleted".format(folder_name))
        else:
            print "No folder '{0}' found.".format(folder_name)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

def find_items(client, user, folder_name, limit, offset, parent_id):
    """Find items by name.
        Issue: search api will miss newly created items"""
    try:
        return client.search(
            folder_name,
            limit=limit,
            offset=offset,
            ancestor_folders=[client.folder(folder_id=parent_id)],
        )
    except BoxAPIException as err:
        exit("Box api error: {0}".format(err))

def get_folder(client, folder_name, parent_id):
    parent_folder = client.folder(folder_id=parent_id).get()
    items = parent_folder.get_items(limit=None, offset=0)
    if len(items) > 0:
        for item in items:
            if item.name == folder_name and item.type == 'folder':
                return(item)
    return None