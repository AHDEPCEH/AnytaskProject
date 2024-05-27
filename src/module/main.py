from differentiation import initialize_expression
def main():
    expression = initialize_expression(input("Введите функцию от x: "))
    differential_expression = expression.differential()
    print(f'Differential: {initialize_expression(differential_expression)}')

if __name__ == "__main__":
    main()
