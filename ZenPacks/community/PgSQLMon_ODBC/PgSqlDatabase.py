################################################################################
#
# This program is part of the PgSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""PgSqlDatabase

PgSqlDatabase is a Database

$Id: PgSqlDatabase.py,v 1.2 2011/01/06 01:14:44 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.RDBMS.Database import Database


class PgSqlDatabase(Database):
    """
    Database object
    """

    ZENPACKID = 'ZenPacks.community.PgSQLMon_ODBC'

    status = 2
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
        if self.allowConn: tnames.append('PgSqlDatabaseStat')
        for tname in tnames:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates


    def totalBytes(self):
        """
        Return the number of total bytes
        """
        return self.cacheRRDValue('statDb_sizeUsed', 0)


InitializeClass(PgSqlDatabase)
