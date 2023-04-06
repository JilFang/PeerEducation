'''
Created on 10 Sep 2020

@author: w
'''
from tables.Table import Table
from ast import literal_eval
from tool.Tools import Tools


class TTrailResultsMean(Table):

    @classmethod
    def getTableName(cls):
        return "trail_results_mean"

    @classmethod
    def getByExpName(cls, exp_name):
        return cls.getByParams(
            equalparams = {"exp_name":exp_name
                           }
            , colparams = [
                {"name":"trail_results_mean_id"}
                , {"name":"episode_dynamics_mean"}   # , "cast_by":literal_eval
                ])