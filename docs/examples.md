# Examples

pymwp analyzes programs written in C language.
The project repository `c_files` directory contains many examples.

### Program Categories

!!! info " "

    : :material-hand-wave-outline: &nbsp; **Basics**<br/>Programs performing operations that correspond to simple derivation trees.
    
    : :material-infinity: &nbsp; **Infinite**<br/>Programs that are assigned matrices that always contain infinite coefficients, no matter the choices.
    
    : :octicons-move-to-end-24: &nbsp; **Not Infinite**<br/>Programs that are assigned matrices that do not always contain infinite coefficients.
    
    : :material-circle-outline: &nbsp; **Original Paper**<br/>Examples taken from or inspired by paper "A Flow Calculus of mwp-Bounds for Complexity Analysis"[&nearr;](https://doi.org/10.1145/1555746.1555752).
    
    : :material-asterisk: &nbsp; **Implementation Paper**<br/>Examples from "mwp-Analysis Improvement and Implementation: Realizing Implicit Computational Complexity"[&nearr;](https://doi.org/10.4230/LIPIcs.FSCD.2022.26).

    : :material-language-python: &nbsp; **Tool paper**<br/>Examples from "pymwp: A Static Analyzer Determining Polynomial Growth Bounds"[&nearr;](https://doi.org/10.1007/978-3-031-45332-8_14).
    
    : :material-dots-horizontal: &nbsp; **Other**<br/>Other programs of interest.

<h3>Demo</h3>

Try the demo to analyze these programs online.

[Go to Demo](demo.md){ .md-button .md-button--primary }

{%
   include-markdown "../c_files/readme.md"
   heading-offset=1
   start="<!--start-->"
   end="<!--end-->"
%}