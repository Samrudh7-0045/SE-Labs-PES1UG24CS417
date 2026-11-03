import pytest
from visa_application import visa_fee, documents_complete, application_status

# ==========================================
# Branch Coverage Tests (Branch Coverage >= 90%, achieving 100%)
# Designed to cover every decision branch and condition pathway
# ==========================================

# ------------------------------------------
# Tests for visa_fee() branches
# ------------------------------------------

def test_visa_fee_unknown_type():
    # Branch: visa_type not in INCLUDED_ENTRIES (True)
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("work", 1, "normal", "A")

def test_visa_fee_invalid_entries():
    # Branch: entries < 0 (True)
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "A")

def test_visa_fee_nationality_a_non_student():
    # Compound Condition: nationality_group == "A" (True) and visa_type != "student" (True)
    # tourist base included = 1 + 1 = 2. entries = 2 -> extra = 0 -> returns 0
    assert visa_fee("tourist", 2, "normal", "A") == 0

def test_visa_fee_nationality_a_student():
    # Compound Condition: nationality_group == "A" (True) and visa_type != "student" (False)
    # student base included = 2. nationality A does NOT add 1 for student.
    # entries = 3 -> extra = 1. speed normal -> rate = 40. fee = 1 * 40 = 40
    assert visa_fee("student", 3, "normal", "A") == 40

def test_visa_fee_nationality_not_a():
    # Compound Condition: nationality_group == "A" (False)
    # tourist base included = 1. entries = 1 -> extra = 0 -> returns 0
    assert visa_fee("tourist", 1, "normal", "B") == 0

def test_visa_fee_extra_negative():
    # Branch: extra <= 0 (True with extra < 0)
    # business base included = 3. entries = 1 -> extra = -2 -> returns 0
    assert visa_fee("business", 1, "normal", "B") == 0

def test_visa_fee_normal_speed_low_extra():
    # Branch: speed == "express" (False) -> rate = 40
    # Branch: extra > 5 (False, extra = 2)
    # tourist included = 1. entries = 3 -> extra = 2. fee = 2 * 40 = 80
    assert visa_fee("tourist", 3, "normal", "B") == 80

def test_visa_fee_express_speed_low_extra():
    # Branch: speed == "express" (True) -> rate = 100
    # Branch: extra > 5 (False, extra = 2)
    # tourist included = 1. entries = 3 -> extra = 2. fee = 2 * 100 = 200
    assert visa_fee("tourist", 3, "express", "B") == 200

def test_visa_fee_normal_speed_high_extra():
    # Branch: speed == "express" (False) -> rate = 40
    # Branch: extra > 5 (True, extra = 6) -> rate = 40 + 20 = 60
    # Branch: inner speed == "express" (False) -> rate remains 60
    # tourist included = 1. entries = 7 -> extra = 6. fee = 6 * 60 = 360
    assert visa_fee("tourist", 7, "normal", "B") == 360

def test_visa_fee_express_speed_high_extra():
    # Branch: speed == "express" (True) -> rate = 100
    # Branch: extra > 5 (True, extra = 6) -> rate = 100 + 20 = 120
    # Branch: inner speed == "express" (True) -> rate = 120 + 10 = 130
    # tourist included = 1. entries = 7 -> extra = 6. fee = 6 * 130 = 780
    assert visa_fee("tourist", 7, "express", "B") == 780


# ------------------------------------------
# Tests for documents_complete() branches
# ------------------------------------------

def test_documents_complete_renewal_true_forms_met():
    # Branch: is_renewal (True), forms_filed >= 1 (True)
    assert documents_complete(1, 0, True) is True

def test_documents_complete_renewal_true_forms_unmet():
    # Branch: is_renewal (True), forms_filed >= 1 (False)
    assert documents_complete(0, 0, True) is False

def test_documents_complete_renewal_false_photos_unmet():
    # Branch: is_renewal (False), photos < 2 (True)
    assert documents_complete(5, 1, False) is False

def test_documents_complete_renewal_false_photos_met_forms_met():
    # Branch: is_renewal (False), photos < 2 (False), forms_filed >= 3 (True)
    assert documents_complete(3, 2, False) is True

def test_documents_complete_renewal_false_photos_met_forms_unmet():
    # Branch: is_renewal (False), photos < 2 (False), forms_filed >= 3 (False)
    assert documents_complete(2, 2, False) is False


# ------------------------------------------
# Tests for application_status() branches
# ------------------------------------------

def test_application_status_express_offpeak_open():
    # is_express (True: cutoff=10), is_peak_season (False: cutoff=10)
    # days_left >= cutoff (True: 10 >= 10) -> "open"
    assert application_status(10, True, False) == "open"

def test_application_status_express_offpeak_closing():
    # cutoff = 10. days_left < 10 and >= -5 (True: 2) -> "closing"
    assert application_status(2, True, False) == "closing"

def test_application_status_express_offpeak_closed():
    # cutoff = 10. days_left < -5 (True: -10) -> "closed"
    assert application_status(-10, True, False) == "closed"

def test_application_status_express_peak_open():
    # is_express (True: cutoff=10), is_peak_season (True: cutoff=25)
    # days_left >= cutoff (True: 30 >= 25) -> "open"
    assert application_status(30, True, True) == "open"

def test_application_status_express_peak_closing():
    # cutoff = 25. days_left < 25 and >= 10 (True: 20) -> "closing"
    assert application_status(20, True, True) == "closing"

def test_application_status_express_peak_closed():
    # cutoff = 25. days_left < 10 (True: 5) -> "closed"
    assert application_status(5, True, True) == "closed"

def test_application_status_standard_offpeak_open():
    # is_express (False: cutoff=30), is_peak_season (False: cutoff=30)
    # days_left >= 30 (True: 30) -> "open"
    assert application_status(30, False, False) == "open"

def test_application_status_standard_offpeak_closing():
    # cutoff = 30. days_left < 30 and >= 15 (True: 20) -> "closing"
    assert application_status(20, False, False) == "closing"

def test_application_status_standard_offpeak_closed():
    # cutoff = 30. days_left < 15 (True: 5) -> "closed"
    assert application_status(5, False, False) == "closed"

def test_application_status_standard_peak_open():
    # is_express (False: cutoff=30), is_peak_season (True: cutoff=45)
    # days_left >= 45 (True: 50) -> "open"
    assert application_status(50, False, True) == "open"

def test_application_status_standard_peak_closing():
    # cutoff = 45. days_left < 45 and >= 30 (True: 35) -> "closing"
    assert application_status(35, False, True) == "closing"

def test_application_status_standard_peak_closed():
    # cutoff = 45. days_left < 30 (True: 25) -> "closed"
    assert application_status(25, False, True) == "closed"

