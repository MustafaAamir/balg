from itertools import product
from graphviz import Digraph
import re
from typing import Dict, Tuple, List

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
    """
    A class to represent and manipulate Boolean expressions.

    This class provides functionality to convert infix Boolean expressions to postfix notation,
    evaluate expressions, generate truth tables, and create logic diagrams.

    Attributes:
        expression (str): The original Boolean expression in infix notation.
        variables (List[str]): A sorted list of variables in the expression.
        postfix (List[str]): The expression converted to postfix notation.
        minterms (List[int]): A list to store the minterms of the expression.
    """
    def __init__(self, expression: str):
        """
        Initializes the BooleanExpression with the given expression.

        Args:
            expression (str): The Boolean expression in infix notation.
        """
        self.expression: str = expression
        # isolates single character variables from expression and sorts them alphabetically
        self.variables: List[str] = sorted(set(re.findall(r'\b[A-Za-z10]\b', expression)))
        self.postfix = self.to_postfix(expression)
        self.minterms = []

    def to_postfix(self, infix: str) -> List[str]:
        """
        Converts the infix Boolean expression to postfix notation.

        Args:
            infix (str): The Boolean expression in infix notation.

        Returns:
            List[str]: The expression in postfix notation.

        Raises:
            SystemExit: If the expression is invalid.
        """

        try:
            precedence = {'~': 3, '&': 2, '+': 1, '(': 0, '^': 2}
            stack = []
            postfix = []
            tokens = re.findall(r'\b[A-Za-z01]\b|\&|\+|\~|\^|[\(\)]', infix)
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
        except (IndexError):
            print(f"\tError: '{infix}' is an invalid expression.")
            exit(0)

    def evaluate(self, values: Dict[str, bool]) -> bool:
        """
        Evaluates the Boolean expression for given variable values.

        Args:
            values (Dict[str, bool]): A dictionary mapping variables to their Boolean values.

        Returns:
            bool: The result of evaluating the expression.
        """
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

    def tt(self) -> List[Tuple[Dict[str, bool], bool]]:
        """
        Generates the truth table for the Boolean expression.

        Returns:
            List[Tuple[Dict[str, bool], bool]]: A list of tuples, each containing a dictionary
            of variable assignments and the corresponding result.
        """
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
        '''
        minth_term = 0
        for values in product([False, True], repeat=len(self.variables)):
            row: Dict[str, bool] = dict(zip(self.variables, values))
            if row.get('1', False):
                row['1'] = True
            if row.get('0', False):
                row['0'] = False
            result: bool = self.evaluate(row)
            if int(result) != 0:
                self.minterms.append(minth_term)
            table.append((row, result))
            minth_term += 1
        return table

    def fmt_tt(self) -> str:
        """
        Formats the truth table as a string.

        Returns:
            str: A formatted string representation of the truth table.
        """
        output_str = ""
        table = self.tt()
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
        tokenDict = {'&': 'AND', '^': 'XOR', '+': 'OR', '~': 'NOT'}
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
                node_name = f'{tokenDict[token]}_{node_count}'
                dot.node(node_name, tokenDict[token], shape='component')
                # edge connects input nodes to gates i think
                dot.edge(left, node_name)
                dot.edge(right, node_name)
                stack.append(node_name)
                node_count += 1

        result_node = 'result'
        dot.node(result_node, 'Result', shape='doublecircle')
        dot.edge(stack[-1], result_node)

        return dot


