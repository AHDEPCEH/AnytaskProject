import re

from differentiation import initialize_expression


def check_expression(expression: str) -> int:
    if not expression:
        return 1

    count_open_brackets = 0
    count_close_brackets = 0
    for i in range(len(expression)):
        char = expression[i]
        if char not in "x+-*/^0123456789()":
            return i + 1
        if char == '(':
            count_open_brackets += 1
        elif char == ')':
            count_close_brackets += 1
            if count_open_brackets < count_close_brackets:
                return i + 1

    if count_close_brackets > count_open_brackets:
        return 1
    elif count_open_brackets > count_close_brackets:
        return len(expression) + 1

    expr = expression
    for match in re.finditer("\\^\\d", expression):
        count_char = len(match.group(0))
        if count_char > 0:
            expr = expr.replace(match.group(0), " " * count_char)
    if "^" in expr:
        return expr.find("^") + 1

    return 0


def main():
    while True:
        command = input("Enter a command or f(x): ")

        if command.lower() in ['--help', '-h']:
            print("Available commands:")
            print("--help, -h: display a list of available commands")
            print("exit: end the program\n")
        elif command.lower() == 'exit':
            break
        else:
            if check_expression(command.replace(" ", "")) != 0:
                print(f'Incorrect expression, error position: {check_expression(command)}')
            else:
                try:
                    expression = initialize_expression(command)
                    differential_expression = expression.differential()
                    print(f'Differential: {initialize_expression(differential_expression)}')
                except Exception:
                    print("Incorrect expression")



if __name__ == "__main__":
    main()
