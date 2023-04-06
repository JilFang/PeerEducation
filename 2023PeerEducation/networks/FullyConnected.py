'''
Created on 28 Aug 2020

@author: w
'''
from networks.AbsGraph import AbsGraph
import networkx as nx


class FullyConnected(AbsGraph):

    def __init__(self, *args, **kwargs):
        AbsGraph.__init__(self, *args, **kwargs)
        self.type = "FC"

    def createOnceByNetworkx(self, networkx_params):
        agent_number = networkx_params["agent_number"]
        return nx.erdos_renyi_graph(agent_number, 1)


