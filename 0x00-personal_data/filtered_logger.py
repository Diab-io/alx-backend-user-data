#!/usr/bin/env python3
"""filter_logger module"""
import re
import logging
import mysql.connector
from typing import List
import os


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}

PII_FIELDS = ('ssn', 'password', 'phone', 'name', 'email')


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """Filters a log line.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Function used in creating a logger"""
    user_logger = logging.getLogger('user_data')
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_logger.setLevel(logging.INFO)
    user_logger.propagate = False
    user_logger.addHandler(handler)
    return user_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ function that creates a connection to a database
    """
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')

    conn = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
    )

    return conn


def main() -> None:
    """
    logs the information of a user got
    from a table in the database
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Method used for formatting a record
        """
        msg_format = super().format(record)
        red_txt = filter_datum(self.fields, self.REDACTION,
                               msg_format, self.SEPARATOR)
        return red_txt


if __name__ == '__main__':
    main()
