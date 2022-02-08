import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt


def read_graphml_with_position(filename):
    """Read a graph in GraphML format with position"""
    G = nx.read_graphml(filename)

    # rearrage node attributes x, y as position for networkx
    pos = (
        dict()
    )  # A dictionary with nodes as keys and positions as values. Positions should be sequences of length 2.
    node_and_x = nx.get_node_attributes(G, "x")
    node_and_y = nx.get_node_attributes(G, "y")

    for node in node_and_x:
        x = node_and_x[node]
        y = node_and_y[node]
        pos[node] = (x, y)

    # add node attribute `pos` to G
    nx.set_node_attributes(G, "pos", pos)

    return G


def readGraphML():
    G = nx.read_graphml("./wf.graphml")

    for node in G.nodes(data=True):
        print(node)


if __name__ == "__main__":
    oregon = (-122.6765, 45.5231)
    washington = (-122.3321, 47.6062)

    # G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43, network_type='drive')
    G = ox.graph_from_bbox(
        washington[1], oregon[1], washington[0], oregon[0], network_type="drive"
    )
    G_projected = ox.project_graph(G)
    # ox.plot_graph(G_projected)

    print(G_projected)
