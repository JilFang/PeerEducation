'''
Created on 28 Aug 2020

@author: w
'''
from tables.Table import Table


class TNetworks(Table):

    @classmethod
    def getTableName(cls):
        return "networks"

    @classmethod
    def getAll(cls):
        return cls.getByParams(
            equalparams = {}
            , colparams = [{"name": "networks_id"}
                           , {"name":"type"}
                           , {"name":"adjlist"}
                           , {"name":"agent_num"}
                        ])
    @classmethod
    def getById(cls, networks_id):
        return cls.getByParams(
            equalparams = {"networks_id":networks_id}
            , colparams = [{"name": "networks_id"}
                           , {"name":"type"}
                           , {"name":"adjlist"}
                           , {"name":"agent_num"}
                        ])