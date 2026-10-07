"""Diagnostic only (not a scorer): in robust-wrong rows, how often the final 'Final Answer:' line uses Unicode math symbols
that the frozen robust parser may not match against LaTeX ground truth. Usage: python diag_unicode.py <run dir> [bench...]"""
import re, sys, json
import pandas as pd
UNI = re.compile('[√²³⁴⁵⁶⁷⁸⁹⁰¹ⁿπ×÷⋅·−≤≥∞∠°]')
run, benches = sys.argv[1], sys.argv[2:] or ['gsm8k_dev', 'math_dev']
res = {}
for b in benches:
    try:
        r = pd.read_json(f'{run}/rows/{b}.jsonl', lines=True); g = pd.read_json(f'{run}/{b}.jsonl', lines=True)
    except Exception as e:
        res[b] = f'missing {type(e).__name__}'; continue
    fa = g['output'].map(lambda s: (re.findall(r'Final Answer:(.*)', s) or [''])[-1])
    uni = fa.map(lambda s: bool(UNI.search(s)))
    wrong = ~r['acc_robust'].astype(bool)
    res[b] = {'rows': len(r), 'final_line_unicode_all': round(100 * uni.mean(), 2), 'robust_wrong': int(wrong.sum()),
              'robust_wrong_with_unicode_final': int((wrong & uni).sum())}
print(json.dumps({run: res}))
