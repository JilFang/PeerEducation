

from enum import Enum
from tables.TNetworks import TNetworks
from networks.GlobalGraphConfig import GlobalGraphConfig
from tables.TTrailParameters import TTrailParameters


class AssDistribution(Enum):
    """
        Agents are distributed:
            1: randomly across a network
            2: be at nodes with more neighbors
    """
    RANDOM = 1
    MORE_NEIGHBOR = 2
    SF_MANY_NEIGHBOR = 3
    CM_ONE_CM = 4
    MANUAL_LISTING = 5  # manually listing the ids of each strategy


class InteractionType(Enum):
    """
        1: sequentially with neighbors
        2: concurrently with neighbors
    """
    SEQ = 1
    CON = 2


class ManualParametersSpace:
    """
        Parameters Space set by hand for
            1: for each parameter combination,
                generate trail parameters to DB
            2: get trail parameters from DB and conduct exp
    """

    def __init__(self, net_params_list = None  # [{"type":"FC"}, ...]
                , game_name_list = None  # [IntersectionGame()]
                 , action_num_list = None
                 , listing_ass_adopted_list = None  # [["Fixed",...], ...]
                 , listing_ass_proportion_list = None  # [[0.4,0.6], ...]
                 , ass_distribution_type = "RANDOM"
#                  , initial_actions_list = None
                 , initial_actions_proportion_list = None
                 , listing_ass_adopted_by_agent_ids = None  # manual indication, not list, just one, focus
                 , listing_ass_proportion = None  # if manual ids are set, this is also set
#                  , distribution_feature_num = None  # if manual ids are set, this is also set
                 , listing_ass_agent_ids_rep_num = 1
                 , exp_name = None
#                  , for_set_params = False
                 , generation_num = 1
                 , episode_num = 100
                 , trial_rep_num = 30
                 , isrecord_episode_stat = True
                 , isrecord_generation_stat = False
#                  , stop_until_ne = False
                 , is_show_log = True
                 ):
#         if for_set_params == False:
#             assert exp_name != None  # need a name, need to know the purpose
        locals_dict = locals()
#         print(locals_dict)
        for attr_name in locals_dict:
            if attr_name != "self":
                setattr(self.__class__, attr_name, locals_dict[attr_name])

        self.net_list = []
        for net_params in net_params_list:
            self.net_list.extend(self.loadNetworks(net_params))

    def printInfo(self):
        print(self.episode_num)

    def loadNetworks(self, net_params):
        nets = []
        colparams = [{"name":"networks_id"}
                     , {"name":"type"}
                     , {"name":"adjlist"}]
        res = TNetworks.getByParams(equalparams = net_params, colparams = colparams)
        for row in res:
            NetClass = GlobalGraphConfig.type_to_netclass[row["type"]]
            nets.append(NetClass(stored_adjlist = row["adjlist"]
                             , stored_id = row["networks_id"]))
        return nets

    def saveToDB(self):
        m_params = self
        trail_id_list = []
        for net in m_params.net_list:
            for game_name in m_params.game_name_list:
                for listing_ass_adopted in m_params.listing_ass_adopted_list:
                    ass_distribution_type = m_params.ass_distribution_type
                    assert ass_distribution_type == "RANDOM"
                    for listing_ass_proportion in m_params.listing_ass_proportion_list:
            #                         for initial_actions_proportion in m_params.initial_actions_proportion_list:
                        for _ in range(m_params.listing_ass_agent_ids_rep_num):
                            data_to_insert = {"networks_id":net.net_id
                                                , "game_name":game_name
                                                , "listing_ass_adopted":listing_ass_adopted
                                                , "listing_ass_proportion":listing_ass_proportion
                                                , "ass_distribution_type":ass_distribution_type
            #                                               , "initial_actions":initial_actions
            #                                               , "initial_actions_proportion":initial_actions_proportion
                                                }
                            equalparams = data_to_insert
                            tid = TTrailParameters.insertIfNotExist(equalparams, data_to_insert)
                            trail_id_list.append(tid)
        return trail_id_list
