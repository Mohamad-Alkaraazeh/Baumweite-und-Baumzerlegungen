import networkx as nx
import itertools
import sys

'''we use min fill in algorithm to decompose the graph, it takes a node from graph where is the number of edges
to make the neighbours of this node a clique is small'''
def min_fill_in(G):
    return treewidth_decomp(G, min_fill_in_h)

def min_fill_in_h(graph):

    if len(graph) == 0:
        return None

    min_fill_in_node = None

    #is set to large value to ensure that the selected node has lower value
    min_fill_in = sys.maxsize

    nodes_by_degree = sorted(graph, key=lambda x: len(graph[x]))
    min_degree = len(graph[nodes_by_degree[0]])

    if min_degree == len(graph) - 1:
        return None

    for node in nodes_by_degree:
        num_fill_in = 0
        nbrs = graph[node]
        for nbr in nbrs:
            num_fill_in += len(nbrs - graph[nbr]) - 1
            if num_fill_in >= 2 * min_fill_in:
                break

        num_fill_in /= 2

        if num_fill_in < min_fill_in:
            if num_fill_in == 0:
                return node
            min_fill_in = num_fill_in
            min_fill_in_node = node

    return min_fill_in_node



"""return the decomposition of graph using the min fill in Algorithm"""
def treewidth_decomp(G, heuristic=min_fill_in_h):

    # make dict of sets that not contain node n
    graph = {n: set(G[n]) - {n} for n in G}

    node_stack = []

    elim_node = heuristic(graph)

    while elim_node is not None:
        # connect all neighbours with each other
        nbrs = graph[elim_node]
        for u, v in itertools.permutations(nbrs, 2):
            if v not in graph[u]:
                graph[u].add(v)

        node_stack.append((elim_node, nbrs))
        for u in graph[elim_node]:
            graph[u].remove(elim_node)

        del graph[elim_node]
        elim_node = heuristic(graph)

    # the condition is met, set all remaining nodes in one bag
    decomp = nx.Graph()
    first_bag = frozenset(graph.keys())
    decomp.add_node(first_bag)

    treewidth = len(first_bag) - 1

    while node_stack:
        (curr_node, nbrs) = node_stack.pop()
        # find a bag all neighbors are inside
        old_bag = None
        for bag in decomp.nodes:
            if nbrs <= bag:
                old_bag = bag
                break

        if old_bag is None:
            old_bag = first_bag
            # print("old bag was:", old_bag)

        nbrs.add(curr_node)

        new_bag = frozenset(nbrs)
        # print('new bag is ::', new_bag)

        # update treewidth
        treewidth = max(treewidth, len(new_bag) - 1)

        # add edge to decomposition
        decomp.add_edge(old_bag, new_bag)
    print('tree width:', treewidth)
    return treewidth, decomp
