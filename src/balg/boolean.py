from .synthesizer import TruthTableSynthesizer
from .expression  import BooleanExpression
from typing import List

class Boolean:
    def expr_to_tt(self, input_expression: str) -> str:
        expressionObject = BooleanExpression(input_expression)
        truthTable: str = expressionObject.tt()
        return truthTable

    def expr_to_dg(self, input_expression: str, filename: str | None = None,
                   directory: str | None = None, format: str = "png"):
        expressionObject = BooleanExpression(input_expression)
        diagram  = expressionObject.generate_logic_diagram()
        diagram.render(filename=filename, directory=directory,
                       format=format, cleanup=True)

    def tt_to_expr(self, variables: List[str], minterms: List[int]) -> str:
        synthesizerObject = TruthTableSynthesizer(variables, minterms)
        expression: str   = synthesizerObject.synthesize()
        return expression

    def tt_to_dg(self, variables: List[str], minterms: List[int],
                 filename: str | None = None, directory: str | None = None,
                 format: str = "png" ):
        expr = self.tt_to_expr(variables, minterms)
        self.expr_to_dg(expr, filename, directory, format)

