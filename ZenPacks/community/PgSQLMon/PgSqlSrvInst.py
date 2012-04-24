################################################################################
#
# This program is part of the PgSQLMon Zenpack for Zenoss.
# Copyright (C) 2009-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""PgSqlSrvInst

PgSqlSrvInst reperesents PostgreSQL server instance

$Id: PgSqlSrvInst.py,v 1.0 2012/04/24 23:19:40 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.RDBMS.DBSrvInst import DBSrvInst


class PgSqlSrvInst(DBSrvInst):
    """
    PgSQL SrvInst object
    """

    ZENPACKID = 'ZenPacks.community.PgSQLMon'

    port = 5432

    _properties = DBSrvInst._properties + (
        {'id':'port', 'type':'int', 'mode':'w'},
        )

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        return []

InitializeClass(PgSqlSrvInst)
