"""
Lab 7: Fuzz Testing for Input Validation Bugs
Test Suite: test_processor.py

Uses Hypothesis to perform property-based and robustness fuzz testing
across parse_application, processing_average, and payable_fee.
"""

import math
import pytest
from hypothesis import given, strategies as st

from processor import (
    parse_application,
    processing_average,
    payable_fee
)


# =====================================================================
# 1. FUZZ TESTING FOR parse_application()
# =====================================================================

@given(st.one_of(st.text(), st.none()))
def test_parse_application_no_crash(s):
    """
    Robustness Fuzz Test:
    Feeds arbitrary text and None. The function must never crash with unhandled
    exceptions like AttributeError, TypeError, or IndexError.
    It must either return a valid (str, int) tuple or raise ValueError.
    """
    try:
        result = parse_application(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert len(result[0]) > 0
        assert isinstance(result[1], int)
        assert result[1] >= 0
    except ValueError:
        pass


@given(
    st.text(
        alphabet=st.characters(
            blacklist_categories=("Cc", "Cs"),
            blacklist_characters=":"
        ),
        min_size=1
    ).filter(lambda x: bool(x.strip())),
    st.integers(min_value=0, max_value=100000)
)
def test_parse_application_valid(visa, entries):
    """
    Property-Based Fuzz Test:
    For any non-empty visa string without colons and any non-negative integer,
    the parsed output must match the stripped title-cased visa and the entry integer.
    """
    result = parse_application(f"{visa}:{entries}")
    assert result[0] == visa.strip().title()
    assert result[1] == entries


# =====================================================================
# 2. FUZZ TESTING FOR processing_average()
# =====================================================================

@given(st.one_of(st.text(), st.none()))
def test_processing_average_no_crash(s):
    """
    Robustness Fuzz Test:
    Feeds arbitrary text and None. The function must never crash with unhandled
    exceptions like AttributeError, ZeroDivisionError, or TypeError.
    It must either return a valid non-negative integer or raise ValueError.
    """
    try:
        result = processing_average(s)
        assert isinstance(result, int)
        assert result >= 0
    except ValueError:
        pass


@given(
    st.lists(
        st.integers(min_value=0, max_value=100000),
        min_size=1,
        max_size=100
    )
)
def test_processing_average_valid(values):
    """
    Property-Based Fuzz Test:
    For any non-empty list of non-negative integers formatted as CSV,
    the result must equal the mathematical integer floor average.
    """
    csv_str = ",".join(map(str, values))
    result = processing_average(csv_str)
    assert result == sum(values) // len(values)


# =====================================================================
# 3. FUZZ TESTING FOR payable_fee()
# =====================================================================

@given(st.one_of(st.text(), st.none()))
def test_payable_fee_no_crash(s):
    """
    Robustness Fuzz Test:
    Feeds arbitrary text and None. The function must never crash with unhandled
    exceptions like AttributeError, TypeError, or IndexError.
    It must either return a non-negative finite float/int or raise ValueError.
    """
    try:
        result = payable_fee(s)
        assert isinstance(result, (int, float))
        assert math.isfinite(result)
        assert result >= 0.0
    except ValueError:
        pass


@given(
    st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False)
)
def test_payable_fee_valid(fee, discount):
    """
    Property-Based Fuzz Test:
    For any valid non-negative finite fee and discount,
    payable_fee must compute max(fee * 1.18 - discount, 0).
    """
    result = payable_fee(f"{fee}|{discount}")
    expected = max(fee * 1.18 - discount, 0.0)
    assert result == pytest.approx(expected, rel=1e-5)


# =====================================================================
# 4. EDGE CASE & INPUT VALIDATION TESTS
# =====================================================================

def test_parse_application_none_input():
    with pytest.raises(ValueError, match="Input must be a valid string"):
        parse_application(None)


def test_parse_application_empty_input():
    with pytest.raises(ValueError, match="Invalid application format"):
        parse_application("")


def test_parse_application_missing_colon():
    with pytest.raises(ValueError, match="Invalid application format"):
        parse_application("tourist 2")


def test_parse_application_multiple_colons():
    with pytest.raises(ValueError, match="Invalid application format"):
        parse_application("tourist:2:express")


def test_parse_application_empty_visa_name():
    with pytest.raises(ValueError, match="Visa type cannot be empty"):
        parse_application("   :2")


def test_parse_application_non_int_entries():
    with pytest.raises(ValueError, match="Entries must be a valid integer"):
        parse_application("tourist:two")


def test_parse_application_negative_entries():
    with pytest.raises(ValueError, match="Entries count cannot be negative"):
        parse_application("tourist:-3")


def test_processing_average_none_input():
    with pytest.raises(ValueError, match="Input must be a valid string"):
        processing_average(None)


def test_processing_average_empty_string():
    with pytest.raises(ValueError, match="Invalid processing days format"):
        processing_average("")


def test_processing_average_trailing_comma():
    with pytest.raises(ValueError, match="Invalid processing days format"):
        processing_average("5,10,")


def test_processing_average_non_int():
    with pytest.raises(ValueError, match="Processing days must be integers"):
        processing_average("5,abc,10")


def test_processing_average_negative_days():
    with pytest.raises(ValueError, match="Processing days cannot be negative"):
        processing_average("5,-10,15")


def test_payable_fee_none_input():
    with pytest.raises(ValueError, match="Input must be a valid string"):
        payable_fee(None)


def test_payable_fee_empty_string():
    with pytest.raises(ValueError, match="Invalid fee format"):
        payable_fee("")


def test_payable_fee_missing_pipe():
    with pytest.raises(ValueError, match="Invalid fee format"):
        payable_fee("6000")


def test_payable_fee_multiple_pipes():
    with pytest.raises(ValueError, match="Invalid fee format"):
        payable_fee("6000|500|100")


def test_payable_fee_non_numeric():
    with pytest.raises(ValueError, match="Fee and discount must be valid numbers"):
        payable_fee("abc|500")


def test_payable_fee_negative_fee():
    with pytest.raises(ValueError, match="Fee and discount cannot be negative"):
        payable_fee("-6000|500")


def test_payable_fee_negative_discount():
    with pytest.raises(ValueError, match="Fee and discount cannot be negative"):
        payable_fee("6000|-500")


def test_payable_fee_nan():
    with pytest.raises(ValueError, match="Fee and discount must be finite numbers"):
        payable_fee("nan|500")


def test_payable_fee_inf():
    with pytest.raises(ValueError, match="Fee and discount must be finite numbers"):
        payable_fee("inf|500")


def test_payable_fee_discount_exceeds_total():
    # Fee = 100 -> total = 118 - 500 = -382 -> max(-382, 0) = 0.0
    assert payable_fee("100|500") == 0.0
