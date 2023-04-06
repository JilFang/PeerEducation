
from tables.TTrailResultsView import TTrailResultsView
from tool.DrawTools import DrawTools
from tool.Tools import Tools


class GetFigures:

    @staticmethod
    def seeDyBytid(tid, pathname):
        res = TTrailResultsView.getByTid(tid)
        dy = res[0]["episode_dynamics"]
        res_id = res[0]["trail_results_id"]

        # convert to proportion
        num_pair_jb = 15
        dy = dy[0:150]
        for row in dy:
            for i in range(1, 5):
                row[i] = row[i] / num_pair_jb

#         line_marker_list = ['o', '^', '+', '<']
        line_style_list = ['-', '-.', '--', ':']
        DrawTools.drawList2d(list2d = dy
#             , header = ['episode', 'teach, learn', 'teach, not learn', 'not teach, learn', 'not teach, not learn']
            , header = ['episode', '(T, L)', '(T, NL)', '(NT, L)', '(NT, NL)']
#              , see_col_list = [3]
#             , line_marker_list = line_marker_list
            , line_style_list = line_style_list
            , xLabel = 'Iterations'
            , yLabel = 'Proportion of joint behaviors'
#             , has_legend = False
            , legend_loc = 5
            , save_to_path = "figures/%s/%s.png" % (pathname, res_id)
             )

    @staticmethod
    def get_wsls_mean():
        exp_name = "T1"
        listing_ass_adopted = ["WSLS"]
        res = TTrailResultsView.getEpisodeDynamicsByExpAss(exp_name
                                                   , listing_ass_adopted)
        print(len(res))
        dy_mean = Tools.meanDictRepeats(res)
        print(dy_mean)
        dy = dy_mean["episode_dynamics_mean"]
        # convert to proportion
        num_pair_jb = 15
        dy = dy[0:150]
        for row in dy:
            for i in range(1, 5):
                row[i] = row[i] / num_pair_jb

        line_style_list = ['-', '-.', '--', ':']
        DrawTools.drawList2d(list2d = dy
    #             , header = ['episode', 'teach, learn', 'teach, not learn', 'not teach, learn', 'not teach, not learn']
            , header = ['episode', '(T, L)', '(T, NL)', '(NT, L)', '(NT, NL)']
    #              , see_col_list = [3]
    #             , line_marker_list = line_marker_list
            , line_style_list = line_style_list
            , xLabel = 'Iterations'
            , yLabel = 'Proportion of joint behaviors'
            , yLim = (0, 1)
    #             , has_legend = False
            , legend_loc = 5
            , save_to_path = "figures/WSLS/%s.png" % ("wsls_mean")
             )

    @staticmethod
    def get_hcr_diff_game_mean():
        list2d_list = []
        exp_name = "T1"
        listing_ass_adopted = ["HCR"]
        game_name = "PCG"
        cvgbeh = "T,L"
        res = TTrailResultsView.getEpisodeDynamicsByExpAssGameCvgbeh(exp_name
                                                   , listing_ass_adopted
                                                   , game_name, cvgbeh)
        print(len(res))
        dy = Tools.meanDictRepeats(res)
        list2d_list.append(dy["episode_dynamics_mean"])

        exp_name = "T2"
        game_name_list = ["PCGLMoreHalf", "PCGL"]
        for game_name in game_name_list:
            res = TTrailResultsView.getEpisodeDynamicsByExpAssGameCvgbeh(exp_name
                                                   , listing_ass_adopted
                                                   , game_name, cvgbeh)
            print(len(res))
            dy = Tools.meanDictRepeats(res)
            list2d_list.append(dy["episode_dynamics_mean"])

        multi_game_setting_dy = Tools.putTgtColTogetherInMultipleResults(list2d_list, 1)

        print(len(multi_game_setting_dy), multi_game_setting_dy)
        dy = multi_game_setting_dy
        # convert to proportion
        num_pair_jb = 15
        dy = dy[0:100]
        for row in dy:
            for i in range(1, len(row)):
                row[i] = row[i] / num_pair_jb

        line_style_list = ['-', '-.', '--']
        DrawTools.drawList2d(list2d = dy
    #             , header = ['episode', 'teach, learn', 'teach, not learn', 'not teach, learn', 'not teach, not learn']
            , header = ['episode', 'diff=0', 'diff=0.5', 'diff=1']
    #              , see_col_list = [3]
    #             , line_marker_list = line_marker_list
            , line_style_list = line_style_list
            , xLabel = 'Iterations'
            , yLabel = 'Proportion of joint behaviors'
            , yLim = (0, 1)
    #             , has_legend = False
            , save_to_path = "figures/HCR/%s.png" % ("hcr_diff_payoff_mean")
             )

    @staticmethod
    def seeInfluFixedBeh():
        total_draw_num = 100

        exp_name = "T3"
        listing_ass_adopted = ["AlwaysTutorAndLearn", "HCR"]
        game_name = "PCG"
        listing_ass_proportion = [0.03, 0.97]

        res = TTrailResultsView.getByExpNameAssGameProp(exp_name
                                                , listing_ass_adopted
                                                , game_name
                                                , listing_ass_proportion)
        c = 0
        print(len(res))
        for row in res:
            c += 1
            if c == total_draw_num + 1:
                break
