
from action_selection.AbsDecisionMaker import AbsDecisionMaker


class AlwaysTutorAndLearnBasedExperienceByEmotion(AbsDecisionMaker):
    """
        requires a game to have aggressive_action
    """

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)
        self.row_action = 0
        self.col_action = 0

    def iniDecisionInfo(self):
        self.row_action = 0
        self.col_action = 0

    def selectRowAction(self, ag):
        if self.agent.queue.qsize() == 10:
            self.agent.queue.get()
        self.agent.queue.put(self.row_action)
        self.rowUpdate(self.row_action, ag.col_action)
        return self.row_action

    def selectColAction(self, ag):
        if self.agent.queue.qsize() == 10:
            self.agent.queue.get()
        self.agent.queue.put(self.col_action)
        self.colUpdate(self.col_action, ag.row_action)
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

    def colUpdate(self, row_action, col_action):
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