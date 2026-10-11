#!/usr/bin/env python3
"""Safely reconcile owned checkpoint exports with GLOBAL_TOP5.json.

Dry-run is the default.  ``--apply`` removes only an unlisted model export's
direct parent when that parent contains exactly that model directory.  It never
removes ``/checkpoints``, an experiment root, or metadata/log files.
"""

import argparse
import json
import shutil
import tempfile
from pathlib import Path


CHECKPOINTS = Path("/checkpoints")
MANIFEST_RELATIVE = Path("exp21-global-top5/GLOBAL_TOP5.json")
REQUIRED_FILES = ("config.json", "tokenizer_config.json")


class ReconcileError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReconcileError(message)


def direct_weight_files(model):
    return [path for path in model.iterdir()
            if path.is_file() and path.stat().st_size > 0 and path.suffix in (".bin", ".safetensors")]


def resolved_inside(path, root):
    require(path.is_absolute() and ".." not in path.parts, f"path escapes checkpoint root: {path}")
    resolved = path.resolve(strict=True)
    require(root == resolved or root in resolved.parents, f"path escapes checkpoint root: {path}")
    return resolved


def assert_no_symlinks(path):
    """Visit every inode below path; a symlink makes inventory unsafe."""
    require(path.is_dir() and not path.is_symlink(), f"missing or unsafe directory: {path}")
    for child in path.iterdir():
        require(not child.is_symlink(), f"refusing symlink: {child}")
        if child.is_dir():
            assert_no_symlinks(child)


def model_signature(path):
    names = {child.name for child in path.iterdir() if child.is_file()}
    return ("config.json" in names or "tokenizer_config.json" in names or
            any(name.endswith((".bin", ".safetensors")) for name in names))


def validate_model(model, root):
    model = resolved_inside(model, root)
    require(model.is_dir() and not model.is_symlink(), f"missing model directory: {model}")
    assert_no_symlinks(model)
    for name in REQUIRED_FILES:
        file = model / name
        require(file.is_file() and not file.is_symlink(), f"missing {name}: {model}")
    require(direct_weight_files(model), f"missing non-empty direct weights: {model}")
    return model


def inventory_models(directory, root):
    """Find complete BF16 export directories and reject incomplete lookalikes."""
    require(directory.is_dir() and not directory.is_symlink(), f"missing or unsafe directory: {directory}")
    if model_signature(directory):
        validate_model(directory, root)
        return [directory]
    models = []
    for child in directory.iterdir():
        require(not child.is_symlink(), f"refusing symlink: {child}")
        if child.is_dir():
            models.extend(inventory_models(child, root))
    return models


def manifest_models(manifest, root):
    require(manifest.is_file() and not manifest.is_symlink(), f"missing manifest: {manifest}")
    try:
        data = json.loads(manifest.read_text())
    except json.JSONDecodeError as error:
        raise ReconcileError(f"invalid manifest JSON: {error}") from error
    entries = data.get("models")
    require(isinstance(entries, list) and len(entries) == 5, "manifest must list exactly five models")
    paths, ranks = [], []
    for index, entry in enumerate(entries):
        require(isinstance(entry, dict) and isinstance(entry.get("path"), str),
                f"manifest model {index}: missing path")
        paths.append(resolved_inside(Path(entry["path"]), root))
        ranks.append(entry.get("rank"))
    require(len(set(paths)) == 5, "manifest contains duplicate model paths")
    require(set(ranks) == {1, 2, 3, 4, 5}, "manifest ranks must be exactly 1..5")
    return [validate_model(path, root) for path in paths]


def export_parent(model, root):
    parent = model.parent
    require(parent != root and parent.parent != root,
            f"refusing model without a removable export parent: {model}")
    children = list(parent.iterdir())
    require(children == [model], f"unknown non-model content in export parent: {parent}")
    return parent


def build_plan(root, manifest):
    root = root.resolve(strict=True)
    require(root.is_dir() and not root.is_symlink(), f"unsafe checkpoint root: {root}")
    assert_no_symlinks(root)
    kept = manifest_models(manifest, root)
    all_models = inventory_models(root, root)
    require(len(set(all_models)) == len(all_models), "incomplete inventory: duplicate model paths")
    require(set(kept) <= set(all_models), "incomplete inventory: manifest model missing")
    remove_models = sorted(set(all_models) - set(kept))
    remove_pairs = [(model, export_parent(model, root)) for model in remove_models]
    remove_parents = [parent for _, parent in remove_pairs]
    require(len(set(remove_parents)) == len(remove_parents), "multiple models share an export parent")
    return {"root": root, "manifest": manifest.resolve(strict=True), "kept": sorted(kept),
            "all_models": sorted(all_models), "remove_models": remove_models,
            "remove_parents": sorted(remove_parents), "remove_pairs": remove_pairs}


def print_plan(plan, applied):
    payload = {
        "mode": "apply" if applied else "dry-run",
        "root": str(plan["root"]),
        "manifest": str(plan["manifest"]),
        "kept_model_dirs": [str(path) for path in plan["kept"]],
        "removed_model_dirs": [str(path) for path in plan["remove_models"]],
        "removed_export_parents": [str(path) for path in plan["remove_parents"]],
        "counts": {"kept_models": len(plan["kept"]), "all_models": len(plan["all_models"]),
                   "removed_models": len(plan["remove_models"]),
                   "removed_export_parents": len(plan["remove_parents"])}
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def apply_plan(plan):
    for model, parent in plan["remove_pairs"]:
        validate_model(model, plan["root"])
        require(export_parent(model, plan["root"]) == parent, f"export parent changed: {model}")
        shutil.rmtree(parent)


def write_model(path):
    path.mkdir(parents=True)
    for name in REQUIRED_FILES:
        (path / name).write_text("{}\n")
    (path / "model.safetensors").write_bytes(b"fixture")


def self_test():
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "checkpoints"
        root.mkdir()
        kept = []
        for index in range(5):
            model = root / f"experiment-{index}" / "step_8" / "model"
            write_model(model)
            kept.append(model)
        extra = root / "experiment-extra" / "step_8" / "model"
        write_model(extra)
        manifest = root / MANIFEST_RELATIVE
        manifest.parent.mkdir()
        manifest.write_text(json.dumps({"models": [
            {"rank": index + 1, "path": str(path)} for index, path in enumerate(kept)]}))
        plan = build_plan(root, manifest)
        require(plan["kept"] == [path.resolve() for path in kept]
                and plan["remove_models"] == [extra.resolve()], "fixture plan mismatch")
        (extra.parent / "run.log").write_text("must block deletion\n")
        try:
            build_plan(root, manifest)
        except ReconcileError as error:
            require("unknown non-model content" in str(error), "fixture unknown-content rejection drift")
        else:
            raise ReconcileError("fixture accepted export parent with metadata")
    print("self-test passed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=CHECKPOINTS)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--apply", action="store_true", help="remove validated, unlisted export parents")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    root = args.root.resolve(strict=True)
    require(root == CHECKPOINTS, f"refusing non-PVC root: {root}")
    manifest = args.manifest or root / MANIFEST_RELATIVE
    plan = build_plan(root, manifest)
    if args.apply:
        apply_plan(plan)
    print_plan(plan, args.apply)


if __name__ == "__main__":
    try:
        main()
    except (ReconcileError, FileNotFoundError, PermissionError) as error:
        raise SystemExit(f"ERROR: {error}") from error
