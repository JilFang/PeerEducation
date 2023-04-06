

import random
from queue import Queue

from action_selection.AlwaysNotTutorOrLearnBasedExperienceByEmotion import AlwaysNotTutorOrLearnBasedExperienceByEmotion
from action_selection.AlwaysNotTutorOrLearnBasedNeighborByEmotion import AlwaysNotTutorOrLearnBasedNeighborByEmotion
from action_selection.AlwaysTutorAndLearnBasedExperienceByEmotion import AlwaysTutorAndLearnBasedExperienceByEmotion
from action_selection.AlwaysTutorAndLearnBasedNeighborByEmotion import AlwaysTutorAndLearnBasedNeighborByEmotion
from action_selection.BasedExperience import BasedExperience
from action_selection.BasedExperienceByEmotion import BasedExperienceByEmotion
from action_selection.BasedNeighbor import BasedNeighbor
from action_selection.BasedNeighborByEmotion import BasedNeighborByEmotion
from action_selection.BasedNeighborP import BasedNeighborP
from agents.Agent import Agent
from action_selection.WSLS import WSLS
from action_selection.WSLpS import WSLpS
from action_selection.ImitateOppoAction import ImitateOppoAction
from action_selection.AlwaysTutorAndLearn import AlwaysTutorAndLearn
from action_selection.PImitateOppoAction import PImitateOppoAction
from action_selection.HCR import HCR
from action_selection.AlwaysNotTutorOrLearn import AlwaysNotTutorOrLearn


class GamePlayAgent(Agent):
    """
        consider two agents interacting,
        so only a row player agent and a column player agent.
        statistics also correspond to row/column play interactions
    """

    def __init__(self, *args, **kwargs):
        Agent.__init__(self, *args, **kwargs)
        self.ass_name_to_obj = {
                    "WSLS":WSLS(self)
                , "WSLpS":WSLpS(self)
                , "ImitateOppoAction":ImitateOppoAction(self)
                , "AlwaysTutorAndLearn":AlwaysTutorAndLearn(self)
                , "AlwaysNotTutorOrLearn":AlwaysNotTutorOrLearn(self)
                , "PImitateOppoAction":PImitateOppoAction(self)
                , "HCR":HCR(self)
#                 , "WSLpS":WSLpS(self)
                , "BasedExperience": BasedExperience(self)
                , "BasedNeighbor": BasedNeighbor(self)
                , "BasedExperienceByEmotion": BasedExperienceByEmotion(self)
                , "BasedNeighborByEmotion": BasedNeighborByEmotion(self)
                , "AlwaysTutorAndLearnBasedExperienceByEmotion": AlwaysTutorAndLearnBasedExperienceByEmotion(self)
                , "AlwaysNotTutorOrLearnBasedExperienceByEmotion": AlwaysNotTutorOrLearnBasedExperienceByEmotion(self)
                , "AlwaysTutorAndLearnBasedNeighborByEmotion": AlwaysTutorAndLearnBasedNeighborByEmotion(self)
                , "AlwaysNotTutorOrLearnBasedNeighborByEmotion": AlwaysNotTutorOrLearnBasedNeighborByEmotion(self)
                , "BasedNeighborP": BasedNeighborP(self)
                }

        self.queue = Queue()
        self.queue.queue.clear()

        self.game = None
        self.ass = None
        # action in an ongoing episode
        self.row_action = None
        self.col_action = None
        # action in last episode or initial
        self.last_row_action = None
        self.last_col_action = None

        # statistics
        self.inter_num = 0
        self.learning_num = 0

        self.row_reward_total = 0
        self.col_reward_total = 0

        # e.g., [2,3] action0 taken 2 times, action1 taken 3 times
#         self.action_taken_num = []
#         self.action_change_num = 0
#         self.r_total = 0
#         self.generation_num = 0
#         self.last_r = None
#         self.episode_num = 0

    def clearQueue(self):
        self.queue.queue.clear()

    def clearEmotion(self):
        self.Joy = 0
        self.Fear = 0
        self.Angry = 0
        self.Sadness = 0
        self.Pressure = 0
        self.Emotion = [self.Joy, self.Fear, self.Angry, self.Pressure]

    def setGame(self, g):
        self.game = g

    def useAss(self, ass_name):
        """
            start to use an action selection strategy
            before a generation starts
        """
        self.ass = self.ass_name_to_obj[ass_name]
        self.ass.iniDecisionInfo()
    
    def useRolColActions(self, row_action, col_action):
        self.row_action = row_action
        self.col_action = col_action
        
        self.last_row_action = row_action
        self.last_col_action = col_action

    def prepareForTrial(self):
        self.ass.resetDecisionInfo()
        self.inter_num = 0
        self.learning_num = 0

        self.clearEmotion()
        self.clearQueue()
        self.row_reward_total = 0
        self.col_reward_total = 0
        self.row_action = random.randint(0, 1)
        self.col_action = random.randint(0, 1)
        self.last_row_action = self.row_action
        self.last_col_action = self.col_action
#         self.action_taken_num.clear()
#         for _ in range(self.game.action_num):
#             self.action_taken_num.append(0)

#         self.action_change_num = 0
#         self.last_action = random.choice(self.game.action_list)  # self.ass.selectAction()
#         self.r_total = 0


    def selRowAction(self, ag):
        self.row_action = self.ass.selectRowAction(ag)
    #
    # def selRowAction(self, a, b, num):
    #     self.row_action = self.ass.selectRowAction(a, b, num)

    def selColAction(self, ag):
        self.col_action = self.ass.selectColAction(ag)

    # def selColAction(self, a, b, num):
    #     self.col_action = self.ass.selectColAction(a, b, num)

    def handleInteractionUpdateWith(self, col_agent):
        """
            use PD game
            row player handles a play interaction
        """
        ra = self.row_action
        ca = col_agent.col_action

        # get row and col rewards based on PD game
        row_reward = self.game.rowReward(ra, ca)
        col_reward = self.game.colReward(ra, ca)
#         print(ra, ca, row_reward, col_reward)
        # update decision information of action selection strategy
        # result1 = self.ass.rowUpdate(row_reward, ra, ca)
        # result2 = col_agent.ass.colUpdate(col_reward, ca, ra)
        result1 = self.ass.rowUpdate(ra, ca)
        result2 = col_agent.ass.colUpdate(ca, ra)
        # self.ass.rowUpdate(ra, ca)
        # col_agent.ass.colUpdate(ca, ra)

        result = [result1, result2]
        # update statistics
        # self.updateStat(ra, ca)
        # col_agent.updateStat(ra, ca)

        return result
        self.updateRowStat(row_reward)
        col_agent.updateColStat(col_reward)

    def updateStat(self, ra, ca):
        self.inter_num += 1
        if self.isLearning(ra, ca):
            self.learning_num += 1

#         self.row_action_taken_num[self.row_action] += 1
#         self.col_action_taken_num[self.col_action] += 1
#         if self.action != self.last_action:
#             self.action_change_num += 1

    def isLearning(self, ra, ca):
        return ra == 0 and ca == 0

    def updateRowStat(self, row_reward):
        self.last_row_action = self.row_action
        self.row_reward_total += row_reward

    def updateColStat(self, col_reward):
        self.last_col_action = self.col_action
        self.col_reward_total += col_reward

    def getTotalReward(self):
        return self.row_reward_total + self.col_reward_total

