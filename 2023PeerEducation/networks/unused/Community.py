'''
Created on 20 Aug 2020

@author: w
'''
from networks.AbsGraph import AbsGraph
import networkx as nx
import math


class Community(AbsGraph):

    def __init__(self, *args, **kwargs):
        AbsGraph.__init__(self, *args, **kwargs)
        self.type = "CM"
#         self.cm_avg_cm_size = None
#         self.cm_sd = None
#         self.cm_cm_num = None
#         self.cm_p_in = None
#         self.cm_p_out = None

    def createOnceByNetworkx(self, networkx_params):
#         agent_number = networkx_params["agent_number"]
        self.cm_cm_num = networkx_params["cm_cm_num"]
        self.cm_avg_cm_size = networkx_params["cm_avg_cm_size"]
        self.cm_sd = networkx_params["cm_sd"]
#         self.cm_cm_num = agent_number / self.cm_avg_cm_size

        self.agent_number = self.cm_cm_num * self.cm_avg_cm_size
#         print(self.agent_number)
        self.cm_p_in = self.cm_avg_cm_size * self.cm_sd / self.cm_avg_cm_size
        self.cm_p_out = self.cm_avg_cm_size * (1 - self.cm_sd) / (self.agent_number - self.cm_avg_cm_size)

        self.cm_p_in = round(self.cm_p_in, 5)
        self.cm_p_out = round(self.cm_p_out, 5)

        variance = 1
        return nx.gaussian_random_partition_graph(self.agent_number
                                          , self.cm_avg_cm_size
                                          , self.cm_avg_cm_size / variance
                                          , self.cm_p_in, self.cm_p_out
                                          , directed = False
                                          )

    def getSavingData(self):
        saving_data = AbsGraph.getSavingData(self)
        saving_data.update({"cm_avg_cm_size":self.cm_avg_cm_size})
        saving_data.update({"cm_cm_num":self.cm_cm_num})
        saving_data.update({"cm_p_in":self.cm_p_in})
        saving_data.update({"cm_p_out":self.cm_p_out})
        saving_data.update({"cm_sd":self.cm_sd})
        return saving_data

    def getEqualCheckingData(self):
        equalparams = AbsGraph.getEqualCheckingData(self)
        equalparams.update({"cm_avg_cm_size":self.cm_avg_cm_size})
        equalparams.update({"cm_cm_num":self.cm_cm_num})
        return equalparams
