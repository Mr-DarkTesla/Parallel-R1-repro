"""Replace machine-specific locations with documented portable placeholders.

This transforms string values and JSON object keys, preserving numeric metrics.
The archive contains historical recipes; substitute these placeholders before
using a recipe in a new environment.
"""
import hashlib
import re


def normalize(text):
    project = r"/home/[^/\s\"'<>`]+/shares/[^/\s\"'<>`]+/[^/\s\"'<>`]+/tmp/r1(?=/|[\s\"'<>`\\]|$)"
    local_project = r"/Users/[^/\s\"'<>`]+/projects/[^/\s\"'<>`]+/sirius-parallel-r1(?=/|[\s\"'<>`\\]|$)"
    text = re.sub(project, "${PROJECT_ROOT}", text)
    text = re.sub(local_project, "${PROJECT_ROOT}", text)
    text = re.sub(r"/home/[^/\s\"'<>`]+/shares/[^/\s\"'<>`\\]+", "${SHARED_ROOT}", text)
    for old, new in [
        ("/dev/shm/r1", "${MODEL_ROOT}"),
        ("/dev/shm", "${SHM_ROOT}"),
        ("/usr/local/cuda", "${CUDA_HOME}"),
        ("/usr/local/nvidia", "${NVIDIA_ROOT}"),
        ("/opt/conda", "${PYTHON_PREFIX}"),
    ]:
        text = text.replace(old, new)
    text = re.sub(r"/Users/[^/\s\"'<>`\\]+/Downloads", "${DATA_SOURCE_ROOT}", text)
    text = re.sub(r"/(?:Users|home)/[^/\s\"'<>`\\]+", "${USER_HOME}", text)
    text = re.sub(r"/root(?=/|[\s\"'<>`\\]|$)", "${USER_HOME}", text)
    text = re.sub(r"/tmp(?=/|[\s\"'<>`\\]|$)", "${TMPDIR}", text)
    # Stable opaque aliases preserve which records used the same allocation.
    text = re.sub(r"lm-mpi-job-([0-9a-f-]{36})", lambda m: "RUN_" + hashlib.sha256(m[1].encode()).hexdigest()[:10], text)
    text = re.sub(r"\.ai\d+-\d+", "", text)
    text = re.sub(r"https?://127\.0\.0\.1:\d+/[A-Za-z0-9_-]{20,}", "${LOCAL_ENDPOINT}", text)
    text = text.replace("ssh 8a100_jupyter", "ssh ${REMOTE_SSH_ALIAS}")
    return text
