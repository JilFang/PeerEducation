
import pymysql
from Config import DB_NAME, PWD
from pip._vendor.pyparsing import col
import numpy
from tool.Tools import Tools


class DB:
    COL_PARAM_NAME = "name"
    COL_PARAM_CAST_BY = "cast_by"
    """
        Default: 
        id column name = table name + "_id"
    """
    __instance = None

    @staticmethod
    def getInstance(db_name = None):
        """ Static access method. """
        if DB.__instance == None:
            DB(db_name)
        return DB.__instance

    def connect(self, databaseName):
        return pymysql.connect(host = "localhost",  # your host, usually localhost
                                 user = "root",  # your username
                                 passwd = PWD,  # your password
                                 db = databaseName)  # name of the data base

    def reConnectToDB(self, databaseName):
        self.db = self.connect(databaseName)
        self.cur = self.db.cursor()
        return self.db

    def __init__(self, db_name = None):
        """ Virtually private constructor. """
        if DB.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DB.__instance = self
            if db_name != None:
                databaseName = db_name
            else:
                databaseName = DB_NAME
            self.db = self.connect(databaseName)
            self.cur = self.db.cursor()

    def __del__(self):
        self.close()

    def insert(self, table, data):

        columns = ', '.join("%s" % (k) for k, v in data.items())
        values = ', '.join("\"%s\"" % (v,) for k, v in data.items())

        sql_str = 'INSERT INTO {table} ({columns}) VALUES ({values})'
        sql_str = sql_str.replace('{table}', table) \
            .replace('{columns}', columns) \
            .replace('{values}', values)
#         print (sql_str)
        try:
            _res = self.cur.execute(sql_str)
            self.db.commit()
            return _res
        except pymysql.MySQLError as e:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            self.db.rollback()

        return None

#             ", ".join "%s" % (k, v) for k, v in data.items()
    def update(self, tableName, data):

        sql = []
        sql.append("UPDATE %s SET" % tableName)
        if len(data) > 0:
            sql.append(", ".join("%s = '%s'" % (k, v) for k, v in data.items()))
        sql.append("WHERE %s_id = %d " % (tableName, data[tableName + "_id"]))
        sql_str = " ".join(sql)
#         print (sql_str)
        try:
            _res = self.cur.execute(sql_str)
            self.db.commit()
            return _res
        except pymysql.MySQLError as e:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            self.db.rollback()

        return None

    def delete(self, tableName, data):
        sql = []
        sql.append("DELETE FROM %s" % tableName)
        if len(data) > 0:
            sql.append("WHERE " + " AND ".join("%s = '%s'" % (k, v) for k, v in data.items()))
        sql_str = " ".join(sql)
        try:
            _res = self.cur.execute(sql_str)
            self.db.commit()
            return _res
        except pymysql.MySQLError as e:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            self.db.rollback()

#         cur.execute("SHOW columns FROM training_results")
    def get_where(self
                  , table = None
                  , equalparams = {}
                  , likeparams = {}
                  , notlikeparams = []
                  , colparams = []  # e.g., colparams = [{"name":"g_u", "cast_by":str},{"name":"distance"}]
                  , distinct = False
                  , order_by_asc = None
                  , order_by_desc = None
                  , group_by = []
                  , to_numpy_array = False
                  , show_sql = False
                  ):
        assert table != None and colparams != None
#         if equalparams != None:
#             Tools.removeNoneValueKeys(equalparams)
        sql = []
        col_names_str = ""
        if len(colparams) == 0:
            col_names_str = "*"
        else:
