"""Conservative exact checking of explicit scalar arithmetic, without eval."""
import ast, operator, re
from fractions import Fraction

OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}
NUM=r'-?\d+(?:\.\d+)?'
EXPR=re.compile(r'(?<![\w.])('+NUM+r'(?:\s*[+*/-]\s*'+NUM+r')+)\s*=\s*('+NUM+r')(?![\w.])')
def calculate(node):
    if isinstance(node,ast.Expression):return calculate(node.body)
    if isinstance(node,ast.Constant) and type(node.value) in (int,float):return Fraction(str(node.value))
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -calculate(node.operand)
    if isinstance(node,ast.BinOp) and type(node.op) in OPS:return OPS[type(node.op)](calculate(node.left),calculate(node.right))
    raise ValueError('unsupported_expression')
def check(text):
    text=text.replace('\\times','*').replace('\\cdot','*').replace('×','*').replace('÷','/').replace('−','-')
    findings=[];checked=0
    for m in EXPR.finditer(text):
        # Parenthesized longer expressions cannot be checked by a suffix match.
        preceding=text[max(0,m.start()-3):m.start()]
        if '(' in preceding or ')' in m.group(1):continue
        try:
            actual=calculate(ast.parse(m.group(1),mode='eval'));claimed=Fraction(m.group(2));checked+=1
            if actual!=claimed:findings.append(dict(expression=m.group(1),claimed=m.group(2),actual=str(actual)))
        except (ValueError,SyntaxError,ZeroDivisionError):continue
    return dict(explicit_scalar_equalities_checked=checked,mismatches=findings,
        limitation='Checks only flat explicit numeric equalities. Governing relations, symbolic algebra and meanings require separate review.')
