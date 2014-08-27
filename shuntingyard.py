################################################################################
# Shunting-Yard Algorithm
# shuntingyard.py
#
# (C) Copyright 2014 Travis Montoya
################################################################################
################################################################################
# error   :  Error string for the user.
# special :  A list of function operators
# ops     :  Dictionary of operators and their precedence.
# outq    :  Output queue which holds the final RPN string
# stack   :  A list that holds the operator stack.
# o1      :  Token from the expression string.
# o2      :  Operator from the operator stack.
################################################################################
from collections import deque

error = "Invalid infix notation."
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
    while len(stack) > 0:
        op = stack.pop()
        if op == special[0]:
            break
        outq.append(op)
    return outq, stack

def check_parenthesis(outq: deque, stack: [], o1):
    """Handle function argument separators."""
    if o1 == special[0]:
        stack.append(o1)
        return outq, stack
    elif o1 == special[1]:
        return pop_functionops(outq, stack)

############### Parse operator stack ###############

def pop_operatorstack(outq: deque, stack: [], o1, o2):
    """Add operators to the output queue depending on precedence."""
    def precedence(a, b):
        return ((ops[a] < 4) and (ops[a] <= ops[b])) or (ops[a] < ops[b])

    while o2 in ops:
        if not precedence(o1, o2):
            stack.append(o2)
            break
        outq.append(o2)
        if len(stack) > 0:
            o2 = stack.pop()
            continue
        break
    stack.append(o1)
    return outq, stack

def check_operatorstack(outq: deque, stack: [], o1):
    """Check precedence of current operator token and stack operator."""
    if len(stack) > 0:
        o2 = stack.pop()
        if o2 not in ops:
            stack.extend((o2, o1))
            return outq, stack
        return pop_operatorstack(outq, stack, o1, o2)
    stack.append(o1)
    return outq, stack

############### Number error checking ###############

def check_number(o1):
    """Check that the number is valid. (we support negative numbers)"""
    if len(o1) < 2: return o1.isdigit()
    return o1[0] == '-' or o1[0].isdigit() and o1[1:].isdigit()

############### Parse the infix expression ###############

def parse_infix(expression):
    """Parse an infix expression into reverse polish notation."""
    outputq = deque()
    stack = []
    tokens = expression.split(" ")

    if len(tokens) < 3: return error
    for o1 in tokens:
        if o1 in special:
            outputq, stack = check_parenthesis(outputq, stack, o1)
            continue
        elif o1 in ops:
            outputq, stack = check_operatorstack(outputq, stack, o1)
            continue
        if not check_number(o1): return error
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