#             col_names_str = ", ".join(cols)
            col_names_str = ", ".join([col[DB.COL_PARAM_NAME] for col in colparams])
        distinctstr = ""
        if distinct:
            distinctstr = "DISTINCT"
        sql.append("SELECT %s %s FROM %s" % (distinctstr, col_names_str, table))
        if len(equalparams) > 0:
            sql.append("WHERE " + " AND ".join("%s = \"%s\"" % (k, v) for k, v in equalparams.items()))
        if len(likeparams) > 0:
            if len(equalparams) > 0:
                sql.append("AND " + self.likeSqlCovertion(likeparams, "")) #" AND ".join("%s LIKE \"%%%s%%\"" % (k, v) for k, v in likeparams.items()))
            else:
                sql.append("WHERE " + self.likeSqlCovertion(likeparams, "")) #" AND ".join("%s LIKE \"%%%s%%\"" % (k, v) for k, v in likeparams.items()))
        if len(notlikeparams) > 0:
            if len(equalparams) != 0 or len(likeparams) != 0:
                sql.append("AND " + self.likeSqlCovertion(notlikeparams, "NOT")) #" AND ".join("%s NOT LIKE \"%%%s%%\"" % (k, v) for k, v in notlikeparams.items()))
            else:
                sql.append("WHERE " + self.likeSqlCovertion(notlikeparams, "NOT")) #  " AND ".join("%s NOT LIKE \"%%%s%%\"" % (k, v) for k, v in notlikeparams.items()))
        if len(group_by) > 0:
            sql.append("GROUP BY %s" % (", ".join(group_by)))
        if order_by_asc != None:
            sql.append("ORDER BY %s ASC" % (order_by_asc))
        if order_by_desc != None:
            sql.append("ORDER BY %s DESC" % (order_by_desc))
        sql_str = " ".join(sql)
        if show_sql:
            print (sql_str)
        self.cur.execute(sql_str)
        res = self.cur.fetchall()
        if to_numpy_array:
            res = numpy.array(res)
        else:
            res = self.convertFetchallToDictList(res, colparams)
        return res

    def likeSqlCovertion(self, params=None, _not = "NOT"):
        sl = []
        for k, vals in params.items():
            s = " AND ".join("%s %s LIKE \"%%%s%%\"" % (k, _not, v) for v in vals)
            sl.append(s)
        return " AND ".join(sl)

    def convertFetchallToDictList(self, res, colparams):
        dict_list = []
        for row in res:
            row_dict = {}
            for ci in range(0, len(colparams)):
                colp = colparams[ci]
                if DB.COL_PARAM_CAST_BY in colp.keys():
                    row_dict[colp[DB.COL_PARAM_NAME]] = colp[DB.COL_PARAM_CAST_BY](row[ci])
                else:
                    row_dict[colp[DB.COL_PARAM_NAME]] = row[ci]
            dict_list.append(row_dict)
        return dict_list

    def select_sql(self, sql_str):
#         print(sql_str)
        self.cur.execute(sql_str)
        return self.cur.fetchall()

    def execute_and_commit(self, sql_str):
        try:
            _res = self.cur.execute(sql_str)
            self.db.commit()
            return _res
        except pymysql.MySQLError as e:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            self.db.rollback()

    def close(self):
        self.db.close()

    def insert_or_update(self, table = None, data = None):
#         res = self.get_where(tableName, data)
#         Tools.removeNoneValueKeys(data)
        if table + "_id" not in data.keys():  # len(res) == 0:
            return self.insert(table, data)
        else:
            return self.update(table, data)

    def insertOrUpdate(self, table = None, equalparams = None, data = None):
        col_id_name = table + "_id"
        colparams = [{"name": col_id_name}]
        res = self.get_where(table = table, equalparams = equalparams, colparams = colparams)
        if len(res) > 0:  # update
            for row in res:
#                 print(row)
                data[col_id_name] = row[col_id_name]
#                 print(data)
                self.insert_or_update(table, data)
        else:  # insert
            self.insert_or_update(table, data)

    def insertIfNotExist(self, table = None, equalparams = None, data = None):
        id_col_name = table + "_id"
#         print(id_col_name)
        colparams = [{"name": id_col_name}]
        res = self.get_where(table = table, equalparams = equalparams, colparams = colparams)
#         print(res, res[0][id_col_name])
        if len(res) == 0:
            self.insert_or_update(table, data)
            return self.LAST_INSERT_ID()
        else:
            return res[0][id_col_name]

        # otherwise do not insert
    def update_by_unique_index(self, table = None, equal_unique_params = None, data = None):
        res = self.get_where(table, equal_unique_params, cols = [table + "_id"])
        data[table + "_id"] = res[0][0]
#         print equal_unique_params, res[0][0], data
        self.insert_or_update(table, data)

    def LAST_INSERT_ID(self):
        sql_str = "SELECT LAST_INSERT_ID()"
        res = self.select_sql(sql_str)
        return res[0][0]

    def showCreateTable(self, table):
        sql_str = "SHOW CREATE TABLE `%s`" % table
        res = self.select_sql(sql_str)
        for text in res[0]:
            print (text)
        return res

    def emptyTable(self, table):
        # sql_str = "TRUNCATE TABLE `%s`" % table
#         res = self.execute_query(sql_str)
        sql_str = "TRUNCATE TABLE `%s`" % table
        try:
            _res = self.cur.execute(sql_str)
            self.db.commit()
            print ("TRUNCATE TABLE `%s`" % table)
            return _res
        except pymysql.MySQLError as e:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            self.db.rollback()

    def dropTable(self, table):
        sql_str = "DROP TABLE `%s`" % table
        try:
            _res = self.cur.execute(sql_str)
            self.db.commit()
            return _res
        except pymysql.MySQLError as e:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            self.db.rollback()

    def dropView(self, table):
        sql_str = "DROP VIEW `%s`" % table
        try:
            _res = self.cur.execute(sql_str)
            self.db.commit()
            return _res
        except pymysql.MySQLError as e:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            self.db.rollback()

    def renameTable(self, oldName, newName):
        sql_str = "RENAME TABLE %s TO %s" % (oldName, newName)
        try:
            _res = self.cur.execute(sql_str)
            self.db.commit()
            return _res
        except pymysql.MySQLError as e:
            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            self.db.rollback()


db = DB.getInstance()
