import unittest
from src.module.differentiation import initialize_expression

class TestDifferentiation(unittest.TestCase):
    def test_simple_differential(self):
        expression = initialize_expression("x^2 + 7x^6")
        differential_expression = expression.differential()
        self.assertEqual(str(initialize_expression(differential_expression)), '42x^5+2x')

    def test_negative_differential(self):
        expression = initialize_expression("-5x^3 * x^2")
        differential_expression = expression.differential()
        self.assertEqual(str(initialize_expression(differential_expression)), '-25x^4')
    def test_differentiation_with_zero(self):
        expression = initialize_expression("x^2 - x + 4")
        differential_expression = expression.differential()
        self.assertEqual(str(initialize_expression(differential_expression)), '2x-1')

    def test_multidiv_defferential(self):
        expression = initialize_expression("(x^2)/(5x + 4)")
        differential_expression = expression.differential()
        self.assertEqual(str(initialize_expression(differential_expression)), '(5x^2+8x)/(25x^2+40x+16)')

    def test_add_with_simular_functions(self):
        expression = initialize_expression("5x^2 + 4x - 21x - 7 + 7x^3 + 10 - 3x^2")
        differential_expression = expression.differential()
        self.assertEqual(str(initialize_expression(differential_expression)), '21x^2+4x-17')

    def test_hard_differential(self):
        expression = initialize_expression("(x^2+5)/(x^3-x) * 5x - 7 + 6x^2 - 1/x")
        differential_expression = expression.differential()
        self.assertEqual(str(initialize_expression(differential_expression)), '(-60x^3)/(x^6-2x^4+x^2)+12x+1/(x^2)')

if __name__ == '__main__':
    unittest.main()