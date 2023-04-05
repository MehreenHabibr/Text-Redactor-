import sys
import os
from io import StringIO
from argparse import Namespace
from unittest import mock
from tempfile import TemporaryDirectory
import pytest

from redactor import output

def test_output_stdout():
    args = Namespace(output="stdout")
    complete_data = "some redacted data"
    files = "test.txt"
    expected_output = f"\n============ Redacted data output from {files} file ==============\n{complete_data}\n"

    # Redirect stdout to a StringIO object to capture the output
    with mock.patch("sys.stdout", new=StringIO()) as fake_out:
        output(args, complete_data, files)
        assert fake_out.getvalue() == expected_output

def test_output_stderr():
    args = Namespace(output="stderr")
    complete_data = "some redacted data"
    files = "test.txt"

    # Redirect stderr to a StringIO object to capture the output
    with mock.patch("sys.stderr", new=StringIO()) as fake_err:
        output(args, complete_data, files)
        assert fake_err.getvalue() == "No Error Found\n"

def test_output_file():
    args = Namespace(output="output_dir")
    complete_data = "some redacted data"
    files = "test.txt"

    with TemporaryDirectory() as temp_dir:
        output_dir = os.path.join(temp_dir, "output_dir")
        os.makedirs(output_dir)
        args.output = output_dir

        output(args, complete_data, files)

        output_file = os.path.join(output_dir, f"{os.path.basename(files)}.redacted")
        assert os.path.exists(output_file)
        with open(output_file, "r", encoding="utf-8") as f:
            assert f.read() == complete_data

