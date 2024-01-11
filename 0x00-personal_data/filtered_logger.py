#!/usr/bin/env python3
"""returns the log message obfuscated"""
import re


def filter_datum(fields, redaction, message, separator):
    """Filtered logs"""
    return re.sub(
        fr"({'|'.join(map(re.escape, fields))})=[^ {re.escape(separator)}]*",
        f"\\1={redaction}", message
    )
