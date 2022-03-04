# pypi-publish-workflow

Creates a Github actions workflow for automatic publications to PyPi. Version data from a python file gets extracted and then used my the PyPi setup process.

## Installation instructions

### Setup Github Secrets

- Create a secret in PyPi Test and PyPi Prod
- In your Github project, goto ``Settings`` - ``Secrets`` - ``Actions``
- Create two keys ``TEST_PYPI_API_TOKEN`` and ``PROD_PYPI_API_TOKEN`` and assign the secrets to these values

### Config files overview

This repo contains three files:

- ``MANIFEST.in``: Copy this file 'as is' to your repo's root folder
- ``setup.py``: regular Python setup.py file; amend the file content and then save the file in your repo's root directory
- ``publish-to-pypi.yml``: Edit this file, amend the configuration settings and then save the file in your repo's Github Actions directory (``.github/workflows``)

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

Replace the placeholder for the source file and amend the regex, if necessary

## Running the Github Action

This Github action will do the following __whenever a new release is published__:

- Read the Python file and extract the version information
- In case of an error, abort the whole process
- In case of success, write a file called VERSION to your repo's root directory, build the package and then publish the content to PyPi Test
- If successful, publish to PyPi Prod.
