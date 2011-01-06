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

$Id: PgSqlDatabaseMap.py,v 1.3 2011/01/02 21:46:18 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

import re
from ZenPacks.community.ZenODBC.OdbcPlugin import OdbcPlugin

class PgSqlDatabaseMap(OdbcPlugin):


    ZENPACKID = 'ZenPacks.community.PgSQLMon_ODBC'

    maptype = "PgSqlDatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.PgSQLMon_ODBC.PgSqlDatabase"
    deviceProperties = \
                OdbcPlugin.deviceProperties + ('zPgSqlUsername',
                                               'zPgSqlPassword',
                                               'zPgSqlConnectionString',
                                               'zPgSqlDatabaseIgnoreNames',
                                               'zPgSqlDatabaseIgnoreTypes',
                                               )


    def queries(self, device):
        uid = pwd = None
        cs = [getattr(device, 'zPgSqlConnectionString', 'DRIVER={PostgreSQL}')]
        options = [opt.split('=')[0].strip().upper() for opt in cs[0].split(';')]
        if 'SERVERNAME' not in options:cs.append('SERVERNAME=%s'%device.manageIp)
        cs.append('DATABASE=template1')
        if 'UID' not in options: uid = getattr(device, 'zPgSqlUsername', None)
        if uid: cs.append('UID=%s'%uid)
        if 'PWD' not in options: pwd = getattr(device, 'zPgSqlPassword', None)
        if pwd: cs.append('PWD=%s'%pwd)
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
                        pg_authid u,
                        pg_tablespace t
                   WHERE d.datdba=u.oid AND d.dattablespace=t.oid""",
                None,
                ';'.join(cs),
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
                om.status = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm
