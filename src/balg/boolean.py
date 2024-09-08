from .synthesizer import TruthTableSynthesizer
from .expression  import BooleanExpression
from typing import List

class Boolean:
    def expr_to_tt(self, input_expression: str) -> str:
        expressionObject = BooleanExpression(input_expression)
        truthTable: str = expressionObject.fmt_tt()
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
    def expr_cmp(self, expressions: List[str]) -> bool:
        minterms: List[List[int]] = []
        for expression in expressions:
            exprObj = BooleanExpression(expression)
            _ = exprObj.tt()
            minterms.append(exprObj.minterms)

        return all(minterms[0]==row for row in minterms)

    def expr_simplify(self, expr: str) -> str:
        expressionObj = BooleanExpression(expr)
        _ = expressionObj.tt()
        return self.tt_to_expr(expressionObj.variables, expressionObj.minterms)
