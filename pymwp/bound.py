from typing import List


class Bound:
    """Represents MWP bound."""

    def __init__(self):
        self.m = []
        self.w = []
        self.p = []

    def __str__(self):
        m_str = ",".join(self.m)
        w_str = ",".join(self.w)
        p_str = ",".join(self.p)
        return "(" + (';'.join([m_str, w_str, p_str])) + ")"

    def append(self, scalar: str, var_name: str):
        """Append variable dependency in the right place by scalar."""
        if scalar == 'm':
            self.m.append(var_name)
        if scalar == 'w':
            self.w.append(var_name)
        if scalar == 'p':
            self.p.append(var_name)

    @staticmethod
    def calculate(variables: List[str], simple_mat: List[List[str]]) -> dict:
        """Calculates mwp-bound from a matrix.

        Arguments:
            variables: variable names (list)
            simple_mat: matrix of scalars

        Returns:
            mwp-bound dictionary.
        """
        result = {}
        for col_id, name in enumerate(variables):
            var_bound = Bound()
            for row_id in range(len(simple_mat)):
                var_bound.append(simple_mat[row_id][col_id], variables[row_id])
            result[name] = var_bound
        return result

    @staticmethod
    def show(bound_dict: dict) -> str:
        """Helper to format a nice display string of mwp-bound."""
        b_str = [f'{k} ≤ {v}' for k, v in bound_dict.items()]
        return ' ∧ '.join(b_str)
