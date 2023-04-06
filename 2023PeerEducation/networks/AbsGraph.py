'''
Created on 20 Aug 2020

@author: w
'''
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from tool.Tools import Tools
import sys
from tables.TNetworks import TNetworks
from tool.DrawTools import DrawTools


class AbsGraph(object):
    """
        use networkx to generate graphs (networks)
        stored_adjlist: use adjlist module to store in DB
        stored_id: read id of a network from DB
    """

    def __init__(self
                 , stored_adjlist = None
                 , stored_id = None
                 , is_from_db = False
                 , networkx_params = None
                 ):
        self.G = None  # follow the package of networkx
        self.type = None
        if stored_adjlist != None:
            assert stored_id != None
            self.net_id = stored_id  #
            self.G = self.loadByStoredAdjlist(stored_adjlist)
        else:
            assert networkx_params != None
            if is_from_db:
                self.readFromDbByParams(networkx_params)
            else:
                self.createUntilSuccessByNetworkx(networkx_params)

        self.inter_edges = [edge for edge in self.G.edges()]

    def readFromDbByParams(self, networkx_params):
        colparams = [{"name":"networks_id"}
                     , {"name":"type"}
                     , {"name":"adjlist"}]
        res = TNetworks.getByParams(equalparams = networkx_params,
                                     colparams = colparams)
        self.G = self.loadByStoredAdjlist(res[0]["adjlist"])
        self.net_id = res[0]["networks_id"]

    def createOnceByNetworkx(self, networkx_params):
        pass

    def createUntilSuccessByNetworkx(self, networkx_params):
        self.G = self.createOnceByNetworkx(networkx_params)
        while not self.isConnectedGraph():
            self.G = self.createOnceByNetworkx(networkx_params)
            print ("Net creation not connected, recreate: ", networkx_params)

    def getSavingData(self):
        """
            rewrite to add more parameters
        """
        adjlist = self.getAdjlistForStore()
        return {"type":self.type
                , "adjlist": adjlist
                , "byte_num": sys.getsizeof(adjlist)
                , "agent_num": self.nodeNumber()
                , "avg_degree": self.avgDegree()
                , "diameter": self.diameter()
                }

    def getEqualCheckingData(self):
        return {"type":self.type
                , "agent_num": self.nodeNumber()
                }

    def loadByStoredAdjlist(self, adjlist):
        adj_lines = adjlist.split("\n")
        return nx.parse_adjlist(adj_lines, nodetype = int)

    def getAdjlistForStore(self):
        adj_lines = []
        for line in nx.generate_adjlist(self.G):
            adj_lines.append(line)
        adjlist = '\n'.join(adj_lines)
        return adjlist

    def insertToDB(self):
        data = self.getSavingData()
        equalparams = self.getEqualCheckingData()
        TNetworks.insertIfNotExist(equalparams, data)

    def agentNeighbors(self, node_id):
        return self.G.neighbors(node_id)

    def nodeNumber(self):
        return len(self.G.nodes())

    def avgDegree(self):
        degree_list = []
        for n in self.G.nodes():
            degree_list.append(self.G.degree(n))
#             print (self.G.degree(n))
        return round(np.mean(degree_list), 2)

    def diameter(self):
#         self.draw()
        return nx.diameter(self.G)

    def randomEdgesInteractionPairsInEpisode(self):
        """
            return the interaction edges indexes
            do not create a new list of pairs for saving memeory
        """
        random.shuffle(self.inter_edges)
        return self.inter_edges

    def concurrentInteractionPairsInEpisode(self):
        """
            return [(node_id1, node_id2), ...]
        """
        inter_pairs_list = []
        # set all nodes to "available"
        A = set(range(0, self.nodeNumber()))
        while len(A) > 0:
            i = random.sample(A, 1)[0]
            # randomly select an available neighbor of i
            j = None
            nbs = list(self.G.neighbors(i))
            while (len(nbs) > 0):
                j_tmp = Tools.getRandomAndThenDel(nbs)
                if j_tmp in A:
                    j = j_tmp
                    break
            if j != None:
                # if i has an available neighbor
                # determine (row player, column player)
                if random.choice([0, 1]) == 0:
                    inter_pairs_list.append((i, j))
                else:
                    inter_pairs_list.append((j, i))

                A.remove(i)
                A.remove(j)
            else:
                A.remove(i)
        return inter_pairs_list

    def draw(self):
        nx.draw_networkx(self.G)
        plt.show()

    def saveFigTo(self, path):
        nx.draw_networkx(self.G)
        DrawTools.saveFig(path)

    def isConnectedGraph(self):
        assert self.G != None
        dfs_node_list = self.depthFirstSearch(0)
        if len(dfs_node_list) == self.nodeNumber():
            return True
        else:
            return False

    def depthFirstSearch(self, start_node_id):
        nodes_to_vist = []
        visited_nodes = set()
        dfs_node_list = []

        nodes_to_vist.append(start_node_id)
        while(len(nodes_to_vist) > 0):
            visit_node_id = nodes_to_vist.pop()
            visited_nodes.add(visit_node_id)
            dfs_node_list.append(visit_node_id)

            for nb_id in self.agentNeighbors(visit_node_id):
                if nb_id not in visited_nodes and nb_id not in nodes_to_vist:
                    nodes_to_vist.append(nb_id)

        return dfs_node_list

    def getAgentsWithNbNumRange(self, small_nb_num, big_nb_num):
        l = []
        for n in self.G.nodes():
            if self.G.degree(n) >= small_nb_num and small_nb_num <= big_nb_num:
                l.append(n)
        return l

    def getTopKNbAgents(self, top_k):
        ag_nb_pairs = []
        for ag_id in self.G.nodes():
            ag_nb_pairs.append((ag_id, self.G.degree(ag_id)))

        ag_nb_pairs.sort(key = lambda x: x[1], reverse = True)
#         print(ag_nb_pairs)

        top_k_nb_agents = []
        for i in range(0, top_k):
            top_k_nb_agents.append(ag_nb_pairs[i][0])
#             print(ag_nb_pairs[i][0], self.G.degree(ag_nb_pairs[i][0]))

        return top_k_nb_agents, self.getRestAgIds(top_k_nb_agents)

    def getBottomKNbAgents(self, bottom_k):
        ag_nb_pairs = []
        for ag_id in self.G.nodes():
            ag_nb_pairs.append((ag_id, self.G.degree(ag_id)))

        ag_nb_pairs.sort(key = lambda x: x[1], reverse = False)
#         print(ag_nb_pairs)

        b_k_nb_agents = []
        for i in range(0, bottom_k):
            b_k_nb_agents.append(ag_nb_pairs[i][0])
#             print(ag_nb_pairs[i][0], self.G.degree(ag_nb_pairs[i][0]))

        return b_k_nb_agents, self.getRestAgIds(b_k_nb_agents)

    def getRestAgIds(self, ag_id_list):
        l = []
        for ag_id in self.G.nodes():
            if ag_id not in ag_id_list:
                l.append(ag_id)
        return l
