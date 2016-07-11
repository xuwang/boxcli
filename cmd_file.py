import os, sys, click
from boxsdk.exception import *
from auth import *

@click.group()
@click.pass_context
def cmd_file(ctx):
    pass

@cmd_file.group()
@click.pass_context
def file(ctx):
    """commands for managing box files."""
    pass

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.option('--parent-id', '-p', default='0', help='parent id')
def list(user, limit, offset, parent_id):
    """List file."""
    client = user_client(user)
    root_file = client.file(file_id=parent_id).get()
    #owner = root_file.owned_by
    #print('The root file is owned by: {0} (id: {1})'.format(owner['name'], owner['id']))

    items = root_file.get_items(limit=limit, offset=offset)
    if len(items) > 0:
        #print('This is the first {0} items in the root file:'.format(limit))
        for item in items:
            print(repr(item))
    else:
        print "No items found."

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('item_name')
def find(user, item_name, limit, offset, parent_id):
    """Find files by name."""
    client=user_client(user)
    results = find_items(client, user, item_name, limit, offset, parent_id)
    if len(results) > 0:
        for item in results:
            print(repr(item))
    else:
        print('no matching items')

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('item_name')
def get(user, item_name, parent_id):
    """Get a file by name."""
    client=user_client(user)
    results = find_items(client, user, item_name, 1, 0, parent_id,)
    if len(results) > 0:
        print results[0]
    else:
        print('no matching items')

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('file_name')
def create(user, file_name, parent_id):
    """Create a file."""
    client=user_client(user)
    try:
        parent = client.file(file_id=parent_id)
        parent.create_subfile(file_name)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.argument('file-id')
def delete(user, file_id):
    """Delete a file."""
    client=user_client(user)
    try:
        forder = client.file(file_id=file_id)
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
            ancestor_files=[client.file(file_id=parent_id)],
        )
    except BoxAPIException as err:
        exit("Box api error: {0}".format(err))
