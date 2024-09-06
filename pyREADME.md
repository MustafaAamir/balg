# Truth Table to Boolean Expression and Logic Diagram Generator

This document explains the workings of our Truth Table Synthesizer, which converts a given truth table into a minimized boolean expression and generates a corresponding logic diagram.

## Overview

The process can be broken down into several key steps:

1. Initialize with variables and minterms
2. Generate prime implicants
3. Identify essential prime implicants
4. Minimize the boolean function
5. Synthesize the boolean expression
6. Generate the logic diagram

Let's dive into each step in detail.

## 1. Initialization

The synthesizer is initialized with a list of variables and minterms:

```
variables = ['A', 'B', 'C']
minterms = [0, 2, 4, 5, 6, 7]
```

This represents a truth table like this:

```
A | B | C | Output
------------------
0 | 0 | 0 |   1
0 | 0 | 1 |   0
0 | 1 | 0 |   1
0 | 1 | 1 |   1
1 | 0 | 0 |   1
1 | 0 | 1 |   1
1 | 1 | 0 |   1
1 | 1 | 1 |   1
```

## 2. Generate Prime Implicants

Prime implicants are found by repeatedly combining minterms that differ by only one variable:

```
Initial minterms:   000, 010, 100, 101, 110, 111
                      |    |    |    |    |    |
                      v    v    v    v    v    v
First combination:  -00, 01-, 10-, 11-, 1-0, 11-
                      |    |    |    |    |    |
                      v    v    v    v    v    v
Final implicants:   -00, 01-, 1--
```

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

We start with essential prime implicants and add others as needed to cover all minterms:

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

This diagram represents the minimized boolean function derived from the original truth table.

By following these steps, our Truth Table Synthesizer efficiently converts a given truth table into a minimized boolean expression and generates a corresponding logic diagram, providing a clear visual representation of the logic function.
