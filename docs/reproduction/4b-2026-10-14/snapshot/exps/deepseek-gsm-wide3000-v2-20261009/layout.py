"""Raw public worked solution -> canonical student think + final solution."""
def split_solution(text):
    reason,marker,final=text.strip().partition('\nFinal solution:\n')
    assert marker and reason.strip() and final.strip(),'missing_final_solution'
    assert '<think>' not in text and '</think>' not in text,'outer_think_in_raw'
    assert final.strip().splitlines()[-1].startswith('Final Answer: '),'final_answer_not_last'
    assert not any(tag in final for tag in ['<Parallel>','<Path>','<Summary>']),'fork_in_final_solution'
    return reason.rstrip(),final.strip()
