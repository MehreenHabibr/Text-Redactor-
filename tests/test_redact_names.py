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
from redactor import redact_names


def test_redact_names():
    text = "The quick brown fox jumped over the lazy dog."
    expected_redacted_text = text
    expected_names = {}
    expected_count = 0
    redacted_text, names, count = redact_names(text)
    assert redacted_text == expected_redacted_text
    assert names == expected_names
    assert count == expected_count

