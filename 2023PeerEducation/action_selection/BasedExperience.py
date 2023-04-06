from queue import Queue

from tool.Tools import Tools
from action_selection.AbsDecisionMaker import AbsDecisionMaker
import random


class BasedExperience(AbsDecisionMaker):
    """
    """

    def __init__(self, *args, **kwargs):
        AbsDecisionMaker.__init__(self, *args, **kwargs)

        self.row_action = random.randint(0, 1)
        self.col_action = random.randint(0, 1)

    def selectRowAction(self, ag):
        if ag.queue.qsize() > 0:
            self.row_action = Tools.findQueueMost(ag.queue)
        else:
            self.row_action = random.randint(0, 1)
        return self.row_action

    def selectColAction(self, ag):
        if ag.queue.qsize() > 0:
            self.col_action = Tools.findQueueMost(ag.queue)
        else:
            self.col_action = random.randint(0, 1)
        return self.col_action

    def rowUpdate(self, ra, row_action, col_action):
        if self.agent.queue.qsize() == 10:
            self.agent.queue.get()
        self.agent.queue.put(self.row_action)

    def colUpdate(self, ra, col_action, row_action):
        if self.agent.queue.qsize() == 10:
            self.agent.queue.get()
        self.agent.queue.put(self.col_action)

