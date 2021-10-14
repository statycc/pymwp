# Organization of the C source code examples

<!-- To reword, but that's the idea. -->

<!--start-->

## Basic Examples

The `basics` folder contains examples of simple C source code performing operations that corresponds to simple derivation trees.

| file | description |
| --- | --- |
`assign_expression.c` | assign result of binary operation to variable
`assign_variable.c` | assign using variable
`if.c` | assignment within conditional statement
`if_else.c` | conditional statement with `if` and `else`
`inline_variable.c` | local variable declaration
`while_1.c` | while loop with assignment
`while_2.c` | while loop with binary operation
`while_if.c` | while loop followed by `if...else`

## Implementation Examples

The `implementation_paper` folder contains examples from "_Implementing the mwp-flow analysis_" paper. <!-- TODO: add link -->

| file | description |
| --- | --- |
`example3.c` | An illustration of the sum of two choices.
`example5_a.c` | Examples with function call
`example5_b.c` | Example of an inlined function call


## Infinite Examples

The `infinite` folder contains examples of C source code that are assigned matrices that always contain infinite coefficients, no matter the choices.

| file | description |
| --- | --- |
`exponent_1.c` | exponential computation
`exponent_2.c` | alternative exponential computation
`infinite_2.c` | `while` loop with binary operations, 2 variables
`infinite_3.c` | `while` loop and `if` statement, 3 variables
`infinite_4.c` | `while` loop, 4 variables
`infinite_5.c` | `while` loop and `if` statement, 5 variables
`infinite_6.c` | `if...else` and `while` loop, 6 variables
`infinite_7.c` | 2 `while` loops and `if`, 7 variables
`infinite_8.c` | `while` with nested `if...else` and other conditionals, 8 variables

## Not Infinite Examples

The `not_infinite` folder contains examples of C source code that are assigned matrices that do not always contain infinite coefficients.

| file | description |
| --- | --- |
`notinfinite_2.c` | binary operations with 2 variables
`notinfinite_3.c` | `if` and `while` loop with 3 variables
`notinfinite_4.c` | `if` and `while` loop with 4 variables
`notinfinite_5.c` | `if` and `while` loop with 5 variables
`notinfinite_6.c` | `if...else` and `while` loop, 6 variables
`notinfinite_7.c` | 2 `while` loops and `if`, 7 variables
`notinfinite_8.c` | `while` with nested `if...else` and other conditionals, 8 variables

## Original Examples

The `original_paper` folder contains examples taken from or inspired from the ["_A Flow Calculus of mwp-Bounds for Complexity Analysis_"](https://doi.org/10.1145/1555746.1555752) paper.

| file | description |
| --- | --- |
`example3_1_a.c` | Analysis of two commands
`example3_1_b.c` | Analysis of two commands
`example3_1_c.c` | Binary operation inside `while` loop 
`example3_1_d.c` | Two variables and a `while` loop
`example3_2.c`  | Three variables and `while` loop
`example3_4.c` |  Iteration with 5 variables
`example5_1.c` | Adding two variables
`example7_10.c` | program with `if...else` and 3 variables
`example7_11.c` | Binary operations with 4 variables


## Other Examples

The `other` folder contains examples of C source code of interest.

| file | description |
| --- | --- |
`dense.c` | Produces a 3 x 3 dense matrix.
`dense_loop.c` | Produces a dense matrix with infinite coefficients in it.
`explosion.c` | Explosion of the number of cases
`for_loop.c` | Loop example using `for`
`simplified_dense.c` | Simplified dense matrix <!-- how is this different? -->

<!--end-->