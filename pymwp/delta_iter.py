from __future__ import annotations
from .delta_graphs import DeltaGraph


def create_delta_list(n, delta_graph: DeltaGraph):
    output = []
    zeroes = []
    for _ in range(n + 1):
        output.append([])
        zeroes.append([])
    for dg in delta_graph.graph_dict.values():
        # Here ↓ monomial_list is a tuple
        for monomial_list in dg.keys():
            delta_list = list(monomial_list)
            i = delta_list[-1][1]
            if delta_list[-1][0]==0:
                zeroes[i].append(delta_list)
            else:
                output[i].append(delta_list)
    return (output,zeroes)


class Deltaiter:
    def __init__(self, max_list, delta_list):
        self.delta_list = delta_list[0]
        self.delta_list_zeroes = delta_list[1]
        self.max_list = max_list
        self.table = [0] * len(max_list)
        (j,bool)=self.check(0)
        if not bool:
            self.next()

    def value(self):
        return self.table

    def next(self):
        (i, bool) = self.plus_one(len(self.max_list) - 1)
        valid = False
        while not valid:
            (j,valid) = self.check(i)
            if not valid:
                (i, bool) = self.plus_one(j)
        return bool

    def plus_one(self, i):
        if i == -1:
            return (-1, False)
        self.table[i] = self.table[i] + 1
        if self.table[i] == self.max_list[i]:
            self.table[i] = 0
            return self.plus_one(i - 1)
        return (i, True)

    def check(self, i):
        for list_of_deltas in self.delta_list[i]:
            if not self.valid(list_of_deltas):
                return (i,False)
        for j in range(i,len(self.table)):
            for list_of_deltas in self.delta_list_zeroes[j]:
                if not self.valid(list_of_deltas):
                    return (j,False)
        return (-1,True)

    def valid(self, list_of_deltas):
        for delta in list_of_deltas:
            if self.table[delta[1]] != delta[0]:
                return True
        return False
