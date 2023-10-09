#!/usr/bin/python3
"""Task3: Fab file for fabric practice in python
to automate compress files and dirs for
web static folder
then deploy on multiple web servers
"""

# Import Fabric's API module
from fabric.api import *
import os
from time import strftime
web_01_IP = '54.165.176.205'
web_02_IP = '52.204.94.151'
env.hosts = [web_01_IP, web_02_IP]


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
        if not (os.path.exists(archive_path)):
            return False

        dirpath = "/data/web_static/releases/"
        # else continue task requirements
        put(archive_path, '/tmp/')

        # flname_wth_ext : filname including(with) extension
        flname_wth_ext = os.path.basename(archive_path)
        # flname_no_extn : filname without extension
        # extn : extension
        flname_no_extn, extn = os.path.splitext(flname_wth_ext)

        # remove old versions of same archive from prev. script runs
        run("rm -rf {}{}/".format(dirpath, flname_no_extn))

        # create all folders and sub folders to uncompress file archive
        run("mkdir -p {}{}/".format(dirpath, flname_no_extn))

        # uncompress archive to desired location
        # --strip-components=1 option means to uncompress content of webstatic
        # folder without creating folder called webstatic

        run("tar -xzf /tmp/{} -C {}{}/ --strip-components=1".format(
            flname_wth_ext, dirpath, flname_no_extn))

        # remove archive from tmp folder after being uncompressed above
        run("rm /tmp/{}".format(flname_wth_ext))

        # Delete symbolic link /data/web_static/current from remote server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on remote web
        # server, linked to the new version of benn uncompressed
        run("ln -s {}{}/ /data/web_static/current".format(
            dirpath, flname_no_extn))

        print("Task 2 : New version deployed!")

        return True

    except Exception as e:
        # print(e)
        return False

def deploy():
    """
    compine above methods do_pack() & do_deploy()
    Usage: 
    fab -f 3-deploy_web_static.py deploy -i ssh_pri_key
    -u remote_username
    """
    # archive file on local machine
    path = do_pack()

    if path is None:
        return False
    # distribute this archive to remote server
    # Also clean tmp or old files on remote before finishing
    return do_deploy(path)
