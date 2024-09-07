# Boolean Algebra Toolkit

- Truth Table to Boolean Expression and Logic Diagram Generator
- Boolean Expression Evaluator and Truth Table Generator

# Installation

```bash
git clone https://www.github.com/MustafaAamir/BooleanAlgebraToolkit \
cd BooleanAlgebraToolkit \
pip install -r requirements.txt \
```

# Usage

```python
from boolean import Boolean
booleanObject = Boolean()
```
1. To generate an expression's truth table:

```python
input_expression: str = "~(A & B & C)+(A & B)+(B & C)"
tt: str = booleanObject.expr_to_tt(input_expression)
```

2. To generate an expression given the minterms and variables:

```python
variables: List[str] = ['A', 'B', 'C']
minterms: List[int]  = [0, 1, 3, 7]
expression: str   = booleanObject.tt_to_expr(variables, minterms)
```

3. To generate a logic diagram given an expression:

```python
input_expression: str = "~(A & B & C)+(A & B)+(B & C)"
file_name: str = "logic_diagram12"
format: str = "png"
directory: str = "examples" # stores in the current directory by default
booleanObject.expr_to_dg(input_expression, file_name, directory, format)
```

4. To generate a logic diagram given variables and minterms

```python
variables: List[str] = ['A', 'B', 'C']
minterms: List[int]  = [0, 1, 3, 7]
file_name: str = "logic_diagram12"
directory: str = "examples"
format: str = "png"
booleanObject.tt_to_dg(variables, minterms, file_name, directory, format)
```

# Example Diagrams

![logic_diagram](https://github.com/user-attachments/assets/5142ee73-0c51-4bcd-9730-0a33129cf72f)

![logic_diagram](https://github.com/user-attachments/assets/ae681531-7076-445b-be9f-41bf98dff005)

Other diagrams can be found in `examples/`

# Explanation of the Quine-McCluskey Algorithm
This section deals with converting a given truth table to a minimized boolean expression using the [Quine-McCluskey algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm) and producing a logic diagram.

## Overview
1. Initialize variables & [Minterms](https://en.wikipedia.org/wiki/Canonical_normal_form#Minterm)
2. Identify essential [Prime implicants](https://en.wikipedia.org/wiki/Implicant)
3. Minimize & Synthesize the boolean function

### Initialization

- The synthesizer is initialized with a list of character variables and [minterms](https://en.wikipedia.org/wiki/Canonical_normal_form#Minterm):
- [Minterms](https://en.wikipedia.org/wiki/Canonical_normal_form#Minterm) refer to values for which the output is 1.
-  [Prime implicants](https://en.wikipedia.org/wiki/Implicant) are found by repeatedly combining minterms that differ by only one variable:

### The Quine-McCluskey Algorithm

```

               The Quine-McCluskey Algorithm

+-----------------------------------+
| initialize variables and minterms |
| variables := [A, B, C]            |
| minterms  := [0, 3, 6, 7]         |
| minters   := [000, 011, 110, 111] |
+-----------------------------------+
                |
                /
               /
               |
               V
        +-----------------------+
        | find prime_implicants |
        | | A | B | C |  out |  |
        | |---|---|---|------|  |
        | | 0 | 0 | 0 |  1   |  |
        | | 0 | 0 | 1 |  0   |  |
        | | 0 | 1 | 0 |  0   |  |
        | | 0 | 1 | 1 |  1   |  |
        | | 1 | 0 | 0 |  0   |  |
        | | 1 | 0 | 1 |  0   |  |
        | | 1 | 1 | 0 |  1   |  |
        | | 1 | 1 | 1 |  1   |  |
        +-----------------------+
                 |
                 |
                  \
                   |
                   V
+----------------------------------+
|  | group | minterm | A | B | C | |
|  |-------|---------|---|---|---| |
|  |   0   | m[0]    | 0 | 0 | 0 | |
|  |   2   | m[1]    | 0 | 1 | 1 | |
|  |       | m[2]    | 1 | 1 | 0 | |
|  |   3   | m[3]    | 1 | 1 | 1 | |
|  |-------|---------|---|---|---| |
+----------------------------------+
                    \
                     \
                      |
                      V
        +-------------------------------------------+
        | find pair where only one variable differs |
        | | group | minterm    | A | B | C |  expr  |
        | |-------|------------|---|---|---|--------|
        | |   0   | m[0]       | 0 | 0 | 0 | ~(ABC) |
        | |   2   | m[1]-m[3]  | _ | 1 | 1 |  BC    |
        | |       | m[2]-m[3]  | 1 | 1 | _ |  AB    |
        +-------------------------------------------+
                        |
                       /
                      |
                      V
    +-------------------------------------------+
    |  since the bit-diff between pairs in each |
    |  class is > 1, we move onto the next step |
    |                                           |
    |   |  expr  | m0  | m1  | m2  | m3   |     |
    |   |--------|-----|-----|-----|------|     |
    |   | ~(ABC) | X   |     |     |      |     |
    |   |   BC   |     |  X  |     |      |     |
    |   |   AB   |     |     |  X  |      |     |
    |   |--------|-----|-----|-----|------|     |
    +-------------------------------------------+
                            |
                            |
                           /
                          |
                          V
              +-----------------------------------------+
              | If each column contains one element     |
              | the expression can't be eliminated.     |
              | Therefore, the resulting expression is: |
              |         ~(ABC) + BC + AB                |
              +-----------------------------------------+



```

# Documentation (for developers)

``` python
class TruthTableSynthesizer(variables: List[str], minterms: List[int])
```
```python
class BooleanExpression(expression: str)
```
```python
class Boolean()
```

```python
TruthTableSynthesizer.decimal_to_binary(num: int) -> str
TruthTableSynthesizer.combine_implicants(implicants: List[Set[str]]) -> Set[str]
TruthTableSynthesizer.get_prime_implicants() -> Set[str]
TruthTableSynthesizer.covers_minterm(implicant: str, minterm: str) -> bool
TruthTableSynthesizer.get_essential_prime_implicants(prime_implicants: Set[str]) -> Set[str]
TruthTableSynthesizer.minimize_function(prime_implicants: Set[str], essential_implicants: Set[str]) -> List[str]
TruthTableSynthesizer.implicant_to_expression(implicant: str) -> str
TruthTableSynthesizer.synthesize() -> str

BooleanExpression.to_postfix(inifx: str) -> List[str]
BooleanExpression.evaluate(values: Dict[str, bool]) -> bool
BooleanExpression.truth_table() -> List[Tuple[Dict[str, bool], bool]]
BooleanExpression.tt() -> str
BooleanExpression.generate_logic_diagram() -> graphviz.Digraph

Boolean.expr_to_tt(input_expression: str) -> str
Boolean.tt_to_expr(variables: List[str], minterms: List[int]) -> str
Boolean.tt_to_dg(variables: List[str], minterms: List[int], file: str | None = None, directory: str | None = None, format: str = "png") -> str
Boolean.expr_to_dg(input_expression: str, file: str | None = None, directory: str | None = None, format: str = "png") -> str
```

