"""Replay every named layered-DAG result and check isolated sibling references."""
import re

def check(text, oracle, blocks):
    names=oracle['names'];alts='|'.join(re.escape(n) for n in names)
    label=re.compile(r'\b('+alts+r')_(\d+)\b')
    # A named independent verification LHS also defines its computed amount.
    # Only the literal assignment suffix is recognized; RHS visibility remains
    # identical and self/sibling reads are still rejected.
    claim=re.compile(r'(?:^|(?<=[\n,;:.>]))\s*('+alts+r')_(\d+)(?:\s+check)?\s*=\s*',re.M)
    expected={(name,0):value for name,value in zip(names,oracle['initial'])}
    for s,layer in enumerate(oracle['stages'],1):
        for name,node in zip(names,layer):expected[name,s]=node['result']
    failures=[];checked=[]
    def key(m):return (m[1],int(m[2]))
    def claims(s):
        matches=list(claim.finditer(s));result=[]
        for i,m in enumerate(matches):
            # Result is the last numeric literal after an equality in this claim.
            end=matches[i+1].start() if i+1<len(matches) else len(s)
            # Stop at sentence/list boundaries: later final sums do not redefine
            # the named amount. Decimal points are not sentence boundaries.
            part=re.split(r'\n|;|,|(?<!\d)\.|\.(?!\d)',s[m.end():end],maxsplit=1)[0]
            eqs=re.findall(r'(?:^|=)\s*(-?\d+(?:\.\d+)?)(?=\s*(?:[,.;$]|$|[A-Za-z]))',part)
            if not eqs:continue
            number=eqs[-1]
            try:value=int(number)
            except ValueError:continue
            result.append((key(m),value,m.start(1)))
        return result
    normalized=text.replace('$','').replace('\\,',' ').replace('\\!',' ')
    for k,value,offset in claims(normalized):
        checked.append(dict(label=f'{k[0]}_{k[1]}',value=value,expected=expected.get(k)))
        if expected.get(k)!=value:failures.append(dict(type='named_intermediate_mismatch',label=f'{k[0]}_{k[1]}',claimed=value,expected=expected.get(k)))
    established={(name,0) for name in names};cursor=0
    # Blocks include their exact matched boundaries, provided by the caller.
    for index,block in enumerate(blocks,1):
        prefork=text[cursor:block['start']].replace('$','').replace('\\,',' ').replace('\\!',' ')
        prefork_claims={k for k,_,_ in claims(prefork)}
        for k in prefork_claims-established:
            failures.append(dict(type='prefork_computes_new_stage_result',round=index,label=f'{k[0]}_{k[1]}'))
        produced=set()
        for pid,body in block['paths']:
            body=body.replace('$','').replace('\\,',' ').replace('\\!',' ')
            local=set(established);definitions={offset:k for k,_,offset in claims(body)};pending=[]
            for m in label.finditer(body):
                while pending and pending[0][1]<=m.start():
                    k_done,_=pending.pop(0);local.add(k_done);produced.add(k_done)
                k=key(m)
                if m.start() in definitions:
                    later=[offset for offset in definitions if offset>m.start()]
                    newline=body.find('\n',m.start())
                    end=min(later+[newline if newline>=0 else len(body)])
                    pending.append((k,end))
                elif k not in local:
                    failures.append(dict(type='reference_unavailable_to_sibling',round=index,path_id=int(pid),label=f'{k[0]}_{k[1]}'))
            for k,_ in pending:local.add(k);produced.add(k)
        summary=block['summary'].replace('$','').replace('\\,',' ').replace('\\!',' ')
        summary_claims={k for k,_,_ in claims(summary)}
        for k in summary_claims:
            if k not in established|produced:failures.append(dict(type='summary_invents_unestablished_result',round=index,label=f'{k[0]}_{k[1]}'))
        established.update(summary_claims);cursor=block['end']
    needed=set(expected)-{(name,0) for name in names}
    missing=needed-established
    if missing:failures.append(dict(type='missing_named_stage_results',labels=[f'{n}_{s}' for n,s in sorted(missing)]))
    return dict(known_oracle_nodes=len(needed),named_claims_checked=len(checked),all_expected_nodes_exposed=not missing,failures=failures,
        limitations='Checks named scalar amounts and availability, not all prose meanings. Manual source-to-relation review remains required.')
