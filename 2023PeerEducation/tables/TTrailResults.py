'''
Created on 10 Sep 2020

@author: w
'''
from tables.Table import Table
from ast import literal_eval
from tool.Tools import Tools
from tables.TTrailResultsMean import TTrailResultsMean


class TTrailResults(Table):

    @classmethod
    def getTableName(cls):
        return "trail_results"

    @classmethod
    def getByExpName(cls, exp_name):
        return cls.getByParams(
            equalparams = {"exp_name":exp_name
                           }
            , colparams = [
                {"name":"trail_results_id"}
                , {"name":"episode_dynamics"}  # , "cast_by":literal_eval
                ])

    @classmethod
    def getByEqualparams(cls, equalparams):
        return cls.getByParams(
            equalparams = equalparams
            , colparams = [
                        {"name":"trail_results_id"}
                        , {"name":"episode_dynamics", "cast_by":Tools.bstr_to_valuestr}
                        ])

    @classmethod
    def getAll(cls):
        equalparams = {}
        return cls.getByEqualparams(equalparams)

    @classmethod
    def setCvgJointBehavior(cls, equalparams):
        res = cls.getByEqualparams(equalparams)
        print(len(res))
        for row in res:
            _id = row["trail_results_id"]
            print(row)
            dy = row["episode_dynamics"]
            cvg_joint_behavior = ""
            last_epi_ja_dis = dy[-1]

            ja00 = last_epi_ja_dis[1]
            ja01 = last_epi_ja_dis[2]
            ja10 = last_epi_ja_dis[3]
            ja11 = last_epi_ja_dis[4]

            if ja00 == 15:
                cvg_joint_behavior = "T,L"
            if ja01 == 15:
                cvg_joint_behavior = "T,NL"
            if ja10 == 15:
                cvg_joint_behavior = "NT,L"
            if ja11 == 15:
                cvg_joint_behavior = "NT,NL"

            equalparams = {"trail_results_id":_id}
            saving_data = {"cvg_joint_behavior":cvg_joint_behavior}
            print(_id, cvg_joint_behavior)
            cls.saveOrUpdate(equalparams, saving_data)
