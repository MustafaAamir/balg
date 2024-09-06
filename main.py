from colorama import Fore
import sys
from synthesizer import TruthTableSynthesizer
from expression  import BooleanExpression


def expression_to_tt_and_diagram():
    input_expression = input(" $ ")
    expr = BooleanExpression(input_expression)
    expr.print_truth_table()
    print_diagram_a = input(Fore.BLUE + " (?) produce diagram? (y/n) " + Fore.WHITE)
    if (print_diagram_a.lower() == "y"):
        diagram = expr.generate_logic_diagram()
        diagram.render(f"logic_diagram")

def tt_to_expression_and_diagram():
    variables = input("Enter variables: ").split()
    looping = True
    minterms = []
    while (looping):
        minterm = input("Enter binary value for which output is 1, q to exit: ")
        if (minterm == "q"):
            break
        else:
            if (int(minterm, 2) > 2**len(variables)):
                print("Value is higher than 2 power {}", len(variables))
            else:
                minterms.append(int(minterm, 2))

    synthesizer = TruthTableSynthesizer(variables, minterms)
    expression = synthesizer.synthesize()
    print(f"Synthesized Boolean Expression: {expression}")

    print_diagram_a = input(Fore.BLUE + " (?) produce diagram? (y/n) " + Fore.WHITE)
    if (print_diagram_a.lower() == "y"):
        diagram = synthesizer.generate_logic_diagram(expression)
        diagram.render('synthesized_logic_diagram', format='png', cleanup=True)
        print("Logic gate diagram saved as 'synthesized_logic_diagram.png'")

def print_help():
    print("""
          usage:

          """)

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        if (sys.argv[1] == "expr"):
            expression_to_tt_and_diagram()
        elif (sys.argv[1] == "tt"):
            tt_to_expression_and_diagram()
    else:
        print_help()


