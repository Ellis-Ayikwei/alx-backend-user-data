#!/usr/bin/env python3
import re
from typing import List
"""Defines a function the retunr an obfuscated msg"""


def filter_datum(fields: List[str], redaction: str, msg: str, sep: str) -> str:
    """ returns the log msg obfuscated """
    return re.sub(r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)",
                  lambda match: match.group(1) + "=" + redaction
                  if match.group(1) in fields else match.group(0), msg)
