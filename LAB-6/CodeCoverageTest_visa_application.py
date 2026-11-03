import pytest
from visa_application import visa_fee, documents_complete, application_status

# ==========================================
# Code Coverage Tests (Line Coverage >= 90%)
# Designed to execute all statements in visa_application.py
# ==========================================

# Tests for visa_fee()
def test_visa_fee_unknown_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 1, "normal", "B")

def test_visa_fee_invalid_entries():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")

def test_visa_fee_included_nationality_a_no_extra():
    # tourist has 1 included, nationality A adds 1 -> included = 2.
    # entries = 2 -> extra = 0 -> returns 0
    assert visa_fee("tourist", 2, "normal", "A") == 0

def test_visa_fee_express_high_extra():
    # tourist has 1 included, nationality B -> included = 1.
    # entries = 8 -> extra = 7 (> 5)
    # speed express -> base rate = 100, extra > 5 -> +20, express -> +10 = 130
    # 7 * 130 = 910
    assert visa_fee("tourist", 8, "express", "B") == 910

def test_visa_fee_normal_speed_extra():
    # business has 3 included, nationality B -> included = 3.
    # entries = 4 -> extra = 1 (<= 5)
    # speed normal -> rate = 40
    # 1 * 40 = 40
    assert visa_fee("business", 4, "normal", "B") == 40


# Tests for documents_complete()
def test_documents_complete_renewal_valid():
    assert documents_complete(1, 0, True) is True

def test_documents_complete_low_photos():
    assert documents_complete(3, 1, False) is False

def test_documents_complete_standard_valid():
    assert documents_complete(3, 2, False) is True


# Tests for application_status()
def test_application_status_express_peak_open():
    # is_express=True (cutoff=10), is_peak_season=True (cutoff=25)
    # days_left=25 >= cutoff -> "open"
    assert application_status(25, True, True) == "open"

def test_application_status_standard_offpeak_closing():
    # is_express=False (cutoff=30), is_peak_season=False (cutoff=30)
    # days_left=20 (cutoff-15 <= days_left < cutoff) -> "closing"
    assert application_status(20, False, False) == "closing"

def test_application_status_standard_offpeak_closed():
    # cutoff=30, cutoff-15 = 15. days_left=10 < 15 -> "closed"
    assert application_status(10, False, False) == "closed"

