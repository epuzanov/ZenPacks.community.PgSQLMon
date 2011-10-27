================================
ZenPacks.community.PgSQLMon_ODBC
================================

About
=====

This project is `Zenoss <http://www.zenoss.com/>`_ extension (ZenPack) that
makes it possible to model and monitor `PostgreSQL <http://www.postgresql.org/>`_
databases.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2 and Zenoss 3.2. You can download the free Core version of
Zenoss from http://community.zenoss.org/community/download

ZenPacks
--------

You must first install

- `SQLDataSource ZenPack <http://community.zenoss.org/docs/DOC-5913>`_
- `RDBMS Monitoring ZenPack <http://community.zenoss.org/docs/DOC-3447>`_

External dependencies
---------------------

You can use **pyisqldb** module provided by SQLDataSource ZenPack (**pyisqldb**
is a wrapper for **isql** command from `unixODBC <http://www.unixodbc.org/>`_
package), or install ONE of DB-API 2.0 compatible modules for PostgrSQL database.
Module must be installed with **easy_install-2.6** command as **zenoss** user.

- **pyisqldb** - DB-API 2.0 compatible wrapper for **isql** command from
  `unixODBC <http://www.unixodbc.org/>`_. PostgreSQL ODBC driver must be
  installed and registered with name "PostgreSQL".

  zPgSqlConnectionString example:

      ::

          'pyisqldb',DRIVER='{PostgreSQL}',port='5432',ansi=True

- `pyodbc <http://code.google.com/p/pyodbc/>`_ - DB-API 2.0 compatible interface
  to unixODBC. PostgreSQL ODBC driver must be installed and registered with name
  "PostgreSQL".

  zPgSqlConnectionString example:

      ::

          'pyodbc',DRIVER='{PostgreSQL}',port='5432',ansi=True

- `pg8000 <http://pybrary.net/pg8000/>`_ - DB-API 2.0 compatible Pure-Python
  interface to the PostgreSQL database engine.

  zPgSqlConnectionString example:

      ::

          'pg8000.dbapi',port=5432

Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `PgSQLMon_ODBC ZenPack <http://community.zenoss.org/docs/DOC-3497>`_.
Copy this file to your Zenoss server and run the following commands as the zenoss
user.

    ::

        zenpack --install ZenPacks.community.PgSQLMon_ODBC-2.3.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the PgSQLMon_ODBC
ZenPack you should clone the git `repository <https://github.com/epuzanov/ZenPacks.community.PgSQLMon_ODBC>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.PgSQLMon_ODBC.git
        zenpack --link --install ZenPacks.community.PgSQLMon_ODBC
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.

Configuration Properties
------------------------

- zPgSqlConnectionString
- zPgSqlUsername
- zPgSqlPassword
- zPgSqlDatabaseIgnoreNames
- zPgSqlDatabaseIgnoreTypes

Modeler Plugins
---------------

- community.odbc.PgSqlDatabaseMap

Monitoring Templates
--------------------

- PgSqlDatabase

Performance graphs
------------------

- PostgreSQL Database Size
- PostgreSQL Connections
- PostgreSQL Transactions
- PostgreSQL Disk Read
- PostgreSQL Command Statistics
- PostgreSQL Scans Statistics
- PostgreSQL Block Requests
- PostgreSQL Toast Block Requests
