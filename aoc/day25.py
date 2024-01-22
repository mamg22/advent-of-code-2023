from collections.abc import Sequence
from collections import Counter, defaultdict
from copy import deepcopy
from itertools import count
from math import prod
from random import choice
from typing import Self


class ZeroDeletingCounter(Counter):
    def __setitem__(self: Self, key, value):
        if value == 0:
            del self[key]
        else:
            super().__setitem__(key, value)


class Multigraph:
    vertices: defaultdict[str, Counter[str]]
    edges: Counter[frozenset[str]]

    __slots__ = 'vertices', 'edges'


    def __init__(self: Self) -> None:
        self.vertices = defaultdict(ZeroDeletingCounter)
        self.edges = ZeroDeletingCounter()
    

    def add_edge(self: Self, u: str, v: str, n: int = 1) -> None:
        self.vertices[u][v] += n
        self.vertices[v][u] += n
        self.edges[frozenset({u, v})] += n

    
    def clear_orphan(self: Self, u: str, v: str):
        for vertex in (u, v):
            if not any(self.vertices[vertex].values()):
                del self.vertices[vertex]

    
    def remove_all_edges(self: Self, u: str, v: str) -> None:
        self.vertices[u][v] = 0
        self.vertices[v][u] = 0

        del self.edges[frozenset({u, v})]


def parse_input(data: Sequence[str]) -> Multigraph:
    graph = Multigraph()
    for line in data:
        vertex, targets = line.split(':')

        for target in targets.strip().split():
            graph.add_edge(vertex, target.strip())
    
    return graph


def contract(graph: Multigraph, t: int = 2):
    graph = deepcopy(graph)

    while len(graph.vertices) > t:
        edges = tuple(graph.edges)
        next_edge = choice(edges)
        u, v = next_edge

        nodename = f"{u}+{v}"

        for u_edge, count in tuple(graph.vertices[u].items()):
            if v != u_edge:
                graph.add_edge(nodename, u_edge, count)
            
            graph.remove_all_edges(u, u_edge)

        for v_edge, count in tuple(graph.vertices[v].items()):
            if u != v_edge:
                graph.add_edge(nodename, v_edge, count)
            
            graph.remove_all_edges(v, v_edge)
        
        graph.clear_orphan(u, v)
        

    return graph


def fastmincut(graph: Multigraph) -> Multigraph:
    n_vertices = len(graph.vertices)
    if n_vertices <= 6:
        return contract(graph, 2)
    else:
        t = 1 + n_vertices // 2
        g1 = contract(graph, t)
        m1 = fastmincut(g1)

        if m1.edges.total() == 3:
            return m1
        else:
            g2 = contract(graph, t)
            return fastmincut(g2)


def solve_part1(data: Sequence[str]) -> int:
    graph = parse_input(data)
    for i in count(1):
        print(f"Attempt {i}")
        cut_graph = fastmincut(graph)

        if cut_graph.edges.total() == 3 and len(cut_graph.vertices) == 2:
            return prod((len(vertex.split('+')) for vertex in cut_graph.vertices))
        else:
            print("Done" + ' ' * 10)
    
    raise RuntimeError("Unreachable")


def solve_part2(data: Sequence[str]) -> int:
    return 0


def main() -> None:
    with open("input/day25.txt", 'r') as data_file:
        data: list[str] = data_file.read().splitlines()

    print("Part 1:", solve_part1(data))
    print("Part 2:", solve_part2(data))


if __name__ == '__main__':
    main()
