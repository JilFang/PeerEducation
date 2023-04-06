from Config import  PROJECT_NAME, PWD, MYSQL_PATH_MAC
import os
from backup.saveProject import saveProject
import re
import time
from tool.Tools import Tools


# ##
# ## work on and dump the latest DB
# ##
mysql_bin_path = ""
if Tools.isMyMacBook():
    mysql_bin_path = MYSQL_PATH_MAC
    
dbzipfilename = "../files/%s.sql.gz" % (PROJECT_NAME)
print ("DB Zip File: %s" % (dbzipfilename))
print("Last modified: %s" % time.ctime(os.path.getmtime(dbzipfilename)))
while True:
    yn = input("Dump and Override this backup file? [y/n]")
    if re.findall("^[Nn]$", yn):
        break
    elif re.findall("^[Yy]$", yn):

        cmd = "%smysqldump -uroot -p%s %s | gzip > ../files/%s.sql.gz" % (mysql_bin_path, PWD, PROJECT_NAME, PROJECT_NAME)
        os.system(cmd)
        print ("mysqldump done")
        saveProject()

        print ("Done")
        break
    else:
        print ("Please input [y/n].")   # TODO learn regex and support yes/no





