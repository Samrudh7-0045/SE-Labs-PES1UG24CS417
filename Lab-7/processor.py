"""
Lab 7: Fuzz Testing for Input Validation Bugs
Module: processor.py (Corrected Application)

This module provides functions for parsing visa applications,
calculating average processing days, and computing payable visa fees.
All functions include rigorous input validation to guard against
malformed inputs, unexpected data types, negative values, and edge cases.
"""

import math


def parse_application(text):
    """
    Parses a visa application string formatted as 'visa_type:entries'.

    Args:
        text (str): Input string containing visa type and number of entries.

    Returns:
        tuple[str, int]: Cleaned title-cased visa type and integer entry count.

    Raises:
        ValueError: If input is not a string, format is malformed, visa type is empty,
                    or entries count is invalid / negative.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a valid string")

    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("Invalid application format: expected 'visa_type:entries'")

    visa = parts[0].strip()
    entries_str = parts[1].strip()

    if not visa:
        raise ValueError("Visa type cannot be empty")

    try:
        entries = int(entries_str)
    except ValueError:
        raise ValueError("Entries must be a valid integer")

    if entries < 0:
        raise ValueError("Entries count cannot be negative")

    return visa.title(), entries


def processing_average(days_csv):
    """
    Calculates the integer average of processing days from a comma-separated string.

    Args:
        days_csv (str): Comma-separated list of processing days (e.g. '5,10,21').

    Returns:
        int: Floor average of the processing days.

    Raises:
        ValueError: If input is not a string, contains empty values, has non-integers,
                    or contains negative numbers.
    """
    if not isinstance(days_csv, str):
        raise ValueError("Input must be a valid string")

    parts = days_csv.split(',')
    if not parts or any(not item.strip() for item in parts):
        raise ValueError("Invalid processing days format: cannot contain empty values")

    try:
        values = [int(item.strip()) for item in parts]
    except ValueError:
        raise ValueError("Processing days must be integers")

    if any(day < 0 for day in values):
        raise ValueError("Processing days cannot be negative")

    if len(values) == 0:
        raise ValueError("No processing days provided")

    return sum(values) // len(values)


def payable_fee(text):
    """
    Calculates the net payable fee after applying 18% tax and subtracting any discount.
    Formula: max(fee * 1.18 - discount, 0)

    Args:
        text (str): Pipe-separated string formatted as 'fee|discount' (e.g. '6000|500').

    Returns:
        float: Payable fee, capped at minimum 0.

    Raises:
        ValueError: If input is not a string, format is malformed, values are non-numeric,
                    infinite/NaN, or negative.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a valid string")

    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("Invalid fee format: expected 'fee|discount'")

    try:
        fee = float(parts[0].strip())
        discount = float(parts[1].strip())
    except ValueError:
        raise ValueError("Fee and discount must be valid numbers")

    if not math.isfinite(fee) or not math.isfinite(discount):
        raise ValueError("Fee and discount must be finite numbers")

    if fee < 0 or discount < 0:
        raise ValueError("Fee and discount cannot be negative")

    total = fee * 1.18 - discount
    return max(total, 0.0)


def main():
    """Interactive command-line interface for the application."""
    print("=" * 45)
    print("    Visa Application Processing System")
    print("=" * 45)

    print("\n==== 1. parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    try:
        result = parse_application(user_input)
        print("Visa Type and Entries:", result)
    except ValueError as err:
        print(f"Error: {err}")

    print("\n==== 2. processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    try:
        result = processing_average(user_input)
        print("Average Processing Days:", result)
    except ValueError as err:
        print(f"Error: {err}")

    print("\n==== 3. payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    try:
        result = payable_fee(user_input)
        print("Payable Fee:", result)
    except ValueError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
