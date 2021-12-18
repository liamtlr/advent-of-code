with open('input_data.txt', 'r') as infile:
    readings: list = infile.readlines()


def _get_increasing_reading_count(readings: list, step: int=1):
    """
    Return a count of the number of increased readings.

    Accepts a step to compare non-sequential entries.
    """
    increased_readings: int = sum(
        1
        for next_index, reading in enumerate(readings[:-step])
        if int(reading) < int(readings[next_index + step])
    )
    return increased_readings

def get_increased_reading_count(readings: list) -> int:
    """Return a count of the number of increased readings based on the previous."""
    return _get_increasing_reading_count(readings)


print(get_increased_reading_count(readings))


def get_sliding_increased_reading_count(readings: list) -> int:
    """Return a count of the number of increased readings based on the sliding total."""
    # Compare the 1st and 4th elements, 2nd and 5th, etc...
    return _get_increasing_reading_count(readings, 4)

print(get_sliding_increased_reading_count(readings))
