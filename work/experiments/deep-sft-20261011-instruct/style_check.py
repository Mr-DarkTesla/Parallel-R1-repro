"""Fail closed on known parser leakage and serial arithmetic before forks."""
import re
MARKERS=[r'Return only',r'[Ll]et.s final',r'[Ww]e won.t',r'[Ww]e.(?:ll| will) output only',r'[Nn]eed ["“]',r'^\s*\.\s*["”]']
def check(text,blocks):
    failures=[];cursor=0
    for ri,block in enumerate(blocks,1):
        prefix=text[cursor:block['start']]
        for pattern in MARKERS:
            if re.search(pattern,prefix):failures.append(dict(type='drafting_or_parser_leak',round=ri,pattern=pattern))
        for m in re.finditer(r'(?<![A-Za-z0-9_])([\d()+*/\s-]+)\s*=\s*(-?\d+)\b',prefix):
            if re.search(r'\d\s*[+*/-]\s*(?:\d|\()',m[1]):
                failures.append(dict(type='serial_prefork_arithmetic',round=ri,expression=m[0]))
        cursor=block['end']
    return dict(failures=failures,limitations='Detects explicit scalar pre-fork arithmetic and known leakage markers, not arbitrary prose computation.')
