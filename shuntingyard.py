################################################################################
# Shunting-Yard Algorithm
# shuntingyard.py
#
# (C) Copyright 2014 Travis Montoya
################################################################################
from collections import deque

special = ["(", ")"]
ops = { '^': 4,
        '*': 3,
        '/': 3,
        '+': 2,
        '-': 2
      }

############### Handle function operators ###############

def pop_functionops(outq: deque, stack: []):
    """Pop items off the stack and onto output queue until we find matching parenthesis."""
    out = outq
    opstack = stack

    while len(opstack) > 0:
        op = opstack.pop()
        if op == special[0]:
            break
        out.append(op)
    return out, opstack

def check_parenthesis(outq: deque, stack: [], value):
    """Handle function argument separators."""
    out = outq
    opstack = stack
    o1 = value

    if o1 == special[0]:
        opstack.append(o1)
        return out, opstack
    elif o1 == special[1]:
        return pop_functionops(out, opstack)

############### Parse operator stack ###############

def pop_operatorstack(outq: deque, stack: [], op1, op2):
    """Add operators to the output queue depending on precedence."""
    out = outq
    opstack = stack
    o1 = op1
    o2 = op2

    def precedence(a, b):
        return ((ops[a] < 4) and (ops[a] <= ops[b])) or (ops[a] < ops[b])

    while o2 in ops:
        if not precedence(o1, o2):
            opstack.append(o2)
            break
        out.append(o2)
        if len(opstack) > 0:
            o2 = opstack.pop()
            continue
        break
    opstack.append(o1)
    return out, opstack


def check_operatorstack(outq: deque, stack: [], value):
    """Check precedence of current operator token and stack operator."""
    out = outq
    opstack = stack
    o1 = value

    if len(opstack) > 0:
        o2 = opstack.pop()
        if o2 not in ops:
            opstack.extend((o2, o1))
            return out, opstack
        return pop_operatorstack(out, opstack, o1, o2)
    opstack.append(o1)
    return out, opstack

############### Number error checking ###############

def check_number(value):
    """Check that the number is valid. (we support negative numbers)"""
    o1 = value
    if len(o1) < 2: return o1.isdigit()
    return o1[0] == '-' or o1[0].isdigit() and o1[1:].isdigit()

############### Parse the infix expression ###############

def parse_infix(expr):
    """Parse an infix expression into reverse polish notation."""
    outputq = deque()
    stack = []
    tokens = expr.split(" ")

    if len(tokens) < 3: return "Invalid infix notation."
    for o1 in tokens:
        if o1 in special:
            outputq, stack = check_parenthesis(outputq, stack, o1)
            continue
        elif o1 in ops:
            outputq, stack = check_operatorstack(outputq, stack, o1)
            continue
        if not check_number(o1): return "Invalid infix notation."
        outputq.append(o1)
    stack.reverse()
    [outputq.append(op) for op in stack]
    return ' '.join(outputq)

############### Parser test ###############

def main():
    """Send an infix expression to parser."""
    infix = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
    print(parse_infix(infix))
    
if __name__ == "__main__":
    main()
