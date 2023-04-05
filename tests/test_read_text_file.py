
#from redactor.py import get_files
import pytest
#import redactor as rd
from argparse import Namespace
import argparse
import sys
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
from redactor import get_files
from redactor import read_text_file

def test_read_text_file_success():
    file_to_read = "Email1.txt"
    expected_text = "Hello, world!"
    with open(file_to_read, "w", encoding="utf-8") as file:
        file.write(expected_text)
    text = read_text_file(file_to_read)
    assert text == expected_text


