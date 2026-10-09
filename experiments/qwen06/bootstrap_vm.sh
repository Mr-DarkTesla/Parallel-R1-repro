#!/usr/bin/env bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
ROOT=${PARALLEL_R1_ROOT:-$HOME/parallel-r1}
BRANCH=${PARALLEL_R1_BRANCH:-qwen3-0.6b-rl}
# Ubuntu 22.04 VM with passwordless sudo (GCP), or a root container without sudo (vast.ai).
as_root() { if [ "$(id -u)" -eq 0 ]; then "$@"; else sudo -n "$@"; fi; }
apt_install() { as_root env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "$@"; }
TOOLS=()
for tool in git gcc tmux python3; do command -v "$tool" >/dev/null || TOOLS+=("$tool"); done
if [ ! -f /usr/include/python3.10/Python.h ] || [ ${#TOOLS[@]} -gt 0 ]; then
  as_root apt-get update -qq
  [ ${#TOOLS[@]} -eq 0 ] || apt_install "${TOOLS[@]}"
  # Not every image has Python 3.10 in apt; the venv then uses uv's own CPython 3.10, which has the headers.
  [ -f /usr/include/python3.10/Python.h ] || apt_install python3.10-dev || echo 'No python3.10-dev from apt'
fi
if ! command -v uv >/dev/null; then
  python3 - <<'PY'
import json, urllib.request, zipfile, io, pathlib
meta = json.load(urllib.request.urlopen('https://pypi.org/pypi/uv/0.8.22/json', timeout=30))
url = next(x['url'] for x in meta['urls'] if 'manylinux_2_17_x86_64' in x['filename'])
archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url, timeout=60).read()))
target = pathlib.Path.home() / '.local/bin/uv'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes(archive.read(next(n for n in archive.namelist() if n.endswith('/uv'))))
target.chmod(0o755)
PY
fi
mkdir -p "$ROOT"
cd "$ROOT"
if [ ! -d repo/.git ]; then
  git clone --branch "$BRANCH" https://github.com/Mr-DarkTesla/Parallel-R1-repro.git repo
fi
if [ ! -x .venv/bin/python ]; then
  if [ -x /usr/bin/python3.10 ] && [ -f /usr/include/python3.10/Python.h ]; then uv venv --python /usr/bin/python3.10 .venv
  else uv venv --python 3.10 --python-preference only-managed .venv; fi
fi
export UV_HTTP_TIMEOUT=120
uv pip install --python .venv/bin/python 'vllm==0.8.5.post1' 'torch==2.6.0' 'torchvision==0.21.0' 'torchaudio==2.6.0' 'tensordict==0.6.2' 'torchdata==0.11.0' 'transformers==4.51.3' 'numpy==1.26.4' 'ray[default]==2.43.0' 'datasets==3.6.0' 'peft==0.15.2' 'accelerate==1.6.0' 'huggingface-hub==0.30.2' codetiming hydra-core pandas pyarrow pylatexenc wandb dill pybind11 liger-kernel mathruler pytest pytest-asyncio matplotlib latex2sympy2_extended math-verify packaging ninja setuptools wheel
uv pip install --python .venv/bin/python 'https://github.com/Dao-AILab/flash-attention/releases/download/v2.7.4.post1/flash_attn-2.7.4.post1+cu12torch2.6cxx11abiFALSE-cp310-cp310-linux_x86_64.whl'
uv pip install --python .venv/bin/python --no-deps -e repo/verl
.venv/bin/python -c 'import torch, vllm, transformers, flash_attn, ray, tensordict; print(torch.__version__, vllm.__version__, transformers.__version__); print(torch.cuda.get_device_name()); print(torch.ones(8, device="cuda").sum().item())'
uv pip freeze --python .venv/bin/python > environment.freeze.txt
echo BOOTSTRAP_DONE
