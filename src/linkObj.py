"""
Template for the link object class
"""


class linkObj(nodeObj): #subclass of the node object

    def __init__(self, linkID, linkBW, linkSrc, linkDest):
        self.linkID = linkID
        self.linkBW = linkBW
        self.linkSrc = linkSrc
        self.linkDest = linkDest
