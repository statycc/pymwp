## TODO: needed imports

class DeltaGraph:
    
    graph_dict={}
    
    def addEdge(self,list1,list2,label):
        if len(list1) not in self.graph_dict:
            self.graph_dict[len(list1)]={}  
        if list1 not in self.graph_dict[len(list1)]:
            self.graph_dict[len(list1)][list1]=[(list2,label)]
        else:
            self.graph_dict[node].append((neighbour,label))
        if list2 not in self.graph_dict[len(list2)]:
            self.graph_dict[len(list2)][list2]=[(list1,label)]
        else:
            self.graph_dict[len(list2)][list2].append((list1,label))
            
    def insert_list(self,monomial_list):
        n=len(monomial_list)
        ## Add here the simplification
        if monomial_list not in self.graph_dict[n]:
            for list in self.graph_dict[n]:
                (diff,i)=MonoDiff(monomial_list,list)
                if diff:
                    self.addEdge(monomial_list,list,i)

## Needed here: the Monodiff method which compares two lists of monomials (of the same lenth) and returns (diff, i) where diff is True if and only if both lists differ only on one element, and i is the index of the corresponding delta.

    def isfull(self,n,mono,index,max_choices=3):
        i=0
        for (m,j) in self.graph_dict[n][mono]:
            if j==index:
                i=i+1
                if i==max_choices-1:
                    return True
        return False

    def simplify(self,list_of_max):
        for n in list(self.graph_dict).sort(reverse=True):
             for list in self.graph_dict[n]:
                  for index in mono.indexes():
                      if self.isfull(n,list,index,list_of_max(index))
                          self.remove_index(list,index)
                          self.insert_list(list.remove_index(index))

## Need here methods on lists of deltas: remove_index removes the delta with the given index value (which is not the index in the list)
## Need here a metho on delta_graphs: remove_index(list,index) loops over all lists list2 of size that of list for which there is an edge list --index-- list2
## For this, we need a method remove() on delta_graphs that remove the dictionary key, and erases all edges.


