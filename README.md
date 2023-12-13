# PyTree

[![Build](https://github.com/BrianLusina/pytree/actions/workflows/build.yml/badge.svg)](https://github.com/BrianLusina/pytree/actions/workflows/build.yml)
[![Lint](https://github.com/BrianLusina/pytree/actions/workflows/lint.yml/badge.svg)](https://github.com/BrianLusina/pytree/actions/workflows/lint.yml)
[![Tests](https://github.com/BrianLusina/pytree/actions/workflows/tests.yaml/badge.svg)](https://github.com/BrianLusina/pytree/actions/workflows/tests.yaml)

This is a command line directory built in Python to view folders and files in specified directories and list them in a
tree fashion.

## Pre-requisites

1. Ensure that you have [Python version 3.12.0](https://www.python.org/) setup locally, you can set this up
   using [pyenv](https://github.com/pyenv/pyenv) if you have multiple versions of Python on your local development
   environment.
2. [Poetry](https://python-poetry.org/) is used for managing dependencies, ensure you have that setup locally.
3. [Virtualenv](https://virtualenv.pypa.io/) Not a hard requirement as poetry should setup a virtual environment for
   you, but can be used as well to setup a virtual environment.

## Setup

1. After cloning the project, install the dependencies required with:

   ```shell
   poetry install
   ```
   > When using poetry

   Or
   ```shell
   make install
   ```
   > When using [GNU Make](https://www.gnu.org/s/make/manual/make.html), this is a wrapper around the top commend

3. Install `pytree` in editable mode:
   ```shell
   cd pytree
   pip install -e .
   ```

## Execution

To execute `pytree`, go ahead and run the below command:

```shell
python pytree --help
```
