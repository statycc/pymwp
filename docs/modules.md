# Modules Index

pymwp is built from modules; each with a specific role.
For example, `Analysis` is the top-level handler for running program analysis,
`matrix` contains matrix-utilities, and the elements stored in matrices are of type `Polynomial`, etc.
This "modules" documentation section explains the internal behaviors of these building blocks,
which is relevant for using pymwp imported in scripts.

## Scripting Examples

### Extend or reuse analysis output

Run pymwp analysis on a program file, then reuse the analysis result in further computation.
An analysis run returns a [`Result`](result.md#pymwp.result.Result) object.
Calling [`get_func()`](result.md#pymwp.result.Result.get_func) then accesses the analysis result of a specific function.

=== "Python script"

    ``` python
    from pymwp import Analysis, Parser
    from pprint import pprint
    
    # path to file to analyze
    file = 'c_files/basics/if.c'
    
    # parses a C-langugage file using pycparser
    ast = Parser.parse(file, use_cpp=True, cpp_path='gcc')
    
    # run analysis, then access result for main function
    result = Analysis.run(ast, fin=True, no_save=True).get_func('main')
    
    # display analysis result and collected data
    pprint(result.to_dict())
    ```

=== "Input program [if.c]"

    ``` c
    // contents of if.c
    int main(int x, int y){
        if (0) {y = x;}
    }
    ```

=== "Terminal output"

    ``` txt
    {'bound': {'x': 'x;;', 'y': 'x,y;;'},
    'choices': [[[0, 1, 2]]],
    'end_time': 1725498245384529000,
    'index': 1,
    'inf_flows': None,
    'infinity': False,
    'name': 'foo',
    'relation': {'matrix': [[[{'deltas': [], 'scalar': 'm'}],
                             [{'deltas': [], 'scalar': 'm'}]],
                            [[{'deltas': [], 'scalar': 'o'}],
                             [{'deltas': [], 'scalar': 'm'}]]]},
    'start_time': 1725498245383927000,
    'variables': ['x', 'y']}
    ```

### Build with analysis modules

Working directly with the internal modules allows customizing the analysis behavior and building related analyses.

=== "Python script"

    ```python
    from pymwp import Polynomial, Monomial
    from pymwp.matrix import identity_matrix, show
    
    matrix = identity_matrix(3)
    matrix[0][1] = Polynomial('m')
    matrix[1][1] = Polynomial('w')
    matrix[2][1] = Polynomial(Monomial('p', (0, 0), (1, 1)))
    
    show(matrix)
    ```

=== "Terminal output"

    ``` txt
    [' +m', ' +m', ' +o']
    [' +o', ' +w', ' +o']
    [' +o', ' +p.delta(0,0).delta(1,1)', ' +m']
    ```
