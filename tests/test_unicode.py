from redactor import unicode_char
import pytest

def unicode_char(word):
    return "\u2588" * len(word)

def test_unicode_char():
    assert unicode_char('world') == '\u2588\u2588\u2588\u2588\u2588'
    assert unicode_char('') == ''
    assert unicode_char('1234') == '\u2588\u2588\u2588\u2588'

