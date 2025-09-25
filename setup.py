#!/usr/bin/env/python

from setuptools import setup, find_packages
import os
import re

VERSION_REGEX = r'__version__\s*=\s*"(.*)"'

PACKAGE_SOURCE_DIR = "src"

PACKAGE_NAME="my package name"
DESCRIPTION = "my description"
AUTHOR = "author_name"
AUTHOR_EMAIL = "author@email"
URL = "https://www.url.com/to/my/repository"
# https://pypi.org/classifiers/
CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Development Status :: 4 - Beta",
    "Framework :: Robot Framework",
]
INSTALL_REQUIRES=[
    "my_packet_1",
    "my_packet_2",
]
KEYWORDS=[
    "My Keyword 1",
    "My Keyword 2",
]
LICENSE="GNU General Public License v3 (GPLv3)"

if __name__ == "__main__":
    # get README and use it as long description
    with open("README.md", "r") as fh:
        LONG_DESCRIPTION = fh.read()

    # get VERSION value from Github workflow and terminate workflow if value is None
    GITHUB_LABEL_VERSION = os.getenv("GITHUB_LABEL_VERSION")
    if not GITHUB_LABEL_VERSION:
        raise ValueError("Did not receive release label version info from GitHub")

    version_from_file = None

    # get version info from a version file
    # amend path to the version file if necessary
    try:
        with open("_version.py", "r") as fh:
            version_file_content = fh.read()
    except FileNotFoundError:
        raise ValueError("Did not find _version.py")

    matches = re.findall(VERSION_REGEX, version_file_content,re.IGNORECASE)
    if not matches:
        raise ValueError("Did not find version info in _version.py")
    try:
        version_from_file = matches[0]
    except IndexError:
        raise ValueError("Did not find version info in _version.py")

    if version_from_file != GITHUB_LABEL_VERSION:
        raise ValueError(f"Version info from _version.py '{version_from_file}' differs from GitHub label version '{GITHUB_LABEL_VERSION}'")

    # Amend with your project information
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        packages=find_packages(where=MY_SOURCE_DIR),
        include_package_data=True,
        classifiers=CLASSIFIERS,
        license=LICENSE,
        install_requires=INSTALL_REQUIRES,
        keywords=KEYWORDS,
    )

