# Supported C-Language Features

This section provides a summary of supported C language features pymwp can
analyze. It also lists language features that are in the process of being
implemented and for which implementation is planned.

!!! info "Note on C file parsing"

    pymwp uses pycparser to process the C input file. Any limitation of
    pycparser is also a limitation in pymwp. From
    [pycparser website](https://github.com/eliben/pycparser):
    "pycparser aims to support the full C99 language (according to the
    standard ISO/IEC 9899). Some features from C11 are also supported."

BY default, analysis bypasses unsupported statements and raises a warning.

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
| while loop                                   |  🟩   | `while(x < 20) { ... }`                     |
| for loop[^2]                                 |  🟩   | `for (i = 0; i < x; ++i) { ... }`           |
| **Jump statements**  (excl. `goto`)          |  🟩   | `break`, `continue`, `return x`             |
| **Functions**                                |  🟧   | `foo(arg1, arg2)`                           |     
| **Pointers** (`*`, `&` address-of)           |   ⬜   |                                             |     
| **Arrays**                                   |   ⬜   |                                             |      
| **Header files inclusion**                   |  🟩   | `#include <stdio.h>`                        |      
| **Comments** (single-line, delimited)        |  🟩   | `// comment`, `/* comment */`               |
| **assume and assert macros**                 |  🟩   | `assert (x == y)`                           |

 
[^1]: Binary operands must be variables or constants.
[^2]: Loop must be recognizable as "run `X` times" and guard variable `X` cannot occur in body.
 