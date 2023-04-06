'''
Created on 6 Sep 2020

@author: w
'''
from games.TwoPlayerGame import TwoPlayerGame


class PCGN(TwoPlayerGame):
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

        self.row_payoff_matrix = self.setRowPayoff()
        self.col_payoff_matrix = self.setColPayoff()

    def setRowPayoff(self):
        return [[1, -1]
                 , [0, 2]]

    def setColPayoff(self):
        return [[1, 0]
                 , [-1, 2]]

    def isWin(self, reward):
        return reward > 0
