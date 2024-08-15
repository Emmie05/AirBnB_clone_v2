#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from datetime import datetime
from fabric.api import *
import os

env.hosts = ["3.83.253.154", "34.229.66.227"]
env.user = "ubuntu"

def do_pack():
    """Generates a .tgz archive from the web_static folder"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    
    result = local("tar -cvzf {} web_static".format(archived_f_path), capture=True)
    
    if result.succeeded:
        return archived_f_path
    else:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        print("Archive path does not exist")
        return False
    
    archive_filename = os.path.basename(archive_path)
    archive_name = archive_filename.split('.')[0]
    
    release_dir = "/data/web_static/releases/{}".format(archive_name)
    tmp_archive = "/tmp/{}".format(archive_filename)
    
    try:
        put(archive_path, tmp_archive)
        
        run("sudo mkdir -p {}".format(release_dir))
        
        run("sudo tar -xzf {} -C {}".format(tmp_archive, release_dir))
        
        run("sudo rm {}".format(tmp_archive))
        
        run("sudo mv {}/web_static/* {}".format(release_dir, release_dir))
        
        run("sudo rm -rf {}/web_static".format(release_dir))
        
        run("sudo rm -rf /data/web_static/current")
        
        run("sudo ln -s {} /data/web_static/current".format(release_dir))
        
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
