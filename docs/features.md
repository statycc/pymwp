# Supported C Language Features

The table below summarizes the supported C language features pymwp can analyze.  

!!! info "Note on C file parsing"

    pymwp uses pycparser to process the C input file. Any limitation of
    pycparser is also a limitation in pymwp. From
    [pycparser website](https://github.com/eliben/pycparser):
    "pycparser aims to support the full C99 language (according to the
    standard ISO/IEC 9899). Some features from C11 are also supported."

**What happens if the C program contains unsupported syntax?** 

- By default, the analysis skips unsupported _statements_ and raises a warning.
- In strict mode (`--strict`), analysis skips whole constructs (_"programs"_) that contain unsupported syntax. 

The strict mode is sound, but not very informative in case of an unsupported program.
The default handling is more useful for developing the analysis.

**Legend**

:  🟩 &nbsp; ready — fully implemented and ready to use
:  🟧 &nbsp; in progress — implementation in progress, but not ready
:  ⬜ &nbsp; planned — implementation is in a planning stage

| Description                                  | State | Example                                     |
|----------------------------------------------|:-----:|---------------------------------------------|
| **Basic data types**                         |       |                                             |
| Integer types (incl. `signed`, `unsigned`)   |  🟩   | `char`, `short`, `int`, `long`, `long long` |
| Floating point types                         |  🟩   | `float`, `double`, `long double`            |
| **Declarations**                             |       |                                             |     
| Variable declarations                        |  🟩   | `int x;`                                    |
| Constant declarations                        |  🟩   | `const int x;`                              |
| **Assignment**                               |  🟩   | `x = y`                                     |
| Compound assignment                          |   ⬜   | `x += 1`                                    |
| **Arithmetic operations**                    |       |                                             |
| Unary operations ($+, -, ++,--,!$, `sizeof`) |  🟩   | `++x`, `x--`, `sizeof(x)`                   |
| Binary operations ($+, \times, -$)[^1]       |  🟩   | `x = y + z`                                 |
| N-ary/nested operation                       |   ⬜   | `y + (++z) * w`                             |
| **Casting** (limited support)                |  🟧   | `x = (int)x`                                |   
| **Conditional statements**                   |       |                                             |
| if statement                                 |  🟩   | `if(x > 0) { ... }`                         |
| if-else statement                            |  🟩   | `if(x > 0) { ... } else { ... }`            |
| Nested conditional                           |  🟩   | `if(x > 0) { if (y > 0) { ... } }`          |
| **Repetition statements**                    |       |                                             |
| `while` loop[^2]                             |  🟩   | `while(x < 20) { ... }`                     |
| `for` loop[^2]                               |  🟩   | `for (i = 0; i < x; ++i) { ... }`           |
| **Jump statements**  (excl. `goto`)          |  🟩   | `break`, `continue`, `return x`             |
| **Functions**                                |  🟧   | `foo(arg1, arg2)`                           |     
| **Pointers** (`*`, `&` address-of)           |   ⬜   |                                             |     
| **Arrays**                                   |   ⬜   |                                             |      
| **Header files inclusion**                   |  🟩   | `#include <stdio.h>`                        |      
| **Comments** (single-line, delimited)        |  🟩   | `// comment`, `/* comment */`               |
| **assume and assert macros**                 |  🟩   | `assert (x == y)`                           |

 
[^1]: Binary operands must be variables or constants.
[^2]: Loop handling is very important in the mwp calculus. 
      A C language looping construct converts to a bounded or unbounded loop.
      A bounded loop must have form "run `X` times" and the guard variable `X` cannot occur in body.
 