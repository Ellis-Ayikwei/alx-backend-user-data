#!/usr/bin/env python3
import re
from typing import List
"""Defines a function the retunr an obfuscated msg"""
regmat = r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)"

def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    return re.sub(regmat,lambda match: match.group(1) + "=" + redaction
                  if match.group(1) in fields else match.group(0), message)
    