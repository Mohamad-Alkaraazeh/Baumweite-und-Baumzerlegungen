import networkx as nx
from algorithm import min_fill_in
from itertools import combinations

def decomposition(edges):
    G = nx.Graph()
    e = []
    for edge in edges:

        edge = edge.replace(",", "").replace("'", "")
        edge = edge[1:3]
        e.append(tuple(edge))
    G.add_edges_from(e)
    # Get the tree decompositiong
    bags = min_fill_in(G)
    if len(bags[1]) == 1:
        bag = [''.join(j for i in bags[1].nodes for j in i)]
        bag[0] += ','
        return(bags[0], bag, bags[1].edges)
    arr = []
    idxes = {}
    # bags will be checked
    for i, bag in enumerate(bags[1].edges()):
        edges = [tuple(x) for x in bag]
        for edge in edges:
            if idxes.get(edge):
                idxes[edge].append(edges)
            else:
                idxes[edge] = [edges]

        arr.append(edges)
    for edges in arr:
        if "".join(sorted(edges[0])) in "".join(sorted(edges[1])):
            arr.remove(edges)
            for e in arr:
                if edges[0] in e:
                    t = list(e)
                    t[t.index(edges[0])] = edges[1]
                    arr[arr.index(e)] = tuple(t)
        if "".join(sorted(edges[1])) in "".join(sorted(edges[0])):
            arr.remove(edges)
            for e in arr:
                if edges[1] in e:
                    t = list(e)
                    t[t.index(edges[1])] = edges[0]
                    arr[arr.index(e)] = tuple(t)
    converted_list = [
        ",".join("".join(subitem) for subitem in sublist) for sublist in arr
    ]
    converted_list = [f"({item})" for item in converted_list]

    return (bags[0], converted_list, bags[1].edges())


# removes any digits in input(nice TD input)
def remove_integers(string):
    return ''.join(char for char in string if not char.isdigit())


'''Nice tree decomposition'''
def nice_tree(edges):
    G = nx.Graph()
    e = []
    for edge in edges:
        edge = edge.replace(")", "").replace("'", "").replace('(', '')
        edge = edge.split(',')
        e.append(tuple(edge))
    G.add_edges_from(e)
    tree: nx.DiGraph = nx.bfs_tree(G, list(G.nodes())[0])
    node = list(tree.nodes())[0]
    copies = {n: 1 for n in tree.nodes()}

    stack = [node]
    visited = set()
    while stack:
        n = stack.pop()
        visited.add(n)

        neighbors = [u for u in tree.neighbors(n) if u not in visited]
        l = len(neighbors)
        # case of NTD Algorithm
        if l == 0:
            for v in remove_integers(n):
                bag = remove_integers(n).replace(v, '')
                if len(bag)>0:
                    if bag not in copies:
                        copies[bag] = 0
                    copies[bag] = copies[bag] + 1
                    bag+=str(copies[bag])
                    tree.add_edge(n, bag)
                    stack.append(bag)
                    break

        elif l == 1:
            if remove_integers(n) == remove_integers(neighbors[0]):
                continue
            bag = None
            delta = remove_integers(n)
            for v in neighbors[0]:
                if v in n:
                    delta = delta.replace(v, '')
            if len(delta) > 0:
                bag = remove_integers(n).replace(delta[0], '')
            else:
                delta = remove_integers(neighbors[0])
                for v in n:
                    if v in neighbors[0]:
                        delta = delta.replace(v, '')
                bag = remove_integers(n)+delta[0]
            if ''.join(sorted(remove_integers(bag))) == ''.join(sorted(remove_integers(neighbors[0]))): 
                stack.append(neighbors[0])
                continue
            if bag not in copies:
                copies[bag] = 0
            copies[bag] = copies[bag] + 1
            bag+=str(copies[bag])
            tree.remove_edge(n, neighbors[0])
            tree.add_edge(n, bag)
            tree.add_edge(bag, neighbors[0])
            stack.append(bag)
        elif l >= 2:
            left = remove_integers(n) + str(copies[remove_integers(n)])

            copies[remove_integers(n)] = copies[remove_integers(n)] + 1

            right = remove_integers(n) + str(copies[remove_integers(n)])

            copies[remove_integers(n)] = copies[remove_integers(n)] + 1
            for u in neighbors:
                tree.remove_edge(n, u)
            tree.add_edge(n, left)
            tree.add_edge(n, right)
            for i, u in enumerate(neighbors):
                if i == 0:
                    tree.add_edge(right, u)
                else:
                    tree.add_edge(left, u)
            stack.append(right)
            stack.append(left)
    result = ['(' + ','.join(t) + ')' for t in tree.edges]
    # print(result)
    return (node, result)


'''Coloring method'''
# retrieves specific columns based on the indices provided in column_indices
def fetch_columns(data, column_indices):
    result = []
    for row in data:
        selected_columns = [row[i] for i in column_indices]
        result.append(selected_columns)
    return result

