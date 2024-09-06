from itertools import product
from graphviz import Digraph
import re

class BooleanExpression:
    def __init__(self, expression):
        self.expression = expression
        # isolates single character variables from expression and sorts them
        # alphabetically
        self.variables = sorted(set(re.findall(r'\b[A-Z]\b', expression)))
        self.postfix = self.to_postfix(expression)

    def to_postfix(self, infix):
        precedence = {'NOT': 3, 'AND': 2, 'OR': 1, '(': 0}
        stack = []
        postfix = []
        tokens = re.findall(r'\b[A-Z]\b|\bAND\b|\bOR\b|\bNOT\b|[\(\)]', infix)

        for token in tokens:
            if token in self.variables:
                postfix.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()  # Discard the '('
            else:
                while stack and precedence.get(stack[-1], 0) >= precedence.get(token, 0):
                    postfix.append(stack.pop())
                stack.append(token)

        while stack:
            postfix.append(stack.pop())

        return postfix

    def evaluate(self, values):
        stack = []
        for token in self.postfix:
            if token in self.variables:
                stack.append(values[token])
            elif token == 'NOT':
                stack.append(not stack.pop())
            elif token == 'AND':
                b, a = stack.pop(), stack.pop()
                stack.append(a and b)
            elif token == 'OR':
                b, a = stack.pop(), stack.pop()
                stack.append(a or b)
        return stack[0]

    def truth_table(self):
        table = []
        for values in product([False, True], repeat=len(self.variables)):
            row = dict(zip(self.variables, values))
            result = self.evaluate(row)
            table.append((row, result))
        return table

    def print_truth_table(self):
        table = self.truth_table()
        header = ' | '.join(self.variables + ['Result'])
        print(header)
        print('-' * len(header))
        for row, result in table:
            values = [str(int(row[var])) for var in self.variables]
            print(' | '.join(values + [str(int(result))]))


    def generate_logic_diagram(self):
        dot = Digraph(comment='Logic Gate Diagram')
        dot.attr(rankdir='LR')  # Left to right layout

        node_count = 0
        stack = []

        for token in self.postfix:
            if token in self.variables:
                node_name = f'var_{token}'
                dot.node(node_name, token, shape='circle')
                stack.append(node_name)
            elif token == 'NOT':
                input_node = stack.pop()
                node_name = f'not_{node_count}'
                dot.node(node_name, 'NOT', shape='invtriangle')
                dot.edge(input_node, node_name)
                stack.append(node_name)
                node_count += 1
            elif token in ('AND', 'OR'):
                right = stack.pop()
                left = stack.pop()
                node_name = f'{token.lower()}_{node_count}'
                dot.node(node_name, token, shape='rectangle')
                dot.edge(left, node_name)
                dot.edge(right, node_name)
                stack.append(node_name)
                node_count += 1

        # Add result node
        result_node = 'result'
        dot.node(result_node, 'Result', shape='doublecircle')
        dot.edge(stack[-1], result_node)

        return dot


