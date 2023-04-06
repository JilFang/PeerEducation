import os
from tool.DB import DB
from Config import PROJECT_NAME, DB_NAME, PWD, MYSQL_PATH_MAC
import time
import re
from tool.Tools import Tools

########################################################
###### when the current DB does NOT contain new experiments
###### restore the latest dumped sql.
########################################################
mysql_bin_path = ""
if Tools.isMyMacBook():
    mysql_bin_path = MYSQL_PATH_MAC

dbzipfilename = "files/%s.sql.gz" % (DB_NAME)
print ("DB Zip File: %s" % (dbzipfilename))
print("Last modified: %s" % time.ctime(os.path.getmtime(dbzipfilename)))
while True:
    yn = input("Restore this backup file to DB? [y/n]")
    if re.findall("^[Nn]$", yn):
        break
    elif re.findall("^[Yy]$", yn):
        db = DB.getInstance()
        res = db.select_sql("show tables")
        # print res
        for table in res:
        #     print table[0]
            table = table[0]
            if table.find("view") != -1:
                db.dropView(table)
            else:
                db.dropTable(table)
            print ('Drop %s' % table)
#         db.close()
        cmd = "gunzip < files/%s.sql.gz | %smysql -uroot -p%s %s" % (DB_NAME, mysql_bin_path, PWD, DB_NAME)
        os.system(cmd)
        print ("Done")
        break
    else:
        print ("Please input [y/n].")  # TODO learn regex and support yes/no
