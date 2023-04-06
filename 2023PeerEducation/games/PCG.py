'''
Created on 6 Sep 2020

@author: w
'''
from games.TwoPlayerGame import TwoPlayerGame


class PCG(TwoPlayerGame):
    """
        Pure Coordination Game
    """
    # actions
#     LEFT = 0
#     RIGHT = 1
#    self.LEFT, self.RIGHT

    def __init__(self, action_num, *args, **kwargs):
        TwoPlayerGame.__init__(self, *args, **kwargs)
        self.action_num = action_num
        self.action_list = []
        for i in range(0, action_num):
            self.action_list.append(i)

        self.row_payoff_matrix = self.setPCGPayoff()
        self.col_payoff_matrix = self.setPCGPayoff()

    def setPCGPayoff(self):
        payoff_matrix = []
        for i in range(0, self.action_num):
            payoff = []
            for j in range(0, self.action_num):
                if i == j:
                    payoff.append(1)
                else:
                    payoff.append(-1)
            payoff_matrix.append(payoff)
        return payoff_matrix

    def isWin(self, reward):
        return reward > 0
