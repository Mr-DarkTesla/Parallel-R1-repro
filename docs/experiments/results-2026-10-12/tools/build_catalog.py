"""Build the portable catalogue from frozen capture tarballs (no network or jobs).

Usage: python build_catalog.py OUTPUT CAPTURE.tar.gz [CAPTURE.tar.gz ...]
Uses Python stdlib. Regenerate plots separately with plot_overview.py.
"""
import csv
import hashlib
import io
import json
import re
import sys
import tarfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from portable_paths import normalize


def relevant(path):
    parts = Path(path).parts
    if path.endswith("night_final_answer.py"):
        return True
    if any(p in {"verl", "exports", "hf", "raw", "tokenizer"} for p in parts):
        return False
    if any(re.fullmatch(r"(?:checkpoint-\d+|global_step_\d+)", p) for p in parts):
        return False
    return not path.endswith(("tokenizer_config.json", "generation_config.json"))


def compact(value):
    """Human report view: preserve configuration, omit large hash inventories."""
    if isinstance(value, dict):
        return {k: compact(v) for k, v in value.items()
                if k not in {"code_sha256", "script_sha256", "changed_file_sha256",
                             "sealed_inputs", "hf_files", "examples", "pids",
                             "owned_alive", "controller_pid", "pid", "source_inventory"}}
    if isinstance(value, list):
        if len(value) > 40:
            return f"{len(value)} records; see original artifact"
        return [compact(x) for x in value]
    return value


def scalar_rows(value, prefix=""):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"rows", "training", "training_series", "per_task", "tasks", "by_id", "by_question", "ranks", "traces", "sha256", "hashes"}:
                continue
            yield from scalar_rows(item, f"{prefix}.{key}" if prefix else str(key))
    elif isinstance(value, list):
        if len(value) <= 40:
            for i, item in enumerate(value):
                yield from scalar_rows(item, f"{prefix}[{i}]")
    elif isinstance(value, (int, float, bool)) or value is None:
        yield prefix, value


def run_name(source):
    parts = Path(source).parts
    return "/".join(parts[:2] if parts[0] == "exps" else parts[:3])


