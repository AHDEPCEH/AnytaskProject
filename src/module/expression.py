class Expression:
    def __init__(self, expression):
        self.expression = expression

    def differential(self):
        if isinstance(self.expression, Add | Sub | Mult | Div | Function):
            return str(self.expression.diff()).replace("+-", "-")
        return None

    def __str__(self):
        return self.expression.__str__()

class Function:
    def __init__(self, coefficient, degree):
        self.degree = degree
        self.coefficient = coefficient

    def diff(self):
        if self.degree != 0:
            return Function(self.coefficient * self.degree, self.degree - 1)
        else:
            return Function(0, 0)

    def __str__(self):
        function = ""
        if self.coefficient != 1 or self.degree == 0:
            function += str(self.coefficient)
        if self.degree == 0:
            return function
        elif self.degree == 1:
            return function + "x"
        return function + "x^" + str(self.degree)

    def __add__(self, other):
        if isinstance(other, Function) and other.degree == self.degree:
            return Function(other.coefficient + self.coefficient, self.degree)
        return self, other

    def __sub__(self, other):
        if isinstance(other, Function) and other.degree == self.degree:
            return Function(self.coefficient - other.coefficient, self.degree)
        return self, other

    def __mul__(self, other):
        if isinstance(other, Function):
            return Function(other.coefficient * self.coefficient, self.degree + other.degree)

    def __divmod__(self, other):
        if isinstance(other, Function):
            return Function(self.coefficient / other.coefficient, self.degree - other.degree)


class Add:
    def __init__(self, left, right):
        if isinstance(right, Function) and isinstance(left, Function) and right.degree == left.degree:
            self.self = Function(left.coefficient + right.coefficient, left.degree)
        elif isinstance(right, Function) and isinstance(left, Add | Sub):
            if isinstance(left.right, Function) and left.right.degree == right.degree:
                self.self = left
                self.right += right
            else:
                self.right = left.right
                self.left = Add(left.left, right)
        elif isinstance(left, Function) and isinstance(right, Add | Sub):
            self.__init__(right, left)
        else:
            self.left = left
            self.right = right

    def diff(self):
        return Add(self.left.diff(), self.right.diff())

    def __str__(self):
        # if isinstance(self.left, Function) and isinstance(self.right, Function):
        #     if self.left.degree == self.right.degree:
        #         self = self.left + self.right
        #         return self.__str__()
        # elif isinstance(self.right, Function):
        #     left_expression = self.left.left
        #     right_expression = self.left.right
        #     if isinstance(right_expression, Function) and left_expression.degree == self.right.degree:
        #         self.left.right += self.right
        #         self = self.left
        #     else:
        #         self.left = Add(left_expression, self.right)
        #         self.right = right_expression
    # Как-то надо доделать
        return f'{self.left}+{self.right}'


class Mult:
    def __init__(self, left, right):
        match (isinstance(left, Function), isinstance(right, Function)):
            case (True, True): #Простое умножение двух функций от x
                self.self = left * right
            case (True, False): #Умножение числа на скобку
                right.left *= left
                if isinstance(right, Add | Sub):
                    right.right *= left
                self.self = right
            case (False, True): #Умножение скобки на число
                left.left *= right
                if isinstance(right, Add | Sub):
                    left.right *= right
                self.self = left
            case (False, False): #Умножение скобки на скобку
                if isinstance(left, Add | Sub): #Сумма/Вычитание на любую скобку
                    left_expression = Mult(left.left, right)
                    right_expression = Mult(left.right, right)
                    self.self = left
                    self.left = left_expression
                    self.right = right_expression
                elif isinstance(right, Add | Sub): #Скобка на сумму/вычитание
                    left_expression = Mult(right.left, left)
                    right_expression = Mult(right.right, left)
                    self.self = right
                    self.left = left_expression
                    self.right = right_expression
                elif isinstance(right, Div): #Скобка на дробь
                    self.self = right
                    if isinstance(left, Div):
                        self.left *= left.left
                        self.right *= left.right
                    else:
                        self.left *= left
                else: #Скобка на умножение
                    if isinstance(left, Div): #Дробь на умножение
                        self.self = left
                        self.left *= right
                    else: #Умножение на умножение
                        self.left = left
                        self.right = right

        self.left = left
        self.right = right

    def diff(self):
        return Add(Mult(self.left.diff(), self.right), Mult(self.left, self.right.diff()))

    def __str__(self):
        match (isinstance(self.left, Function), isinstance(self.right, Function)):
            case (True, True):
                self = Function(self.left.coefficient * self.right.coefficient, self.right.degree + self.left.degree)
                return self.__str__()
            case (True, False):
                if isinstance(self.right, Add):
                    return Add(Mult(self.left, self.right.left), Mult(self.left, self.right.right)).__str__()
                elif isinstance(self.right, Div):
                    return Div(Mult(self.left, self.right.left), self.right.right).__str__()
                return Sub(Mult(self.left, self.right.left), Mult(self.left, self.right.right)).__str__()
            case (False, True):
                if isinstance(self.left, Add):
                    return Add(Mult(self.left.left, self.right), Mult(self.left.right, self.right)).__str__()
                elif isinstance(self.left, Div):
                    return Div(Mult(self.left.left, self.right), self.left.right).__str__()
                return Sub(Mult(self.left.left, self.right), Mult(self.left.right, self.right)).__str__()
        left_expression = Mult(self.left.left, self.right)
        right_expression = Mult(self.left.right, self.right)
        self = self.left
        self.left = left_expression
        self.right = right_expression
        return self.__str__()


class Div:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def diff(self):
        return Div(Sub(Mult(self.left.diff(), self.right), Mult(self.left, self.right.diff())),
                   Mult(self.right, self.right))

    def __str__(self):
        if isinstance(self.left, Function) and isinstance(self.right, Function):
            self = self.left / self.right
            return self.__str__()
        return str(self.left) + '/' + str(self.right)


class Sub:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def diff(self):
        return Sub(self.left.diff(), self.right.diff())

    def __str__(self):
        if isinstance(self.right, Function):
            if isinstance(self.left, Function) and self.left.degree == self.right.degree:
                self = self.left - self.right
                return self.__str__()
            return f'{self.left}-{self.right}'
        else:
            self = Add(self.left, Mult(Function(-1, 0), self.right))
            return self.__str__()
