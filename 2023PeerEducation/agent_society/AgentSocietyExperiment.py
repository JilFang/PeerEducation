from queue import Queue

from agents.GamePlayAgent import GamePlayAgent
from tables.TEmotionResults import TEmotionResults
from tool.Tools import Tools
from tables.TTrailParameters import TTrailParameters
from tables.TTrailResults import TTrailResults
from games.PD import PD
from games.PCG import PCG
from games.PCGL import *
from games.PCGN import PCGN


class AgentSocietyExperiment(object):
    """
        An experiment can have multiple networks. Then,
        for the ease of reusing memory, not follow the natural logic that
        a society relates to one network. Instead, multiple networks, agents
        are put into one class. Also, one society is combined with
        one experiment, which results in this class.
        
        A society contains some agents.
        To save memory and reduce cost, reuse the agents
        for various experiments.
        
        A society has some candidate networks to use.
        A network denotes specific connection relationships.
        In an experimental trial*, only one network is used.
        
        *one trial: one network, corresponding agents and strategies
        *one agent society experiment has some trials with a purpose, e.g., 
            - some repeated networks for getting averaged performance.
            - tests under various average neighbors.
            these trials require various networks, which are put
            class variables for ease of use.
    """

    def __init__(self, agent_in_use_number = 100):
        self.agent_in_use_number = agent_in_use_number
        self.agents = [GamePlayAgent() for _ in range(agent_in_use_number)]
        self.net_in_use = None
        self.game_in_use = None
        self.game_name_to_class = {"PCG":PCG
                                   , "PCGL":PCGL
                                   , "PCGN": PCGN
                                   , "PCGLMoreHalf":PCGLMoreHalf
                                   }

        self.generation_dynamics = []
        self.episode_dynamics = []
        self.emotion_dynamics = []
        self.cvg_check_list = []

    def runExperiment(self, m_params):
        """
            run an experiment with a purpose represented by m_params
            not use name setupSocietyExperiment() as an experiment 
            has multiple trails with various parameters. 
            Each trail needs to be set up properly.
            Also we need a function to run a specific experiment 
        """
        self.m_params = m_params

        for net in m_params.net_list:
#             print(net)
            self.setAgentConnections(net)
            for game_name in m_params.game_name_list:
                self.setAgentGame(game_name, 2)
                for listing_ass_adopted in m_params.listing_ass_adopted_list:
                    assert m_params.ass_distribution_type == "RANDOM"
                    for listing_ass_proportion in m_params.listing_ass_proportion_list:
            #                         for initial_actions_proportion in m_params.initial_actions_proportion_list:
                        trailparams_res = TTrailParameters.getTrailParamsByManualParams(
                            net.net_id, game_name
                            , listing_ass_adopted
                            , listing_ass_proportion
                            , m_params.ass_distribution_type
                            )
            #                             print(trailparams_res)
                        for trailparams in trailparams_res:
                            ass_partition_id_list = Tools.randomPartition(net.nodeNumber(), listing_ass_proportion)
                            self.setAgentAss(listing_ass_adopted, ass_partition_id_list)  # trailparams["listing_ass_adopted_by_agent_ids"]
                                        # now all settings are done. can start trails
                            for _ in range(m_params.trial_rep_num):
                                self.runOneTrail(m_params
                                                , trailparams["trail_parameters_id"]
                                                , listing_ass_adopted
                                                )

    def setAgentConnections(self, net):
        self.net_in_use = net
        # increase agent number to node number
        # only indexes in [0, node number-1] are used
        self.agent_in_use_number = net.nodeNumber()
#         print(net.nodeNumber())
        while len(self.agents) < self.agent_in_use_number:
            self.agents.append(GamePlayAgent())
