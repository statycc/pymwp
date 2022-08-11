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
  
**Legend**

- ✅ &nbsp; **ready** - fully implemented and ready to use
- 🟧 &nbsp; **in progress** - implementation is in progress but not ready
- ⬜ &nbsp; **planned** - implementation is in a planning stage

| Description                                | State | Example                                     |
|--------------------------------------------|:-----:|---------------------------------------------|
| **Basic data types**                       |       |                                             |
| Integer types (incl. `signed`, `unsigned`) |   ✅   | `char`, `short`, `int`, `long`, `long long` |
| Floating point types                       |   ✅   | `float`, `double`, `long double`            |
| **Declarations**                           |       |                                             |     
| Variable declarations                      |   ✅   | `int x;`                                    |
| Constant declarations                      |   ✅   | `const int x;`                              |
| **Arithmetic operations**                  |       | 
| Unary operations                           |  🟧   | `-x`, `--x`, `x++`, ...                     |
| Binary operations ($+, \times, -$)         |   ✅   | `x = y + z`                                 |
| $n$-ary operation                          |  🟧   | `x = y + z * w`                             |
| Compound assignment operators              |   ⬜   | `x += 1`                                    |
| **Conditional statements**                 |       |                                             |
| if statement                               |   ✅   | `if(x > 0) { ... }`                         |
| if-else statement                          |   ✅   | `if(x > 0) { ... } else { ... }`            |
| nested conditional                         |   ✅   | `if(x > 0) {  if (y > 0) { ... } }`         |
| **Repetition statements**                  |       |                                             |
| while loop                                 |   ✅   | `while(x < 20) { ... }`                     |
| for loop                                   |  🟧   | `for (i = 0; i < 10; ++i) { ... }`          |
| **Functions**                              |  🟧   |                                             |     
| **Pointers**                               |   ⬜   |                                             |     
| **Arrays**                                 |   ⬜   |                                             |      
| **Header Files Inclusion** \*              |   ✅   |                                             |      
| **Comments**                               |       |                                             |
| Single-line                                |   ✅   | `// comment`                                |
| Multi-line                                 |   ✅   | `/* comment */`                             |

\*) version > 0.1.6

### Handling of unsupported operations

Analysis will bypass any statement that is unsupported and raises a warning.
