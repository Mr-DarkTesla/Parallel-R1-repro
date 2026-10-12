"""Validate the delivered archive, including source hashes and reader-facing links."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def deliverables():
    return sorted(p for p in ROOT.rglob("*") if p.is_file()
                  and "__pycache__" not in p.parts and p.name != ".DS_Store")


def checksums():
    return "\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}"
                     for p in deliverables() if p.name != "SHA256SUMS") + "\n"


def verify():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    seen = set()
    for rec in manifest["artifacts"]:
        assert rec["artifact"] not in seen, f"Duplicate manifest path: {rec['artifact']}"
        seen.add(rec["artifact"])
        path = ROOT / rec["artifact"]
        assert path.exists(), f"Missing artifact: {path}"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == rec["sha256"], str(path)
    for path in (ROOT / "artifacts").rglob("*"):
        if path.is_file():
            assert str(path.relative_to(ROOT)) in seen, f"Unmanifested artifact: {path}"
    for path in deliverables():
        if path.suffix == ".json":
            json.loads(path.read_text())
        elif path.suffix == ".jsonl":
            for line in path.read_text().splitlines():
                if line.strip(): json.loads(line)
    for rec in json.loads((ROOT / "figures/manifest.json").read_text()):
        for source in rec["sources"]:
            path = ROOT / source["path"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"], str(path)
        for output in rec["outputs"]:
            assert (ROOT / output).stat().st_size > 1000, output
    pages = list(ROOT.glob("*.md")) + list((ROOT / "runs").glob("*.md"))
    missing = []
    for page in pages:
        for link in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", page.read_text()):
            target = link.split("#", 1)[0]
            if not target or "://" in target:
                continue
            if not (page.parent / target).exists():
                missing.append((str(page.relative_to(ROOT)), link))
    assert not missing, f"Broken reader links: {missing[:20]}"
    secret = re.compile(rb"(?:hf_[A-Za-z0-9]{25,}|gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9_-]{30,})")
    for path in deliverables():
        if path.suffix in {".json", ".jsonl", ".yaml", ".yml", ".sh", ".py", ".md", ".txt", ".csv"}:
            assert not secret.search(path.read_bytes()), f"Credential pattern in {path}"
            if path.name != "portable_paths.py":
                internal = re.compile(rb"/(?:home|Users|root)/[A-Za-z0-9_.-]+|lm-mpi-job-[0-9a-f-]{36}")
                assert not internal.search(path.read_bytes()), f"Machine-specific location in {path}"
    assert (ROOT / "SHA256SUMS").read_text() == checksums(), "SHA256SUMS is stale"
    print(f"Verified {len(seen)} source artifacts, {len(pages)} reader pages, "
          f"{len(manifest['runs'])} directories and all figure inputs/checksums.")


if __name__ == "__main__":
    import sys
    if "--update-checksums" in sys.argv:
        (ROOT / "SHA256SUMS").write_text(checksums())
    verify()