# function compares each element in list1 to list2 and returns a new list containing the common elements found in both lists.
def find_common_elements(list1, list2):
    common_elements = []
    for sublist1 in list1:
        if sublist1 in list2:
            common_elements.append(sublist1)
    return common_elements

def suitable_node(graph):
    max_length = 0
    max_node = None

    for node in graph.nodes():
        # Assuming the length of the string is the length of the node itself
        length = len(remove_integers(node))
        if length > max_length:
            max_length = length
            max_node = node

    return max_node

# left child, then right
def order_traversal(graph, node, g: nx.Graph, num):
    visited = set()
    stack = [node]
    comb = {}

    while stack:
        current_node = stack[-1]
        neighbors = list(graph[current_node])

        if len(neighbors) == 0 or all(n in visited for n in neighbors):
            node = stack.pop()
            visited.add(node)
            #print(node)
            neighbors = list(graph[node])
            if len(neighbors) == 0:
                comb[node] = []
                for i in range(num):
                    comb[node].append([i+1])
            elif len(neighbors) == 1:
                isForget = True
                for i in remove_integers(node):
                    if i not in neighbors[0]:
                        isForget = False
                        break
               # print(''.join(sorted(remove_integers(node))))
               # print(''.join(sorted(remove_integers(neighbors[0]))))
               # print(''.join(sorted(remove_integers(node))) in ''.join(sorted(remove_integers(neighbors[0]))))
                comb[node] = []
                temp = comb[neighbors[0]]
                if not isForget:
                    common = remove_integers(neighbors[0])
                    n = remove_integers(node)
                    for i in common:
                        n = n.replace(i, '')
                    adjacent = list(g.neighbors(n))
                    idxes = node.index(n)
                    ad_list = []
                    for i in remove_integers(node).replace(n, ''):
                        if i in adjacent:
                            ad_list.append(neighbors[0].index(i))
                    columns = fetch_columns(temp, ad_list)
                    for i in range(len(temp)):
                        for j in range(num):
                            if columns and j+1 in columns[i]:
                                continue
                            k = temp[i].copy()
                            k.insert(idxes, j+1)
                            comb[node].append(k)
                else:
                    idxes = []
                    for i in remove_integers(node):
                        idxes.append(neighbors[0].index(i))
                    arr = (fetch_columns(temp, idxes))
                    arr = [list(t) for t in set(tuple(sublist) for sublist in arr)]
                    comb[node] = arr
            elif len(neighbors) == 2:
                common = (find_common_elements(comb[neighbors[0]], comb[neighbors[1]]))
                comb[node] = common              
        else:
            for neighbor in neighbors[::-1]:
                if neighbor not in visited:
                    stack.append(neighbor)
                    break
    return comb

#  top_down in tree  to color the nodes, root, let then right
def pre_order(graph, node, comb):
    stack = [node]
    visited = set()
    colors = dict()
    c = comb[node][0]
    while stack:
        n = stack.pop()
        exist = True
        for i in remove_integers(n):
            if i not in colors:
                exist = False
                break
        if remove_integers(n) in visited or exist:
            visited.add(remove_integers(n))
            neighbors = graph.neighbors(n)
            for i in neighbors:
                stack.append(i)
            continue
        if n!=node:
            val = []
            col = []
            for i in range(len(remove_integers(n))):
                if n[i] in colors:
                    col.append(i)
                    val.append(colors[n[i]])
            columns = fetch_columns(comb[n], col)
            for i in range(len(columns)):
                contain = True
                for k, j in enumerate(col):
                    if columns[i][k] != val[k]:
                        contain = False
                        break
                if contain:
                    c = comb[n][i]
                    break
        for i in range(len(remove_integers(n))):
            if n[i] not in colors:
                colors[n[i]] = c[i]
        neighbors = graph.neighbors(n)
        for i in neighbors:
            stack.append(i)
    return colors

def coloring(o_edges, n_edges, node, num):
    g = nx.Graph()
    for e in o_edges:
        e = e.replace('(', '').replace(')', '')
        r = e.split(',')
        g.add_edge(r[0], r[1])

    n = nx.Graph()
    for e in n_edges:
        e = e.replace('(', '').replace(')', '').split(',')
        n.add_edge(e[0], e[1])

    node = suitable_node(n)
    g1 = nx.dfs_tree(n, node)
    comb = order_traversal(g1, node, g, num)
    # for key, value in comb.items():
    #     print(key, ':', value)

    # should not comment
    if comb[list(g1.nodes())[0]]:
        return (pre_order(g1, node,comb))
    else:
        return None


'''Max independent Set'''

# This method is used to find the calculation of a ndoe irrespective of it's order i.e we have node fab we can find it with any combination afb baf etc
def find_key(dictionary, target_key):
    sorted_target_key = ''.join(sorted(target_key))
    for key in dictionary:
        sorted_key = ''.join(sorted(key))
        if sorted_key == sorted_target_key:
            return dictionary[key]
    return None


# This method is used to find subsets of a node i.e. for f,a there will be '', 'f', 'a', 'fa'
def subsets(s):
    subsets = []
    for r in range(len(s) + 1):
        subsets.extend(combinations(s, r))
    return subsets


