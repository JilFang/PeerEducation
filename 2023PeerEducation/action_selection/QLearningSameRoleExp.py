
from action_selection.AbsDecisionMaker import AbsDecisionMaker
import random


class QLearner:
    epsilon = 0.05
    alpha = 0.05
    gamma = 0.9

    def __init__(self):
        self.Q = []
        self.selected_a = None

    def ini(self, action_num):
        self.action_num = action_num
        self.Q.clear()
        for _ in range(action_num):
            self.Q.append(0)
        self.selected_a = None

    def reset(self):
        for i in range(0, self.action_num):
            self.Q[i] = 0
        self.selected_a = None

    def selectAction(self):
        maxQ = max(self.Q[:])
        bestActions = [i for i in range(self.action_num) if self.Q[i] == maxQ]
        notbestActions = [i for i in range(self.action_num) if self.Q[i] != maxQ]
        if random.random() < self.epsilon and len(notbestActions) > 0:
            # explore the non-best actions
            self.selected_a = random.choice(notbestActions)
        else:
            # exploit the best actions
            self.selected_a = random.choice(bestActions)
#         print self.selected_a
        return self.selected_a

    def update(self, r):
        self.Q[self.selected_a] = self.Q[self.selected_a] \
            +self.alpha * (r + self.gamma * max(self.Q[:]) - self.Q[self.selected_a])

#     def selectActionNoExplore(self):
#         maxQ = max(self.Q[:])
#         bestActions = [i for i in range(self.action_num) if self.Q[i] == maxQ]
#         action = random.choice(bestActions)
#         return action


class QLearningSameRoleExp(AbsDecisionMaker):

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)
        self.row_selector = QLearner()
        self.col_selector = QLearner()

    def iniDecisionInfo(self):
        self.row_selector.ini(self.agent.game.action_num)
        self.col_selector.ini(self.agent.game.action_num)

    def resetDecisionInfo(self):
        self.row_selector.reset()
        self.col_selector.reset()

    def selectRowAction(self):
        return self.row_selector.selectAction()

    def selectColAction(self):
        return self.col_selector.selectAction()

    def rowUpdate(self, row_reward, row_action, col_action):
        self.row_selector.update(row_reward)

    def colUpdate(self, col_reward, row_action, col_action):
        self.col_selector.update(col_reward)

