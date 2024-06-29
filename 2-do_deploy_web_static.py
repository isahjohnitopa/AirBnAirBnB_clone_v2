#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from datetime import datetime
from os import path

# Define the hosts, user, and SSH key for Fabric
env.hosts = ['100.26.252.189', '100.26.232.86']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_deploy(archive_path):
    """Deploy web files to server
    """
    try:
        # Check if the archive path exists
        if not path.exists(archive_path):
            return False

        # Upload archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Extract timestamp from the archive path
        timestamp = archive_path[-18:-4]

        # Create the target directory on the server
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # Uncompress the archive into the target directory
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Remove the archive from the /tmp/ directory
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # Move the contents to the web_static folder
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Remove the now-empty web_static directory
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(timestamp))

        # Delete the existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(timestamp))
    except Exception as e:
        print("An error occurred: ", e)
        return False

    return True
