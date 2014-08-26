################################################################################
# Shunting-Yard Algorithm
# shuntingyard.py
#
# ! This needs major refactoring !
#
# (C) Copyright 2014 Travis Montoya
################################################################################
from collections import deque

# Shunting yard implementation
def parse(expr):
    outq  = deque()
    stack = []
    ops   = { '^': 4,
              '*': 3,
              '/': 3,
              '+': 2,
              '-': 2
             }

    tokens = expr.split(" ")
    if(len(tokens) < 3):
        return "Error"

    for o1 in tokens:
        ########################################################################
        # Handle Parenthesis
        ########################################################################
        if o1 == "(":
            stack.append(o1)
        elif o1 == ")":
            while 1:
                par = stack.pop()
                if(par != "("):
                    outq.append(par)
                elif(par == "("):
                    break
                else:
                    stack.append(par)
                    break
        ########################################################################
        # Handle Operators, Check if they "are" an operator, etc..
        ########################################################################
        elif o1 in ops:
            if(len(stack) < 1):
                stack.append(o1)
            else:
                o2 = stack.pop()
                if(o2 not in ops):
                    stack.append(o2)
                    stack.append(o1)
                    continue
                # While there is an operator on the stack check its precedence
                while (o2 in ops):
                    if(((ops[o1] < 4) and (ops[o1] <= ops[o2])) or
                       (ops[o1] < ops[o2])):
                        outq.append(o2)
                    else:
                        stack.append(o2)
                        break
                    if(len(stack) > 0):
                        o2 = stack.pop()
                    else:
                        break
                stack.append(o1)
        ########################################################################
        # It must be an integer than
        ########################################################################
        else:
            outq.append(o1)

    # Tokens are done, pop entire stack
    stack.reverse()
    for i in stack:
        outq.append(i)
        
    return ' '.join(outq)


################################################################################
# Test case for parse()
################################################################################
def main():
    infix_wiki = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
    infix_2 = "( 5 + 3 ) * 12 / 3"
    infix_1 = "( 12 + 33 ) / 4 + 1"
    infix_0 = "2 + 2"
    postfix = parse(infix_wiki)
    print(postfix)
    
if __name__ == "__main__":
    main()
