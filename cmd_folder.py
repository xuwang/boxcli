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
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.argument('path', default='/')
def list(user, limit, offset, path):
    """List folder."""
    client=user_client(user)
    try:
        parent = get_folder(client, path)
        if parent is None:
            exit("No items found.")
        items = parent.get_items(limit=limit, offset=offset)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

    n = 0
    for item in items:
        n += 1
        print(repr(item))
    if n == 0:
        print "No items found."

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.argument('path')
def get(user, path):
    """Get a folder by path."""
    client=user_client(user)
    item = get_folder(client, path)
    #item = get_folder(client, folder_name, parent_id)
    if item is not None:
        exit(repr(item))
    else:
        print "No folder found."

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.argument('path')
def create(user, path):
    """Create a folder."""
    client=user_client(user)
    create_folder(client, path)

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.argument('path')
@click.argument('new_name')
def rename(user, path, new_name):
    """Rename a folder."""

    client=user_client(user)
    item = get_folder(client, path)
    if item is not None:
        try:
            item.rename(new_name)
        except BoxAPIException as err:
            exit("Box api error: {0}".format(err))
    else:
        print "No folder '{0}' found.".format(folder_name)

@folder.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.option('--force/--no-force', default=False, help='force delete even when the folder is not empty')
@click.argument('path')
def delete(user, path, force):
    """Delete a folder."""
    client=user_client(user)
    try:
        item = get_folder(client, path)
        if item is not None:
            children = item.get_items(limit=None, offset=0)
            if len(children) > 0 and not force:
                exit("The folder is not empty, use --force to force the deletion")
            item.delete()
            print ("Folder {0} deleted".format(path))
        else:
            print "No folder '{0}' found.".format(path)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

def get_folder(client, path):
    if path == '/' or not path:
        return client.folder(folder_id='0').get()

    parent_path = os.path.dirname(path)
    item_name = os.path.basename(path)
    parent = get_folder(client, parent_path)
    if parent is not None:
        items = parent.get_items(limit=None, offset=0)
        if len(items) > 0:
            for item in items:
                if item.name == item_name and item.type == 'folder':
                    return item
    return None

def create_folder(client, path):
    item = get_folder(client, path)
    if item is None:
        parent_path = os.path.dirname(path)
        item_name = os.path.basename(path)
        parent = create_folder(client, parent_path)
        try:
            item = parent.create_subfolder(item_name)
            return item.get()
        except BoxAPIException as err:
            exit("Box api error: {0}".format(err))
    return item