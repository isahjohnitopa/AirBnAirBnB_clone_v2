#!/usr/bin/python3
"""Compress web static package and deploy it to web servers"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['100.26.252.189', '100.26.232.86']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        if not path.exists(archive_path):
            return False

        # Extract the file name and the timestamp
        file_name = archive_path.split("/")[-1]
        timestamp = file_name[-18:-4]

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/{}'.format(file_name))

        # Create the directory where the archive will be unpacked
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # Uncompress the archive into the target directory
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/web_static_{}/'.format(file_name, timestamp))

        # Remove the archive from the server
        run('sudo rm /tmp/{}'.format(file_name))

        # Move the contents into the appropriate directory
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Remove the now empty web_static directory
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

        # Remove the current symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))

        return True
    except:
        return False
