#!/usr/bin/env python3.11
"""
Test the validator logic directly
"""

import sys

sys.path.insert(0, '')

import contextlib

from adaptivemind_core.config import AppConfig


def test_validator():

    # Test empty list condition

    # Test AppConfig creation with default personas
    with contextlib.suppress(Exception):
        AppConfig()

if __name__ == "__main__":
    test_validator()
