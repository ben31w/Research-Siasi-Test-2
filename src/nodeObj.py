"""
Template for the node object class
"""


class nodeObj:

    def __init__(self, nodeID, nodeResources, nodeStatus, nodeCost):
        self.nodeID = nodeID
        self.nodeResources = nodeResources
        self.nodeStatus = nodeStatus
        self.nodeCost = nodeCost
