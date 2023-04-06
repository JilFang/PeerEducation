
from action_selection.AbsDecisionMaker import AbsDecisionMaker
import random


class BasedExperienceByEmotion(AbsDecisionMaker):
    """
    """

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)

        self.row_action = random.randint(0, 1)
        self.col_action = random.randint(0, 1)

    def selectRowAction(self, ag):
        flag = self.findMaxThreeEmotion()
        if len(flag) == 1:
            if flag[0] == 'Fear':
                self.row_action = 0
            elif flag[0] == 'Pressure':
                num = random.randint(1, 10)
                if num > 2:
                    self.row_action = 0
                else:
                    self.row_action = 1
            elif flag[0] == 'Angry':
                self.row_action = 1
        else:
            self.row_action = random.randint(0, 1)
        return self.row_action

    def selectColAction(self, ag):
        flag = self.findMaxThreeEmotion()
        if len(flag) == 1:
            if flag[0] == 'Fear':
                self.col_action = 0
            elif flag[0] == 'Pressure':
                num = random.randint(1, 10)
                if num > 2:
                    self.col_action = 0
                else:
                    self.col_action = 1
            elif flag[0] == 'Angry':
                self.col_action = 1
        else:
            self.col_action = random.randint(0, 1)

        return self.col_action

    def rowUpdate(self, row_action, col_action):
        if row_action == 0 and col_action == 0:
            self.agent.Emotion[0] = self.agent.Emotion[0] + 1
        elif row_action == 1 and col_action == 0:
            self.agent.Emotion[1] = self.agent.Emotion[1] + 1
        elif row_action == 0 and col_action == 1:
            self.agent.Emotion[2] = self.agent.Emotion[2] + 1
        elif row_action == 1 and col_action == 1:
            self.agent.Emotion[3] = self.agent.Emotion[3] + 1
        emotion = self.findMaxThreeEmotion()
        if len(emotion) == 1:
            return emotion[0]
        else:
            return None

    def colUpdate(self, col_action, row_action):
        # print(row_action, col_action)
        if col_action == 0 and row_action == 0:
            self.agent.Emotion[0] = self.agent.Emotion[0] + 1
        elif col_action == 1 and row_action == 0:
            self.agent.Emotion[1] = self.agent.Emotion[1] + 1
        elif col_action == 0 and row_action == 1:
            self.agent.Emotion[2] = self.agent.Emotion[2] + 1
        elif col_action == 1 and row_action == 1:
            self.agent.Emotion[3] = self.agent.Emotion[3] + 1
        emotion = self.findMaxThreeEmotion()
        if len(emotion) == 1:
            return emotion[0]
        else:
            return None

    def findMaxThreeEmotion(self):

        highest = max(self.agent.Emotion)
        flag = []
        for i in range(len(self.agent.Emotion)):
            if highest == self.agent.Emotion[i]:
                if i == 0:
                    flag.append("Joy")
                elif i == 1:
                    flag.append("Fear")
                elif i == 2:
                    flag.append("Angry")
                elif i == 3:
                    flag.append("Pressure")
        return flag