
class requestObj:
    def __init__(self, requestID, src, dest, resource_requirement):
        self.requestID = requestID
        self.src = src
        self.dest = dest
        self.resource_requirement = resource_requirement

    def __str__(self):
        return f"{self.requestID};{self.src};{self.dest};{self.resource_requirement}"