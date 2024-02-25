import networkx as nx
import numpy as np

def make_graph(A: np.matrix, filename: str):
    labels = { i: "S" + str(i) for i in range(len(A)) }
    G = nx.DiGraph(np.array(A))

    # Set node labels to A, B, C, D, E
    nx.set_node_attributes(G, {k: {'label': labels[k]} for k in labels.keys()})
    nx.set_edge_attributes(G, {(e[0], e[1]): {'taillabel': e[2]['weight']} for e in G.edges(data=True)})
    D = nx.drawing.nx_agraph.to_agraph(G)

    # Modify node fillcolor and edge color.
    D.node_attr.update(color='blue', style='filled', fillcolor='white')
    D.edge_attr.update(color='blue', arrowsize=1, fontcolor='red', fontsize=5, labeldistance='2', labelangle='0.0')
    D.graph_attr['dpi'] = '200'
    D.graph_attr['size'] = '1000'
    pos = D.layout('circo')
    D.draw(filename)