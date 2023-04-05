import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tempfile
from redactor import get_files
import pytest
import argparse
import glob
from redactor import redact_dates
import spacy


import re


def test_redact_dates():
    # Test case 1: No dates in text
    text = "This is a test sentence."
    expected_redacted_text = "This is a test sentence."
    expected_dates = []
    expected_count = 0
    redacted_text, dates, count = redact_dates(text)
    assert redacted_text == expected_redacted_text
    assert dates == expected_dates
    assert count == expected_count

    # Test case 2: One date in text
    text = "This sentence contains a date: 12/31/2022."
    expected_redacted_text = "This sentence contains a date: ██████████."
    expected_dates = ['12/31/2022']
    expected_count = 1
    redacted_text, dates, count = redact_dates(text)
    assert redacted_text == expected_redacted_text
    assert dates == expected_dates
    assert count == expected_count

    # Test case 3: Multiple dates in text
    text = "There are multiple dates in this sentence: 06/30/2022, 07/01/2022, and 07/02/2022."
    expected_redacted_text = "There are multiple dates in this sentence: ██████████, ██████████, and ██████████."
    expected_dates = ['06/30/2022', '07/01/2022', '07/02/2022']
    expected_count = 3
    redacted_text, dates, count = redact_dates(text)
    assert redacted_text == expected_redacted_text
    assert dates == expected_dates
    assert count == expected_count

