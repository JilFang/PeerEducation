
from action_selection.AbsDecisionMaker import AbsDecisionMaker
import random


class HCRLearner:

    def __init__(self):
        self.action_total_r = []
        self.selected_a = None

    def ini(self, action_num):
        self.action_num = action_num
        self.action_total_r.clear()
        for _ in range(action_num):
            self.action_total_r.append(0)
        self.selected_a = None

    def reset(self):
        for i in range(0, self.action_num):
            self.action_total_r[i] = 0
        self.selected_a = None

    def selectAction(self):
        max_total_r = max(self.action_total_r[:])
        best_actions = [i for i in range(self.action_num) if self.action_total_r[i] == max_total_r]
        self.selected_a = random.choice(best_actions)
        return self.selected_a

    def update(self, r):
        self.action_total_r[self.selected_a] += r


class HCR(AbsDecisionMaker):

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)
        self.row_selector = HCRLearner()
        self.col_selector = HCRLearner()

    def iniDecisionInfo(self):
        self.row_selector.ini(2)
        self.col_selector.ini(2)

    def resetDecisionInfo(self):
        self.row_selector.reset()
        self.col_selector.reset()

    def selectRowAction(self, ag):
        return self.row_selector.selectAction()

    def selectColAction(self, ag):
        return self.col_selector.selectAction()

    def rowUpdate(self, row_reward, row_action, col_action):
        self.row_selector.update(row_reward)

    def colUpdate(self, col_reward, row_action, col_action):
        self.col_selector.update(col_reward)

