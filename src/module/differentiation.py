import re
from src.module.expression import Expression, Function, Add, Sub, Mult, Div
from typing import List


def initialize_expression(expression: str) -> Expression:
    expression = expression.replace(' ', '')
    functions, expression = parse_functions(expression)
    functions, expression = find_unary_minus(expression, functions)
    expression = infix_to_postfix(expression)
    return Expression(split_expression(expression, functions))


def parse_functions(expression: str) -> (List[Function], str):
    functions = []
    count_functions = 0
    abbreviated_expression = expression
    for x in re.finditer("((\\d*)x(\\^\\d+)?|(\\d+)(\\^\\d+)?)", expression):
        if x.group(0) != '':
            if 'x' in x.group(1):
                coef = 1
                degree = 1
                if x.group(2) != '':
                    coef = int(x.group(2))
                if x.group(3) and x.group(3) != '':
                    degree = int(x.group(3)[1:])
            else:
                coef = int(x.group(4))
                degree = 0
                if x.group(5) and x.group(5) != '':
                    coef **= int(x.group(5)[1:])
            functions.append(Function(coef, degree))
            abbreviated_expression = abbreviated_expression.replace(x.group(0), 'f', 1)
    expression = ""
    for char in abbreviated_expression:
        expression += char
        if char == 'f':
            expression += str(count_functions)
            count_functions += 1
    return functions, expression



def find_unary_minus(expression: str, functions: List[Function]) -> (List[Function], str):
    new_expression = ""
    count_operators = 0
    count_functions = 0
    for char in expression:
        if char in ("-", "+", "*", "/"):
            count_operators += 1
            if count_functions < count_operators and char == '-':
                functions[count_functions] *= Function(-1, 0)
                count_operators -= 1
            elif count_functions < count_operators and char == '+':
                count_operators -= 1
            elif count_functions < count_operators:
                raise Exception
            else:
                new_expression += char
        else:
            if char == "f":
                count_functions += 1
            new_expression += char
    return functions, new_expression


def infix_to_postfix(expression) -> str:
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    stack = []

    for char in expression:
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                output.append(stack.pop())
            stack.append(char)

    while stack:
        output.append(stack.pop())

    return ''.join(output)


def split_expression(expression: str, functions: [Function]) -> Add | Sub | Mult | Div:
    start_count = len(functions)
    count = start_count
    while len(expression) != 0:
        if len(re.findall("f\\d+f\\d+[+\\-*\\/]", expression)) != 0:
            pattern = re.findall("f\\d+f\\d+[+\\-*\\/]", expression)[0]
        else:
            break
        numbers = re.findall("\\d+", pattern)
        if pattern != '' and len(numbers) == 2:
            left = functions[int(numbers[0])]
            right = functions[int(numbers[1])]
            match pattern[-1]:
                case '+':
                    functions.append(Add(left, right))
                case '-':
                    functions.append(Sub(left, right))
                case '*':
                    functions.append(Mult(left, right))
                case '/':
                    functions.append(Div(left, right))
        expression = expression.replace(pattern, "f" + str(count))
        count += 1
    if start_count < len(functions) or count == 1:
        return functions[-1]
    else:
        raise Exception
