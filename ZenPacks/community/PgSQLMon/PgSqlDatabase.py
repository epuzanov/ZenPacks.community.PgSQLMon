################################################################################
#
# This program is part of the PgSQLMon Zenpack for Zenoss.
# Copyright (C) 2009-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""PgSqlDatabase

PgSqlDatabase is a Database

$Id: PgSqlDatabase.py,v 1.3 2012/04/18 21:38:03 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.RDBMS.Database import Database


class PgSqlDatabase(Database):
    """
    Database object
    """

    ZENPACKID = 'ZenPacks.community.PgSQLMon'

    allowConn = True

    _properties = Database._properties + (
                 {'id':'allowConn', 'type':'boolean', 'mode':'w'},
                 )

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        tnames = ['PgSqlDatabase',]
        if self.allowConn:
            tnames.append('PgSqlDatabaseStat')
        for tname in tnames:
            templ = self.getRRDTemplateByName(tname)
            if templ is not None:
                templates.append(templ)
        return templates

    def usedBytes(self):
        """
        Return the number of used bytes
        """
        return self.cacheRRDValue('statDb_sizeUsed', 0)

InitializeClass(PgSqlDatabase)
