#!/usr/bin/env python

from __future__ import division

from squawk.parsers.nginx import AccessLogParser
from squawk.query import *

def output_console(query, source):
    print "\t| ".join(query.columns)
    print "-"*40
    for row in query.execute(parser):
        print "\t| ".join(row[k] if isinstance(row[k], basestring) else str(row[k]) for k in query.columns)

if __name__ == "__main__":
    query = Query("SELECT COUNT(1) AS n, remote_addr FROM file WHERE status = 200 AND remote_addr != '-' GROUP BY remote_addr ORDER BY n DESC LIMIT 10")
    # query = Query("SELECT count(1) FROM file WHERE status = 200 AND remote_addr != '-' LIMIT 20")
    # query = Query("SELECT count(1) FROM file")
    parser = AccessLogParser("access.log")
    output_console(query, parser)
    # for row in query.execute(parser):
    #     print "%s\t%d" % (row['remote_addr'], row['n'])
    # for row in query.execute(parser):
    #     print row #"%s\t%d" % (row['remote_addr'], row['n'])
