#!/usr/bin/python3
"""Task0: Fab file for fabric practice in python
to automate compress files and dirs for
web static folder"""

# Import Fabric's API module
from fabric.api import *

from time import strftime


def do_pack():
    """A function to Create .tgz archive from
    the web_static folder.

    Returns:
        path of .tar Archive if succes, else None
    """
    name_time_frmt = strftime('%Y%m%d%H%M%S')

    try:
        local("mkdir -p versions")
        # create the .tar archive
        local("tar -czvf versions/web_static_{}.tgz web_static".format(
            name_time_frmt))
        # if succes return path of the .tar file
        return ("versions/web_static_{}.tgz".format(name_time_frmt))

    except Exception as e:  # if archive creation failed
        return None
