#!/usr/bin/env python3
"""filter_logger module"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """Used to filter sensitive info
    """
    pattern = r"(" + "|".join(map(re.escape, fields))\
        + r")=([^" + re.escape(separator) + r"]+)"
    return re.sub(pattern, r"\1=" + redaction, message)
