
from action_selection.AbsDecisionMaker import AbsDecisionMaker
import random


class WSLpS(AbsDecisionMaker):
    """
        Win Stay Lose Shift, 
        the version in the Peer Education Area
    """

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)
        self.p = 0.5
        """
            has info for coherent logic with other methods
            actually WSLS does not need to store info
            just shift if lose
        """
        self.next_row_action = None
        self.next_col_action = None

    def setP(self, p):
        self.p = p

    def resetDecisionInfo(self):
#         self.next_action = self.agent.last_action
        self.next_row_action = random.choice(self.agent.game.action_list)
        self.next_col_action = random.choice(self.agent.game.action_list)

    def selectRowAction(self, ag):
        return self.next_row_action

    def selectColAction(self, ag):
        return self.next_col_action

    def rowUpdate(self, row_reward, row_action, col_action):
        if not self.agent.game.isWin(row_reward):
            # lose, probably shift action
            if random.random() < self.p:
                self.next_row_action = 1 - self.next_row_action
        # win, stay using current action

    def colUpdate(self, col_reward, row_action, col_action):
        if not self.agent.game.isWin(col_reward):
            if random.random() < self.p:
                self.next_col_action = 1 - self.next_col_action

