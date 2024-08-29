#!/usr/bin/env python3
import re
from typing import List
"""Defines a function the retunr an obfuscated msg"""


def filter_datum(fields: List[str], redaction: str, msg: str, sep: str) -> str:
    return re.sub(r'(?<={sep})({flds})=(.*?)(?={sep}|$)'
                  .format(sep=re.escape(sep), flds='|'.join(fields)),
                  lambda m: f'{m.group(1)}={redaction}', msg)
