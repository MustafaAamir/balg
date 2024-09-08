import random
from typing import List

class BooleanExpressionGenerator:
    def __init__(self, max_depth=4, max_identifiers=5):
        self.max_depth = max_depth
        self.identifiers = tuple(chr(i) for i in range(65, 65 + max_identifiers))
        self.operators = ('~', '&', '+', '^')

    def generate_expression(self, depth=0) -> str:
        if depth >= self.max_depth or random.random() < 0.3:
            return random.choice(self.identifiers)

        operator = random.choice(self.operators)

        if operator == '~':
            return f"~({self.generate_expression(depth + 1)})"
        else:
            left = self.generate_expression(depth + 1)
            right = self.generate_expression(depth + 1)
            return f"({left} {operator} {right})"

    def generate_expressions(self, count) -> List[str]:
        return [self.generate_expression() for _ in range(count)]

generator = BooleanExpressionGenerator()
expressions = generator.generate_expressions(1000)