#         print("prepare net")
        for ag_id in range(0, self.agent_in_use_number):
            agent = self.agents[ag_id]
            # set neighbors
            agent.clearNeighbors()
            nb_ids = net.agentNeighbors(ag_id)
            for nb_id in nb_ids:
                agent.addNeighbor(self.agents[nb_id])

    def setAgentGame(self, game_name, action_num):
        self.game_in_use = game_name
        game = self.game_name_to_class[game_name](action_num)
        for ag_id in range(0, self.agent_in_use_number):
            self.agents[ag_id].setGame(game)

    def setAgentAss(self, listing_ass_adopted
                    , listing_ass_adopted_by_agent_ids):
        ass_index = 0
        for ids in listing_ass_adopted_by_agent_ids:
            ass_name = listing_ass_adopted[ass_index]
            for _id in ids:
                self.agents[_id].useAss(ass_name)
            ass_index += 1


    def recordEpisodeDynamics(self, epi, action_pairs_in_epi):
        ap_stat = {(0, 0):0, (0, 1):0, (1, 0):0, (1, 1):0}
        for action_pair in action_pairs_in_epi:
            ap_stat[action_pair] += 1
        self.episode_dynamics.append([epi
                                      , ap_stat[(0, 0)]
                                      , ap_stat[(0, 1)]
                                      , ap_stat[(1, 0)]
                                      , ap_stat[(1, 1)]
                                      ])

    def recordEmotionDynamics(self, epi, emotion_in_epi):
        emo_stat = {('Joy'):0, ('Fear'):0, ('Angry'):0, ('Pressure'):0}
        for emotion in emotion_in_epi:
            emo_stat[emotion] += 1
        self.emotion_dynamics.append([epi
                                      , emo_stat[('Joy')]
                                      , emo_stat[('Fear')]
                                      , emo_stat[('Angry')]
                                      , emo_stat[('Pressure')]
                                      ])

    def getGenerationStat(self, generation):
        pass

    def clearStat(self):
        self.generation_dynamics.clear()
        self.episode_dynamics.clear()
        self.emotion_dynamics.clear()
        self.cvg_check_list.clear()

    def runOneTrail(self, m_params
                    , trail_parameters_id
                    , listing_ass_adopted
                    ):
        if m_params.is_show_log:
            print(self.globalInfo())
        self.clearStat()
        net = self.net_in_use
        # repeated trails for a setting

        for ag_id in range(0, self.agent_in_use_number):
            agent = self.agents[ag_id]
            agent.prepareForTrial()
#         self.getEpisodeStat(0)
        for episode in range(1, m_params.episode_num + 1):
#             print(episode, -1)
#                 inter_edges = net.randomEdgesInteractionPairsInEpisode()
            inter_edges = net.concurrentInteractionPairsInEpisode()
#                 print(len(inter_edges))

            action_pairs_in_epi = []
            emotion_in_epi = []
            for inter_edge in inter_edges:
                ag1 = self.agents[inter_edge[0]]
                ag2 = self.agents[inter_edge[1]]

                ag1.selRowAction(ag2)
                ag2.selColAction(ag1)
                result = ag1.handleInteractionUpdateWith(ag2)

                if 'Emotion' in m_params.listing_ass_adopted_list[0][0]:
                    if result[0] != None:
                        emotion_in_epi.append((result[0]))
                    if result[1] != None:
                        emotion_in_epi.append((result[1]))

                action_pairs_in_epi.append((ag1.row_action, ag2.col_action))
            #
            self.recordEpisodeDynamics(episode, action_pairs_in_epi)
            if 'Emotion' in m_params.listing_ass_adopted_list[0][0]:
                self.recordEmotionDynamics(episode, emotion_in_epi)
            # an episode ends

        self.saveStat(m_params.exp_name
                      , trail_parameters_id
                      , m_params.episode_num
                      )
        if 'Emotion' in m_params.listing_ass_adopted_list[0][0]:
            self.saveEmotion(m_params.exp_name
                             , trail_parameters_id
                             , m_params.episode_num
                             )
    def saveStat(self, exp_name
                 , trail_parameters_id
                 , episode_num
                 ):
        saving_data = {"trail_parameters_id": trail_parameters_id
                       , "exp_name":exp_name
                       }
        saving_data["episode_dynamics"] = self.episode_dynamics
        saving_data["episode_num"] = episode_num
        TTrailResults.insert(saving_data)

    def saveEmotion(self, exp_name
                 , trail_parameters_id
                 , episode_num
                 ):
        saving_data = {"trail_parameters_id": trail_parameters_id
                       , "exp_name":exp_name
                       }
        saving_data["emotion_dynamics"] = self.emotion_dynamics
        saving_data["episode_num"] = episode_num
        TEmotionResults.insert(saving_data)

    def globalInfo(self):
        ass_class_dict = {}
        for ag_id in range(0, self.agent_in_use_number):
            agent = self.agents[ag_id]
            ass_classname = agent.ass.__class__.__name__
            if ass_classname in ass_class_dict.keys():
                ass_class_dict[ass_classname] += 1
            else:
                ass_class_dict[ass_classname] = 1

        infostr = "Trial info. ass used:%s, net:%s, game:%s" % \
            (ass_class_dict, self.net_in_use.type, self.game_in_use)
        return infostr


