"""Paired fixed-40 comparison for selective v5 step 64."""

from compare_selective_v2_pilot import main


if __name__ == "__main__":
    main("selective_v5_step64_masked_pilot.tgz", "selective_v5_step64", {
        "c0_corrected": "c0-greedy-pilot40.tgz",
        "selective_v2": "selective_v2_masked_pilot.tgz",
        "selective_v4_step64": "selective_v4_step64_masked_pilot.tgz",
    })
