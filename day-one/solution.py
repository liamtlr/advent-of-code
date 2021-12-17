with open('input_data.txt', 'r') as infile:
    readings: list = infile.readlines()

def get_increased_reading_count(readings: list) -> int:
    """Return a count of the number of increased readings based on the previous."""
    increased_readings: int = sum(
        1
        for next_index, reading in enumerate(readings[:-1], start=1)
        if int(reading) < int(readings[next_index])
    )
    return increased_readings


print(get_increased_reading_count(readings))


def get_sliding_increased_reading_count(readings: list) -> int:
    """Return a count of the number of increased readings based on the sliding total."""
    increased_readings: int = sum(
        1
        for next_index, reading in enumerate(readings[:-4])
        # Compare the current reading (the one to leave the grouping) with the
        # reading 3 to the left (the one to join the grouping).
        if int(reading) < int(readings[next_index + 4])
    )
    return increased_readings

print(get_sliding_increased_reading_count(readings))
