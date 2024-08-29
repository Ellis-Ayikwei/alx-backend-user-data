import re


def filter_datum(fields, redaction, message, separator):
    return re.sub(r'(?<={sep})({flds})=(.*?)(?={sep}|$)'
                  .format(sep=re.escape(separator), flds='|'.join(fields)),
                  lambda m: f'{m.group(1)}={redaction}', message)
