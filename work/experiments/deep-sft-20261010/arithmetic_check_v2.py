"""Exact numeric equality-chain checking; symbolic/prose sides remain unproven."""
import ast, operator, re
from fractions import Fraction
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
PURE = re.compile(r'[\d.\s+*/()\-]+')

def calculate(node):
    if isinstance(node, ast.Expression): return calculate(node.body)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float): return Fraction(str(node.value))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub): return -calculate(node.operand)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd): return calculate(node.operand)
    if isinstance(node, ast.BinOp) and type(node.op) in OPS: return OPS[type(node.op)](calculate(node.left), calculate(node.right))
    raise ValueError('unsupported_expression')

def number(segment):
    segment = segment.strip().strip(' ,.;:$').strip()
    if not segment or not PURE.fullmatch(segment): return None
    try: return segment, calculate(ast.parse(segment, mode='eval'))
    except (ValueError, SyntaxError, ZeroDivisionError): return None

def check(text):
    text = text.replace('\\times', '*').replace('\\cdot', '*').replace('×', '*').replace('÷', '/').replace('−', '-')
    findings = []; checked = 0
    for line in re.split(r'\n|</?[^>]+>|;|,(?!\d)', text):
        sides = line.split('=')
        for lhs, rhs in zip(sides, sides[1:]):
            left, right = number(lhs), number(rhs)
            if left is None or right is None: continue
            checked += 1
            if left[1] != right[1]: findings.append(dict(expression=left[0], claimed_expression=right[0], actual=str(left[1]), claimed=str(right[1])))
    return dict(explicit_scalar_equalities_checked=checked, mismatches=findings,
                limitation='Checks adjacent entirely numeric expression sides of equality chains, including parentheses; symbolic/prose relations require independent review.')
