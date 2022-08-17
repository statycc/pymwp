# Choice.py

```python
from pymwp import Choices
```

## Determining valid choices

Choice module calculates and generates a compact representation of analysis derivation result. 
This section gives a high-level description of this process.

| Input             | Data type   |                                                           |
|-------------------|-------------|-----------------------------------------------------------|
| `i`               | `int`       | (index) count of assignments in analyzed program function |
| `choices`         | `List[int]` | possible inference choices at program point               |
| `delta_sequences` | `Set[SEQ]`  | sequences of choices leading to $\\infty$ (from matrix)   |

**Computation Steps**

1. **Simplify**. Using $\delta$-sequences set, simplify it in two ways:

    1. Replace combinations that can be represented by a single shorter
      sequence.
    2. Remove supersets.

    Iteratively apply these simplifications until convergence.

    ??? example "Simplification example"

        (a) All possible choices at index 1 occur in the set: any choice at
        index 1 followed by sequence `(2,2)(1,4)` results in infinity.
        Remove `a b c` and insert `[(2,2)(1,4)]` in their place.

        ```Python
        choices = [0,1,2]

        # sequences before:
          [(0,1)(2,2)(1,4)]     # a
          [(1,1)(2,2)(1,4)]     # b
          [(2,1)(2,2)(1,4)]     # c

        # sequences after:
          [(2,2)(1,4)]
        ```

        (b) Sequence `a` is subset of `b`. Since `b` cannot be selected
        without selecting `a`, we can remove `b`.

        ```Python
        # sequences before:
          [(0,0)]               # a
          [(0,0)(0,1)(2,2)]     # b

        # sequences after:
          [(0,0)]
        ```

2. **Build the choice vectors.** Initially consider all choices as valid.
   Then eliminate those that lead to infinity, for all possible
   combinations.

    Compute cross product of remaining $\delta$-sequences.
    Iterate the product, for each:

    - Create a vector whose length equals `i`.
    - Each vector element is a set of `choices`.
    - Eliminate choices that lead to infinity.

    Discard invalid and redundant vectors. Add remaining vectors to result.

    ??? example "Choice vector example"

        ```Python
        # remining after simplification
        sequences = [[(0,0)], [(1,0)], [(2,1)(1,2)], [(2,0)(1,1)(1,2)]]
   
        # compute cross product of sequences, which gives e.g.
        infty_path = [(0,0) (1,0) (2,1) (1,1)]

        for each infinity path:

            # initialize vector with all choices at each vector element
            vector = [{0,1,2}, {0,1,2}, {0,1,2}]

            # eliminate infinity path choices, to obtain:
            vector = [{2}, {0}, {0,1,2}]  # add to result
        ```

3. **Result.** The result is a disjunction of choice vectors.

    Choose one vector, then select one value at each vector index. 
    This yields a bounded result.

    ???+ example "Result example"

        ```Python
        [  [[1], [1,2], [0,1,2]]  v  [[2], [0,1], [1,2]]  v ... ]

        # => [1, 2, 2] is valid choice, so is [2,1,2] and [1,1,0] ... etc.
        ```

    If all choices are valid, the result is a single vector
    of length `i` and all choices exist at each vector index.
    If non-$\infty$ derivation does not exist, the result is empty `[ ]`.


::: pymwp.choice
