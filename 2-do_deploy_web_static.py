#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to the web servers
"""

from fabric.api import put, run, env, local
from os.path import exists, isdir
from datetime import datetime

env.hosts = ["54.144.222.67", "3.84.239.71"]


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        if not isdir("versions"):
            local("mkdir versions")
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
