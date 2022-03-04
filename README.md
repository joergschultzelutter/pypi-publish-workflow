# pypi-publish-workflow

Creates a Github actions workflow for automatic publications to PyPi. Version data from a python file gets extracted and then used my the PyPi setup process.

## Installation instructions

### Setup Github Secrets

- Create a project-scoped secret in [PyPi Test](https://test.pypi.org/) and [PyPi Prod](https://www.pypi.org/)
- In your Github project, goto ``Settings`` - ``Secrets`` - ``Actions``
- Create two keys ``TEST_PYPI_API_TOKEN`` and ``PROD_PYPI_API_TOKEN`` and assign the secrets to these values

### Overview on config files

This repo contains three files that you may need to amend and copy to your Github repository:

- ``MANIFEST.in``: Copy this file 'as is' to your repo's root folder. It contains a reference to the future VERSION file.
- ``setup.py``: this is a regular Python setup.py file; amend the file content and then save the file in your repo's root directory
- ``publish-to-pypi.yml``: Edit this file, amend the configuration settings and then save the file in your repo's Github Actions directory (``.github/workflows``). You may also need to activate the new workflow (instructions are not part of this documentation)

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

## Test your work flow

The PyPi Prod deployment branch comes with a built-in safeguard which prevents accidental deployments to PyPi prod for cases where you want to do some testing. If you change the default for the Github Action trigger from

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

then every change to your repo will trigger the Github Action but should not lead to a publication to PyPi prod __unless you label the release__. When in doubt, you may also want to remove the ``PROD_PYPI_API_TOKEN``'s secret from your Github account.
