import os, sys, click
from boxsdk.exception import *
from auth import *

@click.group()
@click.pass_context
def cmd_user(ctx):
    pass
    
@cmd_user.group()
@click.pass_context
def user(ctx):
    """commands for managing box app users."""
    pass

@user.command()
def list():
    """List app users."""
    client = instance_client()
    users = client.users()
    for u in users:
        print repr(u)

@user.command()
@click.argument('name')
def create(name):
    """Create new app user."""
    client = instance_client()
    user = get_first_user_by_name(client, name)
    if user is None:
        try:    
            user = client.create_user(name)
            print "Created: " + repr(user)
        except BoxAPIException as err:
            print("Box api error: {0}".format(err)) 
    else:
        print "Error: {0} already exist".format(name)

@user.command()
@click.option('--name', '-u', help='app user name.')
@click.option('--id', '-i', help='app user id.')
def get(name, id):
    """Get app users by name or id."""
    if name is None and id is None:
        raise click.BadParameter('please give either user name or id to get user', param_hint=['--name', '--id'])

    client = instance_client()
    if id is not None:
        user = get_user_by_id(client, id)
        if user is None:
            print "Error: user with user id {0} is not exist".format(id)
        else:
            print repr(user)
    else:
        for user in client.users():
            if user.name == name:
                print repr(user)

@user.command()
@click.argument('id')
def delete(id):
    """Delete app user by id."""
    client = instance_client()
    user = get_user_by_id(client, id)
    if user is None:
        print "Error: user with user id {0} is not exist".format(id)
    else:
        try:
            user.delete()
            print ("Deleted: {0}".format(repr(user)))
        except BoxAPIException as err:
            print("Box api error: {0}".format(err))