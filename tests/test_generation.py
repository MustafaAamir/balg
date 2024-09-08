import unittest
from balg.boolean import Boolean

class TestBoolean(unittest.TestCase):
    def test_expr_cmp(self):
        boolean = Boolean()
        expressions = boolean.generate_expressions(5, 5, 1000)
        for expression in expressions:
            expr1 = boolean.expr_simplify(expression)
            assert boolean.expr_cmp([expr1, expression])

if __name__ == "__main__":
    unittest.main()