#             print(row)
            res_id = row["trail_results_id"]
            dy = row["episode_dynamics"]

            num_pair_jb = 15
            dy = dy[0:150]
            for row in dy:
                for i in range(1, 5):
                    row[i] = row[i] / num_pair_jb

    #         line_marker_list = ['o', '^', '+', '<']
            line_style_list = ['-', '-.', '--', ':']
            DrawTools.drawList2d(list2d = dy
    #             , header = ['episode', 'teach, learn', 'teach, not learn', 'not teach, learn', 'not teach, not learn']
                , header = ['episode', '(T, L)', '(T, NL)', '(NT, L)', '(NT, NL)']
    #              , see_col_list = [3]
    #             , line_marker_list = line_marker_list
                , line_style_list = line_style_list
                , xLabel = 'Iterations'
                , yLabel = 'Proportion of joint behaviors'
    #             , has_legend = False
                , save_to_path = "figures/%s/%s/%s.png" % ("Fixed_Behavior", listing_ass_adopted, res_id)
                 )

    @staticmethod
    def seeInfluFixedBehHCR():
        """
            HCR others to not teach not learn
        """
        total_draw_num = 100

        exp_name = "T3"
        listing_ass_adopted = ["AlwaysTutorAndLearn", "HCR"]
        game_name = "PCG"
        listing_ass_proportion = [0.03, 0.97]

        res = TTrailResultsView.getHCROneFixedNotCvgDynamics(listing_ass_adopted, listing_ass_proportion)
        c = 0
        print(len(res))

        for row in res:
            c += 1
            if c == total_draw_num + 1:
                break
#             print(row)
            res_id = row["trail_results_id"]
            dy = row["episode_dynamics"]

            num_pair_jb = 15
            dy = dy[0:150]
            for row in dy:
                for i in range(1, 5):
                    row[i] = row[i] / num_pair_jb

    #         line_marker_list = ['o', '^', '+', '<']
            line_style_list = ['-', '-.', '--', ':']
            DrawTools.drawList2d(list2d = dy
    #             , header = ['episode', 'teach, learn', 'teach, not learn', 'not teach, learn', 'not teach, not learn']
                , header = ['episode', '(T, L)', '(T, NL)', '(NT, L)', '(NT, NL)']
    #              , see_col_list = [3]
    #             , line_marker_list = line_marker_list
                , line_style_list = line_style_list
                , xLabel = 'Iterations'
                , yLabel = 'Proportion of joint behaviors'
    #             , has_legend = False
                , save_to_path = "figures/%s/%s/%s.png" % ("Fixed_Behavior", listing_ass_adopted, res_id)
                 )

    @staticmethod
    def get_diff_fixed_beh_mean_compare():

        exp_name = "T3"
        game_name = "PCG"
        listing_ass_adopted_list = [
            ["AlwaysTutorAndLearn", "ImitateOppoAction"]
            , ["AlwaysTutorAndLearn", "WSLS"]
            , ["AlwaysTutorAndLearn", "HCR"]]

        cvg_joint_behavior = "T,L"

        listing_ass_proportion_list = [[0.03, 0.97], [0.1, 0.9], [0.16, 0.84]]

        for listing_ass_adopted in listing_ass_adopted_list:
            list2d_list = []

            for listing_ass_proportion in listing_ass_proportion_list:

                res = TTrailResultsView \
                    .getEpisodeDynamicsByExpAssGameCvgbehStraProp(exp_name
                                                , listing_ass_adopted
                                                , listing_ass_proportion
                                                , game_name
                                                , cvg_joint_behavior)
                print(len(res))
                dy = Tools.meanDictRepeats(res)
                list2d_list.append(dy["episode_dynamics_mean"])

            multi_setting_dy = Tools.putTgtColTogetherInMultipleResults(list2d_list, 1)
            print(len(multi_setting_dy), multi_setting_dy)
            dy = multi_setting_dy
            # convert to proportion
            num_pair_jb = 15
            dy = dy[0:100]
            for row in dy:
                for i in range(1, len(row)):
                    row[i] = row[i] / num_pair_jb

            line_style_list = ['--', '-.', '-']
            DrawTools.drawList2d(list2d = dy
        #             , header = ['episode', 'teach, learn', 'teach, not learn', 'not teach, learn', 'not teach, not learn']
                , header = ['episode', '1 fixed agent', '3 fixed agents', '5 fixed agents']
        #              , see_col_list = [3]
        #             , line_marker_list = line_marker_list
                , line_style_list = line_style_list
                , xLabel = 'Iterations'
                , yLabel = 'Average proportion of\njoint behaviors (T, L)'
                , yLim = (0, 1)
        #             , has_legend = False
                , save_to_path = "figures/get_diff_fixed_beh_mean_compare/diff_fixb_%s.png" % (Tools.convertToFigName(listing_ass_adopted))
                 )

    @staticmethod
    def get_hcr_diff_fixed_beh_not_cvg_mean_compare():

        listing_ass_adopted = ["AlwaysTutorAndLearn", "HCR"]

        listing_ass_proportion_list = [[0.03, 0.97], [0.1, 0.9]]

        list2d_list = []

        for listing_ass_proportion in listing_ass_proportion_list:

            res = TTrailResultsView.getHCROneFixedNotCvgDynamics(
                                            listing_ass_adopted
                                            , listing_ass_proportion
                                            )
            print(len(res))
