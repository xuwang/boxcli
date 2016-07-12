import os, sys, click
from os.path import basename, dirname
from boxsdk.exception import *
from auth import *
from cmd_folder import create_folder, get_folder

FOLDER_TYPE='folder'
FILE_TYPE='file'

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
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.option('--limit', '-l', default=20, help='max number of items to get.')
@click.option('--offset', '-o', default=0, help='offset of items to get.')
@click.argument('folder', default='/')
def list(user, folder, limit, offset):
    """List file in folder."""
    client = user_client(user)
    parent = get_folder(client, folder)
    n = 0
    if parent is not None:
        items = parent.get_items(limit=limit, offset=offset)
        for item in items:
            if item.type == FILE_TYPE:
                n += 1
                print(repr(item))
    if n == 0:
        print "No items found."

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.argument('path')
def get(user, path):
    """Get a file by path."""
    client=user_client(user)
    item = get_file(client, path)
    if item is not None:
        exit(repr(item))
    else:
        print "No file found."

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.option('--accelerator/--no-accelerator', default=False, help='enable upload via accelerator')
@click.option('--local-file', '-f', help='local file path to be uploaded')
@click.argument('path')
def upload(user, path, local_file, accelerator):
    """Upload a file."""
    file_name = basename(path)
    if local_file is None:
        local_file = file_name
    client=user_client(user)
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), local_file)

    try:
        parent = create_folder(client, dirname(path))
        a_file = parent.upload(file_path, file_name=file_name, upload_using_accelerator=accelerator)
        print "'{0}' has been uploaded as '{1}'".format(local_file, path)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.option('--local-file', '-f', help='local file name')
@click.argument('path')
def download(user, path, local_file):
    """Download a file."""
    if local_file is None:
        local_file =  basename(path)
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), local_file)

    client=user_client(user)
    try:
        box_file = get_file(client, path)
        if box_file is not None:
            file = open(local_file, 'w')
            box_file.download_to(file)
            file.close()
            print "'{0}' has been downloaded as '{1}'".format(path, local_file)
        else:
            print "File '{0}' not found.".format(path)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.option('--local-file', '-f', help='local content file')
@click.argument('path')
def update(user, path, local_file):
    """Update a file."""
    file_name = basename(path)
    if local_file is None:
        local_file = file_name
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), local_file)

    client=user_client(user)
    try:
        file_v1 = get_file(client, path) 
        if file_v1 is not None:
            file_v1.update_contents(file_path)
            print("File '{0}' updated.".format(path))
        else:
            print "File '{0}' not found.".format(path)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.argument('path')
@click.argument('new_name')
def rename(user, path, new_name):
    """Rename a file."""
    client=user_client(user)
    item = get_file(client, path)
    if item is not None:
        try:
            item.rename(new_name)
            print "File '{0}'' has been renamed to '{1}'".format(path, new_name)
        except BoxAPIException as err:
            exit("Box api error: {0}".format(err))
    else:
        print "No file '{0}' found.".format(path)

@file.command()
@click.option('--user', '-u', envvar='BOX_DEFAULT_APP_USER_NAME', help='box app user name.')
@click.argument('path')
def delete(user, path):
    """Delete a folder."""
    client=user_client(user)
    try:
        file = get_file(client, path)
        if file is not None:
            file.delete()
            print ("File '{0}'' deleted".format(path))
        else:
            print "No file '{0}' found.".format(path)
    except BoxAPIException as err:
        print("Box api error: {0}".format(err))

def get_file(client, path):
    parent_path = dirname(path)
    parent = get_folder(client, parent_path)
    if parent is not None:
        items = parent.get_items(limit=None, offset=0)
        for item in items:
            if item.name == basename(path) and item.type == FILE_TYPE:
                return(item)
    return None