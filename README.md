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

- ``setup.py``: this is a regular Python ``setup.py`` file; amend the file content with your package information and then save the file in your repo's root directory
- ``publish-to-pypi.yml``: Edit this file, amend the configuration settings (see next chapter) and then save the file in your repo's Github Actions directory (``.github/workflows``). You may also need to activate the new workflow once you have installed it - see [documentation on Github](https://docs.github.com/en/actions).

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
  
  # Python version used for building the package
  PYTHON_VERSION: '3.8'
```

Replace the placeholder for the source file with the relative path to your Python file which contains the version information. Amend the RegEx and the Python version, if necessary.

## Running the Github Action

This Github action will do the following __whenever a new release is published__:

- Read the Python file and extract the version information, based on the given Regex. Abort job if no match was found.
- Check if the Github ``ref_type`` has the value ``tag``. This is only the case when you drafted a new release. Otherwise, this value is likely set to ``master``. Abort job in case of a mismatch.
- Check if the Github ``ref_name`` is equal to the extracted version from you Python file. Abort job in case of a mismatch.
- Build the PyPi package. Deploy it to PyPi Test and (if successful) PyPi Prod.

This job will be triggered for releases AND prereleases in 'created' state (read: you tag a (pre)release in Github). Releases will be pushed to both PyPi Test and Prod whereas prereleases will only be pushed to PyPi Test.

## Test your work flow

In case you want to become acquainted with this work flow: The safest way to test the work flow is to create both Github secret entries ``TEST_PYPI_API_TOKEN`` and ``PROD_PYPI_API_TOKEN`` but assign an invalid token to them. When you run the workflow for a new 'master' branch prerelease, the job will try to push it to PyPi Test and will fail because of the invalid token.
