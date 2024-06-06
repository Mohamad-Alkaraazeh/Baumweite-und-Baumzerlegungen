from graphviz import Graph

'''the algorithm explores the solution space of 
all possible combinations of vertices, utilizing 
backtracking to efficiently find the maximal independent sets in the graph.'''

def Draw_Max_Graph(edges, type, max_ind_set, node=None):
    # indirect graph
    G = Graph("graph")
    G.attr("node", shape="circle")
    if node:
        G.attr(root=node)
    colors = ['green', 'white']

    if max_ind_set:
        for key in max_ind_set:
            G.node(key, fillcolor=colors[0], style='filled')
    for i in edges:
        i = i.replace(" ", "")
        i = i.replace("(", "")
        i = i.replace(")", "")
        z = i.split(",")
        s = z[0]
        t = z[1]
        if not t:
            G.node(s)
        else:
            G.edge(s, t)
    if type == 'graph':
        G.render(filename="graph.gy", format="png")


def find_maximal_independent_set(input_edges):
    graph = {}
    vertices = set()

    # Build the graph
    for edge in input_edges:
        v1, v2 = edge.strip('()').split(',')
        vertices.add(v1)
        vertices.add(v2)
        graph.setdefault(v1, set()).add(v2)
        graph.setdefault(v2, set()).add(v1)

    def is_maximal_independent_set(candidate_set):
        # Check if the candidate set is a maximal independent set
        for vertex in candidate_set:
            neighbors = graph.get(vertex, set())
            if any(neighbor in candidate_set for neighbor in neighbors):
                return False
        return True


    '''recursive function that explores all possible combinations of vertices to find the maximal independent sets'''
    def find_independent_sets(current_set, remaining_vertices):
        nonlocal max_length  # Access and modify the max_length variable defined in the outer scope

        if len(remaining_vertices) == 0:
            if len(current_set) > len(max_length):
                maximal_independent_sets.clear()
                max_length = current_set
            if is_maximal_independent_set(current_set):
                maximal_independent_sets.append(current_set)
            return True

        v = remaining_vertices.pop()
        # Recursive call without adding the current vertex to the current set
        find_independent_sets(current_set, remaining_vertices.copy())


        if all(vertex not in graph[v] for vertex in current_set):
            # Check if the current vertex is independent of all vertices in the current set
            current_set.add(v)
            find_independent_sets(current_set.copy(), remaining_vertices.copy())
            # Recursive call with the current vertex added to the current set
            current_set.remove(v)

    maximal_independent_sets = []
    max_length = []
    find_independent_sets(set(), vertices.copy())
    return max_length


# focus on the edges that are relevant to the maximum independent set
def filter_edges_by_max_ind_set(edges, max_ind_set):

    new_edges = []
    for edge in edges:
        u, v = edge.split(",")  #split the edge
        if u in max_ind_set or v in max_ind_set:
            new_edges.append(edge)

    return new_edges

