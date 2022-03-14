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
    valid_requests = []
    file_path = "../data/RequestInputData_30.txt"
    with open(file_path, 'rt') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        DEFAULT_BANDWIDTH = 5
        for line in reader:
            request = requestObj(requestID=int(line[0]), src=int(line[1]), dest=int(line[2]), resource_requirement=int(line[3]))
            paths = list(nx.shortest_simple_paths(GRAPH, request.src, request.dest))
            for path in paths:
                # Find a valid path (src and dest nodes must have enough resources for the request's requirement).
                # Then allocate resources from each node (and link eventually...)
                if node_objects[request.src-1].nodeResources - request.resource_requirement >= 0 \
                        and node_objects[request.dest-1].nodeResources - request.resource_requirement >= 0:
                    node_objects[request.src-1].nodeResources -= request.resource_requirement
                    node_objects[request.dest-1].nodeResources -= request.resource_requirement
                    break  # break when we find a valid path
            valid_requests.append(request)


    for request in valid_requests:
        print(request)
    print()
    for node in node_objects:
        print(node.nodeID, ":", node.nodeResources)
