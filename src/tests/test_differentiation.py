import unittest
from src.module.differentiation import initialize_expression

class TestDifferentiation(unittest.TestCase):
    def test_differentiation(self):
        # expression = initialize_expression("x^2 + 7x^6")
        # differential_expression = expression.differential()
        # self.assertEqual(str(initialize_expression(differential_expression)), '2x+42x^5')
        #
        # expression = initialize_expression("-5x^3 * x^2")
        # differential_expression = expression.differential()
        # self.assertEqual(str(initialize_expression(differential_expression)), '-25x^4')

        expression = initialize_expression("x^2 - x + 4")
        differential_expression = expression.differential()
        self.assertEqual(str(initialize_expression(differential_expression)), '2x-1')

        # expression = initialize_expression("(x^2)/(x + 1)")
        # differential_expression = expression.differential()
        # self.assertEqual(str(initialize_expression(differential_expression)), '(3x^2+2x)/(x+1)^2')

if __name__ == '__main__':
    unittest.main()