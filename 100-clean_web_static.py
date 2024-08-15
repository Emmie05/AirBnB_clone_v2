#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives.
"""
import os
from fabric.api import env, local, run, cd, lcd

env.hosts = ["3.83.253.154", "34.229.66.227"]

def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = int(number)
    if number <= 1:
        number = 1

    with lcd("versions"):
        archives = sorted(os.listdir("versions"), reverse=True)
        if len(archives) > number:
            for archive in archives[number:]:
                local("rm ./{}".format(archive))

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        if len(archives) > number:
            for archive in archives[number:]:
                run("rm -rf ./{}".format(archive))
