
from action_selection.AbsDecisionMaker import AbsDecisionMaker


class AlwaysNotTutorOrLearn(AbsDecisionMaker):
    """
        requires a game to have aggressive_action
    """

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)

        self.row_action = 1
        self.col_action = 1

    def iniDecisionInfo(self):
        self.row_action = 1
        self.col_action = 1

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

    def rowUpdate(self, ra, row_action, col_action):
        self.agent.queue.queue.clear()

    def colUpdate(self, ra, row_action, col_action):
        self.agent.queue.queue.clear()
