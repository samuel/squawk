#!/usr/bin/env python

from __future__ import division
from functools import partial
import logging
from squawk.sql import sql_parser

class CountAggregate(object):
    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self.count = 0

    def update(self, row):
        self.count += 1

    def value(self):
        return self.count

class AvgAggregate(object):
    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self.sum = 0
        self.count = 0

    def update(self, row):
        self.sum += row[self.column]
        self.count += 1

    def value(self):
        if self.count == 0:
            return None
        return self.sum / self.count

class SumAggregate(object):
    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self.sum = 0

    def update(self, row):
        self.sum += row[self.column]

    def value(self):
        return self.sum

class Column(object):
    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self._value = None

    def update(self, row):
        self._value = row[self.column]

    def value(self):
        return self._value

class Limit(object):
    def __init__(self, source, limit):
        self.source = source
        self.limit = limit

    def __iter__(self):
        for i, row in enumerate(self.source):
            yield row
            if i+1 >= self.limit:
                return

class OrderBy(object):
    def __init__(self, source, order_by, descending=False):
        self.source = source
        self.order_by = order_by.lower()
        self.descending = descending

    def __iter__(self):
        results = list(self.source)
        results.sort(key=lambda row:row[self.order_by], reverse=self.descending)
        for r in results:
            yield r

class GroupBy(object):
    def __init__(self, source, group_by, select):
        self.source = source
        self.group_by = group_by.lower()
        self.select = select

    def __iter__(self):
        groups = {}
        for row in self.source:
            value = row[self.group_by]
            if value not in groups:
                groups[value] = [x() for x in self.select]
            for s in groups[value]:
                s.update(row)
        for key, row in groups.iteritems():
            yield dict((r.name, r.value()) for r in row)

class Filter(object):
    def __init__(self, source, function):
        self.source = source
        self.function = function

    def __iter__(self):
        for row in self.source:
            if self.function(row):
                yield row

class Query(object):
    def __init__(self, sql):
        self.tokens = sql_parser.parseString(sql)
        self._parts = []
        self._generate_parts()

    def _generate_parts(self):
        tokens = self.tokens
        if tokens.where:
            # TODO
            pass
        if tokens.groupby:
            self._parts.append(partial(GroupBy,
                    group_by = tokens.groupby[0][0],
                    select = [self._column_builder(c) for c in tokens.columns]))
        if tokens.orderby:
            order = tokens.orderby
            self._parts.append(partial(OrderBy, order_by=order[0][0], descending=order[1]=='DESC'))
        if tokens.limit:
            self._parts.append(partial(Limit, limit=int(tokens.limit)))

    def _column_builder(self, col):
        if len(col.name) > 1:
            # Aggregate
            if col.name[0] == 'count':
                return lambda:CountAggregate('count(%s)' % col.name[1], col.alias if col.alias else None)
            elif col.name[0] == 'sum':
                return lambda:SumAggregate(col.name[1], col.alias if col.alias else 'sum(%s)' % col.name[1])
            else:
                raise Exception("Unknown aggregate function %s" % col.name[0])
        else:
            # Column
            return lambda:Column(col.name[0], col.alias)

    def execute(self, source):
        executor = source
        for p in self._parts:
            executor = p(source=executor)
        return executor
