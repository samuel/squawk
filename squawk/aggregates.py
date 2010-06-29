
from __future__ import division

"""
An aggregate class is expected to accept two values at
instantiation: 'column' and 'name', and the class
must have two methods 'update(self, row)' and 'value(self)'.
The 'update' method is called for each row, and the 'value'
must return the final result of the aggregation.
"""

class Aggregate(object):
    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()

    def _to_number(self, val):
        if isinstance(val, (int, long, float)):
            return val
        if isinstance(val, basestring):
            if '.' in val:
                return float(val)
            return int(val)
        return float(val)

class AvgAggregate(Aggregate):
    """Calculate the average value for a column"""

    def __init__(self, *args, **kwargs):
        super(AvgAggregate, self).__init__(*args, **kwargs)
        self.sum = 0
        self.count = 0

    def update(self, row):
        self.sum += self._to_number(row[self.column]) 
        self.count += 1

    def value(self):
        if self.count == 0:
            return None
        return self.sum / self.count

class CountAggregate(Aggregate):
    """Count the number of rows"""

    def __init__(self, *args, **kwargs):
        super(CountAggregate, self).__init__(*args, **kwargs)
        self.count = 0

    def update(self, row):
        self.count += 1

    def value(self):
        return self.count

class MaxAggregate(Aggregate):
    """Calculate the maximum value for a column"""

    def __init__(self, *args, **kwargs):
        super(MaxAggregate, self).__init__(*args, **kwargs)
        self.max = None

    def update(self, row):
        val = self._to_number(row[self.column])
        if self.max is None:
            self.max = val
        else:
            self.max = max(self.max, val)

    def value(self):
        return self.max

class MinAggregate(Aggregate):
    """Calculate the minimum value for a column"""

    def __init__(self, *args, **kwargs):
        super(MinAggregate, self).__init__(*args, **kwargs)
        self.min = None

    def update(self, row):
        val = self._to_number(row[self.column])
        if self.min is None:
            self.min = val
        else:
            self.min = min(self.min, val)

    def value(self):
        return self.min

class SumAggregate(Aggregate):
    """Calculate the sum of values for a column"""

    def __init__(self, *args, **kwargs):
        super(SumAggregate, self).__init__(*args, **kwargs)
        self.sum = 0

    def update(self, row):
        self.sum += self._to_number(row[self.column])

    def value(self):
        return self.sum

aggregate_functions = dict(
    avg = AvgAggregate,
    count = CountAggregate,
    max = MaxAggregate,
    min = MinAggregate,
    sum = SumAggregate,
)
