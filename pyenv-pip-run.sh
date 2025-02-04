#!/bin/bash

# Check that system utilities are installed
for utility in git python3 pip3 docker; do
    if ! [ -x "$(command -v $utility)" ]; then
        echo "Error: $utility is not installed." >&2
        exit 1
    fi
done 
echo "All required utilities available"

# Confirm that python version 9 or 10 is available
version=`python3 -c 'from sys import version_info; print(version_info[1])'`
if [ $version -gt 10 ] || [ $version -lt 9 ]; then

    if [ ! -d "./pyenv" ]; then
        echo "git cloning pyenv"
        git clone https://github.com/pyenv/pyenv.git
    fi
    echo "pyenv cloned"

    version="3.10.16"
    export PYENV_ROOT="$PWD/.pyenv"
    if [ ! -d "./.pyenv/versions/$version" ]; then
        ./pyenv/bin/pyenv install $version
    fi
    export PATH=".pyenv/versions/$version/bin:$PATH"
    echo "pyenv set up with python $version"
fi

# Set up venv and requirements
echo "Setting up virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "Installing pip requirements"
pip3 install -r requirements.txt --quiet

python3 run_benchmark.py --max_iterations 25 --max_input_tokens 150000 --max_output_tokens 150000 --provider openai --model deepseek-r1-distill-qwen-14b --responses_to_keep 25 --observations_to_keep 25
