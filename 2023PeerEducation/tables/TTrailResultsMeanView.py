'''
Created on 10 Sep 2020

@author: w
'''
from tables.Table import Table
from ast import literal_eval
from tool.Tools import Tools


class TTrailResultsMeanView(Table):

    @classmethod
    def getTableName(cls):
        return "trail_results_mean_view"

    @classmethod
    def getByExpNameAss(cls, exp_name, listing_ass_adopted, episode_num):
        return cls.getByParams(
            equalparams = {
                "exp_name":exp_name
                , "listing_ass_adopted":listing_ass_adopted
                , "episode_num": episode_num
               }
            , colparams = [
                {"name":"trail_results_mean_id"}
                , {"name":"episode_num"}
                , {"name":"listing_ass_proportion"}
                , {"name":"episode_dynamics_mean", "cast_by":Tools.bstr_to_valuestr}
                ]
            , order_by_asc = "listing_ass_proportion"
            )
        
        
    @classmethod
    def getInterNumByExpNameAss(cls, exp_name, listing_ass_adopted):
        return cls.getByParams(
            equalparams = {
                "exp_name":exp_name
                , "listing_ass_adopted":listing_ass_adopted
               }
            , colparams = [
                {"name":"trail_results_mean_id"}
                , {"name":"ass_class_inter_num_mean", "cast_by":Tools.bstr_to_valuestr}
                , {"name":"listing_ass_proportion", "cast_by":literal_eval}
                ]
            , order_by_asc = "listing_ass_proportion"
            )
        
