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


def filter_requests(requests, nodes, links, graph):
    """
    Read a list of requests and filter out the invalid ones.
    For a request to be valid, there must be:
     1) a valid path between the request's src and dest
     2) src and dest nodes must have enough resources for the request's cost,
        and the links between the nodes must have enough bandwidth.

    :param requests: list of requestObj objects to filter
    :param nodes: nodeObj list (resources will be allocated)
    :param links: linkObj list (bandwidth will be allocated)
    :param graph: nx graph
    :return: a list of valid requests
    """
    valid_requests = []
    DEFAULT_BANDWIDTH_COST = 5
    for request in requests:
        valid_connection = True
        paths = list(nx.shortest_simple_paths(graph, request.src, request.dest))
        for path in paths:
            sub_paths = get_sub_paths(path)
            for sub_path in sub_paths:
                enough_bandwidth = allocate_bandwidth(sub_path, DEFAULT_BANDWIDTH_COST, links)
                if not enough_bandwidth:
                    valid_connection = False
                    break
            if not valid_connection:
                break
            successful_connection = connect_nodes(nodes[request.src - 1], nodes[request.dest - 1],
                    request.resource_requirement)
            if successful_connection:
                # break once a successful connection is established
                # (no need to search other paths once this request is filled)
                valid_requests.append(request)
                break
    return valid_requests


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


def get_requests():
    """Create request objects from input file."""
    requests = []
    file_path = "../data/RequestInputData_30.txt"
    with open(file_path, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        for line in reader:
            requests.append( requestObj(requestID=int(line[0]), src=int(line[1]),
                    dest=int(line[2]), resource_requirement=int(line[3])) )
    return requests


def get_sub_paths(path):
    """
    Given a path from a src node to a dest node (e.g. [1,5,2],
    return a list of the links between them (e.g., [[1,5], [5,2]].
    """
    sub_paths = []
    for i in range(len(path) - 1):
        link = [path[i], path[i+1]]
        sub_paths.append(link)
    return sub_paths


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
    requests = get_requests()
    requests = filter_requests(requests, node_objects, link_objects, GRAPH)
    for request in requests:
        print(request)

