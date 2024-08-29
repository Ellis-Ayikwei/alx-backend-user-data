#!/usr/bin/env python3
import re
"""Defines a function the retunr an obfuscated message"""


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    return re.sub(r'(?<={sep})({flds})=(.*?)(?={sep}|$)'
                  .format(sep=re.escape(separator), flds='|'.join(fields)),
                  lambda m: f'{m.group(1)}={redaction}', message)
