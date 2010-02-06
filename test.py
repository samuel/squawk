#!/usr/bin/env python

from __future__ import division

from squawk.parsers.nginx import AccessLogParser
from squawk.query import *

# tokens =  ['select', [[['count', '1'], 'AS', 'N'], [['IP']]], 'from', ['FILE'], 'where', ['STATUS', '=', 200], 'group', 'by', [['IP']], 'order', 'by', [['N'], 'DESC'], 'limit', 10]
# tokens.columns =
#   ['count', '1'] AS N
#   ['IP'] AS 
# tokens.tables = ['FILE']
# tokens.where = [['STATUS', '=', 200]]
# tokens.groupby = [['IP']]
#   ['IP']
# tokens.orderby = [['N'], 'DESC']
# tokens.limit = 10

if __name__ == "__main__":
    query = Query("SELECT COUNT(1) AS n, remote_addr FROM file WHERE status = 200 GROUP BY remote_addr ORDER BY n DESC LIMIT 10")
    parser = AccessLogParser("access.log")
    for row in query.execute(parser):
        print "%s\t%d" % (row['remote_addr'], row['n'])

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
