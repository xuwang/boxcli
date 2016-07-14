# boxcli - A Command Line Utility for Box 
_boxcli_ is written in Python with Click and Box SDK.

## Clone the repo

```
$ git clone https://gitlab.med.stanford.edu/irt-dcs/boxcli
$ cd boxcli

```

## Install 
Using python virtualenv is highly recommended.

### Setup Virtualenv (Optional) 

```
# Install virtualenv if not already installed
$ sudo pip install virtualenv

# Create project venv
$ virtualenv venv

# Activate  project venv whenever you want to work the project
$ . venv/bin/activate

# And if you want to go back to the real world:
$ deactivate

```

### Install boxcli

```
$ pip install --editable .
```

## Setup Box App and Config JWT Auth for _boxcli_

* Create and Config a new Box App by following instructions on [This Doc](https://docs.box.com/docs/configuring-box-platform)
* Config JWT Authentication by following instructions on [This Doc](https://docs.box.com/docs/app-auth)
* Set following values in env.sh:

	```
	export BOX_CLIENT_ID=
	export BOX_CLIENT_SECRET=
	export BOX_ENTERPRISE_ID=
	export BOX_JWT_KEY_ID=
	export BOX_PRIVATE_KEY_FILE=
	export BOX_DEFAULT_APP_USER_NAME=
	```
	
## Create the Default App User if you don't already have one
_boxcli_ handles box resources, i.e. folders/files, on behalf of a "box app user" as documented in [Creating Your First App User](https://docs.box.com/docs/app-users):

```
$ source env.sh
$ boxcli user create "${BOX_DEFAULT_APP_USER_NAME}"
```
This is the default app user when you manange folder/files in Box.

## Folder Operations

### List folders

```
$ boxcli folder list
```

### Create a folder

```
$ boxcli folder create myfiles
```

### Delete a folder

```
$ boxcli folder delete  myfiles
```
**Warning:** All items under _myfiles_ will be deleted recursively!

## File Operations

### List files

```
$ boxcli file list
```

### Upload a file

```
$ boxcli file upload README.md
```

### Download a file

```
$ boxcli file download README.md
```

### Update content of a file

```
$ boxcli file update README.md
```

### Delete a file

```
$ boxcli file delete README.md
```

## Getting Help

```
$ boxcli --help 
Usage: boxcli [OPTIONS] COMMAND [ARGS]...
  box command line tool
Options:
  --help  Show this message and exit.
Commands:
  file    sub-commands for manage box files.
  folder  sub-commands for manage box folders.
  user    sub-commands for manage box app users.
...

$ boxcli folder --help
Usage: boxcli folder [OPTIONS] COMMAND [ARGS]...
  sub-commands for manage box folders.
Options:
  --help  Show this message and exit.
Commands:
  create  Create a folder.
  delete  Delete a folder.
  get     Get a folder attributes by path.
  list    List items in a folder.
...
```
