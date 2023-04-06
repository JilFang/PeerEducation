'''
Created on 20 Aug 2020

@author: w
'''
from networks.AbsGraph import AbsGraph
import networkx as nx


class Grid(AbsGraph):

    def __init__(self, *args, **kwargs):
        AbsGraph.__init__(self, *args, **kwargs)
        self.type = "GR"

    def createOnceByNetworkx(self, networkx_params):
        # agent_number = networkx_params["agent_number"]
        self.gr_row_num = networkx_params["gr_row_num"]
        self.gr_col_num = networkx_params["gr_col_num"]
        return Grid.grid_2d(self.gr_row_num, self.gr_col_num)

    def getSavingData(self):
        saving_data = AbsGraph.getSavingData(self)
        saving_data.update({"gr_row_num":self.gr_row_num})
        saving_data.update({"gr_col_num":self.gr_col_num})
        return saving_data

    @staticmethod
    def grid_2d(gr_row_num, gr_col_num):
        G = nx.grid_2d_graph(gr_row_num, gr_col_num)

        nodeToId = {}
        i = 0
        for node in list(G.nodes()):
            nodeToId[node] = i
            i += 1

        adjlist = []
        for node in list(G.nodes()):
            edges = G.edges(node)
            edgeList = []
            edgeList.append(nodeToId[node])
            for edge in edges:
        #         print nodeToId[edge[1]]
                edgeList.append(nodeToId[edge[1]])

            edgStr = ' '.join(str(x) for x in edgeList)
            adjlist.append(edgStr)

        G = nx.parse_adjlist(adjlist, nodetype = int)
        return G
