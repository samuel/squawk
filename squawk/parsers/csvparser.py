
import csv

class CSVParser(object):
    def __init__(self, file):
        if isinstance(file, basestring):
            fp = open(file, "rb")
        else:
            fp = file
        self.reader = csv.DictReader(fp)
        self.columns = [x.lower() for x in self.reader.fieldnames]

    def __iter__(self):
        for row in self.reader:
            yield dict((k.lower(), v) for k, v in row.items())
