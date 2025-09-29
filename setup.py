#!/usr/bin/env/python

from setuptools import setup, find_packages
import os
import re

# source path for the class' package. Amend if necessary
PACKAGE_SOURCE_DIR = "path/to/class/directorz"

# Amend this section with your custom data
PACKAGE_NAME="package-name"
DESCRIPTION = "package-description"
AUTHOR = "author-name"
AUTHOR_EMAIL = "author@email.com"
URL = "https://www.url.com/to/my/repository"
# https://pypi.org/classifiers/
CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
    "Operating System :: OS Independent",
    "Development Status :: 4 - Beta",
    "Framework :: Robot Framework",
]
INSTALL_REQUIRES=[
    "package_1", 
    "package_2"
]
KEYWORDS=[
    "Notifications", 
    "Notification Service", 
    "Push Notifications", 
    "Notifier", 
    "Alerts", 
    "Robot Framework"
]
LICENSE="GNU General Public License v3 (GPLv3)"

def running_in_a_github_action():
    return os.getenv("GITHUB_ACTIONS") == "true"

if __name__ == "__main__":
    # get README and use it as long description
    with open("README.md", "r") as fh:
        LONG_DESCRIPTION = fh.read()

    GITHUB_PROGRAM_VERSION = ""
    
    if running_in_a_github_action():
        # Only run this branch if we are part of a Github action. Otherwise, just skip
        # it as we won't be able to get the version info from Github anyway
        #
        # get VERSION value from Github workflow and terminate workflow if value is None
        GITHUB_PROGRAM_VERSION = os.getenv("GITHUB_PROGRAM_VERSION")
        if not GITHUB_PROGRAM_VERSION:
            raise ValueError("Did not receive release label version info from GitHub")
    else:
        if len(GITHUB_PROGRAM_VERSION == 0):
            raise ValueError("Manual run requires a manually set GITHUB_PROGRAM_VERSION; change setup.py accordingly")
    
    # Main setup branch
    setup(
        name=PACKAGE_NAME,
        version=GITHUB_PROGRAM_VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        packages=find_packages(where=PACKAGE_SOURCE_DIR),
        include_package_data=True,
        classifiers=CLASSIFIERS,
        license=LICENSE,
        install_requires=INSTALL_REQUIRES,
        keywords=KEYWORDS,
    )
