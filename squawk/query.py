
from __future__ import division
from functools import partial

from squawk.aggregates import aggregate_functions
from squawk.sql import sql_parser

OPERATOR_MAPPING = {
    '<>': '!=',
    '!=': '!=',
    '=': '==',
    '<': '<',
    '>': '>',
    '<=': '<=',
    '>=': '>=',
}

class Column(object):
    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self._value = None

    def update(self, row):
        self._value = row[self.column]

    def value(self):
        return self._value

class LimitOffset(object):
    def __init__(self, source, limit, offset=0):
        self.source = source
        self.limit = limit
        self.offset = offset

    def __iter__(self):
        for i, row in enumerate(self.source):
            if i < self.offset:
                continue

            yield row

            if self.limit is not None and i+1 >= self.limit + self.offset:
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
    def __init__(self, source, group_by, columns):
        self.source = source
        self.group_by = group_by
        self._columns = columns

    def __iter__(self):
        groups = {}
        for row in self.source:
            key = tuple(row[k] for k in self.group_by)
            if key not in groups:
                groups[key] = [x() for x in self._columns]
            for s in groups[key]:
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

class Selector(object):
    def __init__(self, source, columns):
        self.source = source
        self._columns = [(n.lower(), (a or n).lower()) for n, a in columns] if columns else None

    def __iter__(self):
        if self._columns:
            for row in self.source:
                yield dict((alias, row[name]) for name, alias in self._columns)
        else:
            for row in self.source:
                yield row

class Aggregator(object):
    def __init__(self, source, _columns):
        self.source = source
        self._columns = columns

    def __iter__(self):
        columns = [c() for c in self._columns]
        for row in self.source:
            for c in columns:
                c.update(row)
        yield dict((c.name, c.value()) for c in columns)

class Query(object):
    def __init__(self, sql):
        self.tokens = sql_parser.parseString(sql) if isinstance(sql, basestring) else sql
        self.columns = None
        self._table_subquery = None
        self._parts = self._generate_parts()

    def _generate_parts(self):
        """Return a list of callables that can be composed to build a query generator"""
        tokens = self.tokens
        parts = []

        self.columns = [self._column_builder(c) for c in tokens.columns] if tokens.columns != '*' else None

        if not isinstance(tokens.tables[0][0], basestring):
            self._table_subquery = Query(tokens.tables[0][0])

        if tokens.where:
            func = eval("lambda row:"+self._filter_builder(tokens.where))
            parts.append(partial(Filter, function=func))
        if tokens.groupby:
            # Group by query
            parts.append(partial(GroupBy,
                    group_by = [c[0] for c in tokens.groupby],
                    columns = self.columns))
        elif self.columns and any(len(c.name)>1 for c in tokens.columns):
            # Aggregate query
            parts.append(partial(Aggregator, columns=self.columns))
        else:
            # Basic select
            parts.append(partial(Selector, columns=[(c.name[0], c.alias) for c in tokens.columns] if tokens.columns != '*' else None))
        if tokens.orderby:
            order = tokens.orderby
            parts.append(partial(OrderBy, order_by=order[0][0], descending=order[1]=='DESC' if len(order) > 1 else False))
        if tokens.limit or tokens.offset:
            parts.append(partial(LimitOffset,
                limit = int(tokens.limit) if tokens.limit else None,
                offset = int(tokens.offset) if tokens.offset else 0))

        return parts

    def _filter_builder(self, where):
        """Return a Python expression from a tokenized 'where' filter"""
        l = []
        for expr in where:
            if expr[0] == '(':
                l.append("(")
                l.append(self._filter_builder(expr[1:-1]))
                l.append(")")
            else:
                if isinstance(expr, basestring):
                    l.append(expr)
                elif len(expr) == 3:
                    op = OPERATOR_MAPPING[expr[1]]
                    l.append('(row["%s"] %s %s)' % (expr[0].lower(), op, expr[2]))
                elif expr[1] == "in":
                    l.append('(row["%s"] in %r)' % (expr[0].lower(), expr[3:-1]))
                else:
                    raise Exception("Don't understand expression %s in where clause" % expr)
        return " ".join(l)

    def _column_builder(self, col):
        """Return a callable that builds a column or aggregate object"""
        if len(col.name) > 1:
            # Aggregate
            try:
                aclass = aggregate_functions[col.name[0]]
            except KeyError:
                raise KeyError("Unknown aggregate function %s" % col.name[0])
            return lambda:aclass(col.name[1], col.alias if col.alias else '%s(%s)' % (col.name[0], col.name[1]))
        else:
            # Column
            return lambda:Column(col.name[0], col.alias)

    def __call__(self, source):
        executor = self._table_subquery(source) if self._table_subquery else source
        for p in self._parts:
            executor = p(source=executor)
        executor.columns = [c().name for c in self.columns] if self.columns else source.columns
        return executor
