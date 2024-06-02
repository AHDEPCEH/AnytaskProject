class Expression:
    def __init__(self, expression):
        self.expression = expression

    def differential(self):
        if isinstance(self.expression, Add | Sub | Mult | Div | Function):
            diff_expression = self.expression.diff().__str__()
            return diff_expression.replace("+-", "-")
        return None

    def __str__(self):
        return self.expression.__str__().replace("+-", "-")


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

    def __truediv__(self, other):
        if isinstance(other, Function):
            return Function(self.coefficient / other.coefficient, self.degree - other.degree)


class Add:
    def __init__(self, left, right):
        if isinstance(right, Function) and isinstance(left, Function):
            if left.degree == right.degree:
                function = left + right
                self.__class__ = function.__class__
                self.__dict__ = function.__dict__
            elif left.degree > right.degree:
                self.left = left
                self.right = right
            else:
                self.left = right
                self.right = left
        elif isinstance(left, Function):
            if isinstance(right, Add | Sub) and isinstance(right.right, Function):
                if right.right.degree == left.degree:
                    self.__class__ = right.__class__
                    self.__dict__ = right.__dict__
                    self.right += left
                elif right.right.degree > left.degree:
                    self.left = right
                    self.right = left
                else:
                    if isinstance(right, Add):
                        self.left = Add(right.left, left)
                    else:
                        self.__class__ = Sub
                        self.left = Sub(right.left, left)
                    self.right = right.right
            else:
                self.left = right
                self.right = left
        elif isinstance(right, Function):
            if isinstance(left, Add | Sub) and isinstance(left.right, Function):
                if left.right.degree == right.degree:
                    self.__class__ = left.__class__
                    self.__dict__ = left.__dict__
                    self.right += right
                elif left.right.degree > right.degree:
                    self.left = left
                    self.right = right
                else:
                    if isinstance(left, Sub):
                        self.__class__ = Sub
                    self.left = Add(left.left, right)
                    self.right = left.right
            else:
                self.left = left
                self.right = right
        else:
            self.left = left
            self.right = right

    def diff(self):
        return Add(self.left.diff(), self.right.diff())

    def __str__(self):
        if isinstance(self.left, Function) and isinstance(self.right, Function) and self.left.coefficient == self.right.coefficient == 0:
            return ""
        elif isinstance(self.left, Function) and self.left.coefficient == 0:
            return self.right.__str__()
        elif isinstance(self.right, Function) and self.right.coefficient == 0:
            return self.left.__str__()
        return f'{self.left}+{self.right}'


class Mult:
    def __init__(self, left, right):
        match (isinstance(left, Function), isinstance(right, Function)):
            case (True, True):  # Простое умножение двух функций от x
                function = left * right
                self.__class__ = function.__class__
                self.__dict__ = function.__dict__
            case (True, False):  # Умножение числа на скобку
                self.__init__(right, left)
            case (False, True):  # Умножение скобки на число
                if isinstance(left, Add):
                    self.__class__ = Add
                    self.left = Mult(left.left, right)
                    self.right = Mult(left.right, right)
                elif isinstance(left, Sub):
                    self.__class__ = Sub
                    self.left = Mult(left.left, right)
                    self.right = Mult(left.right, right)
                elif isinstance(left, Div):
                    self.__class__ = Div
                    self.left = Mult(left.left, right)
                    self.right = left.right
                else:  # можно просто объявить как иначе
                    self.left = left
                    self.right = right
            case (False, False):  # Умножение скобки на скобку
                if isinstance(left, Add | Sub) or isinstance(right, Add | Sub):# Сумма/Вычитание на любую скобку
                    if isinstance(right, Add | Sub):
                        left, right = right, left
                    left_expression = Mult(left.left, right)
                    right_expression = Mult(left.right, right)
                    if isinstance(left, Add):
                        self.__class__ = Add
                    else:
                        self.__class__ = Sub
                    self.left = left_expression
                    self.right = right_expression
                elif isinstance(right, Div):  # Скобка на дробь
                    self.__class__ = right.__class__
                    if isinstance(left, Div):
                        self.left *= left.left
                        self.right *= left.right
                    else:
                        self.left *= left
                else:  # Скобка на умножение
                    if isinstance(left, Div):  # Дробь на умножение
                        self.__class__ = left.__class__
                        self.__dict__ = left.__dict__
                        self.left *= right
                    else:  # Умножение на умножение
                        self.left = left
                        self.right = right

    def diff(self):
        return Add(Mult(self.left.diff(), self.right), Mult(self.left, self.right.diff()))

    def __str__(self):
        return f'{self.left}*{self.right}'


class Div:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def diff(self):
        left = Sub(Mult(self.left.diff(), self.right),
                   Mult(self.left, self.right.diff()))
        right = Mult(self.right, self.right)
        return Div(left, right)

    def __str__(self):
        if isinstance(self.left, Function):
            return f'{self.left}/({self.right})'
        return f'({self.left})/({self.right})'


class Sub:
    def __init__(self, left, right):
        expression = Add(left, Mult(right, Function(-1, 0)))
        self.__class__ = expression.__class__
        self.__dict__ = expression.__dict__
