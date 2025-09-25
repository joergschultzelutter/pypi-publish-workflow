#!/usr/bin/env/python

from setuptools import setup, find_packages
import os
import re

VERSION_REGEX = r'__version__\s*=\s*"(.*)"'
MY_SOURCE_DIR = "src"

if __name__ == "__main__":
    # get README gnd use as long description
    with open("README.md", "r") as fh:
        long_description = fh.read()

    # get VERSION value from Github workflow and terminate workflow if value is None
    GITHUB_LABEL_VERSION = os.getenv("GITHUB_LABEL_VERSION")
    if not GITHUB_LABEL_VERSION:
        raise ValueError("Did not receive release label version info from GitHub")

    version_from_file = None

    # get version info from version file
    with open("_version.py", "r") as fh:
        version_file_content = fh.read()
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
        name="my package name",
        version=VERSION,
        description="my description",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="My Name",
        author_email="My email addresse",
        url="URL to my repo",
        packages=find_packages(where=MY_SOURCE_DIR),
        include_package_data=True,
        classifiers=[
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            "Development Status :: 4 - Beta",
            "Framework :: Robot Framework",
        ],
        license="GNU General Public License v3 (GPLv3)",
        install_requires=["my_packet_1", "my_packet_2"],
        keywords=["My Keyword 1", "My Keyword 2"],
    )

