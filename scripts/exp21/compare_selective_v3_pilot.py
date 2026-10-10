"""Compare selective v3 with the fixed 40-question masked pilot archives.

Usage: python3 scripts/exp21/compare_selective_v3_pilot.py
"""

from compare_selective_v2_pilot import main


if __name__ == "__main__":
    main("selective_v3_masked_pilot.tgz", "selective_v3", {
        "c0_corrected": "c0-greedy-pilot40.tgz",
        "selective_v1": "selective_blocks_masked_pilot.tgz",
        "selective_v2": "selective_v2_masked_pilot.tgz",
        "m1_text1": "text1_masked_pilot.tgz",
        "m1_tagweighted": "m1-tagweighted-greedy-pilot40.tgz",
    }, candidate_corrections=(("MATH_DEV", "math-test/29", 0),))
