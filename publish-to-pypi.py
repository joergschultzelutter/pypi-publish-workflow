# Workflow: Extract version from Python file, write VERSION file, generate PyPi package and
#           upload content to PyPi Test / Prod
#           Will only be executed when a new release is being published
# Author  : Joerg Schultze-Lutter
#
##
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
#
# Generic PyPi workflow documentation: https://github.com/marketplace/actions/pypi-publish
#
# Github Action consists of 2 jobs:
#
# Job 1 will read the Python file which contains the version data, extract it and
# write a VERSION file to the repo's root folder. For other 
#
# Job 2 will build and distribute the PyPi package to PyPi Test and (if Test deployment
# was successful) also to Prod
#
# External dependencies: 
# - MANIFEST.im and setup.py from repo root folder
# - PROD_PYPI_API_TOKEN and TEST_PYPI_API_TOKEN as Github Secrets (Settings > Secrets > Actions)
#
# Configuration settings: 
# - SOURCE_FILE environment variable: path.to.your.Python.file
# - REGEX_PATTERN: change this if your version info in the Python file uses
#                  a different pattern. Default behavior assumes that
#                  the version information in your file looks something like this:
#                  __version__ = "1.2.3"

name: Upload Python Package 

on:
#  release:
#    types: [published]
  push:

# 
# Configuration section - change values if necessary
#
env:

  # relative path to your file, e.g.
  # ./src/MyLib/MyLib.py
  SOURCE_FILE:  ./REPLACE/ME

  # Regex pattern used for extracting the version data from your fil
  # (usually, this does not need to be changed)
  REGEX_PATTERN:  __version__\s*=\s*"(.*)"

#
# Job section
#
jobs:
  # 
  # BEGIN of Job 1
  #
  # Get version from Python file and write it to a file named 
  # VERSION wrhich resides in the repo's root dir
  update-version:
    runs-on: ubuntu-latest

    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v2

      # Read source file
      - name: Read source file
        id: reader
        uses: juliangruber/read-file-action@v1
        with:
          path: ${{ env.SOURCE_FILE }}
      # Run regex on content and try to get the version data
      - name: get version via regex
        id: regex
        uses: actions-ecosystem/action-regex-match@v2
        with:
          regex: ${{ env.REGEX_PATTERN }}
          flags: 'gim'
          text: '${{ steps.reader.outputs.content }}'
      # Cancel current build if we did not get a match. Note:
      # Cancellation will have no immediate effect!!!
      - name: Cancel build if version not found
        if: ${{ steps.regex.outputs.match == '' }}
        uses: andymckay/cancel-action@0.2
      # Execute sleep if cancellation was triggered
      - name: Sleep if build was cancelled
        if: ${{ steps.regex.outputs.match == '' }}
        run: sleep 30s
        shell: bash
      # Write version to 'VERSION' file
      # As an additional safeguard, the Write command will fail
      # in case the Regex lookup was unsuccessful and the 
      # 'cancel build' command didn't kill off our job in time
      # so don't use an 'if' statement here!
      #
      # 'path' needs to be set relative to repo root
      - name: Write local VERSION file to work repo
        uses: DamianReeves/write-file-action@master
        with:
          path: './VERSION'
          contents: "${{ steps.regex.outputs.group1 }}"
          write-mode: overwrite
      # Push 'VERSION' file to repo.
      #
      # 'file-path' does not seem to support absolute or
      # relative paths, thus making the 'VERSION' file appear 
      # in the repo's root
      - name: Update VERSION file in Repo
        uses: test-room-7/action-update-file@v1
        with:
          file-path: 'VERSION'
          commit-msg: Auto-update of VERSION file
          github-token: ${{ secrets.GITHUB_TOKEN }}

  #
  # END of Job 1
  # 
  # If you have reached this point in time, then the 'VERSION' file was
  # successfully created/updated in the repo's root directory
  #

  # 
  # BEGIN of Job 2
  #
  # This section will create the PyPi package and first deploy it to PyPi test.
  # If successful, it will also try to issue a PyPi Prod deployment afterwards
  #
  deploy-to-pypi:
    runs-on: ubuntu-latest
    needs: update-version

    steps:
    - uses: actions/checkout@v2
    # Set up Python environment
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    # Install all dependencies
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build
    # Build the package
    - name: Build package
      run: python -m build
    # Publish everything to Test PyPi
    - name: Publish package to Test PyPi
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        user: __token__
        password: ${{ secrets.TEST_PYPI_API_TOKEN }}
        repository_url: https://test.pypi.org/legacy/
    # Publish everything to Prod PyPi
    # If you use job action 'on -> release -> types[published]' at the 
    # beginning of this file, then the 'if' statement is not really 
    # necessary. I'll keep this one as safeguard for testing in 
    # case this Github action  is triggered via 'on -> push'
    - name: Publish package to Prod PyPi
      if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags')
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        user: __token__
        password: ${{ secrets.PROD_PYPI_API_TOKEN }}
  #
  # END of Job 2
  #