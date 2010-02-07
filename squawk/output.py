
import csv
import sys
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        json = None

def output_tabular(columns, rows, fp=None):
    fp = fp or sys.stdout
    fp.write("\t| ".join(columns))
    fp.write("\n")
    fp.write("-"*40+"\n")
    for row in rows:
        fp.write("\t| ".join(row[k] if isinstance(row[k], basestring) else str(row[k]) for k in columns))
        fp.write("\n")

def output_json(columns, rows, fp=None):
    fp = fp or sys.stdout
    fp.write('[')
    first = True
    for row in rows:
        if not first:
            fp.write(',\n')
        else:
            first = False
        fp.write(json.dumps(row))
    fp.write(']')

def output_csv(columns, rows, fp=None, **kwargs):
    fp = fp or sys.stdout
    writer = csv.writer(fp, **kwargs)
    writer.writerow(columns)
    for row in rows:
        writer.writerow([row[k] for k in columns])

output_formats = dict(
    tabular = output_tabular,
    json = output_json,
    csv = output_csv,
)
