# Organization of the C source code examples

<!--start-->

## List of Examples

| Category             | Program               | Description                                               |
|----------------------|-----------------------|-----------------------------------------------------------|
| Basics               | `assign_expression.c` | assign result of binary operation to variable             |
|                      | `assign_variable.c`   | assign using variable                                     |
|                      | `if.c`                | assignment within conditional statement                   |
|                      | `if_else.c`           | conditional statement with `if` and `else`                |
|                      | `inline_variable.c`   | local variable declaration                                |
|                      | `while_1.c`           | while loop with assignment                                |
|                      | `while_2.c`           | while loop with binary operation                          |
|                      | `while_3.c`           | non-infinite while loop with three variables              |
|                      | `while_if.c`          | while loop followed by `if...else`                        |
| Implementation Paper | `example8.c`          | An illustration of the sum of two choices.                |
|                      | `example14.c`         | Examples with function call                               |
|                      | `example16.c`         | Example of an inlined function call                       |
| Infinite             | `exponent_1.c`        | exponential computation                                   |
|                      | `exponent_2.c`        | alternative exponential computation                       |
|                      | `infinite_2.c`        | `while` loop with binary operations                       |
|                      | `infinite_3.c`        | `while` loop and `if` statement                           |
|                      | `infinite_4.c`        | `while` loop                                              |
|                      | `infinite_5.c`        | `while` loop and `if` statement                           |
|                      | `infinite_6.c`        | `if...else` and `while` loop                              |
|                      | `infinite_7.c`        | 2 `while` loops and `if`                                  |
|                      | `infinite_8.c`        | `while` with nested `if...else` and other conditionals    |
| Not Infinite         | `notinfinite_2.c`     | binary operations                                         |
|                      | `notinfinite_3.c`     | `if` and `while` loop                                     | 
|                      | `notinfinite_4.c`     | `if` and `while` loop                                     | 
|                      | `notinfinite_5.c`     | `if` and `while` loop                                     | 
|                      | `notinfinite_6.c`     | `if...else` and `while` loop                              |
|                      | `notinfinite_7.c`     | 2 `while` loops and `if`                                  |
|                      | `notinfinite_8.c`     | `while` with nested `if...else` and other conditionals    |
| Original Paper       | `example3_1_a.c`      | Analysis of two commands                                  |
|                      | `example3_1_b.c`      | Analysis of two commands                                  |
|                      | `example3_1_c.c`      | Binary operation inside `while` loop                      |
|                      | `example3_1_d.c`      | Two variables and a `while` loop                          |
|                      | `example3_2.c`        | Three variables and `while` loop                          |
|                      | `example3_4.c`        | Iteration with 5 variables                                |
|                      | `example5_1.c`        | Adding two variables                                      |
|                      | `example7_10.c`       | program with `if...else` and 3 variables                  |
|                      | `example7_11.c`       | Binary operations with 4 variables                        |
| Other                | `dense.c`             | Produces a 3 x 3 dense matrix.                            |
|                      | `dense_loop.c`        | Produces a dense matrix with infinite coefficients in it. |
|                      | `explosion.c`         | Explosion of the number of cases                          |
|                      | `gcd.c`               | Greatest common divisor by subtraction                    |
|                      | `long.c`              | Longer program with multiple loops and nested statements  |
|                      | `simplified_dense.c`  | Simplified dense matrix                                   |
|                      | `xnu.c`               | SPEC CPU2006	hmmer/src/masks.c XNU function               |
| Tool paper[^2]       | `tool_ex_1.c`         | Sect 1. Example 1 from pymwp tool paper                   |
|                      | `tool_ex_2.c`         | Sect 2.2 Example 2 from pymwp tool paper                  |
|                      | `tool_ex_3.c`         | Sect 2.2 Example 3 from pymwp tool paper                  |
|                      | `t19.c_c4b`           | Table 1: t19.c from Carbonneaux et al. 2015[^1]           |
|                      | `t20.c_c4b`           | Table 1: t20.c from Carbonneaux et al. 2015[^1]           |
|                      | `t47.c_c4b`           | Table 1: t47.c from Carbonneaux et al. 2015[^1]           |

[^1]: Syntax of these examples is adjusted to semantically equivalent statements supported by pymwp, e.g., unary `x++` must be expressed as `x = x + 1`.
[^2]: Sect 4.2 Example 4 is `infinite/infinite_3.c`

<!--end-->
