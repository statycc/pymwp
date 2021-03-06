# Organization of the C source code examples

<!-- To reword, but that's the idea. -->

<!--start-->

|||
| --- | --- |
| **Basics** | Simple C programs performing operations that corresponds to simple derivation trees. |
| `assign_expression.c` | assign result of binary operation to variable
| `assign_variable.c` | assign using variable
| `if.c` | assignment within conditional statement
| `if_else.c` | conditional statement with `if` and `else`
| `inline_variable.c` | local variable declaration
| `while_1.c` | while loop with assignment
| `while_2.c` | while loop with binary operation
| `while_if.c` | while loop followed by `if...else`

|||
| --- | --- |
| **Implementation Paper** | Examples from "mwp-Analysis Improvement and Implementation: Realizing Implicit Computational Complexity" paper. | 
| `example7.c` | An illustration of the sum of two choices.
| `example15_a.c` | Examples with function call
| `example15_b.c` | Example of an inlined function call

|||
| --- | --- |
| **Infinite** | Programs that are assigned matrices that always contain infinite coefficients, no matter the choices. |
| `exponent_1.c` | exponential computation |
| `exponent_2.c` | alternative exponential computation |
| `infinite_2.c` | `while` loop with binary operations |
| `infinite_3.c` | `while` loop and `if` statement |
| `infinite_4.c` | `while` loop |
| `infinite_5.c` | `while` loop and `if` statement |
| `infinite_6.c` | `if...else` and `while` loop |
| `infinite_7.c` | 2 `while` loops and `if` |
| `infinite_8.c` | `while` with nested `if...else` and other conditionals |

|||
| --- | --- |
| **Not Infinite** |  Programs that are assigned matrices that do not always contain infinite coefficients. |
| `notinfinite_2.c` | binary operations |
| `notinfinite_3.c` | `if` and `while` loop | 
| `notinfinite_4.c` | `if` and `while` loop | 
| `notinfinite_5.c` | `if` and `while` loop | 
| `notinfinite_6.c` | `if...else` and `while` loop |
| `notinfinite_7.c` | 2 `while` loops and `if` |
| `notinfinite_8.c` | `while` with nested `if...else` and other conditionals |

|||
| --- | --- |
| **Original Paper** | Examples taken from or inspired from the ["A Flow Calculus of mwp-Bounds for Complexity Analysis"](https://doi.org/10.1145/1555746.1555752) paper. |
| `example3_1_a.c` | Analysis of two commands
| `example3_1_b.c` | Analysis of two commands
| `example3_1_c.c` | Binary operation inside `while` loop 
| `example3_1_d.c` | Two variables and a `while` loop
| `example3_2.c`  | Three variables and `while` loop
| `example3_4.c` |  Iteration with 5 variables
| `example5_1.c` | Adding two variables
| `example7_10.c` | program with `if...else` and 3 variables
| `example7_11.c` | Binary operations with 4 variables

|||
| --- | --- |
| **Other** | Other programs of interest. |
| `dense.c` | Produces a 3 x 3 dense matrix.
| `dense_loop.c` | Produces a dense matrix with infinite coefficients in it.
| `explosion.c` | Explosion of the number of cases
| `for_loop.c` | Loop example using `for`
| `gcd.c` | Greatest common divisor by subtraction
| `simplified_dense.c` | Simplified dense matrix |
<!--end-->