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


def test_get_files_no_input():
    with pytest.raises(SystemExit) as e:
        args = argparse.Namespace(input=[])
        get_files(args)
    assert e.value.code == 1


def test_get_files_invalid_path():
    with pytest.raises(SystemExit) as e:
        args = argparse.Namespace(input=['invalid/path'])
        get_files(args)
    assert e.value.code == 1


def test_get_files_no_txt_files():
    with pytest.raises(SystemExit) as e:
        args = argparse.Namespace(input=['tests/test_files_no_txt'])
        get_files(args)
    assert e.value.code == 1



