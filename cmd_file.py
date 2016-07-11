import os, sys, click
from os.path import basename
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
    root_folder = client.folder(folder_id=parent_id).get()
    #owner = root_folder.owned_by
    #print('The root file is owned by: {0} (id: {1})'.format(owner['name'], owner['id']))

    items = root_folder.get_items(limit=limit, offset=offset)
    n = 0
    for item in items:
        if item.type == 'file':
            n += 1
            print(repr(item))
    if n == 0:
        print "No items found."

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('file_name')
def find(user, file_name, limit, offset, parent_id):
    """Find files by name."""
    client=user_client(user)
    results = find_items(client, user, file_name, limit, offset, parent_id)
    if len(results) > 0:
        for item in results:
            if item.type == 'file':
                print(repr(item))
    else:
        print('no matching items')

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('file_name')
def get(user, file_name, parent_id):
    """Get a file by name."""
    client=user_client(user)
    item = get_file(client, file_name, parent_id)
    if item is not None:
        exit(repr(item))
    else:
        print "No file found."

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.option('--accelerator/--no-accelerator', default=False, help='enable upload via accelerator')
@click.argument('file')
def upload(user, file,parent_id, accelerator):
    """Upload a file."""
    client=user_client(user)
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file)
    file_name = basename(file)

    try:
        parent = client.folder(folder_id=parent_id)
        a_file = parent.upload(file_path, file_name=file_name, upload_using_accelerator=accelerator)
        print("File '{0}' uploaded.".format(file_name))
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.option('--local-file', '-f', help='local file name')
@click.argument('file')
def download(user, file, local_file, parent_id, ):
    """download a file."""
    file_name = basename(file)
    if local_file is None:
        local_file = file_name
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), local_file)

    client=user_client(user)
    try:
        parent = client.folder(folder_id=parent_id)
        box_file = get_file(client, file_name, parent_id)
        if box_file is not None:
            file = open(local_file, 'w')
            file.write(box_file.content())
            file.close()
        else:
            print "File '{0}' not found.".format(file_name)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.option('--local-file', '-f', help='local content file')
@click.argument('file')
def update(user, file, local_file, parent_id, ):
    """Update a file."""
    file_name = basename(file)
    if local_file is None:
        local_file = file_name
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), local_file)

    client=user_client(user)
    try:
        parent = client.folder(folder_id=parent_id)
        file_v1 = get_file(client, file_name, parent_id) 
        if file_v1 is not None:
            file_v2 = file_v1.update_contents(file_path)
            print("File '{0}' updated.".format(file_name))
        else:
            print "File '{0}' not found.".format(file_name)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('file_name')
@click.argument('new_name')
def rename(user, file_name, new_name, parent_id):
    """Rename a file."""
    client=user_client(user)
    item = get_file(client, file_name, parent_id)
    if item is not None:
        try:
            item.rename(new_name)
            print "File '{0}'' has been renamed to '{1}'".format(file_name, new_name)
        except BoxAPIException as err:
            exit("Box api error: {0}".format(err))
    else:
        print "No file '{0}' found.".format(file_name)

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app name.')
@click.option('--parent-id', '-p', default='0', help='parent id')
@click.argument('file_name')
def delete(user, file_name, parent_id):
    """Delete a folder."""
    client=user_client(user)
    try:
        file = get_file(client, file_name, parent_id)
        if file is not None:
            file.delete()
            print ("File '{0}'' deleted".format(file_name))
        else:
            print "No file '{0}' found.".format(file_name)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

def find_items(client, user, file_name, limit, offset, parent_id):
    """Find items by name.
        Issue: search api may miss newly created items"""
    try:
        return client.search(
            file_name,
            limit=limit,
            offset=offset,
            ancestor_folders=[client.folder(folder_id=parent_id)],
        )
    except BoxAPIException as err:
        exit("Box api error: {0}".format(err))

def get_file(client, file_name, parent_id):
    parent_folder = client.folder(folder_id=parent_id).get()
    items = parent_folder.get_items(limit=None, offset=0)
    if len(items) > 0:
        for item in items:
            if item.name == file_name and item.type == 'file':
                return(item)
    return None