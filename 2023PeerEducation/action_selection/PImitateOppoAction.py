
from action_selection.AbsDecisionMaker import AbsDecisionMaker
import random


class PImitateOppoAction(AbsDecisionMaker):
    """
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

    def selectRowAction(self):
        return self.next_row_action

    def selectColAction(self):
        return self.next_col_action

    def rowUpdate(self, row_reward, row_action, col_action):
        if random.random() < self.p:
            self.next_col_action = col_action

    def colUpdate(self, col_reward, row_action, col_action):
        if random.random() < self.p:
            self.next_row_action = row_action
