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

$Id: PgSqlDatabaseMap.py,v 1.9 2012/04/26 23:14:12 egor Exp $"""

__version__ = "$Revision: 1.9 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.DataMaps import MultiArgs
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
import re

DBQUERY = """SELECT
    d.datname as dbname,
    u.rolname as contact,
    current_setting('server_version') as version,
    current_setting('block_size')::float as blocksize,
    current_setting('port') as setdbsrvinst,
    d.datallowconn::int as allowconn,
    CASE d.datistemplate
        WHEN True THEN 'PgSqlTemplate'
        ELSE 'PgSqlDatabase'
    END as type,
    ceil(pg_database_size(d.datname)::float/current_setting('block_size')::float) as totalblocks
FROM pg_database d,
    pg_roles u,
    pg_tablespace t
WHERE d.datdba=u.oid AND d.dattablespace=t.oid"""

class PgSqlDatabaseMap(ZenPackPersistence, SQLPlugin):


    ZENPACKID = 'ZenPacks.community.PgSQLMon'

    maptype = "DatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.PgSQLMon.PgSqlDatabase"
    deviceProperties = SQLPlugin.deviceProperties+('zPgSqlUsername',
                                                   'zPgSqlPassword',
                                                   'zPgSqlConnectionString',
                                                   'zPgSqlPorts',
                                                   'zPgSqlDatabaseIgnoreNames',
                                                   'zPgSqlDatabaseIgnoreTypes',
                                                   )


    def queries(self, device):
        tasks = {}
        connectionString = getattr(device, 'zPgSqlConnectionString', '') or \
            "'pyisqldb',DRIVER='{PostgreSQL}',host='${here/manageIp}',port='${here/port}',database='${here/dbname}',user='${here/zPgSqlUsername}',password='${here/zPgSqlPassword}',ansi=True"
        setattr(device, 'dbname', 'template1')
        ports = getattr(device,'zPgSqlPorts', '') or '5432'
        if type(ports) is str:
            ports = [ports]
        for inst in ports:
            setattr(device, 'port', inst or '5432')
            cs = self.prepareCS(device, connectionString)
            tasks["si_%s"%inst] = (
                "SELECT 'PostgreSQL '||current_setting('server_version') as product, current_setting('port') as port",
                None,
                cs,
                {
                    'setProductKey':'product',
                    'port':'port',
                })
            tasks["db_%s"%inst] = (
                DBQUERY,
                None,
                cs,
                {
                    'dbname': 'dbname',
                    'contact':'contact',
                    'version':'version',
                    'blockSize':'blocksize',
                    'setDBSrvInst':'setdbsrvinst',
                    'allowConn':'allowconn',
                    'type':'type',
                    'totalBlocks': 'totalblocks',
                })
        return tasks


    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        skiptsnames = getattr(device, 'zPgSqlDatabaseIgnoreNames', None)
        skiptstypes = getattr(device, 'zPgSqlDatabaseIgnoreTypes', None)
        dbrm = self.relMap()
        irm = self.relMap()
        irm.relname = "softwaredbsrvinstances"
        for tname, result in results.iteritems():
            if tname.startswith('si_'):
                try:
                    inst = result[0]
                    om = self.objectMap(inst)
                except:
                    continue
                om.modname = "ZenPacks.community.PgSQLMon.PgSqlSrvInst"
                om.dbsiname = str(om.port).strip()
                om.id = self.prepId(om.dbsiname)
                om.setProductKey = MultiArgs(om.setProductKey, 'PostgreSQL')
                irm.append(om)
                continue
            elif tname.startswith('db_'):
                for db in result or ():
                    if skiptsnames and re.search(skiptsnames,
                                                db.get('dbname','')): continue
                    if skiptstypes and re.search(skiptstypes,
                                                db.get('type','')): continue
                    try:
                        om = self.objectMap(db)
                        om.id = self.prepId(om.dbname)
                    except AttributeError:
                        continue
                    dbrm.append(om)
            else: continue
        return [irm, dbrm]
