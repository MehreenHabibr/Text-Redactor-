import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tempfile
from redactor import get_files
import pytest
import argparse
import os
import glob
import sys
from redactor import redact_gender
import re


def test_redact_gender():
    input_text = "The tree is tall and green."
    expected_redacted_text = "The tree is tall and green."
    expected_gender_list = []
    expected_count = 0

    actual_redacted_text, actual_gender_list, actual_count = redact_gender(input_text)

    assert actual_redacted_text == expected_redacted_text
    assert actual_gender_list == expected_gender_list
    assert actual_count == expected_count
