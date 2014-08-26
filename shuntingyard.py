################################################################################
# Shunting-Yard Algorithm
# shuntingyard.py
#
# (C) Copyright 2014 Travis Montoya
################################################################################
from collections import deque

def parse(expr):
    """
    This function parses an infix expression into Reverse Polish Notation.
    :param expr: An infix notation string
    :return: An RPN string
    """
    outq  = deque()
    stack = []
    ops   = { '^': 4,
              '*': 3,
              '/': 3,
              '+': 2,
              '-': 2
             }

    tokens = expr.split(" ")
    if len(tokens) < 3:
        return "Error"

    for o1 in tokens:
        # -- Handle Parenthesis
        if o1 == "(":
            stack.append(o1)
        elif o1 == ")":
            par = None
            while len(stack) > 0:
                par = stack.pop()
                if par == "(":
                    break
                outq.append(par)
            if not par:
                stack.append(par)
        # -- Handle Operators, Check if they "are" an operator, etc..
        elif o1 in ops:
            if len(stack) > 0:
                o2 = stack.pop()
                if o2 not in ops:
                    stack.append(o2)
                    stack.append(o1)
                    continue
                # While there is an operator on the stack check its precedence
                while o2 in ops:
                    if not (not ((ops[o1] < 4) and (ops[o1] <= ops[o2])) and
                       not (ops[o1] < ops[o2])):
                        outq.append(o2)
                    else:
                        stack.append(o2)
                        break
                    if len(stack) > 0:
                        o2 = stack.pop()
                    else:
                        break
            stack.append(o1)
        # -- Only numbers should be appended here
        else:
            outq.append(o1)

    # -- Tokens are done, reverse and pop entire stack and return RPN string
    stack.reverse()
    [outq.append(op) for op in stack]
    return ' '.join(outq)

def main():
    """
    Main is just a test to see the RPN output from the parser.
    Unit tests are in test_parse.py
    """
    infix = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
    #infix = "2 + 2"
    print(parse(infix))
    
if __name__ == "__main__":
    main()
