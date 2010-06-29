try:
    import cPickle as pickle
except ImportError:
    import pickle

class PickleParser(object):
    def __init__(self, file):
        if isinstance(file, basestring):
            self.fp = open(file, "rb")
        else:
            self.fp = file

        self.data = pickle.load(self.fp)
        if not isinstance(self.data, (list, tuple)):
            raise Exception("Unsupported format for pickled data. Should be a list of dictionaries e.g. [{'col': 'value'}]")

        self.columns = self.data[0].keys()

    def __iter__(self):
        for row in self.data:
            yield row
