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
# Need these for path finding and graphing
import networkx as nx   # K-shortest paths library
import matplotlib.pyplot as plt # Create the graph

def set_edges(link_list):
    visited_links = []

    for link in link_list:
        u = link[0]
        v = link[1]
        temp = [u, v]
        if link not in visited_links:
            edges.append(temp)
            visited_links.append(link)


if __name__ == '__main__':
    GRAPH = nx.Graph()  # Creates the graph

    edges = [[1, 2], [1, 4], [2, 3], [3, 5], [2, 6], [6, 3]]  # List of the links or edges between the graph
    nodes = [1, 2, 3, 4, 5, 6]  # List of the nodes or points on the graph

    GRAPH.add_edges_from(edges)

    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show() # Need this line to make sure the graph actually shows up
