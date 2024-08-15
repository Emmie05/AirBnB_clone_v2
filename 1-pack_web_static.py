#!/usr/bin/python3
"""A module for Fabric script that generates a .tgz archive."""
import os
from datetime import datetime
from fabric.api import local, runs_once

@runs_once
def do_pack():
    """Archives the static files."""
    # Create the versions directory if it doesn't exist
    if not os.path.isdir("versions"):
        os.makedirs("versions")
    
    # Generate the filename with timestamp
    d_time = datetime.now()
    output = "versions/web_static_{:04}{:02}{:02}{:02}{:02}{:02}.tgz".format(
        d_time.year,
        d_time.month,
        d_time.day,
        d_time.hour,
        d_time.minute,
        d_time.second
    )
    
    try:
        print("Packing web_static to {}".format(output))
        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(output))
        
        # Check the size of the created archive
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
        
        return output
    except Exception as e:
        print("Failed to pack web_static: {}".format(e))
        return None
