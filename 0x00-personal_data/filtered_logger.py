#!/usr/bin/env python3
"""returns the log message obfuscated"""
import re
import logging
from typing import List
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] user_data %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
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


def get_logger() -> logging.Logger:
    """Create logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = os.getenv("PERSONAL_DATA_DB_NAME", "")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=dbname
    )


def main() -> None:
    """Main function to retrieve and filter data from the database"""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    for row in rows:
        log_message_parts = []
        for key, value in row.items():
            log_message_parts.append(f"{key}={value}")

        log_message = "; ".join(log_message_parts)
        logger.info(log_message)

    cursor.close()
    db.close()


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


if __name__ == "__main__":
    main()
