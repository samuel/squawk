
from squawk.parsers.access_log import AccessLogParser
from squawk.parsers.csvparser import CSVParser

parsers = dict(
    access_log = AccessLogParser,
    apache = AccessLogParser,
    apache2 = AccessLogParser,
    nginx = AccessLogParser,
    csv = CSVParser,
)
