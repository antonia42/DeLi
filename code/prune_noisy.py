import networkx as nx
import numpy as np

def get_publisher_nodes(nodeslist):
    """
    Function to get all user-nodes for a list of nodes.

    Args:
        nodelist (list): The list with the all types of the networkx instances
            of Node().

    Returns:
        A list contains only the user-nodes.

    """
    publisher_list = []
    for (pid, attr_dict) in nodeslist:
        nodetype = attr_dict['nodetype']
        if nodetype == 'publisher':
            publisher_list.append(pid)

    return publisher_list


def find_star_like(G):
    """
    Function to get all 'star-like' connected components. More specifically,
    those are the connected components were there are less than three
    user-nodes.

    Args:
        G (networkx.Graph()): The initialized instance of the networkx Graph()
            class.

    Returns:
        True, if the graph G has a 'star-like' structure, and False otherwise.

    """
    nodeslist = G.nodes(data=True)
    publisher_list = get_publisher_nodes(nodeslist)
    if len(publisher_list) < 3:
        return True
    return False


def prune_noisy_CCs(G):
    """
    Function to prune all 'star-like' connected components.

    Args:
        G (networkx.Graph()): The initialized instance of the networkx Graph()
            class.

    Returns:
        A tuple consisted of the graph (networkx.Graph()) after the pruning and
        a list of the size of the connected components (that is next used to
        calculate average and standard deviation).

    """
    # print 'before', len(G.nodes())
    ccs = nx.connected_component_subgraphs(G)
    noisy_nodeslist = []
    cc_lengths = []
    for cc in ccs:
        if find_star_like(cc):
            noisy_nodeslist += cc.nodes()
        else:
            cc_lengths.append(len(cc.nodes()))

    G.remove_nodes_from(noisy_nodeslist)
    # print 'after', len(G.nodes())

    return (G, np.array(cc_lengths))
