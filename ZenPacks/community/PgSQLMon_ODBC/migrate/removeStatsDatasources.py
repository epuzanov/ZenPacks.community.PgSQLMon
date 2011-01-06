################################################################################
#
# This program is part of the PgSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

class removeStatsDatasources( ZenPackMigration ):
    """
    remove statUser and statioUser Data Sources from RRDTemplates
    """
    version = Version(2, 2)

    def migrate(self, pack):


        for template in pack.dmd.Devices.Server.getAllRRDTemplates():
            if template.id != 'PgSqlDatabase': continue
            if hasattr(template.graphDefs, 'Postgresql Connections'):
                template.graphDefs._delObject('Postgresql Connections')
            if hasattr(template.graphDefs, 'Postgresql Database Size'):
                template.graphDefs._delObject('Postgresql Database Size')
            if hasattr(template.graphDefs, 'Postresql Disk Read'):
                template.graphDefs._delObject('Postresql Disk Read')
            if hasattr(template.graphDefs, 'Postgresql Transactions'):
                template.graphDefs._delObject('Postgresql Transactions')
            if hasattr(template.graphDefs, 'Postgresql DB Row'):
                template.graphDefs._delObject('Postgresql DB Row')
            if hasattr(template.graphDefs, 'Postgresql DB Row Index'):
                template.graphDefs._delObject('Postgresql DB Row Index')
            if hasattr(template.datasources, 'sizeUsed'):
                template.datasources._delObject('sizeUsed')
            if hasattr(template.datasources, 'statUser'):
                template.datasources._delObject('statUser')
            if hasattr(template.datasources, 'statioUser'):
                template.datasources._delObject('statioUser')

removeStatsDatasources()
