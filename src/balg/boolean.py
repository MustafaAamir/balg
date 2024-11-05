from .synthesizer import TruthTableSynthesizer
from .expression  import BooleanExpression
from .generator   import BooleanExpressionGenerator
from typing import List

class Boolean:
    """
    Interface class for evaluating expressions and minterms
    """
    def expr_to_tt(self, input_expression: str) -> str:
        """
        Converts a boolean expression to a truth table

        Args:
            input_expression (str): boolean expression

        Returns:

        """
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
            simplified: str = self.expr_simplify(expression)
            exprObj = BooleanExpression(simplified)
            _ = exprObj.tt()
            minterms.append(exprObj.minterms)

        return all(minterms[0]==row for row in minterms)

    def expr_simplify(self, expr: str) -> str:
        expressionObj = BooleanExpression(expr)
        _ = expressionObj.tt()
        simplified_expr = self.tt_to_expr(expressionObj.variables, expressionObj.minterms)
        if len(expr.replace('(', '').replace(')', '')) > len(simplified_expr.replace('(', '').replace(')', '')):
            return simplified_expr
        else:
            return expr

    def generate_expression(self, max_identifiers: int = 5, nesting_depth: int=4) -> str:
        generatorObj = BooleanExpressionGenerator(max_identifiers, nesting_depth)
        return generatorObj.generate_expression()

    def generate_expressions(self, max_identifiers: int = 5, nesting_depth: int=4, count: int=1) -> List[str]:
        generatorObj = BooleanExpressionGenerator(nesting_depth, max_identifiers)
        return generatorObj.generate_expressions(count)

