"""
FEEL FREE TO EDIT THIS, this is just a starting template you can work from!

I included the libraries I recommend you use for this project.
Network x will allow you to easily path find and traverse the graph.
Ive provided links to the k-shortest paths documentation that you can take a look at if you want.
I also provided links to a series of videos on graphs that might be useful for you.

YOU DO NOT NEED TO WATCH ALL THE VIDEOS THEY ARE JUST THERE IF YOU NEED THEM OR WANT TO LEARN MORE

k-shortest-path documentation: https://networkx.org/documentation/networkx-1.10/reference/generated/networkx.algorithms.simple_paths.shortest_simple_paths.html
Graph videos: https://www.coursera.org/lecture/cs-fundamentals-3/3-1-1-graphs-introduction-1mr1X
Graph website: http://web.cecs.pdx.edu/~sheard/course/Cs163/Doc/Graphs.html
"""
import csv
# Need these for path finding and graphing
import networkx as nx   # K-shortest paths library
import matplotlib.pyplot as plt  # Create the graph

from linkObj import linkObj
from nodeObj import nodeObj
from requestObj import requestObj


def set_edges(link_list):
    visited_links = []

    for link in link_list:
        u = link[0]
        v = link[1]
        temp = [u, v]
        if link not in visited_links:
            edges.append(temp)
            visited_links.append(link)


def get_nodes():
    """Create node objects from input file."""
    node_objects = []
    file_path = "../data/NodeInputData.csv"
    with open(file_path, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)  # skip header line
        for line in reader:
            node_objects.append(
                nodeObj(nodeID=int(line[0]), nodeResources=int(line[1]), nodeStatus=False, nodeCost=int(line[2]))
            )
    return node_objects


def get_links():
    """Create link objects from input file."""
    link_objects = []
    file_path = "../data/LinkInputData.csv"
    with open(file_path, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)  # skip header line
        for line in reader:
            link_objects.append(
                linkObj(linkID=int(line[0]), linkBW=int(line[1]), linkSrc=int(line[2]), linkDest=int(line[3]))
            )
    return link_objects


def get_sub_paths(path):
    """
    Given a path from a src node to a dest node (e.g. [1,5,2],
    return a list of the links between them (e.g., [[1,5], [5,2]].
    """
    sub_paths = []
    for i in range(len(path) - 1):
        link = [path[i], path[i+1]]
        links.append(link)
    return sub_paths


def get_valid_requests(nodes, links):
    """
    Read the requests input file and return a list of valid requests.
    For a request to be valid, there must be:
     1) a valid path between src and dest
     2) src and dest nodes must have enough resources for the request's cost,
        and the links between the nodes must have enough bandwidth.

    :param nodes: list of nodeObj objects (so resources can be allocated)
    :param links: list of linkObj objects (so bandwidth can be allocated)
    :return: a list of valid requests
    """
    valid_requests = []
    file_path = "../data/RequestInputData_30.txt"
    DEFAULT_BANDWIDTH = 5
    with open(file_path, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        for line in reader:
            # Make a request from the data. Get a list of paths from the request's
            # source to its destination. Then loop through the paths and
            # establish the shortest possible connection.
            request = requestObj(requestID=int(line[0]), src=int(line[1]), dest=int(line[2]),
                                 resource_requirement=int(line[3]))
            paths = list(nx.shortest_simple_paths(GRAPH, request.src, request.dest))
            for path in paths:
                successful_connection = connect_nodes( nodes[request.src - 1], nodes[request.dest - 1], request.resource_requirement )
                if successful_connection:
                    break  # break once a successful connection is established
            valid_requests.append(request)

    return valid_requests


def connect_nodes(src, dest, resource_cost):
    """
    Establish a connection between src and dest nodes.
    Return True if a connection is established; False otherwise.

    :param src: a nodeObj where the connection starts
    :param dest: a nodeObj where the connection ends
    :param resource_cost: (int) the resources that must be allocated from src and dest
    :return: True if a connection is established; False otherwise.
    """
    if src.nodeResources >= resource_cost and dest.nodeResources >= resource_cost:
        src.nodeResources -= resource_cost
        dest.nodeResources -= resource_cost
        return True
    return False


def allocate_bandwidth(path, bandwidth_cost, links):
    """
    Given a two-node path a list of links connecting nodes, allocate
    bandwidth the links specified in the path.

    :param path: a two-node path on the graph (e.g., [7, 5])
    :param bandwidth_cost: (int) the bandwidth that must be allocated from the
        link connecting the nodes
    :param links: a list of the graph's linkObj objects
    :return: True if the link has enough bandwidth to support this connection;
        False otherwise
    """
    for link in links:
        if link.linkSrc == path[0] and link.linkDest == path[1] or \
                link.linkSrc == path[1] and link.linkDest == path[0] and \
                link.linkBW >= bandwidth_cost:
            return True
    return False


if __name__ == '__main__':
    GRAPH = nx.Graph()  # Creates the graph

    # Create node and link objects by reading the input files.
    node_objects = get_nodes()
    link_objects = get_links()

    # Create a graph from the objects (store nodes as a list of integers; edges as a list of node connections)
    edges = [[link.linkSrc, link.linkDest] for link in link_objects]
    nodes = [node.nodeID for node in node_objects]
    GRAPH.add_edges_from(edges)
    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()  # Need this line to make sure the graph actually shows up

    # Process requests one by one (Determine if request is possible)
    # a) Find traversable path from point a to b
    # b) Allocate resources from each node and link.
    # c) Map path through network
    valid_requests = get_valid_requests(node_objects, link_objects)

    print("valid requests")
    for request in valid_requests:
        print(request)
    print("\nnodes")
    for node in node_objects:
        print(node.nodeID, ":", node.nodeResources)
    print("\nlinks")
    for link in link_objects:
        print(f"SRC: {link.linkSrc}, DEST: {link.linkDest}, BANDWIDTH: {link.linkBW}")
    print(edges)
