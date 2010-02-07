
Description
===========

Squawk is a library and command line tool for running SQL queries
against structured/semi-structured static files.
(e.g. Apache logs, csv files, tcpdump output).

Status
======

Still in major development. API is guaranteed to change.

Supported SQL Features
======================

 * Aggregates: count, min, max, avg, sum
 * GROUP BY (single column)
 * ORDER BY (single column)
 * LIMIT (no offset)
 * WHERE
 * Aliases for columns
 * Subqueries in FROM

Departures from Standard SQL
============================

 * Table list in FROM uses spaces rathe than commands. This makes it easier
   on the command line to specify files. (e.g. FROM access.log* )

Supported Output Formats
========================

 * Basic tabular for console
 * JSON

Examples
========

SQL query on the command line::

    python -m squawk.command "SELECT COUNT(1) AS n, status FROM" access.log "GROUP BY status ORDER BY n DESC"

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
