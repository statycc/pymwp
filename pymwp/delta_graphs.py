## TODO: needed imports

from __future__ import annotations
from typing import List, Tuple, Optional
from .monomial import Monomial

#
class DeltaGraph:
    """
    DeltaGraph is a dictionary representing a weighted graph
    of tuple of deltas (also referenced here as monomial_list
    aka: a monomial without its scalar).

    We use tuple here instead of list because we want them to be
    hashable (as key in dictionary).

    We will often refere to tuple of deltas as simple node.
    But a node with lenght !

    Nodes are "sorted" by this lenght in order to be compared by chunks of
    same size.

    Weight of edge represents the index where the nodes differ.

    example:

    ```
                                 ↓
        n1 = ( (0,1) , (0,2) , (0,3), (0,4) )
        n2 = ( (0,1) , (0,2) , (1,3), (0,4) )
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

    Note: yes it also means it's symetric :

    ```python
    graph_dict[4][n2][n1] = 3
    ```

    This representation will help us simplify the evaluation by
    removing redundant/irrelevant choices/paths.
    """

    def __init__(self, monomials: Optional[List[Monomial]]= None):
        """Create DeltaGraph
            fill with empty dictionary all monomial_list of monomials given
        """
        self.graph_dict= {}
        if monomials:
            for ml in monomials:
                size = len(ml.list)
                if size not in self.graph_dict:
                    self.graph_dict[size] = {}
                self.graph_dict[size][tuple(ml.list)] = {}

    def import_monomials(self, monomials_list):
        if monomials_list:
            for ml in monomials_list:
                size = len(ml)
                if size not in self.graph_dict:
                    self.graph_dict[size] = {}
                self.graph_dict[size][ml] = {}

    def addEdge(self,node1,node2,label):
        """Add an edge of label `label` btwn `node1` and `node2`
        If one node does not exists, it's created

        Symetry is also added in the graph

        Note:
            node2 should always exists if addEdge is always called
            from insert_tuple

        Arguments:
            node1: first node
            node2: second node
            label: label over the edge

        """
        # addEdge is called only when len(node1) = len(node2)
        size = len(node1)
        if node1 not in self.graph_dict[size]:
            self.graph_dict[size][node1]={}

        # self.graph_dict[size][node1]=[(node2,label)]
        self.graph_dict[size][node1][node2]=label

        # If addEdge is always called from insert_tuple
        # node2 should always be in self.graph_dict[size]
        if node2 not in self.graph_dict[size]:
            self.graph_dict[size][node2]={}
        self.graph_dict[size][node2][node1]=label

    # monomial_list : Tuple[Tuple[int,int]]
    def insert_tuple(self, monomial_list, simplification=False):
        """Insert tuple in the graph

        it may exists cases where we need to perform simplification
        over monomials, this is why we added simplification boolean

        if monomial_list is already in the graph do nothing
        else compare it with all monomial_list of same size with
        mono_diff

        Note:
            Is it possible that we've already computed that diff in
            the other way ? (symetry)
            Answer:
                AFA it's called now, NO

        Arguments:
            monomial_list: tuple to insert in the graph
            simplification: boolean to inform if simplification is
            necessary
        """
        n=len(monomial_list)

        if n not in self.graph_dict:
            self.graph_dict[n] = {}
            self.graph_dict[n][monomial_list] = {}
        else:
            #if simplification:
            ## Add here the simplification

            if monomial_list not in self.graph_dict[n]:
                for listi in list(self.graph_dict[n]):
                    # Already tested when listi[listi][monomial_list] exists
                    # FIXME is it possible ?
                    # if monomial_list not in listi[listi]:
                    (diff,i)=self.mono_diff(monomial_list,listi)
                    if diff:
                        self.addEdge(monomial_list,listi,i)


    @staticmethod
    def remove_index(ml, index):
        """Remove delta with given index
        Arguments:
            ml: monomial_list as tuple
            index: index to remove

        Returns:
            a new tuple without detlas with index `index`
        """
        return tuple(filter(lambda x: x[1] != index, list(ml)))

    # Remove tuple from graph and related edges
            #: Tuple[Tuple[int,int]]
    def remove_tuple(self, ml, index):
        """Remove given tuple and neighbors connected with same label

        Removes also edge/labels connected to that node (which no longer exists)
        """
        size = len(ml)

        # Keep track of neighbors before removing node
        neighbos = list(self.graph_dict[size][ml])

        # Remove node
        del self.graph_dict[size][ml]

        # For each neighbour
        for ml_nb in neighbos:
            if ml_nb in self.graph_dict[size]:
                labl = self.graph_dict[size][ml_nb][ml]
                # If same label then recursively remove neighbour
                if labl == index:
                    self.remove_tuple(ml_nb,index)
                # if not just remove the edge
                else:
                    del self.graph_dict[size][ml_nb][ml]

    @staticmethod
    def mono_diff(ml1, ml2, index=None):
        """Compares two nodes
        Compares two lists of monomials (of the same lenth)
        and returns (diff, i) where diff is True if and only if
        both lists differ only on one element regarding to the same index
        and i is the index of the corresponding delta.

        Arguments:
            ml1: first monomial_list
            ml2: second monomial_list
            index: index with to check number of diff

        Returns:
            Tuple (diff, i)
            diff: boolean True if the lists differ of one element
            i: the index of the delta which differs
        """
        diff_count = 0
        i = 0
        while diff_count < 2 and i < len(ml1):
            if ml1[i] not in ml2:
                i1 = ml1[i][1]
                if index:
                    # Differ on 2 different indexes
                    if index != i1:
                        return (False,index)
                    else:
                        diff_count+=1
                else:
                    (diff,_) = DeltaGraph.mono_diff(ml2,ml1,i1)
                    if diff:
                        index = i1
                        diff_count+=1
                    else:
                        return (False,i1)
            i+=1
        return (diff_count == 1), index


    def isfull(self,n,mono,index,max_choices=3):
        """Check for cliques of same label

        example :

        m3 = ((0, 1), (2, 2), (0, 3))
        m4 = ((0, 1), (2, 2), (1, 3))
        m5 = ((0, 1), (2, 2), (2, 3))

        mono = m4
        index = 3
        max_choices = 3

        # m3 --3-- m4
        #   \\       |
        #    \\      |
        #     3     3
        #      \\    |
        #       \\   |
        #         m5

        return True

        Arguments:
            n: size of nodes or "level"
            mono: arround that node
            index: index with to find clique

        Returns:
            True if there is a clique
        """
        i=0
        for mono2 in self.graph_dict[n][mono]:
            j = self.graph_dict[n][mono][mono2]
            if j==index:
                i=i+1
                if i==max_choices-1:
                    return True
        return False

    @staticmethod
    def getIndexes(lm):
        _, listi = zip(*lm)
        return listi

    def fusion(self,list_of_max):
        # Start from longest monomial list to the shortest
        for n in sorted(self.graph_dict,reverse=True):
            # For all monomial list of size n
            for lm in list(self.graph_dict[n]):
                # For all indexes in deltas of that monomial
                for index in self.getIndexes(lm):
                    # Check if it's full of same index
                    if lm in self.graph_dict[n] and self.isfull(n,lm,index,list_of_max[index]):
                        self.remove_tuple(lm,index)
                        self.insert_tuple(DeltaGraph.remove_index(lm,index))

