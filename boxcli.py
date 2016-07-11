import click

from cmd_user import cmd_user
from cmd_folder import cmd_folder
from cmd_file import cmd_file

boxcli = click.CommandCollection(sources=[cmd_user, cmd_folder, cmd_file])
