class Function:
    def __init__(self, expression):
        self.expression = expression

    def splitExpr(self):
        expr = ""
        flag = False
        functions = []
        operations = []
        for c in self.expression:
            match c:
                case '(':
                    flag = True
                case ')':
                    flag = False
                case '+' | '-' | '/' | '*':
                    if not flag:
                        functions.append(Function(expr))
                        operations.append(c)
                        expr = ""
                    else:
                        expr += c
                case _:
                    expr += c
        functions.append(Function(expr))
        return functions, operations

    def differentiate(self):
        functions, operations = self.splitExpr()
        index = 0
        diff_func = functions[index]
        if len(operations) > 0:
            while index < len(operations) and operations[index] not in ['+', '-']:
                match operations[index]:
                    case '*':
                        diff_func = (diff_func.differentiate() * functions[index + 1]
                                    + diff_func * functions[index + 1].differentiate())
                    case '/':
                        diff_func = (((diff_func.differentiate() * functions[index + 1]
                                      - diff_func * functions[index + 1].differentiate()))
                                    / Function(functions[index + 1].expression + "^2"))
                index += 1
            newExpr = "0"
            for i in range(index + 1, len(functions)):
                newExpr += functions[i].expression
                if (i != len(operations)):
                    newExpr += operations[i]
            if index == 0:
                if operations[0] == '+':
                    print(diff_func.differentiate())
                    return diff_func.differentiate() + Function(newExpr).differentiate()
                return diff_func.differentiate() - Function(newExpr).differentiate()
            elif index == len(operations):
                print(diff_func)
                return diff_func
            else:
                if operations[0] == '+':
                    return diff_func + Function(newExpr).differentiate()
                return diff_func - Function(newExpr).differentiate()
        else:
            if 'x^' in diff_func.expression:
                expr = diff_func.expression.split('^')
                return Function(str(expr[1]) + "x^(" + str(expr[1]) + "-1)")
            else:
                if 'x' == diff_func.expression:
                    return Function('1')
                return Function('0')

    def __str__(self):
        return self.expression

    def __add__(self, other):
        return Function(self.expression + '+' + other.expression)

    def __sub__(self, other):
        return Function(self.expression + '-' + other.expression)

    def __truediv__(self, other):
        return Function(self.expression + '/' + other.expression)

    def __mul__(self, other):
        return Function(self.expression + '*' + other.expression)



def main():
    expression = input("Введите функцию от x: ")
    func = Function(expression)
    print("Производная равна: ", func.differentiate())

if __name__ == "__main__":
    main()