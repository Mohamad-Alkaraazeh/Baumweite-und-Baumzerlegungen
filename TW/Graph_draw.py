from graphviz import Graph
from webcolors import CSS3_NAMES_TO_HEX, hex_to_rgb
def Draw_Graph(edges, type, color=None, node=None, max_set =None):
    # undirected graph
    G = Graph("graph")
    G.attr("node", shape="circle")
    if node:
        G.attr(root=node)
    # colors = ['red', 'green', 'blue', 'yellow']
              # 'gold', 'lime', 'mistyrose', 'maroon', 'sienna',
              # 'tomato', 'peru', 'sandybrown', 'khaki', 'aquamarine', 'darkorchid']
    colors = generate_color_list(num_colors)
    if color:
        for key, value in color.items():
            G.node(key, fillcolor=colors[value-1], style='filled')
    if max_set:
        for n in max_set:
            G.node(n, fillcolor='green', style='filled')

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
    # save the graph to file, or you can leave it out.
    if type == 'graph':
        G.render(filename="graph.gy", format="png")
    elif type == 'decomposition':
        G.render(filename="decomposition.gy", format="png")
    elif type == 'nice':
        G.render(filename="nice.gy", format="png")
    # G.view() graph will in adobe displyed


def generate_color_list(num_colors):
    color_list = []
    for color_name, hex_value in CSS3_NAMES_TO_HEX.items():
        if color_name.lower() != 'black':  # Exclude the color black
            rgb_value = hex_to_rgb(hex_value)
            color_list.append((color_name, rgb_value))
    color_list = sorted(color_list, key=lambda x: sum(x[1]))
    color_list = color_list[:num_colors]
    return [color[0] for color in color_list]

num_colors = 11



