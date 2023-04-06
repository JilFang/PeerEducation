'''
Created on 11 Sep 2020

@author: w
'''
from tables.Table import Table
from ast import literal_eval
from tool.Tools import Tools


class TTrailResultsView(Table):

    @classmethod
    def getTableName(cls):
        return "trail_results_view"

    @classmethod
    def getByTid(cls, tid):
        return cls.getByParams(
            equalparams = {
                "trail_results_id":tid
               }
            , colparams = [
                {"name":"trail_results_id"}
                , {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}
                ])

    @classmethod
    def getByExpNameAss(cls, exp_name, listing_ass_adopted):
        return cls.getByParams(
            equalparams = {
                "exp_name":exp_name
                , "listing_ass_adopted":listing_ass_adopted
               }
            , colparams = [
                {"name":"trail_results_id"}
                , {"name":"listing_ass_proportion"}
                , {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}
                ])

    @classmethod
    def getByExpNameAssGame(cls, exp_name, listing_ass_adopted, game_name):
        return cls.getByParams(
            equalparams = {
                "exp_name":exp_name
                , "listing_ass_adopted":listing_ass_adopted
                , "game_name":game_name
               }
            , colparams = [
                {"name":"trail_results_id"}
                , {"name":"listing_ass_proportion"}
                , {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}
                ])

    @classmethod
    def getByExpNameAssGameProp(cls, exp_name, listing_ass_adopted
                            , game_name, listing_ass_proportion):
        return cls.getByParams(
            equalparams = {
                "exp_name":exp_name
                , "listing_ass_adopted":listing_ass_adopted
                , "game_name":game_name
                , "listing_ass_proportion":listing_ass_proportion
               }
            , colparams = [
                {"name":"trail_results_id"}
                , {"name":"listing_ass_proportion"}
                , {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}
                ])

    @classmethod
    def getEpisodeDynamicsByExpAssGameCvgbeh(cls, exp_name
                                             , listing_ass_adopted
                                             , game_name
                                             , cvg_joint_behavior):
        return cls.getByParams(
            equalparams = {"exp_name":exp_name
                           , "listing_ass_adopted":listing_ass_adopted
                           , "game_name":game_name
                           , "cvg_joint_behavior":cvg_joint_behavior
                           }
            , colparams = [
#                 {"name":"trail_results_id"}
                {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}  # , "cast_by":literal_eval
                ]
#             , to_numpy_array = True
            , show_sql = True
            )

    @classmethod
    def getEpisodeDynamicsByExpAss(cls, exp_name, listing_ass_adopted):
        return cls.getByParams(
            equalparams = {"exp_name":exp_name
                           , "listing_ass_adopted":listing_ass_adopted
                           }
            , colparams = [
#                 {"name":"trail_results_id"}
                {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}  # , "cast_by":literal_eval
                ]
#             , to_numpy_array = True
            , show_sql = True
            )

    @classmethod
    def getHCROneFixedNotCvgDynamics(cls, listing_ass_adopted, listing_ass_proportion):
#         sql = "SELECT * FROM `trail_results_view` WHERE exp_name=\"T3\" AND listing_ass_adopted=\"['AlwaysTutorAndLearn', 'HCR']\" AND listing_ass_proportion=\"[0.03, 0.97]\" AND cvg_joint_behavior != \"T,L\""
        return cls.getByParams(
            equalparams = {"exp_name":"T3"
                           , "listing_ass_adopted":listing_ass_adopted
                           , "listing_ass_proportion":listing_ass_proportion
                           }
            , colparams = [
#                 {"name":"trail_results_id"},
                 {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}  # , "cast_by":literal_eval
                ]
            , notlikeparams = {"cvg_joint_behavior":["T,L"]}
#             , to_numpy_array = True
            , show_sql = True
            )

    @classmethod
    def getEpisodeDynamicsByExpAssGameCvgbehStraProp(cls, exp_name
                                             , listing_ass_adopted
                                             , listing_ass_proportion
                                             , game_name
                                             , cvg_joint_behavior):
        return cls.getByParams(
            equalparams = {"exp_name":exp_name
                           , "listing_ass_adopted":listing_ass_adopted
                           , "listing_ass_proportion":listing_ass_proportion
                           , "game_name":game_name
                           , "cvg_joint_behavior":cvg_joint_behavior
                           }
            , colparams = [
#                 {"name":"trail_results_id"}
                {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}  # , "cast_by":literal_eval
                ]
#             , to_numpy_array = True
            , show_sql = True
            )

    @classmethod
    def getAllFixedOppoBehDy(cls, listing_ass_adopted, listing_ass_proportion):
        return cls.getByParams(
            equalparams = {"exp_name":"T4"
                           , "listing_ass_adopted":listing_ass_adopted
                           , "listing_ass_proportion":listing_ass_proportion
                           }
            , colparams = [
                 {"name":"trail_results_id"},
                 {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}  # , "cast_by":literal_eval
                ]
#             , notlikeparams = {"cvg_joint_behavior":["T,L"]}
#             , to_numpy_array = True
            , show_sql = True
            )
