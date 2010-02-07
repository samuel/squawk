
from squawk.parsers.csvparser import CSVParser
from squawk.parsers.nginx import AccessLogParser

parsers = dict(
    access_log = AccessLogParser,
    apache = AccessLogParser,
    nginx = AccessLogParser,
    csv = CSVParser,
)
