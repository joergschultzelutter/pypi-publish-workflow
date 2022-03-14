#!/usr/bin/env/python

from setuptools import setup, find_packages
import os

if __name__ == "__main__":
    # get README gnd use as long description
    with open("README.md", "r") as fh:
        long_description = fh.read()

    # get VERSION value from Github workflow and terminate workflow if value is None
    VERSION = os.getenv("GITHUB_PROGRAM_VERSION")
    if not VERSION:
        raise ValueError("Did not receive version info from GitHub")

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
        packages=find_packages(),
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
