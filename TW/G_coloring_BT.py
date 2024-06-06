from graphviz import Graph

class Graph_coloring:
    def __init__(self, edges):
        self.edges = edges
        self.colors = {}
        self.solutions = []

    def color_bt(self):
        graph = self.build_graph()
        vertices = list(graph.keys())
        self.backtrack(graph, vertices, 0)

    def remove_parentheses(self):
        for i in range(len(self.edges)):
            self.edges[i] = self.edges[i].replace("(", "").replace(")", "")
    def build_graph(self):
        graph = {}
        self.remove_parentheses()
        for edge in self.edges:
            #print(edge)
            u, v = edge.split(',')
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append(v)
            graph[v].append(u)
        return graph


    def backtrack(self, graph, vertices, index):
        if index == len(vertices):
            return True

        vertex = vertices[index]
        available_colors = self.get_available_colors(graph, vertex)
        for color in available_colors:
            if self.is_safe(graph, vertex, color):
                self.colors[vertex] = color
                print(f"Assigned color {color} to vertex {vertex}")
                if self.backtrack(graph, vertices, index + 1):
                    return True
                self.colors[vertex] = None

        return False

    def get_available_colors(self, graph, vertex):
        used_colors = set()
        for neighbor in graph[vertex]:
            if neighbor in self.colors:
                color = self.colors[neighbor]
                if color is not None:
                    used_colors.add(color)
        available_colors = [c for c in range(len(graph)) if c not in used_colors]

        return available_colors

    def is_safe(self, graph, vertex, color):
        if vertex in self.colors and self.colors[vertex] == color:
            return False
        for neighbor in graph[vertex]:
            if neighbor in self.colors and self.colors[neighbor] == color:
                return False
        return True
    # def is_safe(self, graph, vertex, color):
    #     for neighbor in graph[vertex]:
    #         if neighbor in self.colors and self.colors[neighbor] == color:
    #             return False
    #     return True

    def get_colors(self):
        return self.colors

    def create_colored_graph(self):
        colored_nodes = set(self.colors.keys())  # Set of colored nodes

        colored_graph = {}


        for node in colored_nodes:
            cleaned_node = node.strip('()')  # Remove parentheses from the node
            colored_graph[cleaned_node] = self.colors[node]

        return colored_graph


# edges = ['(A,B)', '(A,C)', '(A,D)', '(A,N)', '(B,C)', '(B,D)', '(B,N)',
#          '(N,D)', '(N,M)', '(D,M)', '(D,H)', '(M,H)', '(D,F)', '(D,C)',
#          '(F,K)','(H,K)','(A,F)','(F,B)','(F,N)']
#
# coloring = Graph_coloring(edges)
# coloring.color_bt()
# colored_graph = coloring.create_colored_graph()
#



"""second version of Backtracking Algorithm.
To evaluate the algorithm, please comment out lines 1 to 95 and uncomment lines 104 to 170.
JUST FOR TESTING"""

# class Graph_coloring:
#     def __init__(self, edges):
#         self.edges = edges
#         self.colors = {}
#         self.solutions = []
#         self.num_colors = 3
#
#     def set_num_colors(self, num_colors):
#         self.num_colors = num_colors
#
#     def color_bt(self):
#         graph = self.build_graph()
#         vertices = list(graph.keys())
#         self.backtrack(graph, vertices, 0)
#
#     def remove_parentheses(self):
#         for i in range(len(self.edges)):
#             self.edges[i] = self.edges[i].replace("(", "").replace(")", "")
#
#     def build_graph(self):
#         graph = {}
#         self.remove_parentheses()
#         for edge in self.edges:
#             u, v = edge.split(',')
#             if u not in graph:
#                 graph[u] = []
#             if v not in graph:
#                 graph[v] = []
#             graph[u].append(v)
#             graph[v].append(u)
#         return graph
#
#     def backtrack(self, graph, vertices, index):
#         if index == len(vertices):
#             self.solutions.append(self.colors.copy())
#             return
#
#         vertex = vertices[index]
#         available_colors = self.get_available_colors(graph, vertex)
#         for color in available_colors:
#             if self.is_safe(graph, vertex, color):
#                 self.colors[vertex] = color
#                 if self.backtrack(graph, vertices, index + 1):
#                     return True
#                 self.colors[vertex] = None
#
#         return False
#
#     def get_available_colors(self, graph, vertex):
#         used_colors = set()
#         for neighbor in graph[vertex]:
#             if neighbor in self.colors:
#                 color = self.colors[neighbor]
#                 if color is not None:
#                     used_colors.add(color)
#         available_colors = [c for c in range(1, self.num_colors + 1) if c not in used_colors]
#
#         return available_colors
#
#     def is_safe(self, graph, vertex, color):
#         for neighbor in graph[vertex]:
#             if neighbor in self.colors and self.colors[neighbor] == color:
#                 return False
#         return True
#
#
#     def get_all_solutions(self):
#         return self.solutions
#
#


'''TEST example'''

import matplotlib.pyplot as plt
import numpy as np
import time

# Beispiel, wie Sie die Farbanzahl festlegen können
# edges = ['(A,B)', '(B,C)', '(C,A)', '(B,D)', '(D,E)', '(E,F)', '(F,D)']
# # edges = ['(芌,冦)', '(芌,节)', '(冦,橾)', '(冦,跪)', '(嶶,沄)', '(嶶,顰)', '(嶶,鍮)',
# #          '(嶶,蘽)', '(沄,焷)', '(沄,劜)', '(沄,碠)', '(沄,碭)', '(沄,鵐)', '(攭,节)',
# #          '(蟥,輫)', '(兿,曘)', '(兿,桝)']
#
# unique_nodes = set()
# for edge in edges:
#     u, v = edge.strip('()').split(',')
#     unique_nodes.add(u)
#     unique_nodes.add(v)
#
# # Anzahl der einzigartigen Knotennamen
# num_nodes = len(unique_nodes)
# print("Anzahl der Knoten:", num_nodes)
# print(len(edges))
#
#
# start_time = time.time()
# coloring = Graph_coloring(edges)
# coloring.set_num_colors(3)  # Setzen Sie die Farbanzahl auf die gewünschte chromatische Zahl
# coloring.color_bt()
# all_solutions = coloring.get_all_solutions()
# for solution in all_solutions:
#         print(solution)
# colored_graph = coloring.create_colored_graph()
# end_time = time.time()
# execution_time = end_time - start_time
# print('execution time:', execution_time)
# # print(colored_graph)
#
# num_nodes = 24  # Anzahl der Knoten, die Sie manuell eingeben
#
# # Erstellen Sie eine Sequenz von X-Werten, die die Anzahl der Knoten repräsentieren
# x_values = [0, num_nodes]  # X-Werte: 0 und Anzahl der Knoten
# y_values = [0, execution_time]  # Y-Werte: 0 und gemessene Ausführungszeit
#
# # Erstellen Sie ein Diagramm mit einer Linie von (0,0) bis (Anzahl der Knoten, gemessene Ausführungszeit)
# plt.plot(x_values, y_values, marker='o', linestyle='-')
# plt.xlabel('Number of nodes')
# plt.ylabel('Execution time (seconds)')
# plt.title('Execution time of the backtracking algorithm')
# plt.grid(True)
# plt.show()
