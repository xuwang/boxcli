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
@click.option('--parent-id', '-p', default='0', help='parent id')
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
@click.option('--parent-id', '-p', default='0', help='parent id')
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
@click.argument('folder-id')
def delete(user, folder_id):
    """Delete a folder."""
    client=user_client(user)
    try:
        forder = client.folder(folder_id=folder_id)
        forder.delete()
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

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
