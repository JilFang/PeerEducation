


class Agent(object):

    def __init__(self, neighbors = []):
        self.neighbors = neighbors
        self.local_agents = [self]
        for nb in self.neighbors:
            self.local_agents.append(nb)

    def clearNeighbors(self):
        self.neighbors.clear()
        self.local_agents.clear()
        self.local_agents.append(self)

    def addNeighbor(self, nb):
        self.neighbors.append(nb)
        self.local_agents.append(nb)
