'''
Created on 20 Aug 2020

@author: w
'''
from networks.AbsGraph import AbsGraph
import networkx as nx


class ScaleFree(AbsGraph):

    def __init__(self, *args, **kwargs):
        AbsGraph.__init__(self, *args, **kwargs)
        self.type = "SF"
#         self.sf_num_edges_attach = None

    def createOnceByNetworkx(self, networkx_params):
        agent_number = networkx_params["agent_number"]
        self.sf_num_edges_attach = networkx_params["sf_num_edges_attach"]
        return nx.barabasi_albert_graph(agent_number, self.sf_num_edges_attach)

    def getSavingData(self):
        saving_data = AbsGraph.getSavingData(self)
        saving_data.update({"sf_num_edges_attach":self.sf_num_edges_attach})
        return saving_data


    def getManyNeibNodesPartition(self):
        many_nb_nodes = []
        not_many_nb_nodes = []
        for ag_id in self.G.nodes():
            if len(self.G.neighbors(ag_id)) >= 5:
                many_nb_nodes.append(ag_id)
            else:
                not_many_nb_nodes.append(ag_id)
#         print(many_nb_nodes)
#         print(not_many_nb_nodes)
        mnn_prop = len(many_nb_nodes) / self.nodeNumber()
        return many_nb_nodes, not_many_nb_nodes, mnn_prop
