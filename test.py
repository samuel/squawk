#!/usr/bin/env python

from __future__ import division

from squawk.parsers.nginx import AccessLogParser
from squawk.query import *
from squawk.output import output_console, output_json
from squawk.sql import sql_parser

if __name__ == "__main__":
    # t = sql_parser.parseString("SELECT COUNT(1) FROM (SELECT COUNT(1) AS n FROM file WHERE status = 200 GROUP BY remote_addr) t1 WHERE t1.n > 100")
    # for x in t.tables:
    #     print x

    # query = Query(
    #     "SELECT COUNT(1)"
    #     " FROM ("
    #     "  SELECT COUNT(1) n"
    #     "  FROM file"
    #     "  WHERE status = 200 AND remote_addr != '-'"
    #     "  GROUP BY remote_addr"
    #     " )"
    #     " WHERE n > 1000")
    # # parser = Limit(AccessLogParser("access.log"), 1000)
    # parser = AccessLogParser("access.log")
    # output_console(query.columns, query(parser))

    query = Query("SELECT COUNT(1) AS n, remote_addr FROM file WHERE status = 200 AND remote_addr != '-' GROUP BY remote_addr ORDER BY n DESC") #" LIMIT 10")
    # query = Query("SELECT count(1) FROM file WHERE status = 200 AND remote_addr != '-' LIMIT 20")
    # query = Query("SELECT count(1) FROM file")
    parser = AccessLogParser("access.log")
    output_console(query.columns, query(parser))
    # parser = AccessLogParser("access.log")
    # output_json(query.columns, query.execute(parser))
    # for row in query.execute(parser):
    #     print "%s\t%d" % (row['remote_addr'], row['n'])
    # for row in query.execute(parser):
    #     print row #"%s\t%d" % (row['remote_addr'], row['n'])
