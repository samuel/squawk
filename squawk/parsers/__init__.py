
from squawk.parsers.access_log import AccessLogParser
from squawk.parsers.csvparser import CSVParser
from squawk.parsers.pickleparser import PickleParser

parsers = dict(
    access_log = AccessLogParser,
    apache = AccessLogParser,
    apache2 = AccessLogParser,
    pickle = PickleParser,
    nginx = AccessLogParser,
    csv = CSVParser,
)
