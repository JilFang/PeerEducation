'''
Created on 27Jun.,2020

@author: wang
'''
from tool.DB import db


class Table(object):
    """
        manage a table, e.g., getting data of interest
    """

    @classmethod
    def getTableName(cls):
        pass
    
    @classmethod
    def getDistinctColumnValues(cls, param_name_list, equalparams):
        colparams = []
        for param_name in param_name_list:
            colparams.append({"name":param_name})
        return db.get_where(table = cls.getTableName()
                     , equalparams = equalparams
                     , colparams = colparams
                     , distinct = True)

    @classmethod
    def insert(cls, data = None):
        """
            data: dictionary type
        """
        assert data != None
        db.insert_or_update(cls.getTableName(), data)
        return db.LAST_INSERT_ID()

    @classmethod
    def save(cls, equalparams = None, data = None):
        assert data != None
        db.insertOrUpdate(cls.getTableName(), equalparams, data)

    @classmethod
    def getByParams(cls
            , equalparams = None
            , likeparams = {}
            , notlikeparams = {}
            , colparams = None
            , to_numpy_array = False
            , order_by_asc = None
            , group_by = []
            , show_sql = False
            ):
        return db.get_where(table = cls.getTableName()
                 , equalparams = equalparams
                 , likeparams = likeparams
                 , notlikeparams = notlikeparams
                 , colparams = colparams
                 , to_numpy_array = to_numpy_array
                 , order_by_asc = order_by_asc
                 , group_by = group_by
                 , show_sql = show_sql
                 )

    @classmethod
    def getBySql(cls, sql):
        return db.select_sql(sql)

    @classmethod
    def saveOrUpdate(cls, equalparams, saving_data):
        db.insertOrUpdate(cls.getTableName(), equalparams, saving_data)

    @classmethod
    def insertIfNotExist(cls, equalparams, saving_data):
        return db.insertIfNotExist(cls.getTableName(), equalparams, saving_data)
