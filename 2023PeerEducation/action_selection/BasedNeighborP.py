
from tool.Tools import Tools
from action_selection.AbsDecisionMaker import AbsDecisionMaker

import random



class BasedNeighborP(AbsDecisionMaker):
    """
    """

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)

        self.row_action = random.randint(0, 1)
        self.col_action = random.randint(0, 1)


    def selectRowAction(self, ag):
        l = []
        count = 0
        for nb in self.agent.local_agents:
            if count != 0:
                l.append(nb.row_action)
            count = count + 1
        self.row_action = Tools.findMostP(l)
        return self.row_action

    def selectColAction(self, ag):
        l = []
        count = 0
        for nb in self.agent.local_agents:
            if count != 0:
                l.append(nb.col_action)
            count = count + 1
        self.col_action = Tools.findMostP(l)
        return self.col_action

    def rowUpdate(self, ra,row_action, col_action):
        pass

    def colUpdate(self, ra,col_action, row_action):
        pass

