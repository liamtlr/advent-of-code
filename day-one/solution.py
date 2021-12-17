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