def main():
    output = Path(sys.argv[1])
    output.mkdir(parents=True, exist_ok=True)
    chosen = {}
    inventory = {}
    conflicts = []
    captures = []
    for filename in sys.argv[2:]:
        with tarfile.open(filename) as archive:
            manifest = json.load(archive.extractfile("capture-manifest.json"))
            captures.append({k: manifest[k] for k in ["captured_at", "origin", "scope"]})
            if any(relevant(r["source"]) for r in manifest["rejected"]):
                raise ValueError("Capture rejected sensitive files; review before publishing")
            for run in manifest["runs"]:
                inventory.setdefault(run["run"], {"run": run["run"], "origins": []})["origins"].append(manifest["origin"])
            for record in manifest["artifacts"]:
                path = record["artifact"]
                if not relevant(path):
                    continue
                blob = archive.extractfile(path).read()
                assert hashlib.sha256(blob).hexdigest() == record["sha256"]
                old = chosen.get(path)
                if old and old[1] != blob:
                    # Keep both dated observations. Remote capture wins the primary path.
                    previous = old if record["origin"] != "local_saved" else (record, blob)
                    history = "history/" + previous[0]["origin"] + "/" + previous[0]["sha256"][:12] + "/" + path
                    conflicts.append((history, previous[0], previous[1]))
                if not old or record["origin"] != "local_saved":
                    chosen[path] = (record, blob)

    artifacts = []
    for path, (record, blob) in chosen.items():
        target = output / "artifacts" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        # Raw generated examples are not needed to reproduce aggregate metrics.
        transformation = None
        if path.endswith("reward-analysis.json"):
            value = json.loads(blob)
            if "examples" in value:
                del value["examples"]
                blob = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
                transformation = "Removed generated text examples; all numeric metrics retained"
        try:
            portable = normalize(blob.decode()).encode()
        except UnicodeDecodeError:
            portable = blob
        if portable != blob:
            transformation = "; ".join(filter(None, [transformation, "Machine-specific paths replaced with portable aliases"]))
            blob = portable
        target.write_bytes(blob)
        artifacts.append(dict(record, artifact="artifacts/" + path,
                              source_sha256=record["sha256"],
                              sha256=hashlib.sha256(blob).hexdigest(),
                              bytes=len(blob), transformation=transformation))
    seen = set()
    for path, record, blob in conflicts:
        digest = hashlib.sha256(blob).hexdigest()
        if (path, digest) in seen:
            continue
        seen.add((path, digest))
        # Local snapshots are useful when the local report schema differs.
        # Source recipes/configs superseded by identical or newer remote files
        # need not add duplicate historical source trees.
        if record["kind"] in {"configuration", "recipe_source"}:
            continue
        try:
            portable = normalize(blob.decode()).encode()
        except UnicodeDecodeError:
            portable = blob
        transformed = portable != blob
        blob = portable
        digest = hashlib.sha256(blob).hexdigest()
        target = output / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
        artifacts.append(dict(record, artifact=path, source_sha256=record["sha256"],
                              sha256=digest, bytes=len(blob), transformation="Machine-specific paths replaced with portable aliases" if transformed else None))

    grouped = defaultdict(list)
    for record in artifacts:
        grouped[run_name(record["source"])].append(record)
    pages = output / "runs"
    pages.mkdir(exist_ok=True)
    index = ["# Каталог всех найденных каталогов экспериментов\n",
             "Снимки исходных конфигураций, метрик, числовой телеметрии и графиков. "
             "Каталог включает диагностику, подготовку данных и неуспешные попытки. "
             "Наличие каталога или конфигурации не означает завершённое обучение.\n",
             "| Каталог | Конфигурации | Метрики / отчёты | Графики | Карточка |",
             "|---|---:|---:|---:|---|"]
    numeric = []
    for name in sorted(inventory):
        records = sorted(grouped[name], key=lambda x: x["artifact"])
        slug = name.replace("/", "--")
        config = [r for r in records if r["kind"] == "configuration"]
        figures = [r for r in records if r["kind"] == "figure"]
        metrics = [r for r in records if r["kind"] in {"metrics", "numeric_log_extract"}]
        recipes = [r for r in records if r["kind"] == "recipe_source"]
        index.append(f"| `{name}` | {len(config)} | {len(metrics)} | {len(figures)} | [Открыть](runs/{slug}.md) |")
        page = [f"# {name}\n",
                "Ниже — сохранённые наблюдения и настройки конкретного каталога. "
                "Значения в plan/manifest могут быть плановыми; исполнение подтверждают "
                "метрики, число завершённых задач и terminal status соответствующей попытки. "
                "Неподтверждённые параметры нельзя переносить из соседнего запуска.\n"]
        if not records:
            page.append("В проверенных местах не найдено сохраняемых конфигураций или метрик. "
                        "Это не доказательство отсутствия запусков в иных местах.\n")
        for title, items in [("Полная конфигурация и данные", config),
                             ("Метрики и полнота результатов", metrics),
                             ("Графики", figures), ("Исходники рецепта и награды", recipes)]:
            if not items:
                continue
            page.append(f"## {title}\n")
            for record in items:
                relative = record["artifact"]
                page.append(f"- [{record['source']}](../{relative}) "
                            f"— {record['origin']}, снимок {record['captured_at']}.\n")
                source = output / relative
                if source.suffix in {".json", ".yaml", ".yml"} and title in {"Полная конфигурация и данные", "Метрики и полнота результатов"}:
                    try:
                        value = json.loads(source.read_text()) if source.suffix == ".json" else None
                    except ValueError:
                        value = None
                    if value is not None:
                        if title == "Метрики и полнота результатов" and source.stat().st_size < 150000 and "telemetry" not in relative:
                            numeric.extend((name, relative, key, val) for key, val in scalar_rows(value))
                        view = json.dumps(compact(value), indent=2, ensure_ascii=False)
                    else:
                        view = source.read_text()
                    if len(view) <= 28000 and "telemetry" not in relative and "charts/metrics" not in relative:
                        page.extend(["<details>\n", "<summary>Числа и параметры</summary>\n",
                                     "```" + ("json" if value is not None else "yaml"), view, "```\n", "</details>\n"])
        (pages / f"{slug}.md").write_text("\n".join(page), encoding="utf-8")
        inventory[name].update(configurations=len(config), metrics=len(metrics), figures=len(figures),
                               artifact_count=len(records), page=f"runs/{slug}.md")
    (output / "CATALOG.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    with (output / "metrics-index.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["experiment_directory", "artifact", "json_field", "value"])
        writer.writerows(numeric)
    (output / "manifest.json").write_text(json.dumps({
        "captures": captures, "scope": "All discovered exps and work/experiments directories; see catalogue for missing evidence",
        "runs": list(inventory.values()), "artifacts": artifacts,
    }, indent=2, ensure_ascii=False) + "\n")
    write_checksums(output)
    print(json.dumps({"directories": len(inventory), "artifacts": len(artifacts),
                      "figures": sum(r["kind"] == "figure" for r in artifacts),
                      "bytes": sum(r["bytes"] for r in artifacts)}))


def write_checksums(output):
    rows = []
    for path in sorted(output.rglob("*")):
        if path.is_file() and path.name != "SHA256SUMS":
            rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(output)}")
    (output / "SHA256SUMS").write_text("\n".join(rows) + "\n")


if __name__ == "__main__":
    main()
