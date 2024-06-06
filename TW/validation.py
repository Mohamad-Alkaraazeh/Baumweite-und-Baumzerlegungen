import networkx as nx
from itertools import combinations

#edges = [
#    ("a", "c"),
#   ("a", "b"),
#    ("c", "d"),
#    ("b", "e"),
#    ("d", "e"),
#    ("e", "f"),
#    ("f", "g"),
#    ("f", "h"),
#]
#tree_edges = ["(bed,bdc)", "(bed,ef)", "(bdc,bac)", "(fe,hf)", "(fe,gf)"]

class TreeDecomposition:
    def __init__(self, graph_edges, tree_edges):
        g = nx.Graph()
        e = []
        for edge in graph_edges:
            edge = edge.replace(",", "").replace("'", "")
            edge = edge[1:3]
            e.append(tuple(edge))
        g.add_edges_from(e)
        self.graph = g
        #self.tree = self.construct_tree(tree_edges)
        tree = []
        neighbors = {}
        for i in tree_edges:
            i = i.replace("(", "").replace(")", "").split(",")
            i[0] = "".join(sorted(i[0]))
            i[1] = "".join(sorted(i[1]))
            if not neighbors.get(i[1]):
                neighbors[i[1]] = set()
            if not neighbors.get(i[0]):
                neighbors[i[0]] = set()
            neighbors[i[1]].add(i[0])
            neighbors[i[0]].add(i[1])
            for j in i:
                tree.append(set(j))
        self.tree = tree
        self.neighbors = neighbors

    def construct_tree(self, tree_edges):
        tree = []
        for node in self.graph.nodes():
            neighbors = [n for n in self.graph.neighbors(node)]
            bag = set()
            bag.add(node)
            for neighbor in neighbors:
                bag.add(neighbor)
                if (node, neighbor) in tree_edges:
                    self.graph.remove_edge(node, neighbor)
            tree.append(bag)
        print("tree", tree)
        return tree

    def is_valid(self):
        valid = True

        # Property 1: every vertex is in a bag
        for e in self.graph.nodes():
            contained = False
            for bag in self.tree:
                if e in bag:
                    contained = True
                    break
            if not contained:
                valid = False
                print("Vertex", e, "not contained in any bag!")

        # Property 2: every edge is in a bag
        for e in self.graph.edges():
            e, w = e
            if e >= w:
                continue
            contained = False
            for bag in self.tree:
                if e in bag and w in bag:
                    contained = True
                    break
            if not contained:
                valid = False
                print("Edge {", e, w, "} not contained in any bag!")
        # property 3 subtree is connected
        for v in self.graph.nodes:
            connected = {}
            contained = set()
            for e in self.tree:
                e = "".join(sorted("".join(str(x) for x in e)))
                if v in e:
                    connected[e] = False
                    contained.add(e)
            contained = list(contained)
            if len(contained) == 1:
                continue
            for i in range(len(contained) - 1):
                for j in range(i + 1, len(contained)):
                    if (contained[j]) in self.neighbors[contained[i]]:
                        connected[contained[i]] = True
                        connected[contained[j]] = True
            for k in contained:
                if not connected[k]:
                    valid = False
                    print("Tree containing vertex", v, "is not connected!")
                    break
        # done
        return valid

