#!/usr/bin/python3
"""Task0: Fab file for fabric practice in python
to automate compress files and dirs for
web static folder"""

# Import Fabric's API module
from fabric.api import *
from os import path
from time import strftime
web_01_IP = '54.165.176.205'
web_02_IP = '52.204.94.151'
env.hosts = [web_01_IP, web_02_IP]
env.hosts = [web_01_IP]


def do_pack():
    """A function to Create .tgz archive from
    the web_static folder.

    Returns:
        path of .tar Archive if succes, else None
    """
    name_time_frmt = strftime('%Y%m%d%H%M%S')
    arch_file_name = "web_static_{}.tgz".format(name_time_frmt)
    arch_file_path = "versions/{}".format(arch_file_name)

    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static".format(
            name_time_frmt))
        return (arch_file_path)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    transfer an archive file to all specified web servers.

    Args:
        archive_path (str): The path to the archive file to be deployed.
        it will be passed as argument to fab command, see usage

    Usage:
        fab -f 2-do_deploy_web_static.py do_deploy:archive_path=
        versions/web_static_20190513002232.tgz -i my_ssh_priv_key -u username

        as you can see -i and -u are builtin options for fab related to ssh
        connection
        will be assigned to ssh_private_key_path and ssh_username respectively
        --------------------
        Of course, you could define them as Fabric environment variables
        (ex: env.user =...), env.key_filename = ...., -i is stands for identity
        -------------------------------
        unfortunatly there is no option for passphrase I will handle this later
        outside this project, by assign a custom option just for that
        then assign this value to env.passphrase

    Returns:
        True if all operations are successful, False otherwise.
    """
    try:
        # if archive_path doesn't exist return false
        if not (path.exists(archive_path)):
                return False

        # else continue task requirements
        put(archive_path, '/tmp/')

        # flname_wth_ext : filname including(with) extension
        flname_wth_ext = os.path.basename(archive_path)
        # flname_no_extn : filname without extension
        # extn : extension
        flname_no_extn, extn = os.path.splitext(flname_wth_ext)

        dirpath = "/data/web_static/releases/"

        # remove old versions of same archive from prev. script runs
        run("rm -rf {}{}/".format(dpath, flname_no_extn))

        #create all folders and sub folders to uncompress file archive
        run("mkdir -p {}{}/".format(dpath, flname_no_extn))

        # uncompress archive to desired location
        run("tar -xzf /tmp/{} -C {}{}/".format(flname_wth_ext, dpath, flname_no_extn))

        # remove archive from tmp folder after being uncompressed above
        run("rm /tmp/{}".format(flname_wth_ext))
        return True

    except:
        return False
