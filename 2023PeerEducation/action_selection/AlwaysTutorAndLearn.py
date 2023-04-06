
from action_selection.AbsDecisionMaker import AbsDecisionMaker


class AlwaysTutorAndLearn(AbsDecisionMaker):
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
        return self.row_action

    def selectColAction(self, ag):
        if self.agent.queue.qsize() == 10:
            self.agent.queue.get()
        self.agent.queue.put(self.col_action)
        return self.col_action

    def rowUpdate(self,rd, row_action, col_action):
        self.agent.queue.queue.clear()

    def colUpdate(self,rd, row_action, col_action):
        self.agent.queue.queue.clear()