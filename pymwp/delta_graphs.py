## TODO: needed imports

# from __future__ import annotations
# from typing import List, Tuple

class DeltaGraph:
    def __init__(self):
        self.graph_dict={}

    def addEdge(self,list1,list2,label):
        # addEdge is called only when len(list1) = len(list2)
        size = len(list1)
        if size not in self.graph_dict:
            self.graph_dict[size]={}
        if list1 not in self.graph_dict[size]:
            self.graph_dict[size][list1]={}

        # self.graph_dict[size][list1]=[(list2,label)]
        self.graph_dict[size][list1][list2]=label

        # symetry ↓ ?? Is it usefull ?? FIXME test…
        # If addEdge is always called from insert_tuple
        # list2 should always be in self.graph_dict[size]
        if list2 not in self.graph_dict[size]:
            self.graph_dict[size][list2]={}
        self.graph_dict[size][list2][list1]=label

        # monomial_list : Tuple[Tuple[int,int]]
    def insert_tuple(self, monomial_list):
        n=len(monomial_list)
        ## Add here the simplification
        if monomial_list not in self.graph_dict[n]:
            for listi in self.graph_dict[n]:
                # Already tested when listi[listi][monomial_list] exists
                # FIXME is it possible ?
                # if monomial_list not in listi[listi]:
                (diff,i)=self.mono_diff(monomial_list,listi)
                if diff:
                    self.addEdge(monomial_list,listi,i)

## Need here methods on lists of deltas: remove_index removes the delta with the given index value (which is not the index in the list)
## Need here a metho on delta_graphs: remove_index(list,index) loops over all lists list2 of size that of list for which there is an edge list --index-- list2
## For this, we need a method remove() on delta_graphs that remove the dictionary key, and erases all edges.


    # Remove tuple from graph and related edges
            #: Tuple[Tuple[int,int]]
    def remove_tuple(self, ml, index):
        size = len(ml)

        # Keep track of neighbors before removing node
        neighbos = list(self.graph_dict[size][ml])

        # Remove node
        del self.graph_dict[size][ml]

        # For each neighbour
        for ml_nb in neighbos:
            labl = self.graph_dict[size][ml_nb][ml]
            # If same label then recursively remove neighbour
            if labl == index:
                self.remove_tuple(ml_nb,index)
            # if not just remove the edge
            else:
                del self.graph_dict[size][ml_nb][ml]

    @staticmethod
    def mono_diff(ml1, ml2):
        index = None
        diff_count = 0
        i = 0
        while diff_count < 2:
            if ml1[i] not in ml2:
                index = i
                diff_count+=1
            i+=1
        return (diff_count == 1), index

## Needed here: the Monodiff method which compares two lists of monomials (of the same lenth) and returns (diff, i) where diff is True if and only if both lists differ only on one element, and i is the index of the corresponding delta.

    def isfull(self,n,mono,index,max_choices=3):
        i=0
        for (_,j) in self.graph_dict[n][mono]:
            if j==index:
                i=i+1
                if i==max_choices-1:
                    return True
        return False

    @staticmethod
    def getIndexes(lm):
        _, listi = zip(*lm)
        return listi

    def simplify(self,list_of_max):
        for n in sorted(self.graph_dict,reverse=True):
             for lm in self.graph_dict[n]:
                 # Récupère les index de delta (_,j) ← j
                  for index in self.getIndexes(lm):
                      if self.isfull(n,lm,index,list_of_max(index)):
                          self.remove_tuple(lm,index)
                          self.insert_tuple(lm.remove_index(index))

# TODO test on:
# d(0,1)d(0,2)
# d(0,1)d(1,2)
# d(0,1)d(2,2)d(0,3)
# d(0,1)d(2,2)d(1,3)
# d(0,1)d(2,2)d(2,3)

# should give d(0,1)
