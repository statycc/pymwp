# Choice.py

```python
from pymwp import Choices
```


Choice module generates a compact representation of analysis derivation result.

The Choice module allows determining valid derivation choices and analyzing available choices.
By default, the term _valid_ means derivations that do not fail, i.e., give $\infty$ in matrix; 
but other interpretations of valid choice can be defined also.

<h2>Determining valid derivation choices</h2>

Inputs:

* `index`: `int` degree of choice; total number of derivation choices in an analyzed program.               
* `domain`: `List[int]` possible inference choices at a program point, e.g. `[0,1,2]`.               
* `delta_sequences`: `Set[SEQ]` sequences of choices  _to negate_.

For example, to obtain derivation choices excluding failing derivations ($\infty$ in matrix),
the `delta_sequences` should be all sequences of deltas with scalar `i`.

The choice module converts the delta sequences to their negated choices,
in a compact regular expression-like format:

```{: .py3 .optional-language-as-class .no-copy}
# Input:
index = 3
domain = [0, 1, 2]
delta_sequences = {((0, 0), (2, 1)), ((1, 1),)}

# Output:
[[[1, 2], [0, 2], [0, 1, 2]], 
 [[0, 1, 2], [0], [0, 1, 2]]] 
```

A regular expression matching the output is `([1|2][0|2][0-2])|([0-2]0[0-2])`.

<h3>Steps</h3>

1. **Simplify**. Using $\delta$-sequences set, simplify it:

    1. Replace combinations that can be represented by a single shorter sequence.
    2. Remove supersets.
    3. Preemptively remove deltas that would lead to invalid choice vectors.

    Apply simplifications iteratively until convergence.

    !!! example "Simplifications"

        This example assumes domain = `[0,1,2]`.

        (A) All possible choices occur at index 0: any choice
        followed by sequence `(2,1)(1,2)` results in infinity.
        Therefore, remove $a, b, c$ and insert `[(2,1)(1,2)]` in their place.
        Choices are reduced similarly from both ends.

        ```{: .optional-language-as-class .no-copy}
        BEFORE                           AFTER
        [(0,0)(2,1)(1,2)]     # a        [(2,1)(1,2)]
        [(1,0)(2,1)(1,2)]     # b
        [(2,0)(2,1)(1,2)]     # c
        ```

        (B) Sequence $a$ is subset of $b$. Since $b$ cannot be selected
        without selecting $a$, discard $b$.

        ```{: .optional-language-as-class .no-copy}
        BEFORE                           AFTER
        [(0,0)]               # a        [(0,0)]
        [(0,0)(0,1)(2,2)]     # b
        ```
         
        (C) Constructing a choice vector requires selecting deltas from each
        remaining sequence $a, b, c$. Therefore, deltas `(0,0)` and `(1,0)` 
        must always be selected, and one of $c$, `[(2,0)(2,1)(1,2)]`. However, 
        selecting `(0,0)`, `(1,0)`, and `(2,0)` eliminates all choices at index 0. 
        This allows to reduce sequences $c$ to `(2,1)(1,2)`.

        ```{: .optional-language-as-class .no-copy}
        BEFORE                           AFTER
        [(0,0)]               # a        [(0,0)]
        [(1,0)]               # b        [(1,0)] 
        [(2,0)(2,1)(1,2)]     # c        [(2,1)(1,2)]
        ```


3. **Build choice vectors.** Initially consider all choices as valid.
   Then eliminate unwanted sequences, for all possible combinations.

    Compute cross product of remaining $\delta$-sequences.
    Iterate the product, for each:

    - Create a vector whose length is `index`.
    - Each vector element is a set of choices defined by `domain`.
    - Eliminate choices that lead to an unwanted outcome.

    Discard invalid and redundant vectors. Add remaining vectors to result.

    !!! example "Choice vector generation"

        ```{: .py3 .optional-language-as-class .no-copy}
        # remaining after simplification
        sequences = [[(0,0)], [(1,0)], [(2,1)(1,2)], [(2,0)(1,1)(1,2)]]
   
        # compute a cross product of sequences (6 total)
        choice_paths = [[(0,0) (1,0) (2,1) (2,0)],
                        [(0,0) (1,0) (2,1) (1,1)],
                        [(0,0) (1,0) (2,1) (1,2)],…]

        for each path:

            # initialize a vector with all choices at each index
            vector_init = [{0,1,2}, {0,1,2}, {0,1,2}]

            # eliminate path choices, and add to result:
            vector_final = [[2], [0], [0,1,2]] 
        ```

4. **Result.** The result is a disjunction of choice vectors.
    Choose one vector, then select one value at each vector index. 
    This yields a valid derivation result. For example, for a choice vector,

    ```{: .py3 .optional-language-as-class .no-copy}
    [[[2], [0],   [0,1,2]],
     [[1], [1,2], [0,1,2]]]  
    ```

    selecting $(1, 2, 2)$ is valid choice, so is $(2, 0, 2)$ and $(1, 1, 0)$, …etc.

    * If all choices are valid, the Choice vector has a single vector permitting all choices.
    * If no valid derivation exists, the result is empty choice: `[ ]`.
    * If `index=0`, i.e., no choice needs to be made, also result is empty `[ ]`.

---

::: pymwp.choice