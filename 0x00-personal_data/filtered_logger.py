#!/usr/bin/env python3
import re
import logging
from typing import List
"""Defines a function the retunr an obfuscated msg"""
regmat = r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)"


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns the log message obfuscated """
    return re.sub(regmat, lambda match: match.group(1) + "=" + redaction
                  if match.group(1) in fields else match.group(0), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    FIELDS = []

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.FIELDS=fields
        
        
    def format(self, record: logging.LogRecord) -> str:
        """ Formats a log record, obfuscating fields as needed """
        formatted_record = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.redaction,
                            formatted_record, self.separator)
