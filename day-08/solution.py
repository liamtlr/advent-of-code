from typing import List


def extract_raw_data(path: str) -> List[str]:
    """Extract the raw source data.."""
    with open(path, 'r') as infile:
        raw_data: list = infile.readlines()
    return raw_data


def handle_row(row: str) -> List[str]:
    """Extract digits from a row of data"""
    _, digits_string = row.split(" | ")
    digits: List[str] = [digit.strip() for digit in digits_string.split(" ")]
    return digits


def count_unique_digits(digits: List[str]) -> int:
    """Count digits with identifiable sector counts."""
    UNIQUE_DIGIT_SEGMENT_COUNTS = (2, 4, 3, 7)
    unique_segment_digits: int = sum(
        1
        for digit in digits
        if len(digit) in UNIQUE_DIGIT_SEGMENT_COUNTS
    )
    return unique_segment_digits


def get_unique_segment_counts(raw_data: list) -> int:
    """Retrun count of readings with uniquely IDable segments counts."""
    unique_segment_counts = 0
    for row in raw_data:
        digits: List[str] = handle_row(row)
        unique_segment_digits: int = count_unique_digits(digits)
        unique_segment_counts += unique_segment_digits
    return unique_segment_counts


data = extract_raw_data('input_data.txt')
print(get_unique_segment_counts(data))