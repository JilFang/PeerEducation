'''
Created on 20 Aug 2020

@author: w
'''
from networks.AbsGraph import AbsGraph
import networkx as nx


class SmallWorld(AbsGraph):

    def __init__(self, *args, **kwargs):
        AbsGraph.__init__(self, *args, **kwargs)
        self.type = "SW"
        """
            createOnceByNetworkx() is called by AbsGraph
            where self.sw_avg_nb_num is set to AbsGraph
            
            if set "self.sw_avg_nb_num = None" here,
            sw_avg_nb_num is in SmallWorld.
            getSavingData() is called by SmallWorld, which visits 
            self.sw_avg_nb_num in SmallWorld and get None
            
            if not set, getSavingData() visits
            self.sw_avg_nb_num in AbsGraph
        """
#         self.sw_avg_nb_num = None
#         self.sw_rw_prob = None

    def createOnceByNetworkx(self, networkx_params):
        agent_number = networkx_params["agent_number"]
        self.sw_avg_nb_num = 5 #networkx_params["sw_avg_nb_num"]#每个平均邻居数
        self.sw_rw_prob = 0.5 #networkx_params["sw_rw_prob"]#0.5 随机性
        return nx.watts_strogatz_graph(agent_number
                                   , self.sw_avg_nb_num
                                   , self.sw_rw_prob)

    def getSavingData(self):
        saving_data = AbsGraph.getSavingData(self)  # {}
#         print (self.sw_avg_nb_num, self.sw_rw_prob, self.type)
        saving_data.update({"sw_avg_nb_num":self.sw_avg_nb_num})
        saving_data.update({"sw_rw_prob":self.sw_rw_prob})
#         print (saving_data)
        return saving_data

    def getEqualCheckingData(self):
        equalparams = AbsGraph.getEqualCheckingData(self)
        equalparams.update({"sw_avg_nb_num":self.sw_avg_nb_num})
        equalparams.update({"sw_rw_prob":self.sw_rw_prob})
        return equalparams
