"""
An aggregate class is expected to except two values at
instantiation: 'column' and 'name', and the class
must have two methods 'update(self, row)' and 'value(self)'.
The 'update' method is called for each row, and the 'value'
must return the final result of the aggregation.
"""

class AvgAggregate(object):
    """Calculate the average value for a column"""

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

class CountAggregate(object):
    """Count the number of rows"""

    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self.count = 0

    def update(self, row):
        self.count += 1

    def value(self):
        return self.count

class MaxAggregate(object):
    """Calculate the maximum value for a column"""

    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self.max = None

    def update(self, row):
        if self.max is None:
            self.max = row[self.column]
        else:
            self.max = max(self.max, row[self.column])

    def value(self):
        return self.max

class MinAggregate(object):
    """Calculate the minimum value for a column"""

    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self.min = None

    def update(self, row):
        if self.min is None:
            self.min = row[self.column]
        else:
            self.min = min(self.min, row[self.column])

    def value(self):
        return self.min

class SumAggregate(object):
    """Calculate the sum of values for a column"""

    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self.sum = 0

    def update(self, row):
        self.sum += row[self.column]

    def value(self):
        return self.sum

aggregate_functions = dict(
    avg = AvgAggregate,
    count = CountAggregate,
    max = MaxAggregate,
    min = MinAggregate,
    sum = SumAggregate,
)
