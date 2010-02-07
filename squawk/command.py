
from __future__ import with_statement

import sys
import optparse
from squawk.query import Query
from squawk.output import output_tabular, output_json, output_csv
from squawk.parsers.nginx import AccessLogParser
from squawk.sql import sql_parser

def get_table_names(tokens):
    if not isinstance(tokens.tables[0][0], basestring):
        return [get_table_names(tokens.tables[0][0])]
    return [tokens.tables[0][0]]

def combiner(files):
    for fname in files:
        with open(fname, 'rb') as fp:
            parser = AccessLogParser(fp)
            for row in parser:
                yield row

def main():
    sql = ' '.join(sys.argv[1:])
    files = get_table_names(sql_parser.parseString(sql))
    source = combiner(files)
    query = Query(sql)
    output_console(query.columns, query(source))

if __name__ == "__main__":
    main()
