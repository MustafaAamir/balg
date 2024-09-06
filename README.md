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

## 1. Boolean Expression Evaluator and Truth Table Generator

```shell
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
Afterwards, you'll get a prompt to produce a logic diagram
```shell
 (?) Would you like to generate a logic diagram for <expression>? (y/n)
```
After which it produces a png in the root directory

# Truth table to Boolean Expression and Logic Diagram
This section deals with how to convert a given truth table to a minimized boolean expression and generates a corresponding logic diagram using the [Quine-McCluskey algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm)

## Overview
1. Initialize variables and minterms
2. Generate prime implicants
3. Identify essential prime implicants
4. Minimize the boolean function
5. Synthesize the boolean expression
6. Generate the logic diagram (Optional)

## 1. Initialization

- The synthesizer is initialized with a list of character variables and [minterms](https://en.wikipedia.org/wiki/Canonical_normal_form#Minterm):
- [Minterms](https://en.wikipedia.org/wiki/Canonical_normal_form#Minterm) refer to values for which the output is 1.

- Let's generate the truth table for (~A ⋅ B) + (~A ⋅ \~C)
```
A | B | C | Output | minterm |
-----------------------------
0 | 0 | 0 |   1    |  000   |
0 | 0 | 1 |   0    |  ...   |
0 | 1 | 0 |   1    |  010   |
0 | 1 | 1 |   1    |  011   |
1 | 0 | 0 |   0    |  ...   |
1 | 0 | 1 |   0    |  ...   |
1 | 1 | 0 |   0    |  ...   |
1 | 1 | 1 |   0    |  ...   |
```

Here, the minterms are 0, 2, and 3

## 2. Generate Prime Implicants

[Prime implicants](https://en.wikipedia.org/wiki/Implicant) are found by repeatedly combining minterms that differ by only one variable:

```
Initial minterms:   000, 010, 100, 101, 110, 111
                      |    |    |    |    |    |
                      v    v    v    v    v    v
First combination:  -00, 01-, 10-, 11-, 1-0, 11-
                      |    |    |    |    |    |
                      v    v    v    v    v    v
Final implicants:   -00, 01-, 1--
```

#TODO
Add more to this

## 3. Identify Essential Prime Implicants

Essential prime implicants are those that are the only ones covering a particular minterm:

```
Minterm | Covered by
---------------------
  000   |    -00
  010   |    01-
  100   |    1--
  101   |    1--
  110   |    1--
  111   |    1--
```

In this case, `-00` and `01-` are essential prime implicants.

## 4. Minimize Boolean Function

Start with essential prime implicants and add others as needed to cover all minterms:

```
Essential:    -00, 01-
Added:        1--
```

## 5. Synthesize Boolean Expression

Convert each implicant to a term in the boolean expression:

```
-00 -> NOT C
01- -> B
1-- -> A
```

Combine terms with OR:

```
(NOT C) OR (B) OR (A)
```

Further simplification:

```
(NOT C) OR (B)
```

## 6. Generate Logic Diagram

The boolean expression is parsed and converted into a logic diagram:

```
   A    B    C
   |    |    |
   |    |    v
   |    |   NOT
   |    |    |
   |    v    |
   |    OR<--'
   |    |
   '---->OR
         |
         v
      Result
```


## Suggestions for Publishing

4. **Code Comments**: Ensure your code is well-commented, explaining complex algorithms and non-obvious decisions.

5. **Unit Tests**: Implement unit tests to verify the correctness of your functions and make it easier for others to contribute without breaking existing functionality.

6. **Example Scripts**: Provide example scripts that demonstrate how to use your toolkit for various scenarios.

7. **Requirements File**: Include a requirements.txt file listing all necessary Python packages.

8. **Version Control**: Use semantic versioning for releases to clearly communicate changes to users.

9. **Continuous Integration**: Set up CI/CD pipelines (e.g., GitHub Actions) to automatically run tests and lint your code on each push.

10. **Community Guidelines**: Create CONTRIBUTING.md and CODE_OF_CONDUCT.md files to set expectations for community interactions.

11. **Package Distribution**: Consider packaging your toolkit and distributing it via PyPI for easy installation.

12. **Interactive Demo**: Create a simple web interface or Jupyter notebook demonstrating the toolkit's capabilities.

By following these suggestions, you'll create a well-structured, documented, and accessible project that others can easily use, understand, and contribute to.
