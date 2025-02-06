#!/bin/bash

#git clone https://github.com/pyenv/pyenv.git

version="3.10.16"
export PYENV_ROOT="$PWD/.pyenv"
#./pyenv/bin/pyenv install $version
export PATH=".pyenv/versions/$version/bin:$PATH"
echo "pyenv set up with python $version"

python3 -m venv venv
source venv/bin/activate

#pip3 install -r requirements.txt --quiet

python3 run_benchmark.py --max_iterations 25 --max_input_tokens 150000 --max_output_tokens 150000 --provider openai --model deepseek-r1-distill-qwen-14b --responses_to_keep 25 --observations_to_keep 25
