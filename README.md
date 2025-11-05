# pypi-publish-workflow

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![CodeQL](https://github.com/joergschultzelutter/pypi-publish-workflow/actions/workflows/codeql.yml/badge.svg)](https://github.com/joergschultzelutter/pypi-publish-workflow/actions/workflows/codeql.yml)

This is a __Github Actions__ workflow for automatic publications to PyPi. Version data from a python file is extracted and then used by the PyPi setup process which will publish the package to PyPi Test and Prod, following PyPi's [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) model. 

The workflow will only be triggered for the publication of new repo releases / prereleases for the 'master' repo branch.

## Overview on config files

This repo contains three files that you may need to amend and copy to your Github repository:

- ``setup.py``: this is a regular Python ``setup.py`` file; amend the file content with your package information and then save the file in your repo's root directory
- ``publish-to-pypi.yml``: Edit this file, amend the configuration settings (see next chapter) and then save the file in your repo's Github Actions directory (``.github/workflows``). You may also need to activate the new workflow once you have installed it - see [documentation on Github](https://docs.github.com/en/actions).

## Configuration file instructions

### `publish-to-pypi.yml`

Open the file. You will notice a section which looks like this:

```yml
env:

  # relative path to the file containing your version info, e.g.
  # ./MyLib/MyLib.py
  SOURCE_FILE: ./REPLACE/ME

  # Regex pattern used for extracting the version data from your file
  # (usually, this does not need to be changed)
  REGEX_PATTERN:  __version__\s*=\s*"(.*)"
  
  # Python version used for building the package
  PYTHON_VERSION: '3.11'
```

Replace the placeholder for the source file with the relative path to your Python file _which contains the version information_. Amend the RegEx and the Python version, if necessary.

### `setup.py` configuration

Open the file. You will need to pupulate the header fields:

```python
# source path for the class' package. Amend if necessary
PACKAGE_SOURCE_DIR = "path/to/class/directory"

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
```

- `PACKAGE_SOURCE_DIR` - the path to your package source directory, containing your Python code
- `PACKAGE_NAME` - (future) PyPi package name
- `DESCRIPTION` - PyPi package short dkescription
- `AUTHOR` and `AUTHOR_EMAIL` - self-explanatory
- `URL` - URL to your package`s repository on GitHub
- `CLASSIFIERS` - List of classifiers; have a look at [the official list](https://pypi.org/classifiers/)
- `INSTALL_REQUIRES` - Python packages that are required by your package
- `KEYWORDS` - Keywords which are associated with your Python package

> [!INFO]
> When being run as part of the provided GitHub workflow, `setup.py` will receive the future Python package's version info from the GitHub workflow and store it in the `GITHUB_PROGRAM_VERSION` variable. If you intend to install the package directly via `pip install`, you need to set the version info directly in the setup file or the process will fail.

Necessary steps for a manual usage:

- open `setup.py` and assign a version number to the `GITHUB_PROGRAM_VERSION` variable
- `pip install git+https://github.com/my-repository-name@my-branch#egg=my-package-name`

## Installation instructions

The workflow uses PyPi's [Trusted Publisher](https://docs.pypi.org/trusted-publishers/) model. For a new project on PyPi, follow [these instructions](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/) for setting up a trusted publisher. For an existing project which you may want to migrate from a secret-based workflow to the new trusted workflows, use [these instructions](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).

### Step 1: set up a Github environment

- In your GitHub project, go to **Settings > Environments** and create a new environment called `pypi`.
- Configure `Required reviewers` or other settings, if necessary. You do NOT need to configure any secrets here.

### Step 2: Deploy the workflow and the setup file

- You need to configure the files prior to deployment, see previous chapter **Configuration file instructions**
- `setup.py` goes into your repository's root directory
- `publish-to-pypi.yml` goes into your repository's `.github/workflows` directory (or add as a new GitHub action)

### Step 3: Trusted Publisher Setup

- Log on to your PyPi Test & Prod accounts
- Follow the instructions on how to set up a [Trusted Publisher](https://docs.pypi.org/trusted-publishers/) on both Test and Prod environments:
  - Set the `Workflow Name` to `publish-to-pypi.yml`
  - Set the `Environment` to `pypi`

## Running the Github Action

This Github action will do the following __whenever a new release/pre-release is published for the 'master' branch__:

- Read the Python file and extract the version information, based on the given Regex. Abort job if no match was found.
- Check if the Github ``ref_type`` has the value ``tag``. This is only the case when you drafted a new release. Otherwise, this value is likely set to ``master``. Abort job in case of a mismatch.
- Check if the Github ``ref_name`` is equal to the extracted version from you Python file. Abort job in case of a mismatch. This will prevent issues where there is a mismatch between your Github release version (tag) and the one in the Python file.
- Build the PyPi package. Deploy it to PyPi Test and (if successful AND not a pre-release) PyPi Prod. Note: This is done as a separate workflow step, see [this issue](https://github.com/pypa/gh-action-pypi-publish/issues/319) for technical details.

This job will be triggered for releases AND prereleases in 'created' state (read: you tag a (pre)release in Github). Releases will be pushed to both PyPi Test and Prod whereas prereleases will only be pushed to PyPi Test.

## Test your work flow

- Publish your package as a prerelease. This should deploy your code only to PyPi Test.

## Workflow
A basic workflow diagram of this Github Action can be found [here](docs/workflow.jpg)

