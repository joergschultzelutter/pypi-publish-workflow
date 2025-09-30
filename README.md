# pypi-publish-workflow

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![CodeQL](https://github.com/joergschultzelutter/pypi-publish-workflow/actions/workflows/codeql.yml/badge.svg)](https://github.com/joergschultzelutter/pypi-publish-workflow/actions/workflows/codeql.yml)

This is a __Github Actions__ workflow for automatic publications to PyPi. Version data from a python file is extracted and then used by the PyPi setup process which will publish the package to PyPi Test and Prod. 

The workflow will only be triggered for the publication of new repo releases / prereleases for the 'master' repo branch.

## Installation instructions

### Setup Github Secrets

- Create token secrets for both [PyPi Test](https://test.pypi.org/) and [PyPi Prod](https://www.pypi.org/) (``Account Settings`` > ``API Tokens`` > ``Add API token``). 
- In your Github project, goto ``Settings`` > ``Secrets and Variables`` > ``Actions``
- Create two `Secrets` keys (`New repository secret`) named ``TEST_PYPI_API_TOKEN`` and ``PROD_PYPI_API_TOKEN`` and assign the previously created token secrets to these keys

### Overview on config files

This repo contains three files that you may need to amend and copy to your Github repository:

- ``setup.py``: this is a regular Python ``setup.py`` file; amend the file content with your package information and then save the file in your repo's root directory
- ``publish-to-pypi.yml``: Edit this file, amend the configuration settings (see next chapter) and then save the file in your repo's Github Actions directory (``.github/workflows``). You may also need to activate the new workflow once you have installed it - see [documentation on Github](https://docs.github.com/en/actions).

### `publish-to-pypi.yml` configuration

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

## Running the Github Action

This Github action will do the following __whenever a new release/pre-release is published for the 'master' branch__:

- Read the Python file and extract the version information, based on the given Regex. Abort job if no match was found.
- Check if the Github ``ref_type`` has the value ``tag``. This is only the case when you drafted a new release. Otherwise, this value is likely set to ``master``. Abort job in case of a mismatch.
- Check if the Github ``ref_name`` is equal to the extracted version from you Python file. Abort job in case of a mismatch. This will prevent issues where there is a mismatch between your Github release version (tag) and the one in the Python file.
- Build the PyPi package. Deploy it to PyPi Test and (if successful AND not a pre-release) PyPi Prod.

This job will be triggered for releases AND prereleases in 'created' state (read: you tag a (pre)release in Github). Releases will be pushed to both PyPi Test and Prod whereas prereleases will only be pushed to PyPi Test.

## Test your work flow

In case you want to become acquainted with this work flow: The safest way to test the work flow is to create both Github secret entries ``TEST_PYPI_API_TOKEN`` and ``PROD_PYPI_API_TOKEN`` but assign an invalid token to them. When you run the workflow for a new 'master' branch prerelease, the job will try to push it to PyPi Test and will fail because of the invalid token.

## Workflow
A basic workflow diagram of this Github Action can be found [here](docs/workflow.jpg)

