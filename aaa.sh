#!/bin/bash


version="3.10.16"
export PYENV_ROOT="$PWD/.pyenv"
export PATH=".pyenv/versions/$version/bin:$PATH"
echo "pyenv set up with python $version"

python3 -m venv venv
source venv/bin/activate

python check_models.py http://172.31.4.136:8000/v1 asdf
