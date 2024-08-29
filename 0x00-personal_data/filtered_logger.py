import re
from typing import List
"""Defines a function returns the log message obfuscated"""

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Returns the log message with specified fields obfuscated"""
    pattern = r'(?<={separator})({fields})=(.*?)(?={separator}|$)'.format(
        separator=re.escape(separator),
        fields='|'.join(fields)
    )
    return re.sub(pattern, lambda match: f'{match.group(1)}={redaction}', message)




