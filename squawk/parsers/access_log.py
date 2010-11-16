import re

log_re = re.compile(
    r'^(?P<remote_addr>("[^"]+"|[^\s]+))'
    r" -"
    r" (?P<remote_user>[^\s]+)"
    r" \[(?P<time>[^\]]+)\]"
    r'\s+"(?P<request>[^"]*)"'
    r" (?P<status>[^\s]+)"
    r" (?P<bytes>[^\s]+)"
    r'\s+"(?P<referrer>[^"]*)"'
    r'\s+"(?P<user_agent>[^"]*)"'
    r".*$")

class AccessLogParser(object):
    def __init__(self, file):
        if isinstance(file, basestring):
            self.fp = open(file, "rb")
        else:
            self.fp = file

        self.columns = [x[0] for x in sorted(log_re.groupindex.items(), key=lambda g:g[1])]
        self.columns.remove("request")
        self.columns += ["method", "path", "httpver"]

    def __iter__(self):
        for line in self.fp:
            m = log_re.match(line.strip())
            d = m.groupdict()
            d['remote_addr'] = d['remote_addr'].replace('"', '')
            try:
                request = d.pop('request')
                d['method'], d['path'], d['httpver'] = request.split(' ')
            except ValueError:
                d['method'], d['path'], d['httpver'] = None, None, None
            try:
                d['bytes'] = int(d['bytes'])
            except ValueError:
                d['bytes'] = 0
            d['status'] = int(d['status'])
            yield d
