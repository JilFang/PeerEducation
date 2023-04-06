

from networks.Smallworld import SmallWorld
from networks.Community import Community
from networks.FullyConnected import FullyConnected
from tables.TNetworks import TNetworks
from networks.GlobalGraphConfig import GlobalGraphConfig
from tool.DrawTools import DrawTools


class SetupNet:

    @staticmethod
    def fc():
        agent_number = 30
        net = FullyConnected(networkx_params = {"agent_number":agent_number})
        net.insertToDB()

    @staticmethod
    def drawAll():
        equalparams = {}
        colparams = [{"name":"networks_id"}
                     , {"name":"type"}
                     , {"name":"adjlist"}]
        res = TNetworks.getByParams(equalparams = equalparams, colparams = colparams)
        for row in res:
            NetClass = GlobalGraphConfig.type_to_netclass[row["type"]]
            net = NetClass(stored_adjlist = row["adjlist"]
                             , stored_id = row["networks_id"])
            net.saveFigTo("net_figures/%s" % (net.net_id))

if __name__ == "__main__":
#     SetupNet.fc()
    SetupNet.drawAll()
    print("Done")
