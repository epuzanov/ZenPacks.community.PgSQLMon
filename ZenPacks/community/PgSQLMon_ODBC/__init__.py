
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ PgSQLMon loader
    """

    packZProperties = [
            ('zPgSqlConnectionString', "'pyisqldb',DRIVER='{PostgreSQL}',port='5432',ansi=True", 'string'),
            ('zPgSqlUsername', 'zenoss', 'string'),
            ('zPgSqlPassword', '', 'password'),
            ('zPgSqlDatabaseIgnoreNames', '', 'string'),
            ('zPgSqlDatabaseIgnoreTypes', '', 'string'),
            ]
