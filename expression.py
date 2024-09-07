from itertools import product
from graphviz import Digraph
import re
from typing import Dict, Tuple, List, Any

'''
tokenize
   |
   V
postfix
   |
   V
replace variables with boolean values and evaluate for every combination
   |
   V
incrementally append result to table
   |
   V
print truth_table
   |
   V
parse postfix representation and generate logic diagram
'''

class BooleanExpression:
    def __init__(self, expression: str):
        self.expression: str = expression
        # isolates single character variables from expression and sorts them alphabetically
        self.variables: List[str] = sorted(set(re.findall(r'\b[A-Za-z]\b', expression)))
        self.postfix = self.to_postfix(expression)

    def to_postfix(self, infix) -> List[str]:
        precedence = {'~': 3, '&': 2, '+': 1, '(': 0, '^': 2}
        stack = []
        postfix = []
        tokens = re.findall(r'\b[A-Za-z]\b|\&|\+|\~|\^|[\(\)]', infix)
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

    def evaluate(self, values: Dict[str, bool]) -> bool:
        stack: List[bool] = []
        for token in self.postfix:
            if token in self.variables:
                stack.append(values[token])
            elif token == '~':
                stack.append(not stack.pop())
            elif token == '&':
                b, a = stack.pop(), stack.pop()
                stack.append(a and b)
            elif token == '+':
                b, a = stack.pop(), stack.pop()
                stack.append(a or b)
            elif token == '^':
                b, a = stack.pop(), stack.pop()
                stack.append(a != b)

        return stack[0]

    def truth_table(self) -> List[Tuple[Dict[str, bool], bool]]:
        table: List[Tuple[Dict[str, bool], bool]] = []
        '''
        input : A and B
        for 2 variables, generates combinations of True and False
        (False, False),
        (False, True),
        (True, False),
        (True, True),

        (A, B) are mapped to their corresponding element in the generated tuple
        [((A, False), (B, False))],
        [((A, False), (B, True))],
        [((A, True), (B, False))],
        [((A, True), (B, True))],

        row = dict([("A", False), ("B", True)])
        row = {'A': False, 'B': True}
        therefore, row is a dictionary of variables with a boolean key.
        '''
        for values in product([False, True], repeat=len(self.variables)):
            row: Dict[str, bool] = dict(zip(self.variables, values))
            result: bool = self.evaluate(row)
            table.append((row, result))
        return table

    def tt(self):
        output_str = ""
        table = self.truth_table()
        header = ' | '.join(self.variables + ['Res'])
        output_str += header
        output_str += "\n" + ('-' * len(header)) + "\n"
        for row, result in table:
            values = [str(int(row[var])) for var in self.variables]
            output_str += ' | '.join(values + [str(int(result))]) + "\n"
        return output_str


    def generate_logic_diagram(self) -> Digraph:
        dot = Digraph(comment='Logic Gate Diagram')
        dot.attr(rankdir='LR')
        node_count = 0
        stack = []
        for token in self.postfix:
            if token in self.variables:
                node_name = f'var_{token}'
                dot.node(node_name, token, shape='square')
                stack.append(node_name)
            elif token == '~':
                input_node = stack.pop()
                node_name = f'not_{node_count}'
                dot.node(node_name, 'NOT', shape='diamond')
                dot.edge(input_node, node_name)
                stack.append(node_name)
                node_count += 1
            elif token in ('&', '+', '^'):
                right = stack.pop()
                left = stack.pop()
                node_name = f'{token.lower()}_{node_count}'
                dot.node(node_name, token, shape='component')
                # edge connects input nodes to gates i think
                dot.edge(left, node_name)
                dot.edge(right, node_name)
                stack.append(node_name)
                node_count += 1

        result_node = 'result'
        dot.node(result_node, 'Result', shape='doublecircle')
        dot.edge(stack[-1], result_node)

        return dot


