#!/usr/bin/env python3
"""returns the log message obfuscated"""
from typing import List
import re
import logging



class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Class constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats message"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filtered logs"""
    return re.sub(
        fr"({'|'.join(map(re.escape, fields))})=[^ {re.escape(separator)}]*",
        f"\\1={redaction}", message)
