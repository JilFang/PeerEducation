

class AbsDecisionMaker(object):

    def __init__(self, agent):
        """
            a decision maker belongs to an agent，and
            can visit the agent's info like game, neighbors, etc.
        """
        self.agent = agent

    def iniDecisionInfo(self):
        """
            after a game is set to an agent,
            initialise decision info based on the game
        """
        pass

    def resetDecisionInfo(self):
        pass

    def selectRowAction(self):
        pass
    
    def selectColAction(self):
        pass

    def rowUpdate(self, row_reward, row_action, col_action):
        pass

    def colUpdate(self, col_reward, row_action, col_action):
        pass