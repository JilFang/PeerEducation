'''
Created on 6 Sep 2020

@author: w
'''
from games.TwoPlayerGame import TwoPlayerGame


class PD(TwoPlayerGame):
    """
        prisoner's dilemma
    """
    # actions
#     0: Cooperate
#     1: Defect

    T = 5
    R = 3
    P = 1
    S = 0
    
    def __init__(self, *args, **kwargs):
        TwoPlayerGame.__init__(self, *args, **kwargs)
        action_num = 2
        self.action_num = action_num
        self.action_list = []
        for i in range(0, action_num):
            self.action_list.append(i)

        self.row_payoff_matrix = [[PD.R,PD.S]
                                  ,[PD.T,PD.P]]
        self.col_payoff_matrix = [[PD.R,PD.T]
                                  ,[PD.S,PD.P]]


