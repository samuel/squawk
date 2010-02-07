
from squawk.parsers.nginx import AccessLogParser

parsers = dict(
    access_log = AccessLogParser,
    apache = AccessLogParser,
    nginx = AccessLogParser,
)
