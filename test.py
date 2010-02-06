#!/usr/bin/env python

from __future__ import division

from squawk.parsers.nginx import AccessLogParser
from squawk.query import *

if __name__ == "__main__":
    # query = Query("SELECT COUNT(1) AS n, remote_addr FROM file WHERE status = 200 AND remote_addr != '-' GROUP BY remote_addr ORDER BY n DESC LIMIT 10")
    # query = Query("SELECT count(1) FROM file WHERE status = 200 AND remote_addr != '-' LIMIT 20")
    query = Query("SELECT count(1) FROM file")
    parser = AccessLogParser("access.log")
    # for row in query.execute(parser):
    #     print "%s\t%d" % (row['remote_addr'], row['n'])
    for row in query.execute(parser):
        print row #"%s\t%d" % (row['remote_addr'], row['n'])

    # filtered = Filter(parser, lambda row:row['status'] == 200)
    # group_by = GroupBy(filtered, group_by="remote_addr", select=[
    #     lambda:Column('remote_addr'),
    #     lambda:SumAggregate('bytes', 'bandwidth')])
    #     # lambda:CountAggregate(None, 'count(1)')])
    # order_by = OrderBy(group_by, 'bandwidth', True)
    # # order_by = OrderBy(group_by, 'count(1)', True)
    # limit = Limit(order_by, 10)
    # for row in limit:
    #     print "%s\t%.3f" % (row['remote_addr'], row['bandwidth'] / (1024*1024*1024))
