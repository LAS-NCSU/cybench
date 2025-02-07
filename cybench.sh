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

#python check_models.py http://172.31.4.136:8000/v1 asdf
echo "Installing pip requirements"

model=deepseek-ai/DeepSeek-R1-Distill-Llama-70B
# max token length of 73376 total (input and output combined)

python3 run_benchmark.py --max_iterations 25 --max_input_tokens 35000 --max_output_tokens 38376 --provider openai --model $model --responses_to_keep 25 --observations_to_keep 25
