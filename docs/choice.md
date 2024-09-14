# Choice.py

```python
from pymwp import Choices
```

<h2>Determining valid derivation choices</h2>

Choice module generates a compact representation of analysis derivation result.

<h3>Inputs</h3>

*  `index`: `int` degree (total number) of choices in an analyzed program.               
* `choices`: `List[int]` possible inference choices at a program point, e.g. `[0,1,2]`.               
* `delta_sequences`: `Set[SEQ]` sequences of choices  _to negate_.

For example, to obtain derivation choices excluding failing derivations ($\infty$ from matrix),
the `delta_sequences` should be all sequences of deltas with scalar `i`.

The choice module converts the delta sequences to their negated choices,
in a compact regular expression-like format:

```Python
# Input:
index, choices = 3, [0, 1, 2]
delta_sequences = {((0, 0), (2, 1)), ((1, 1),)}

# Output:
[[[1, 2], [0, 2], [0, 1, 2]], 
 [[0, 1, 2], [0], [0, 1, 2]]] 
```

A regular expression matching the output is `[1|2][0|2][0-2]|[0-2]0[0-2]`.

<h3>Steps</h3>

1. **Simplify**. Using $\delta$-sequences set, simplify it in two ways:

    1. Replace combinations that can be represented by a single shorter sequence.
    2. Remove supersets.

    Apply simplifications iteratively until convergence.

    !!! example "Simplification"

        (a) All possible choices occur at index 0: any choice
        followed by sequence $(2,1)(1,2)$ results in infinity.
        Remove $a, b, c$ and insert $[(2,1)(1,2)]$ in their place.
        Choices are reduced from both ends of sequences.

        ```Python
        choices = [0,1,2]

        # sequences before:
          [(0,0)(2,1)(1,2)]     # a
          [(1,0)(2,1)(1,2)]     # b
          [(2,0)(2,1)(1,2)]     # c

        # sequences after:
          [(2,1)(1,2)]
        ```

        (b) Sequence $a$ is subset of $b$. Since $b$ cannot be selected
        without selecting $a$, we can remove $b$.

        ```Python
        # sequences before:
          [(0,0)]               # a
          [(0,0)(0,1)(2,2)]     # b

        # sequences after:
          [(0,0)]
        ```

2. **Build choice vectors.** Initially consider all choices as valid.
   Then eliminate unwanted sequences, for all possible combinations.

    Compute cross product of remaining $\delta$-sequences.
    Iterate the product, for each:

    - Create a vector whose length equals `i`.
    - Each vector element is a set of `choices`.
    - Eliminate choices that lead to an unwanted outcome.

    Discard invalid and redundant vectors. Add remaining vectors to result.

    !!! example "Choice vector generation"

        ```Python
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
    This yields a bounded result. For example, for choice vector,

    ```Python
    [[[2], [0],   [0,1,2]],
     [[1], [1,2], [0,1,2]]]  
    ```

    selecting $(1, 2, 2)$ is valid choice, so is $(2, 0, 2)$ and $(1, 1, 0)$, …etc.

    * If all choices are valid, the result is a single vector allowing all choices.
    * If no valid derivation exists, the result is empty choice: `[ ]`.
    * Case `index=0`, where no choice needs to be made, the result is `[ ]`.

---

::: pymwp.choice