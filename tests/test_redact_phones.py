import pytest
from redactor import redact_phones

def test_redact_phones():
    text = "Call me at (555) 555-1234 or 555-123-4567."
    redacted_text, phones, count = redact_phones(text)
    expected1 = "Call me at ██████████████ or ████████████."
    expected2 = "Call me at ████████████ or ██████████████."
    assert redacted_text == expected1 or redacted_text == expected2


