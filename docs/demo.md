This demo allows running pymwp analysis on these **[examples](examples.md)** 
on the web. 

#### How to interpret the output

There will be 3 outputs:

1. **program** - the exact C language program that was analyzed
2. **matrix** - the final matrix computed by pymwp analysis
3. **evaluation** 
    - list of choices that stay within polynomial bounds <!-- ? -->
    - when no such choices exist, evaluation says "infinite"


{%
   include-markdown "assets/demo.html"
%}