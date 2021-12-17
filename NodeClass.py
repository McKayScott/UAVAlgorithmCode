class gridNode:
    def __init__(self, newX, newY, newZ, uI):
        self.x_val = newX
        self.y_val = newY
        self.z_val = newZ
        self.neighborNodes = []
        self.uniqueIdentifier = uI
        self.parentNode = None
        self.prevNodes = []
        self.score = -1
    
    def addNeighbor(self, nnn):
        self.neighborNodes.append(nnn)

    def setParent(self, pNode):
        self.parentNode = pNode

    def addPrevNode(self, pNode):
        self.prevNodes.append(pNode)

    def getParent(self):
        return self.parentNode

    def setScore(self, newScore):
        self.score = newScore

    def getScore(self):
        return self.score