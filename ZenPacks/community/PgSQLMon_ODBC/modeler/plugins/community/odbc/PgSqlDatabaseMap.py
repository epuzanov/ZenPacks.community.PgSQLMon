################################################################################
#
# This program is part of the PgSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010. 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""PgSqlDatabaseMap.py

PgSqlDatabaseMap maps the PostgreSQL Databases table to Database objects

$Id: PgSqlDatabaseMap.py,v 1.6 2011/12/18 20:36:17 egor Exp $"""

__version__ = "$Revision: 1.6 $"[11:-2]

import re
from string import lower
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class PgSqlDatabaseMap(SQLPlugin):


    ZENPACKID = 'ZenPacks.community.PgSQLMon_ODBC'

    maptype = "DatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.PgSQLMon_ODBC.PgSqlDatabase"
    cspropname = "zPgSqlConnectionString"
    deviceProperties = SQLPlugin.deviceProperties+('zPgSqlUsername',
                                                   'zPgSqlPassword',
                                                   'zPgSqlConnectionString',
                                                   'zPgSqlDatabaseIgnoreNames',
                                                   'zPgSqlDatabaseIgnoreTypes',
                                                   )


    def prepareCS(self, device):
        args = [getattr(device, self.cspropname, '') or \
                    "'pyisqldb',DRIVER='{PostgreSQL}',port='5432',ansi=True"]
        kwkeys = map(lower, eval('(lambda *arg,**kws:kws)(%s)'%args[0]).keys())
        if 'user' not in kwkeys:
            args.append("user='%s'"%getattr(device, 'zPgSqlUsername', ''))
        if 'host' not in kwkeys:
            args.append("host='%s'"%getattr(device, 'manageIp', 'localhost'))
        if 'database' not in kwkeys:
            args.append("database='template1'")
        if 'password' not in kwkeys:
            args.append("password='%s'"%getattr(device, 'zPgSqlPassword', ''))
        return ','.join(args)


    def queries(self, device):
        return {
            "databases": (
                """SELECT d.datname as dbname,
                          u.rolname as contact,
                          'Ver.'||current_setting('server_version') as version,
                          current_setting('block_size')::float as blocksize,
                          t.spcname as setdbsrvinst,
                          d.datallowconn::int as allowconn,
                          CASE d.datistemplate
                              WHEN True THEN 'PgSqlTemplate'
                              ELSE 'PgSqlDatabase'
                          END as type,
                          pg_database_size(d.datname)::float as totalblocks
                   FROM pg_database d,
                        pg_roles u,
                        pg_tablespace t
                   WHERE d.datdba=u.oid AND d.dattablespace=t.oid""",
                None,
                self.prepareCS(device),
                {
                    'dbname': 'dbname',
                    'contact':'contact',
                    'version':'version',
                    'blocksize':'_blockSize',
                    'setdbsrvinst':'_setDBSrvInst',
                    'allowconn':'allowConn',
                    'type':'type',
                    'totalblocks': 'totalBlocks',
                }
            ),
        }


    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        skiptsnames = getattr(device, 'zPgSqlDatabaseIgnoreNames', None)
        skiptstypes = getattr(device, 'zPgSqlDatabaseIgnoreTypes', None)
        rm = self.relMap()
        for db in results.get('databases', []):
            if (skiptsnames and re.search(skiptsnames,db['dbname'])):continue
            if (skiptstypes and re.search(skiptstypes,db['type'])):continue
            try:
                om = self.objectMap(db)
                om.id = self.prepId(om.dbname)
                om.version = str(om.version[4:])
            except AttributeError:
                continue
            rm.append(om)
        return rm
