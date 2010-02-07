
Description
===========

Squawk is a library and command line tool for running SQL queries
against structured/semi-structured static files.
(e.g. Apache logs, csv files, tcpdump output).

License
=======

BSD

See LICENSE

Goal
====

The purpose is Squawk is to make querying for data in log files or other
structured files easier. Everything that Squawk does can be done by
combining various unix tools, but Squawk makes it ever easier to express
more complex relationships. It is in no way a database or meant to be
used as such. It's merely a reporting tool.

Squawk can be used from the command line for ad-hoc queries, and it can
also be used as a library as a part of a more in-depth reporting tool.

Status
======

Still in major development. API is guaranteed to change.

Supported SQL Features
======================

 * Aggregates: count, min, max, avg, sum
 * GROUP BY (single column)
 * ORDER BY (single column)
 * LIMIT
 * OFFSET
 * WHERE
 * Column aliases
 * Subqueries in FROM

Departures from Standard SQL
============================

 * Table list in FROM uses a space rather than a comma as a separator.
   This makes it easier on the command line to specify files.
   (e.g. FROM access.log* )

Supported Output Formats
========================

 * Basic tabular for console (like most database command line tools)
 * JSON
 * CSV

Examples
========

SQL query on the command line::

    $ python -m squawk.command "SELECT COUNT(1) AS n, status FROM" access.log "GROUP BY status ORDER BY n DESC"
    n	| status
    ----------------------------------------
    381353	| 200
    180668	| 302
    17976	| 404
    12952	| 301
    10836	| 304
    735	| 403
    420	| 206
    376	| 416
    123	| 400
    46	| 500
    5	| 502
    3	| 408
    3	| 405
    1	| 504

SQL based query through API::

    query = Query("SELECT COUNT(1) AS n, remote_addr FROM file WHERE status = 200 AND remote_addr != '-' GROUP BY remote_addr ORDER BY n DESC LIMIT 10")
    source = AccessLogParser("access.log")
    output_console(query, source)
    
    # or
    
    query = Query("SELECT COUNT(1) AS n, remote_addr FROM file WHERE status = 200 AND remote_addr != '-' GROUP BY remote_addr ORDER BY n DESC LIMIT 10")
    source = AccessLogParser("access.log")
    for row in query.execute(source):
        print row

Code generated query::

    source = AccessLogParser("access.log")
    filtered = Filter(source, lambda row:row['status'] == 200)
    group_by = GroupBy(filtered, group_by="remote_addr", select=[
        lambda:Column('remote_addr'),
        lambda:CountAggregate(None, 'count(1)')])
    order_by = OrderBy(group_by, 'count(1)', True)
    limit = Limit(order_by, 10)
    for row in limit:
        print row
