'''
Created on 10 Sep 2020

@author: w
'''
from tables.Table import Table
from ast import literal_eval
from tool.Tools import Tools
from tables.TTrailResultsMean import TTrailResultsMean


class TEmotionResults(Table):

    @classmethod
    def getTableName(cls):
        return "emotion_results"

    @classmethod
    def getByExpName(cls, exp_name):
        return cls.getByParams(
            equalparams = {"exp_name":exp_name}
            , colparams = [
                {"name":"emotion_results_id"}
                , {"name":"emotion_dynamics"}  # , "cast_by":literal_eval
                ])

    @classmethod
    def getByEqualparams(cls, equalparams):
        return cls.getByParams(
            equalparams = equalparams
            , colparams = [
                        {"name":"emotion_results_id"}
                        , {"name":"emotion_dynamics", "cast_by":Tools.bstr_to_valuestr}
                        ])

    @classmethod
    def getAll(cls):
        equalparams = {}
        return cls.getByEqualparams(equalparams)

    @classmethod
    def setCvgJointBehavior(cls, equalparams):
        print("1")
        res = cls.getByEqualparams(equalparams)
        print(len(res))
        for row in res:
            _id = row["emotion_results_id"]
            print(row)
            dy = row["emotion_dynamics"]
            cvg_emotion = ""
            last_epi_ja_dis = dy[-1]

            ja00 = last_epi_ja_dis[1]
            ja01 = last_epi_ja_dis[2]
            ja10 = last_epi_ja_dis[3]
            print(ja00)
            if ja00 == 15:
                cvg_emotion = "Joy"
            if ja01 == 15:
                cvg_emotion = "Fear"
            if ja10 == 15:
                cvg_emotion = "Angry"

            equalparams = {"emotion_results_id":_id}
            saving_data = {"cvg_emotion":cvg_emotion}
            print(_id, cvg_emotion)
            cls.saveOrUpdate(equalparams, saving_data)
