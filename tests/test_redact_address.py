import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tempfile
from redactor import get_files
import pytest
import argparse
import os
import glob
import spacy
import re
from redactor import redact_address

import spacy
import re
#from my_module import redact_address
import re
import spacy
import pytest

import re
import spacy
import pytest

@pytest.fixture
def nlp():
    return spacy.load("en_core_web_sm")

@pytest.fixture
def text_with_address():
    return "My address is 123 Main St, New York, NY"

@pytest.fixture
def text_without_address():
    return "Hello, world!"
def test_redact_address_without_address(nlp, text_without_address):
    redacted_text, address_list, count = redact_address(text_without_address)

    assert count == 0
    assert address_list == []
    assert redacted_text == "Hello, world!"


