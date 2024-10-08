#!/usr/bin/env python3
"""Defines a function the retunr an obfuscated msg"""

import re
import logging
from typing import List, Optional
import mysql.connector
from mysql.connector import connection
from mysql.connector import Error
import os
import bcrypt

regmat = r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)"

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns the log message obfuscated"""
    return re.sub(
        regmat,
        lambda match: (
            match.group(1) + "=" + redaction
            if match.group(1) in fields
            else match.group(0)
        ),
        message,
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record, obfuscating fields as needed"""
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


def get_logger() -> logging.Logger:
    """
    Returns a logger with a valid filename and a custom formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """Creates a connector to a database."""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    conn = connection.MySQLConnection(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return conn


def main():
    """Logs the information about user records in a table."""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(",")
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: "{}={}".format(x[0], x[1]),
                zip(columns, row),
            )
            msg = "{};".format("; ".join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


if __name__ == "__main__":
    main()
