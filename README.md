# pypi-publish-workflow

This is a __Github Actions__ workflow for automatic publications to PyPi. Version data from a python file is extracted and then used by the PyPi setup process which will publish the package to PyPi Test and Prod. 

The workflow will only be triggered for the publication of new repo releases.

## Installation instructions

### Setup Github Secrets

- Create token secrets for both [PyPi Test](https://test.pypi.org/) and [PyPi Prod](https://www.pypi.org/) (``Account Settings`` > ``API Tokens`` > ``Add API token``). 
- In your Github project, goto ``Settings`` > ``Secrets`` > ``Actions``
- Create two keys ``TEST_PYPI_API_TOKEN`` and ``PROD_PYPI_API_TOKEN`` and assign the previously created token secrets to these keys

### Overview on config files

This repo contains three files that you may need to amend and copy to your Github repository:

- ``MANIFEST.in``: Copy this file 'as is' to your repo's root folder. It contains a reference to the future ``VERSION`` file which will be created by the Github Action.
- ``setup.py``: this is a regular Python ``setup.py`` file; amend the file content with your package information and then save the file in your repo's root directory
- ``publish-to-pypi.yml``: Edit this file, amend the configuration settings (see next chapter) and then save the file in your repo's Github Actions directory (``.github/workflows``). You may also need to activate the new workflow - see [documentation on Github](https://docs.github.com/en/actions).

### Configuring publish-to-pypi.yml

Open the file. You will notice a section which looks like this:

```yml
env:

  # relative path to your file, e.g.
  # ./src/MyLib/MyLib.py
  SOURCE_FILE:  ./REPLACE/ME

  # Regex pattern used for extracting the version data from your fil
  # (usually, this does not need to be changed)
  REGEX_PATTERN:  __version__\s*=\s*"(.*)"
```

Replace the placeholder for the source file with the relative path to your Python file which contains the version information. Amend the RegEx, if necessary.

## Running the Github Action

This Github action will do the following __whenever a new release is published__:

- Read the Python file and extract the version information
- In case of an error, abort the whole process
- In case of success, write a file called ``VERSION`` to your repo's root directory, build the package and then publish the content to PyPi Test
- If successful, publish to PyPi Prod.

## Test your work flow

The PyPi Prod deployment branch comes with a built-in safeguard which prevents accidental deployments to PyPi Prod for cases where you want to do some testing. If you change the default for the Github Action trigger from

```yml
on:
  release:
    types: [published]
```

to

```yml
on:
  push:
```

then every change to your Github repo will trigger the Github Action but should not lead to a publication to PyPi Prod __unless you label the release__. When in doubt, you may also want to remove the ``PROD_PYPI_API_TOKEN``'s secret from your Github account to ensure that this workflow cannot write to PyPi Prod.
