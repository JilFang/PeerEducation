'''
Created on 5 Sep 2020

@author: w
'''

from tables.Table import Table
from ast import literal_eval


class TTrailParameters(Table):

    @classmethod
    def getTableName(cls):
        return "trail_parameters"

    @classmethod
    def getTrailParamsByManualParams(cls, net_id, game_name, listing_ass_adopted
                          , listing_ass_proportion, ass_distribution_type):
        return cls.getByParams(
            equalparams = {"networks_id":net_id
                           , "game_name":game_name
                           , "listing_ass_adopted":listing_ass_adopted
                           , "listing_ass_proportion":listing_ass_proportion
                           , "ass_distribution_type":ass_distribution_type
                           }
            , colparams = [
                        {"name":"trail_parameters_id"}
#                         , {"name":"listing_ass_adopted_by_agent_ids", "cast_by":literal_eval}
                        ]
#             , show_sql= True
            )

    @classmethod
    def getTrailParamsByManualParamsNoProp(cls, net_id, game_name, listing_ass_adopted
                          , ass_distribution_type):
        print(net_id, listing_ass_adopted, ass_distribution_type)
        return cls.getByParams(
            equalparams = {"networks_id":net_id
                           , "game_name":game_name
                           , "listing_ass_adopted":listing_ass_adopted
                           , "ass_distribution_type":ass_distribution_type
                           }
            , colparams = [
                        {"name":"trail_parameters_id"}
                        , {"name":"listing_ass_adopted_by_agent_ids"
                         , "cast_by":literal_eval}
                        ])

    @classmethod
    def getAll(cls):
        equalparams = {}
        return cls.getTrailParamsByEqualparams(equalparams)

    @classmethod
    def getTrailParamsByEqualparams(cls, equalparams):
        return cls.getByParams(
            equalparams = equalparams
            , colparams = [
                        {"name":"trail_parameters_id"}
                        , {"name":"listing_ass_adopted", "cast_by":literal_eval}
                        , {"name":"listing_ass_proportion", "cast_by":literal_eval}
#                         , {"name":"listing_ass_adopted_by_agent_ids", "cast_by":literal_eval}
                        , {"name":"ass_distribution_type"}
                        ])
