#!/usr/bin/env python3
"""Make Sol196 plain control by removing only Multiverse tags from tagged rows."""
import json
import sys
from pathlib import Path

import pandas as pd

from mv_format import ANY_TAG


def main():
    tagged_path, prior_plain_path, build_path, out_path, audit_path = map(Path, sys.argv[1:6])
    tagged = pd.read_parquet(tagged_path).to_dict("records")
    plain = pd.read_parquet(prior_plain_path).to_dict("records")
    positives = set(json.loads(build_path.read_text())["positive"]["ids"])
    assert len(tagged) == len(plain) == 383 and len(positives) == 196
    changed = 0
    for left, right in zip(tagged, plain):
        assert left["id"] == right["id"]
        assert left["extra_info"]["question"] == right["extra_info"]["question"]
        if left["id"] in positives:
            original = left["extra_info"]["answer"]
            answer = ANY_TAG.sub("", original)
            assert original.startswith("<think>") and "</think>" in original
            assert not ANY_TAG.search(answer)
            assert answer != right["extra_info"]["answer"]
            right["extra_info"] = dict(right["extra_info"], answer=answer)
            changed += 1
        else:
            assert left["extra_info"]["answer"] == right["extra_info"]["answer"]
    assert changed == len(positives)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(plain).to_parquet(out_path, index=False)
    audit_path.write_text(json.dumps({
        "status": "verified_equal_text_plain_control", "rows": len(plain),
        "positive_rows": changed, "source_tagged": str(tagged_path),
        "source_prior_plain": str(prior_plain_path), "output": str(out_path),
        "transform": "remove only the ten Multiverse XML tags; keep all other characters",
        "same_id_order_and_prompts": True, "nonpositive_identical": True,
    }, indent=2) + "\n")
    print(audit_path.read_text())


if __name__ == "__main__":
    main()
