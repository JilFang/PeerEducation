
from action_selection.AbsDecisionMaker import AbsDecisionMaker
import random


class ImitateOppoAction(AbsDecisionMaker):
    """
    """

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)
        """
            has info for coherent logic with other methods
            actually WSLS does not need to store info
            just shift if lose
        """
        self.next_row_action = None
        self.next_col_action = None

    def resetDecisionInfo(self):
#         self.next_action = self.agent.last_action
        self.next_row_action = random.choice(self.agent.game.action_list)
        self.next_col_action = random.choice(self.agent.game.action_list)

    def selectRowAction(self, ag):
        return self.next_row_action

    def selectColAction(self, ag):
        return self.next_col_action

    def rowUpdate(self, row_reward, row_action, col_action):
        self.next_col_action = col_action

    def colUpdate(self, col_reward, row_action, col_action):
        self.next_row_action = row_action
