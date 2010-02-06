
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

class CountAggregate(object):
    def __init__(self, column, name=None):
        self.column = column.lower()
        self.name = (name or column).lower()
        self.count = 0

    def update(self, row):
        self.count += 1

    def value(self):
        return self.count

class MaxAggregate(object):
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
