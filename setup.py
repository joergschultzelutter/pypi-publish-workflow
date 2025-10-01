#!/usr/bin/env/python

from setuptools import setup, find_packages
import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

# source path for the class' package. Amend if necessary
PACKAGE_SOURCE_DIR = "path/to/class/directory"

# Amend this section with your custom data
PACKAGE_NAME = "package-name"
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
INSTALL_REQUIRES = ["package_1", "package_2"]
KEYWORDS = [
    "Notifications",
    "Notification Service",
    "Push Notifications",
    "Notifier",
    "Alerts",
    "Robot Framework",
]
LICENSE = "GNU General Public License v3 (GPLv3)"


def running_in_a_github_action():
    return os.getenv("GITHUB_ACTIONS") == "true"


# Absolute URL to base repo; change this setting!
BASE_URL = "https://github.com/joergschultzelutter/MY_REPO_NAME/blob/master/"

# Markdown link recognition (will not work on image links)
LINK_RE = re.compile(r"(?<!\!)\[(?P<text>[^\]]+)\]\((?P<href>[^)\s]+)\)")


def is_absolute_url(href: str) -> bool:
    return href.startswith(("http://", "https://", "mailto:"))


def is_root_relative(href: str) -> bool:
    return href.startswith("/")


def looks_like_md(href: str) -> bool:
    path = urlsplit(href).path
    return path.lower().endswith(".md")


def to_absolute_md(href: str) -> str:
    parts = urlsplit(href)  # (scheme, netloc, path, query, fragment)
    abs_url = urljoin(BASE_URL, parts.path)
    return urlunsplit(
        urlsplit(abs_url)._replace(query=parts.query, fragment=parts.fragment)
    )


def rewrite_md_links(md_text: str) -> str:
    def repl(m: re.Match) -> str:
        text = m.group("text")
        href = m.group("href")

        if (
            not is_absolute_url(href)
            and not is_root_relative(href)
            and looks_like_md(href)
        ):
            href = to_absolute_md(href)

        return f"[{text}]({href})"

    return LINK_RE.sub(repl, md_text)


def transform_file(filename: str) -> str:
    in_path = Path(filename)
    if not in_path.exists():
        raise FileNotFoundError(filename)

    content = in_path.read_text(encoding="utf-8")
    transformed = rewrite_md_links(content)
    return transformed


if __name__ == "__main__":

    LONG_DESCRIPTION = transform_file("README.md")

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
        if len(GITHUB_PROGRAM_VERSION) == 0:
            raise ValueError(
                "Manual run requires a manually set GITHUB_PROGRAM_VERSION; change setup.py accordingly"
            )

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
