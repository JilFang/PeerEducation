'''
Created on 9 Sep 2020

@author: w
'''


class TwoPlayerGame:

    def __init__(self):
        self.row_payoff_matrix = None
        self.col_payoff_matrix = None

    def rowReward(self, row_action, col_action):
#         print(self.row_payoff_matrix)
        return self.row_payoff_matrix[row_action][col_action]

    def colReward(self, row_action, col_action):
        return self.col_payoff_matrix[row_action][col_action]