#             print(res)
            dy = Tools.meanDictRepeats(res)
            list2d_list.append(dy["episode_dynamics_mean"])

        multi_setting_dy = Tools.putTgtColTogetherInMultipleResults(list2d_list, 4)
        print(len(multi_setting_dy), multi_setting_dy)
        dy = multi_setting_dy
        # convert to proportion
        num_pair_jb = 15
        dy = dy[0:100]
        for row in dy:
            for i in range(1, len(row)):
                row[i] = row[i] / num_pair_jb

        line_style_list = ['--', '-.', '-']
        DrawTools.drawList2d(list2d = dy
    #             , header = ['episode', 'teach, learn', 'teach, not learn', 'not teach, learn', 'not teach, not learn']
            , header = ['episode', '1 fixed agent', '3 fixed agents']
    #              , see_col_list = [3]
    #             , line_marker_list = line_marker_list
            , line_style_list = line_style_list
            , xLabel = 'Iterations'
            , yLabel = 'Average proportion of\njoint behaviors (NT, NL)'
            , yLim = (0, 1)
    #             , has_legend = False
            , save_to_path = "figures/get_hcr_diff_fixed_beh_not_cvg_mean_compare/hcr_fixb_not_cvg.png" % (listing_ass_adopted)
             )

    @staticmethod
    def fixed_opposite_behavior():

        listing_ass_adopted_list = [["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "ImitateOppoAction"]
                                    , ["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "WSLS"]
                                    , ["AlwaysTutorAndLearn", "AlwaysNotTutorOrLearn", "HCR"]]

        listing_ass_proportion_list = [[0.03, 0.03, 0.94], [0.1, 0.1, 0.8], [0.16, 0.16, 0.68]]

        for listing_ass_adopted in listing_ass_adopted_list:
            for listing_ass_proportion in listing_ass_proportion_list:

                res = TTrailResultsView.getAllFixedOppoBehDy(
                    listing_ass_adopted
                    , listing_ass_proportion)
                print(len(res))

                for row in res:
                    res_id = row["trail_results_id"]
                    dy = row["episode_dynamics"]

                    # convert to proportion
                    num_pair_jb = 15
                    dy = dy[0:150]
                    for row in dy:
                        for i in range(1, 5):
                            row[i] = row[i] / num_pair_jb

            #         line_marker_list = ['o', '^', '+', '<']
                    line_style_list = ['-', '-.', '--', ':']
                    DrawTools.drawList2d(list2d = dy
            #             , header = ['episode', 'teach, learn', 'teach, not learn', 'not teach, learn', 'not teach, not learn']
                        , header = ['episode', '(T, L)', '(T, NL)', '(NT, L)', '(NT, NL)']
            #              , see_col_list = [3]
            #             , line_marker_list = line_marker_list
                        , line_style_list = line_style_list
                        , xLabel = 'Iterations'
                        , yLabel = 'Proportion of joint behaviors'
            #             , has_legend = False
                        , save_to_path = "figures/fixed_opposite_behavior/%s_%s/%s.png" % (listing_ass_adopted, listing_ass_proportion, res_id)
                         )

    @staticmethod
    def getFinalFigByIds():
        tid_list = [2,16,87,89,1001,2001,2008,5541,5766,5820,7950]
        tid_list = [1001, 14507]
        tid_list = [14567]
        for tid in tid_list:
            GetFigures.seeDyBytid(tid, "getFinalFigByIds")


if __name__ == "__main__":
    # (1, 101)  (1001, 1002) (2001, 2002)
#     for i in range(2001, 2012):
#         GetFigures.seeDyBytid(i)

    # WSLS mean
#     GetFigures.get_wsls_mean()

    # HCR diff game compare
#     GetFigures.get_hcr_diff_game_mean()

    # Influence Fixed Behavior
#     GetFigures.seeInfluFixedBeh()

#     GetFigures.seeInfluFixedBehHCR()
#     GetFigures.get_diff_fixed_beh_mean_compare()
#     GetFigures.get_hcr_diff_fixed_beh_not_cvg_mean_compare()

#     GetFigures.fixed_opposite_behavior()

    GetFigures.getFinalFigByIds()
    print("Done")
