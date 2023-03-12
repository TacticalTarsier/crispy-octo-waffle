"""import modules"""
from typing import List
import re


def valid_emails(strings: List[str]) -> List[str]:
    """Take list of potential emails and returns only valid ones"""

    valid_email_regex = re.compile("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$")

    return [email for email in strings if valid_email_regex.match(email)]
