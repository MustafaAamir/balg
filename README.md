# Boolean Algebra Toolkit

1. Boolean Expression Evaluator and Truth Table Generator
2. Truth Table to Boolean Expression and Logic Diagram Generator

# Installation

```bash
git clone https://www.github.com/MustafaAamir/logic-simulator \
cd logic-simulator \
pip install -r requirements.txt \
python main.py --help
```

# 1. Boolean Expression Evaluator and Truth Table Generator

```
$ python main.py expression
 > Enter an expression: <expression>
 <expression truth table>
    A | B | C | Output
    ------------------
    0 | 0 | 0 |   1
    0 | 0 | 1 |   0
    0 | 1 | 0 |   1
    0 | 1 | 1 |   0
    1 | 0 | 0 |   1
    1 | 0 | 1 |   0
    1 | 1 | 0 |   1
    1 | 1 | 1 |   1
```
Afterwards, the user gets a prompt to produce a logic diagram
```
 $ Would you like to generate a logic diagram for <expression>? (y/n)
```
After which it produces a png in the root directory

# 2. Truth table to Boolean Expression and Logic Diagram
This section deals with converting a given truth table to a minimized boolean expression using the [Quine-McCluskey algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm) and producing a logic diagram.

## Overview
1. Initialize variables and [Minterms](https://en.wikipedia.org/wiki/Canonical_normal_form#Minterm)
2. Generate prime implicants
3. Identify essential [Prime implicants](https://en.wikipedia.org/wiki/Implicant)
4. Minimize the boolean function
5. Synthesize the boolean expression
6. Generate the logic diagram (Optional)

## 1. Initialization

- The synthesizer is initialized with a list of character variables and [minterms](https://en.wikipedia.org/wiki/Canonical_normal_form#Minterm):
- [Minterms](https://en.wikipedia.org/wiki/Canonical_normal_form#Minterm) refer to values for which the output is 1.
-  [Prime implicants](https://en.wikipedia.org/wiki/Implicant) are found by repeatedly combining minterms that differ by only one variable:

```
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

if the `-d` or `--diagram` flag is set, the boolean expression is parsed and converted into a logic diagram:

