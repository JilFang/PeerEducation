from tables.TEmotionResults import TEmotionResults
from tables.TTrailResults import TTrailResults
from ast import literal_eval
from tool.DrawTools import DrawTools
from agent_society.AgentSocietyExperiment import AgentSocietyExperiment
from experiments.ManualParametersSpace import ManualParametersSpace
from tool.Tools import Tools
from tables.TTrailResultsMeanView import TTrailResultsMeanView
from tool.DBDO import DBDO


class NewExperiments:
    """
        combine -set params, -run exp, -see res
    """

    @staticmethod
    def run():
        so = AgentSocietyExperiment()

        """ ------------ game, epi, trial, etc. settings. ----------- """
        """
            exp_name:
            T1: three ass, PCG
            T2: HCR various payoff values
            T3: agents with fixed behavior
            T4: agents with fixed and opposite behavior
        """
        exp_name = "T21"  #
        # PCG PCGL PCGLMoreHalf
        game_name_list = ["PCG"]
        trial_rep_num = 10
        episode_num = 500
        is_show_log = False

        """ ------------ net condition ----------- """
        net_params_list = []
        # net_params_list.append({"type":"FC", "agent_num":30})
        # net_params_list.append({"type": "SW", "agent_num": 30})
        net_params_list.append({"type": "GR", "agent_num": 30})


        """ ------------ strategy condition & strategy-location condition----------- """
        ass_distribution_type = "RANDOM"

        listing_ass_adopted_list = [["BasedExperienceByEmotion", "AlwaysTutorAndLearnBasedExperienceByEmotion"]]#, "AlwaysTutorAndLearn"
        listing_ass_proportion_list = [[0.8, 0.2]]
        # WSLS ImitateOppoAction HCR AlwaysTutorAndLearn
#         listing_ass_adopted_list = [["AlwaysTutorAndLearn", "ImitateOppoAction"]
#                                     , ["AlwaysTutorAndLearn", "WSLS"]
#                                     ,["AlwaysTutorAndLearn", "HCR"]]

        # listing_ass_adopted_list = [["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "ImitateOppoAction"]
                                    # , ["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "WSLS"]
                                    # , ["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "HCR"]]
        # [0.03,0.97] [0.1, 0.9] [0.16,0.84]
#         listing_ass_proportion_list = [[0.16,0.84]]

        # listing_ass_proportion_list = [[0.03, 0.03, 0.94], [0.1, 0.1, 0.8], [0.16, 0.16, 0.68]]
#         initial_actions_list = [[0,1]] # fixed for all exp in this paper
        """
            proportions of
            row action 0
            row action 1
            column action 0
            column action 1
        """
#         initial_actions_proportion_list = [[0.5, 0.5, 0.5, 0.5]]

#         listing_ass_proportion_list = []
#         for prop in [0.1, 0.3, 0.5, 0.7, 0.9]:
#             listing_ass_proportion_list.append([prop, round(1 - prop, 3)])

        print(listing_ass_adopted_list, listing_ass_proportion_list)
#         print(initial_actions_proportion_list)
        for netp in net_params_list:
            print(netp)
        # print(game_name_list)
        #
        # if not Tools.messageBoxYNConti("Run above setting?"):
        #     print("Stopped")
        #     return

        """ ------------ start simulation----------- """
        m_params = ManualParametersSpace(net_params_list = net_params_list
                , game_name_list = game_name_list
                 , listing_ass_adopted_list = listing_ass_adopted_list
                 , listing_ass_proportion_list = listing_ass_proportion_list
                 , ass_distribution_type = ass_distribution_type
#                  , initial_actions_list = initial_actions_list
#                  , initial_actions_proportion_list = initial_actions_proportion_list
                 , episode_num = episode_num
                 , trial_rep_num = trial_rep_num
                 , exp_name = exp_name
                 , is_show_log = is_show_log
                 )

        trail_id_list = m_params.saveToDB()  # save params
        so.runExperiment(m_params)
        name_list = ['BasedExperience', 'BasedNeighbor', 'HCR', 'WSLS', 'BasedExperienceByEmotion', 'BasedNeighborByEmotion','BasedNeighborP']
        if listing_ass_adopted_list[0][0] == name_list[0]:
            name = "iomb"
        elif listing_ass_adopted_list[0][0] == name_list[1]:
            name = "mn"
        elif listing_ass_adopted_list[0][0] == name_list[2]:
            name = "hcr"
        elif listing_ass_adopted_list[0][0] == name_list[3]:
            name = "wsls"
        elif listing_ass_adopted_list[0][0] == name_list[4]:
            name = "ebe"
        elif listing_ass_adopted_list[0][0] == name_list[5]:
            name = "nbe"
        elif listing_ass_adopted_list[0][0] == name_list[6]:
            name = "mnp"
        num = round(float(listing_ass_proportion_list[0][1]) * 30)
        # num = 0
        for tid in trail_id_list:
            # print(tid)
            # TTrailResults.meanEpiRes(exp_name, episode_num, tid)
            # TTrailResults.meanNormEmergenceStatRes(exp_name, episode_num, tid)
            # NewExperiments.seeMeanRes(exp_name, 0, episode_num, tid)
            # NewExperiments.combine_res(exp_name, listing_ass_adopted_list, episode_num, 100)
            NewExperiments.seeExpResults(exp_name, 0, name, num)   # see res
            if 'Emotion' in listing_ass_adopted_list[0][0]:
                NewExperiments.seeEmotionResults(exp_name, 0, name, num)
            pass

    @staticmethod
    def seeExpResults(exp_name = None, skip_footer = 0, name = None, num = 0):
        res = TTrailResults.getByExpName(exp_name)
        for row in res:
            print(row)

            dy = literal_eval(row["episode_dynamics"].decode())

            for i in range(0, len(dy)):
                sum = 0
                for j in range(1, 5):
                    sum = sum + dy[i][j]
                for k in range(1, 5):
                    dy[i][k] = dy[i][k] / sum
                # print(sum)
            # print(dy)
            res_id = row["trail_results_id"]
            DrawTools.drawList2d(list2d=dy
                                 , header=['episode', 'T, L', 'T, NL', 'NT, L', 'NT, NL']
                                 , see_col_list=[1, 2, 3, 4]
                                 , save_to_path="figures/%s/%s/%s/%s.png" % (exp_name, name, num, res_id)
                                 , skip_footer=skip_footer
                                 )

    def seeEmotionResults(exp_name=None, skip_footer=0, name = None, num = 0):

        res = TEmotionResults.getByExpName(exp_name)

        for row in res:
            # print(row)

            dy = literal_eval(row["emotion_dynamics"].decode())

            for i in range(0, len(dy)):
                sum = 0
                for j in range(1, 5):
                    sum = sum + dy[i][j]
                for k in range(1, 5):
                    dy[i][k] = dy[i][k] / sum
                # print(sum)
            # print(dy)
            res_id = row["emotion_results_id"]
            DrawTools.drawList3d(list2d=dy
                                 , header=['episode', 'Joy', 'Fear', 'Angry', 'Pressure']
                                 , see_col_list=[1, 2, 3, 4]
                                 , save_to_path="figures/%s/%s/%s/emotion/%s.png" % (exp_name, name, num, res_id)
                                 , skip_footer=skip_footer
                                 )

    @staticmethod
    def seeMeanRes(exp_name = None, skip_footer = 0, episode_num = 200, tid = None):
        param_name_list = ["trail_parameters_id", "exp_name", "episode_num"]
        equalparams = {"exp_name":exp_name
                       , "episode_num":episode_num
                       , "trail_parameters_id":tid}
        distinct_params_list = TTrailResultsMeanView.getDistinctColumnValues(param_name_list, equalparams)
        for distinct_params in distinct_params_list:
            res = TTrailResultsMeanView.getByParams(equalparams = distinct_params
                    , colparams = [{"name":"trail_results_mean_id"}
                                   , {"name":"trail_parameters_id"}
                                   , {"name":"listing_ass_adopted"}
                                   , {"name":"episode_dynamics_mean", "cast_by":Tools.bstr_to_valuestr}])
            for row in res:
#                 print(row["episode_dynamics_mean"])
                dy = row["episode_dynamics_mean"]
                res_id = row["trail_results_mean_id"]
                t_id = row["trail_parameters_id"]
                ass_list = row["listing_ass_adopted"]
    #             print(dy)
                DrawTools.drawList2d(list2d = dy
                 , header = ['episode', 'avg_r', 'avg_cg', 'max_proption']
                 , see_col_list = [1, 2, 3]
                 , save_to_path = "figures/%s/mean_tid%s_%s_sk_%s.png" % (exp_name, t_id, ass_list, skip_footer)
                 , skip_footer = skip_footer
                 )

    @staticmethod
    def combine_res(exp_name, listing_ass_adopted_list, episode_num, skip_footer):
        for listing_ass_adopted in listing_ass_adopted_list:
            res = TTrailResultsMeanView.getByExpNameAss(exp_name, listing_ass_adopted, episode_num)
#             print(len(res))
            dy_list = []
            header = ['episode']
            for row in res:
                dy_list.append(row["episode_dynamics_mean"])
                header.append(row["listing_ass_proportion"])
            combined_res = DBDO.putTgtColTogetherInMultipleResults(dy_list, 3)  # 3 is max_proportion
            DrawTools.drawList2d(list2d = combined_res
             , header = header
             , skip_footer = skip_footer
#              , see_col_list = [1, 2, 3, 4]
             , save_to_path = "figures/%s/%s_%s.png" % (exp_name, listing_ass_adopted, episode_num)
             )


if __name__ == "__main__":
    NewExperiments.run()
    print("Done")
