from shutil import copytree, ignore_patterns
import os
import shutil
from Config import ROOT_DIR, PROJECT_NAME
import datetime
from tool.Tools import Tools


def saveProject():
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    now = datetime.datetime.now()

    timestampPath = "%s/backup/files/latestSavedTimestamp" % (ROOT_DIR)
    Tools.writeStringToFile(str(now), timestampPath)

    dest = '%s/%s_%s_%s_%s' % (desktop, PROJECT_NAME, now.year, now.month, now.day)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    copytree(ROOT_DIR, dest, ignore = ignore_patterns(
    #     'res*',
        '*.pyc',
        'tmp*'))

    print ('copy %s to %s' % (PROJECT_NAME, desktop))



if __name__ == "__main__":
    saveProject()
