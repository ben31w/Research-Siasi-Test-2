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


def get_links_from_path(path):
    """
    Given a path from a src node to a dest node (e.g. [1,5,2],
    return a list of the links between them (e.g., [[1,5], [5,2]].
    """
    links = []
    for i in range(len(path) - 1):
        link = [path[i], path[i+1]]
        links.append(link)
    return links


def get_valid_requests():
    """
    Read the requests input file and return a list of valid requests.
    For a request to be valid, there must be:
     1) a valid path between src and dest
     2) src and dest nodes must have enough resources for the request's cost,
        and the links between the nodes must have enough bandwidth.

    :param edges: a list of edges in the graph (e.g., [[7,5], [6,7], etc.]
    :return: valid requests from input file
    """
    valid_requests = []
    file_path = "../data/RequestInputData_30.txt"
    DEFAULT_BANDWIDTH = 5
    with open(file_path, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        for line in reader:
            request = requestObj(requestID=int(line[0]), src=int(line[1]), dest=int(line[2]),
                                 resource_requirement=int(line[3]))
            paths = list(nx.shortest_simple_paths(GRAPH, request.src, request.dest))
            for path in paths:
                # Find a valid path.
                # First check src and dest nodes, and allocate resources.
                source = node_objects[request.src - 1]
                destination = node_objects[request.dest - 1]
                cost = request.resource_requirement
                if source.nodeResources - cost >= 0 and destination.nodeResources - cost >= 0:
                    source.nodeResources -= cost
                    destination.nodeResources -= cost

                    # Next check the links between src and dest, and allocate bandwidth.
                    links_between_src_dest = get_links_from_path(path)

                    break  # break when we find a valid path
            valid_requests.append(request)

    return valid_requests


def connect_nodes(src, dest, bandwidth_cost, links):
    """
    Search through the links and attempt to establish a connection between src and dest.
    There must be a link connecting src and dest, with enough bandwidth.

    If such a link is found, a connection is establish by subtracting bandwidth
    from the link, and the method returns True.

    If no link is found, return False.

    :param src: a node ID (int)
    :param dest: a node ID (int)
    :param bandwidth_cost: the cost of this connection (int)
    :param links: a list of linkObj objects.
    :return: True if a src-dest connection is found and established
    """
    for link in links:
        if (link.linkSrc == src and link.linkDest == dest or \
                link.linkSrc == dest and link.linkDest == src) and \
                link.linkBW > bandwidth_cost:
            link.linkBW -= bandwidth_cost
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
    valid_requests = get_valid_requests()


    # for request in valid_requests:
    #     print(request)
    # print()
    # for node in node_objects:
    #     print(node.nodeID, ":", node.nodeResources)
    # print()
    connect_nodes(5,7,5,link_objects)
    for link in link_objects:
        print(f"SRC: {link.linkSrc}, DEST: {link.linkDest}, BANDWIDTH: {link.linkBW}")
    print(edges)
