
from __future__ import with_statement

import sys
from optparse import OptionParser
from squawk.query import Query
from squawk.output import output_formats
from squawk.parsers import parsers
from squawk.sql import sql_parser

def get_table_names(tokens):
    if not isinstance(tokens.tables[0][0], basestring):
        return [get_table_names(tokens.tables[0][0])]
    return [tokens.tables[0][0]]

def combiner(files, parser_class):
    for fname in files:
        with (sys.stdin if fname == '-' else open(fname, 'rb')) as fp:
            parser = parser_class(fp)
            for row in parser:
                yield row

def build_opt_parser():
    parser = OptionParser()
    parser.add_option("-p", "--parser", dest="parser",
                      help="name of parser for input")
    parser.add_option("-f", "--format", dest="format", default="tabular",
                      help="write output in FORMAT format", metavar="FORMAT")
    # parser.add_option("-q", "--quiet",
    #                   action="store_false", dest="verbose", default=True,
    #                   help="don't print status messages to stdout")
    return parser

def main():
    parser = build_opt_parser()
    (options, args) = parser.parse_args()

    sql = ' '.join(args)
    files = get_table_names(sql_parser.parseString(sql))

    parser_name = options.parser
    if parser_name:
        parser = parsers[parser_name]
    else:
        fn = files[0]
        if fn.rsplit('/', 1)[-1] == 'access.log':
            parser = parsers['access_log']
        else:
            sys.stderr.write("Can't figure out parser for input")
            sys.exit(1)

    source = combiner(files, parser)
    query = Query(sql)

    output = output_formats[options.format]

    output(query.columns, query(source))

if __name__ == "__main__":
    main()