'''
# This method does postorder traversal from leaf to root (left, right, root) and does calculations for max independent set
find combination of nodes and then make calculations
'''
def postorder(graph, node, g: nx.Graph):
    visited = set()
    stack = [node]
    c = dict()

    while stack:
        current_node = stack[-1]
        neighbors = list(graph[current_node])

        if len(neighbors) == 0 or all(n in visited for n in neighbors):
            node = stack.pop()
            visited.add(node)
            # print(node)  # or do whatever you want with the node
            neighbors = list(graph[current_node])
            if len(neighbors) == 0:
                c[node] = {'': 0, node[0]: 1}
            elif len(neighbors) == 1:
                isForget = True
                for i in remove_integers(node):
                    if i not in neighbors[0]:
                        isForget = False
                        break
                if not isForget:
                    i = set(remove_integers(node))
                    j = set(remove_integers(neighbors[0]))
                    v = ''.join(i.intersection(j))
                    u = remove_integers(node)
                    for k in v:
                        if k in u:
                            u = u.replace(k, '')
                    s = subsets(j)
                    for st in s:
                        if len(st) == 0:
                            val = c[neighbors[0]]['']
                            c[node] = {'': val, u: val + 1}
                        else:
                            inf = False
                            for k in st:
                                if k in list(g.neighbors(u)):
                                    inf = True
                                    break
                            st = ''.join(st)
                            # val = c[neighbors[0]][st]
                            val = find_key(c[neighbors[0]], st)
                            c[node][st] = val
                            if inf:
                                c[node][u + st] = float('-inf')
                            else:
                                c[node][u + st] = val + 1
                else:
                    i = set(remove_integers(node))
                    j = set(remove_integers(neighbors[0]))
                    v = ''.join(i.symmetric_difference(j))
                    u = remove_integers(node).replace(v, '')
                    s = subsets(i)
                    neighbor = c[neighbors[0]]

                    for st in s:
                        if len(st) == 0:
                            val = find_key(neighbor, v)
                            c[node] = {'': max(neighbor[''], neighbor[v])}
                        else:
                            st = ''.join(st)
                            v1 = find_key(neighbor, st)
                            v2 = find_key(neighbor, st + v)
                            c[node][st] = max(v1, v2)
            else:
                i = set(remove_integers(node))
                s = subsets(i)
                c[node] = dict()
                for st in s:
                    st = ''.join(st)
                    c[node][st] = find_key(c[neighbors[0]], st) + find_key(c[neighbors[1]], st) - len(st)
                    #print(find_key(c[neighbors[0]], st) + find_key(c[neighbors[1]], st) - len(st))
        else:
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
                    break
    return c


# This method is used to find the maximum value and the node which has maximumm value for root in calculations
def max_in_dict(c):
    max = float('-inf')
    node = ''
    for key, value in c.items():
        if value >= c[''] and key != '' and value > max:
            node = key
            max = value
    return (max, node)


# This method uses the calculations does pre order traversal from root to leaf (root, left, right) and return a set of independent nodes
def max_ind(graph, node, c, g):
    visited = {remove_integers(node)}
    stack = []
    max_set = set()
    cant = set()
    max, n = max_in_dict(c[node])
    for i in n:
        max_set.add(i)
        cant.add(i)
    n = set(n.split(' '))
    n = subsets(n)
    for i in n:
        i = ''.join(i)
        if i == '':
            continue
        for j in c[node]:
            if len(j) > len(i):
                if i in j:
                    if c[node][j] == max:
                        for k in j:
                            max_set.add(k)
                            cant.add(k)
                    else:
                        for k in j:
                            cant.add(k)
        stack += list(graph.neighbors(node))
    while stack:
        node = stack.pop()
        neighbors = list(graph.neighbors(node))
        if remove_integers(node) not in visited:
            visited.add(remove_integers(node))
            m_set = []
            toadd = []
            for i in remove_integers(node):
                if i in max_set:
                    m_set.append(i)
                    continue
                if i not in cant:
                    toadd.append(i)

            if toadd:
                toadd = ''.join(toadd) + ''.join(m_set)
                v = find_key(c[node], toadd)
                if v >= c[node]['']:
                    for i in toadd:
                        max_set.add(i)
                        cant.add(i)
                else:
                    for i in toadd:
                        cant.add(i)

        stack += neighbors
    return (max_set, max)


# This method takes the original graph and nice edges from gui, uses upper methods and return max independent set
def max_independent_set(edges, o):
    n = nx.DiGraph()
    for e in edges:
        e = e.replace('(', '').replace(')', '')
        e = e.split(',')
        n.add_edge(e[0].strip(), e[1].strip())

    g = nx.Graph()
    for e in o:
        e = e.replace('(', '').replace(')', '')
        e = e.split(',')
        g.add_edge(e[0], e[1])
    node = list(n.nodes())[0]
    c = postorder(n, node, g)
    #for k, v in c.items():
     #   print('\n')
      #  print(k, ":", v)
    # print("Max: ", max_ind(n, node, c, g))
    return max_ind(n, node, c, g)

