#!/usr/bin/env bash
# Offline install into /home/jovyan/venv. Usage: bash env/install_pod.sh <wheelhouse_dir>...
set -euxo pipefail

find_links=$(printf -- "--find-links %s " "$@")
env_dir=$(cd "$(dirname "$0")" && pwd)

python3.10 -m venv /home/jovyan/venv
source /home/jovyan/venv/bin/activate
pip install --no-index $find_links setuptools wheel
pip install --no-index $find_links --no-build-isolation -r "$env_dir/requirements.lock"
pip install --no-index $(find "$@" -maxdepth 1 -name "flash_attn-2.7.4.post1*.whl")
pip install --no-index --no-build-isolation --no-deps -e "$env_dir/../verl"
python -c "import torch, vllm, flash_attn, transformers; print(torch.__version__, vllm.__version__, flash_attn.__version__, transformers.__version__, torch.cuda.is_available())"
