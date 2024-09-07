from synthesizer import TruthTableSynthesizer
from expression import BooleanExpression
import unittest
from random import randint

class TestTruthTableToExpression(unittest.TestCase):
    def testEdgeCases(self):
        variables = [chr(i) for i in range(65, 70)]
        minterms = [int(i, 2) for i in ['1', '101', '10101', '11101']]
        synthesizer = TruthTableSynthesizer(variables, minterms)
        expression  = synthesizer.synthesize()
        print(expression)

unittest.main()
