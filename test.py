import re
from itertools import product, combinations
from graphviz import Digraph

class TruthTableSynthesizer:
    def __init__(self, variables, minterms):
        self.variables = variables
        self.minterms = set(minterms)
        self.num_vars = len(variables)
        self.max_iterations = 1000  # Safeguard against excessive looping

    def decimal_to_binary(self, num):
        return format(num, f'0{self.num_vars}b')

    def combine_implicants(self, implicants):
        combined = set()
        for a, b in combinations(implicants, 2):
            diff = [i for i in range(self.num_vars) if a[i] != b[i]]
            if len(diff) == 1:
                combined_implicant = list(a)
                combined_implicant[diff[0]] = '-'
                combined.add(''.join(combined_implicant))
        return combined

    def get_prime_implicants(self):
        groups = [set() for _ in range(self.num_vars + 1)]
        for m in self.minterms:
            groups[bin(m).count('1')].add(self.decimal_to_binary(m))

        prime_implicants = set()
        iteration = 0
        while iteration < self.max_iterations:
            new_groups = [set() for _ in range(self.num_vars)]
            for i in range(len(groups) - 1):
                new_implicants = self.combine_implicants(groups[i] | groups[i+1])
                new_groups[i] = new_implicants
                uncombined = groups[i] | groups[i+1] - {imp for imp in new_implicants for c in imp if c != '-'}
                prime_implicants |= uncombined

            if not any(new_groups):
                prime_implicants |= set.union(*groups)
                break

            groups = new_groups
            iteration += 1

        return prime_implicants

    def covers_minterm(self, implicant, minterm):
        return all(i == '-' or i == m for i, m in zip(implicant, self.decimal_to_binary(minterm)))

    def get_essential_prime_implicants(self, prime_implicants):
        coverage = {m: [pi for pi in prime_implicants if self.covers_minterm(pi, m)] for m in self.minterms}
        essential = set()
        for m, implicants in coverage.items():
            if len(implicants) == 1:
                essential.add(implicants[0])
        return essential

    def minimize_function(self, prime_implicants, essential_implicants):
        covered_minterms = set()
        result = list(essential_implicants)
        remaining_implicants = prime_implicants - essential_implicants

        for ei in essential_implicants:
            covered_minterms |= {m for m in self.minterms if self.covers_minterm(ei, m)}

        while covered_minterms != self.minterms:
            best_implicant = max(remaining_implicants, key=lambda x: sum(self.covers_minterm(x, m) for m in self.minterms - covered_minterms))
            result.append(best_implicant)
            covered_minterms |= {m for m in self.minterms if self.covers_minterm(best_implicant, m)}
            remaining_implicants.remove(best_implicant)

        return result

    def implicant_to_expression(self, implicant):
        terms = []
        for var, value in zip(self.variables, implicant):
            if value == '1':
                terms.append(var)
            elif value == '0':
                terms.append(f'NOT {var}')
        return ' AND '.join(terms) if terms else '1'

    def synthesize(self):
        if not self.minterms:
            return '0'
        if len(self.minterms) == 2**self.num_vars:
            return '1'

        prime_implicants = self.get_prime_implicants()
        essential_implicants = self.get_essential_prime_implicants(prime_implicants)
        minimal_implicants = self.minimize_function(prime_implicants, essential_implicants)

        expression_terms = [self.implicant_to_expression(imp) for imp in minimal_implicants]
        expression = ' OR '.join(f'({term})' for term in expression_terms)

        return expression


    def generate_logic_diagram(self, expression):
        dot = Digraph(comment='Logic Gate Diagram')
        dot.attr(rankdir='LR')

        def parse_expression(expr):
            tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
            output_queue = []
            operator_stack = []

            for token in tokens:
                if token in self.variables:
                    output_queue.append(token)
                elif token == 'NOT':
                    operator_stack.append(token)
                elif token in ('AND', 'OR'):
                    while operator_stack and operator_stack[-1] != '(' and (operator_stack[-1] == 'NOT' or token == 'OR'):
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)
                elif token == '(':
                    operator_stack.append(token)
                elif token == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        output_queue.append(operator_stack.pop())
                    if operator_stack and operator_stack[-1] == '(':
                        operator_stack.pop()

            while operator_stack:
                output_queue.append(operator_stack.pop())

            return output_queue

        def create_node(token, node_count):
            if token in self.variables:
                node_name = f'var_{token}'
                dot.node(node_name, token, shape='circle')
            elif token == 'NOT':
                node_name = f'not_{node_count}'
                dot.node(node_name, 'NOT', shape='invtriangle')
            else:  # AND or OR
                node_name = f'{token.lower()}_{node_count}'
                dot.node(node_name, token, shape='rectangle')
            return node_name

        tokens = parse_expression(expression)
        stack = []
        node_count = 0

        for token in tokens:
            if token in self.variables:
                stack.append(create_node(token, node_count))
            elif token == 'NOT':
                input_node = stack.pop()
                node_name = create_node(token, node_count)
                dot.edge(input_node, node_name)
                stack.append(node_name)
                node_count += 1
            elif token in ('AND', 'OR'):
                right = stack.pop()
                left = stack.pop()
                node_name = create_node(token, node_count)
                dot.edge(left, node_name)
                dot.edge(right, node_name)
                stack.append(node_name)
                node_count += 1

        result_node = 'result'
        dot.node(result_node, 'Result', shape='doublecircle')
        dot.edge(stack[-1], result_node)

        return dot



class BooleanExpression:
    def __init__(self, expression):
        self.expression = expression
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

# Example usage
if __name__ == "__main__":
    input_expression = input(" $ ")
    expr = BooleanExpression(input_expression)
    expr.print_truth_table()
    print_diagram_a = input(" (?) produce diagram? (y/n)")
    if (print_diagram_a.lower() == "y"):
        diagram = expr.generate_logic_diagram()
        diagram.render(f"logic_diagram")


'''
variables = ['A', 'B', 'C']
minterms = [0, 2, 4, 5, 6, 7]  # Minterms where the function is true

synthesizer = TruthTableSynthesizer(variables, minterms)
expression = synthesizer.synthesize()
print(f"Synthesized Boolean Expression: {expression}")

diagram = synthesizer.generate_logic_diagram(expression)
diagram.render('synthesized_logic_diagram', format='png', cleanup=True)
print("Logic gate diagram saved as 'synthesized_logic_diagram.png'")
'''


