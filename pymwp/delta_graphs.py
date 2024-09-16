# ------------------------------------------------------------------------------
# Copyright (c) 2020-2024 C. Aubert, T. Rubiano, N. Rusch and T. Seiller.
#
# This file is part of pymwp.
#
# pymwp is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pymwp is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pymwp. If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional, Tuple, Union

from . import Monomial, NODE


class DeltaGraph:
    """
    Delta Graph is a dictionary representing a weighted graph of tuples of
    deltas (also referenced here as a _monomial_list_, a list of Monomials
    without its scalar). We will often refer to tuple of deltas as simple
    node, but a node with length!

    Nodes are "sorted" by this length in order to be compared by chunks of
    same size.

    Weight of edge represents the index where the nodes differ.

    We use tuple because we want them to be hashable (as key in dictionary).

    Example:
        ```
                              ↓
        n1 = ((0,1), (0,2), (0,3), (0,4))
        n2 = ((0,1), (0,2), (1,3), (0,4))
        ```

        in our graph will have:

        ```
        n1 <---- 3 ----> n2
        ```

        or

        ```python
        size = 4   ↓
        graph_dict[4][n1][n2] = 3
        ```

        The graph is symmetric:

        ```python
        graph_dict[4][n2][n1] = 3
        ```

    This representation will help us simplify the evaluation by
    removing redundant/irrelevant choices/paths.

    Attributes:
        graph_dict (dict): Dictionary of nodes.
        degree (int): Graph degree.
    """

    def __init__(
            self,
            *init_nodes: Optional[Union[Monomial, NODE]],
            degree: int = 3
    ):
        """Create a Delta Graph.

        Arguments:
            *init_nodes: Initial list of monomials or nodes.
            degree: Degree of a full node.

        Example:
            Create an empty delta graph

            ```python
            dg = DeltaGraph()
            ```

            Create delta graph with some initial nodes from monomials.

            ```python
            dg = DeltaGraph(mono1, mono2)
            ```
        """
        self.degree = degree
        self.graph_dict = {}
        if init_nodes:
            for node in init_nodes:
                if isinstance(node, Monomial):
                    self.from_monomial(node)
                if isinstance(node, Tuple):
                    self.insert_node(node)

    def __str__(self):
        return "".join(
            [f'{n} {self.graph_dict[n]}\n{26 * "--"}\n' for n in
             self.graph_dict])

    def from_monomial(self, monomial: Monomial) -> None:
        """Add monomial's deltas to the delta graph.

        Arguments:
            monomial: monomial
        """
        self.insert_node(tuple(monomial.deltas))

    def insert_edge(self, node1: NODE, node2: NODE, label: int) -> None:
        """Add an edge of label `label` between `node1` and `node2`
        If one node does not exist, it's created

        Symmetry is also added in the graph.

        Arguments:
            node1: first node
            node2: second node
            label: label over the edge

        """
        size = len(node1)
        if node1 not in self.graph_dict[size]:
            self.graph_dict[size][node1] = {}

        self.graph_dict[size][node1][node2] = label

        # node2 should always exist if add_edge is always called
        # from insert_tuple
        if node2 not in self.graph_dict[size]:
            self.graph_dict[size][node2] = {}
        self.graph_dict[size][node2][node1] = label

    def insert_node(self, node: NODE) -> None:
        """Insert a node into the graph.

        If a node is already in the graph do nothing.
        Else compare it with all nodes of same size with `node_diff`.

        Arguments:
            node: tuple to insert in the graph
        """
        size = len(node)
        # Is it possible that we've already computed that diff in
        # the other way ? (symmetry)
        # Answer: AFA it's called now, NO
        if size not in self.graph_dict:
            self.graph_dict[size] = {}
            self.graph_dict[size][node] = {}
        else:
            # Case may exist where we need to perform simplification
            #    over monomials -> Add here the simplification
            inserted = False
            if node not in self.graph_dict[size]:
                for node2 in list(self.graph_dict[size].keys()):
                    # Already tested when node2[node2][monomial_list] exists
                    # FIXME is it possible ?
                    # if monomial_list not in node2[node2]:
                    diff, i = self.node_diff(node, node2)
                    if diff:
                        inserted = True
                        self.insert_edge(node, node2, i)
                if not inserted:
                    self.graph_dict[size][node] = {}

    @staticmethod
    def remove_index(node: NODE, index: int) -> NODE:
        """Remove delta with given index.

        Example:
            ```
            remove index 4:
            ((0, 2), (1, 3), (2, 4))  ->  ((0, 2), (1, 3))
            ```

        Arguments:
            node: monomial list
            index: index to remove

        Returns:
            a new tuple without deltas with index `index`
        """
        return tuple(filter(lambda x: x[1] != index, node))

    def remove_node(self, node: NODE, index: int) -> None:
        """Remove given node and neighbors connected with same label.

        Also removes edges/labels connected to the node (they no longer exist).
        """
        size = len(node)

        # Keep track of neighbors before removing node
        neighbors = list(self.graph_dict[size][node])

        # Remove node
        del self.graph_dict[size][node]

        # For each neighbour
        for neighbor in neighbors:
            if neighbor in self.graph_dict[size]:
                label = self.graph_dict[size][neighbor][node]
                # If same label then recursively remove neighbour
                if label == index:
                    self.remove_node(neighbor, index)
                # if not just remove the edge
                else:
                    del self.graph_dict[size][neighbor][node]

    @staticmethod
    def node_diff(
            node1: NODE, node2: NODE, index: Optional[int] = None
    ) -> Tuple[bool, int]:
        """Compares two nodes of the same length.

        The return value is a tuple representing the result of comparison
        (boolean) and an index.

        The result is True, if and only if both lists differ only on one
        element regarding the same index. The second return value is the index
        of the corresponding delta.

        Arguments:
            node1: first monomial list
            node2: second monomial list
            index: index with to check number of diff

        Returns:
            diff: boolean True if the lists differ of one element
            i: the index of the delta which differs
        """
        diff_found = False
        i = 0
        while i < len(node1):
            if node1[i] not in node2:
                i1 = node1[i][1]
                # We've already recorded one so two diff
                if diff_found:
                    return False, i1
                # Case recursive call, we've not found yet
                # But index is defined by arguments
                if index is not None:
                    # If the diff has different index than expected
                    if index != i1:
                        return False, index
                    else:
                        # We've found one but still searching more
                        diff_found = True
                # Found first diff without init of index
                else:
                    # Search in other monomial if it has only one diff
                    # Of same index `i1`
                    (diff, _) = DeltaGraph.node_diff(node2, node1, i1)
                    if diff:
                        index = i1
                        # Continue searching see if there are more diff
                        diff_found = True
                    else:
                        return False, i1
            i += 1
        return diff_found, index

    def is_full(self, node: NODE, size: int, index: int) -> bool:
        """Check for cliques of same label.

        Example:
            ```Python
            n3 = ((0, 1), (2, 2), (0, 3))
            n4 = ((0, 1), (2, 2), (1, 3))
            n5 = ((0, 1), (2, 2), (2, 3))

            node = n4
            size = 3
            index = 3
            degree = 3

            n3 -- 3 -- n4
             ⟍         |
                3       3
                  ⟍    |
                    ⟍  |
                      n5

            return True
            ```

        Arguments:
            node: check for clique around that graph node.
            size: size of nodes or graph "level".
            index: index where to find clique.

        Returns:
            True if there is a clique.
        """
        src = self.graph_dict[size][node]
        adjacent = sum([1 for n2 in src if src[n2] == index])
        return adjacent == (self.degree - 1)

    def fusion(self) -> None:
        """Eliminates cliques of same label in a delta graph.

        Example:
            ```python
            m1 = ((0, 1), (0, 2))
            m2 = ((0, 1), (1, 2))
            m3 = ((0, 1), (2, 2), (0, 3))
            m4 = ((0, 1), (2, 2), (1, 3))
            m5 = ((0, 1), (2, 2), (2, 3))

            Delta graph:

              m1 -- 2 -- m2
              m3 -- 3 -- m4
               ⟍         |
                  3      3
                    ⟍    |
                      ⟍  |
                        m5

            Looks for cliques (size default 3) at each index.
            => Graph will simplify to: ((0,1)).
            ```
        """
        # Start from the longest node to the shortest
        for size in sorted(self.graph_dict, reverse=True):
            for node in list(self.graph_dict[size]):
                # For all indexes in deltas of that node
                for index in (list(zip(*node))[1]):
                    # Check if it's full of same index
                    if node in self.graph_dict[size] and \
                            self.is_full(node, size, index):
                        self.remove_node(node, index)
                        self.insert_node(DeltaGraph.remove_index(node, index))

    @property
    def is_empty(self) -> bool:
        return 0 in self.graph_dict and self.graph_dict[0] == {(): {}}
