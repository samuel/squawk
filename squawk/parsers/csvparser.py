
import csv

class CSVParser(object):
    def __init__(self, file):
        if isinstance(file, basestring):
            self.fp = open(file, "rb")
        else:
            self.fp = file

    def __iter__(self):
        for row in csv.DictReader(self.fp):
            yield dict((k.lower(), v) for k, v in row.items())
