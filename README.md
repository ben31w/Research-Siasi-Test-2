# Research-Siasi-Test-2
Second litmus test.
Overview:
You are to create a small local working simulation of a network in python. The network will consist of 8 nodes and 16 links. 
You are then to read in requests from a file. Then process those requests through the network. Then output those requests onto an output file. 
You should be creating a class for the nodes, links and requests.

Pseudocode: (General idea outline of how things should run)
Read input graph data(nodes, links, requests)

Create objects using input data

Create graph of network using nodes and links

Process requests one by one (Determine if request is possible)
  a) Find traversable path from point a to b
  b) Allocate resources from each node and link.
  c) Map path through network
  
Create output file showing in order what requests passed and failed.
  
FAILURE: Requests can fail because a node might not have enough resources, node/link might not have enough bandwidth. If a node runs out of resources it can still be used for traversal but CANNOT be used for mapping. 

Node Class:
The node class will have blank parameters. The NodeID, integer value indicating the identification number of the node. NodeResources, integer value indicating the current number of available resources the node has at any given moment. You will also have a parameter indicating whether a node is online or offline.

Link Class:
The link class will have a blank number of parameters. The LinkID, integer value indicating the identification number of the link. LinkBandwidth, integer value indicating the current number of available bandwidth the link has at any given moment. LinkSource, a pointer or value pointing to the corresponding node that the link is starting at. As well as LinkDestination, a pointer or value indicating the node that the link is ending at. 

Request Class:
The request class will have an integer value called RequestID, indicating the number of the request object. Each object will also have a src, and dest parameter indicating the beginning node and ending node of the given request. Then each request object will also have a resource_requirement integer that indicates the amount of resources needed to be processed by nodes during the requests traversal throughout the network.
