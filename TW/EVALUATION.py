import random
import networkx as nx
import matplotlib.pyplot as plt
import time
import dec1 as d
from G_coloring_BT import Graph_coloring
from Alt_max_ind_set import find_maximal_independent_set
def generate_alphabets(length=1000):
    alphabets = set()

    # English alphabet (26 characters)
    alphabets.update(chr(code) for code in range(65, 91))
    alphabets.update(chr(code) for code in range(97, 123))
    # alphabets.update(string.ascii_lowercase)
    # alphabets.update(string.ascii_uppercase)
    # Spanish alphabet (27 characters)
    alphabets.update(['ñ', 'Ñ'])

    # German alphabet (30 characters)
    alphabets.update(['ä', 'ö', 'ü', 'ß'])

    # French alphabet (26 characters)
    alphabets.update(['à', 'â', 'æ', 'ç', 'é', 'è', 'ê',
                     'ë', 'î', 'ï', 'ô', 'œ', 'ù', 'û', 'ü'])

    # Russian alphabet (33 characters)
    alphabets.update(chr(code) for code in range(1040, 1104))

    # Chinese alphabet (50 characters)
    alphabets.update(chr(code) for code in range(19968, 40870))

    # Randomly select alphabets from the existing sets
    while len(alphabets) < length:
        random_alphabet = chr(random.randint(33, 126))
        alphabets.add(random_alphabet)

    return alphabets

def create_connected_random_graph(nodes, max_unit_size=5, min_unit_size=1):
    G = nx.Graph()
    remaining_nodes = list(nodes)

    # Initially, connect two random nodes to create a starting point
    if remaining_nodes:
        start_node1 = random.choice(remaining_nodes)
        remaining_nodes.remove(start_node1)
        start_node2 = random.choice(remaining_nodes)
        G.add_edge(start_node1, start_node2)

    while remaining_nodes:
        # Calculate the maximum unit size based on remaining nodes
        max_unit_size = min(max_unit_size, len(remaining_nodes))

        # Ensure that min_unit_size is not greater than max_unit_size
        min_unit_size = min(min_unit_size, max_unit_size)

        unit_size = random.randint(min_unit_size, max_unit_size)
        unit_nodes = random.sample(remaining_nodes, unit_size)

        for node1 in unit_nodes:
            for node2 in unit_nodes:
                if node1 != node2 and not G.has_edge(node1, node2) and random.random() < 0.5:
                    G.add_edge(node1, node2)

        remaining_nodes = [node for node in remaining_nodes if node not in unit_nodes]

    # Add random edges while preserving connectivity
    while not nx.is_connected(G):
        node1 = random.choice(nodes)
        node2 = random.choice(nodes)
        if node1 != node2 and not G.has_edge(node1, node2):
            G.add_edge(node1, node2)

    if nx.is_connected(G):
        print("The graph is fully connected.")
    else:
        print("The graph is not fully connected.")

    return G

dec_list = []
nice_list = []
clr_list = []
max_list = []
maxalt_list = []
cloringbt_list = []
def measure_total_time(nodes):
    max_unit_size = 3 # change the size of small graphs inside the random one
    g = create_connected_random_graph(nodes, max_unit_size)

    print(g)
    result = ['(' + ','.join(t) + ')' for t in g.edges]
    print('result is :::', result)
    # Tree decomposition
    start_time = time.time()

    width, edges, dec = d.decomposition(result)
    dec_time = time.time()
    dec_list.append(dec_time - start_time)
    print('decomposition time is :',dec_time - start_time)

    # Nice tree dec (NTD)
    node, nice = d.nice_tree(edges)
    nice_time = time.time()
    nice_list.append(nice_time-start_time)
    print('nice time is :',nice_time - start_time)

    # coloring with NTD
    d.coloring(result, nice, node, 3)
    clr_time = time.time()
    clr_list.append(clr_time-start_time)
    print('Coloring take time:', clr_time - start_time)

    # Max Ind set with NTD
    # d.max_independent_set(nice, result)
    # max_time = time.time()
    # max_list.append(max_time - start_time)
    # print('max time: ',max_time - start_time)

    # Max ind set with Backtracking
    # tt = time.time()
    # find_maximal_independent_set(result)
    # maxalt_time = time.time()
    # maxalt_list.append(maxalt_time - tt)
    # print('maxalt time is :', maxalt_time - tt)


    #coloring with backtracking (PLEASE SEE G_coloring_BT.py line 100)
    start = time.time()
    coloring = Graph_coloring(result)
    coloring.set_num_colors(3)
    coloring.color_bt()
    end = time.time()
    cloringbt_list.append(end - start)
    clrbt = end - start
    print("execution time is:", clrbt)


    return dec_time, nice_time, clr_time, clrbt


# Parameters for iteration (If you want to run all method together 40 is the better choice
# because max alternative set and Coloring with Backtracking take alot of time)
start = 15
stop = 35
step = 5

nodes_list = []
characters = list(generate_alphabets(100))

print(len(characters))
# Iterate through the numbers and record time taken
for num_nodes in range(start, stop + 1, step):
    nodes = characters[:num_nodes]
    time_taken = measure_total_time(nodes)
    nodes_list.append(num_nodes)

# Display the graph of time taken

plt.plot(nodes_list, dec_list, color='blue', label='decomposition')
plt.plot(nodes_list, nice_list, color='black', label='ntd')
plt.plot(nodes_list, clr_list, color='red', label='coloring with NTD')
# plt.plot(nodes_list, max_list, color='green', label='max independent set')
# plt.plot(nodes_list, maxalt_list, color='peru', label='max independent set wih Backtracking')
plt.plot(nodes_list, cloringbt_list, color='fuchsia', label='coloring wih Backtracking')
plt.xlabel('Number of Nodes')
plt.ylabel('Time Taken (seconds)')
plt.title('Computation')
plt.grid(True)
plt.legend()
plt.show()
