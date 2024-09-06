from colorama import Fore, init, Style
import sys
from synthesizer import TruthTableSynthesizer
from expression import BooleanExpression
import argparse

def expression_to_tt_and_diagram(diagram_print: bool):
    input_expression = input(f"{Fore.GREEN} $ {Style.RESET_ALL}Enter expression: ")
    expr = BooleanExpression(input_expression)
    print(f"{expr.print_truth_table()}")
    if (diagram_print):
        print(f"{Fore.MAGENTA} $ {Style.RESET_ALL}Generating logic diagram...")
        diagram = expr.generate_logic_diagram()
        diagram.render("logic_diagram", format='png', cleanup=True)
        print(f"{Fore.GREEN} $ {Style.RESET_ALL}Logic gate diagram saved as 'logic_diagram.png'")

def tt_to_expression_and_diagram(print_diagram: bool):
    variables = input(f"{Fore.GREEN} $ {Style.RESET_ALL}Enter variables (comma-separated): ").split(',')
    minterms = input(f"{Fore.GREEN} $ {Style.RESET_ALL}Enter minterms (comma-separated): ").replace(' ', '').split(',')
    minterms = [int(i, 2) for i in minterms]
    synthesizer = TruthTableSynthesizer(variables, minterms)
    expression = synthesizer.synthesize()
    print(f" > Generated Boolean Expression: {expression}")
    if (print_diagram):
        print(f"{Fore.MAGENTA} $ Generating logic diagram from truth table...{Style.RESET_ALL}")
        expr = BooleanExpression(expression)
        diagram = expr.generate_logic_diagram()
        diagram.render('synthesized_logic_diagram', format='png', cleanup=True)
        print(f"{Fore.GREEN} $ {Style.RESET_ALL}Logic gate diagram saved as 'synthesized_logic_diagram.png'")

def main():
    init(autoreset=True)
    parser = argparse.ArgumentParser(
        description='Logic Gate Expression and Truth Table Processor',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('mode', choices=['Expression', 'TruthTable'],
                        help='Mode of operation:\n'
                             'Expression: Parse and evaluate logic expressions\n'
                             'TruthTable: Generate expressions from truth tables')
    parser.add_argument('-d', '--diagram', action='store_true',
                        help='Generate a logic diagram')

    args = parser.parse_args()

    print(f"{Fore.CYAN}    Boolean Algebra Toolkit\n{Style.RESET_ALL}")

    if args.mode == "Expression":
        expression_to_tt_and_diagram(args.diagram)

    if args.mode == "TruthTable":
        tt_to_expression_and_diagram(args.diagram)

if __name__ == "__main__":
    main()

