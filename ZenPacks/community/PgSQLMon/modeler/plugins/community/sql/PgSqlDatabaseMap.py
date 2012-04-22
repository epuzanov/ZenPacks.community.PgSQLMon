################################################################################
#
# This program is part of the PgSQLMon Zenpack for Zenoss.
# Copyright (C) 2009-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""PgSqlDatabaseMap.py

PgSqlDatabaseMap maps the PostgreSQL Databases table to Database objects

$Id: PgSqlDatabaseMap.py,v 1.7 2012/04/18 20:57:30 egor Exp $"""

__version__ = "$Revision: 1.7 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
import re

class PgSqlDatabaseMap(ZenPackPersistence, SQLPlugin):


    ZENPACKID = 'ZenPacks.community.PgSQLMon'

    maptype = "DatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.PgSQLMon.PgSqlDatabase"
    deviceProperties = SQLPlugin.deviceProperties+('zPgSqlUsername',
                                                   'zPgSqlPassword',
                                                   'zPgSqlConnectionString',
                                                   'zPgSqlDatabaseIgnoreNames',
                                                   'zPgSqlDatabaseIgnoreTypes',
                                                   )


    def queries(self, device):
        queries = {}
        connectionString = getattr(device, 'zPgSqlConnectionString', '') or \
            "'pyisqldb',DRIVER='{PostgreSQL}',host='${here/manageIp}',port='5432',database='${here/dbname}',user='${here/zPgSqlUsername}',password='${here/zPgSqlPassword}',ansi=True"
        setattr(device, 'dbname', 'template1')
        cs = self.prepareCS(device, connectionString)
        queries["databases"] = (
                """SELECT d.datname as dbname,
                          u.rolname as contact,
                          current_setting('server_version') as version,
                          current_setting('block_size')::float as blocksize,
                          t.spcname as setdbsrvinst,
                          d.datallowconn::int as allowconn,
                          CASE d.datistemplate
                              WHEN True THEN 'PgSqlTemplate'
                              ELSE 'PgSqlDatabase'
                          END as type,
                          ceil(pg_database_size(d.datname)::float/current_setting('block_size')::float) as totalblocks
                   FROM pg_database d,
                        pg_roles u,
                        pg_tablespace t
                   WHERE d.datdba=u.oid AND d.dattablespace=t.oid""",
                None,
                cs,
                {
                    'dbname': 'dbname',
                    'contact':'contact',
                    'version':'version',
                    'blocksize':'blockSize',
                    'setdbsrvinst':'_setDBSrvInst',
                    'allowconn':'allowConn',
                    'type':'type',
                    'totalblocks': 'totalBlocks',
                })
        return queries


    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        skiptsnames = getattr(device, 'zPgSqlDatabaseIgnoreNames', None)
        skiptstypes = getattr(device, 'zPgSqlDatabaseIgnoreTypes', None)
        rm = self.relMap()
        for db in results.get('databases', ()):
            if skiptsnames and re.search(skiptsnames, db.get('dbname','')):
                continue
            if skiptstypes and re.search(skiptstypes, db.get('type','')):
                continue
            try:
                om = self.objectMap(db)
                om.id = self.prepId(om.dbname)
            except AttributeError:
                continue
            rm.append(om)
        return rm
