from typing import Dict, List


class SignalDecoder:

    """Class for discerning sector mappings from raw data."""

    def __init__(self, path: str):
        """Extract the raw dara from the given path."""
        with open(path, 'r') as infile:
            self.raw_data: list = infile.readlines()

    def parse_readings(self) -> List[int]:
        """Get a list of readings from the source data"""
        readings = []
        for row in self.raw_data:
            base_data, reading = row.split(" | ")
            digits: List[str] = [digit.strip() for digit in base_data.split(" ")]
            reading_segments: List[str] = ["".join(sorted(digit.strip())) for digit in reading.split(" ")]
            mappings = self.get_mapping(digits)
            reverse_mappings = {
                "".join(sorted(list(v))): k
                for k, v in mappings.items()
            }
            print(mappings)
            reading_numbers = [
                str(reverse_mappings[segment])
                for segment in reading_segments
            ]
            reading_proper = "".join(reading_numbers)
            print(reading_proper)
            readings.append(int(reading_proper))
        return sum(readings)


    def get_mapping(self, digits: List[str]) -> dict:
        """Get a mapping of digits to their underlying segments."""
        unique_segment_mappings = self.get_unique_segment_mappings(digits)
        six_segment_mappings = self.discern_six_segment_digits(digits, unique_segment_mappings)
        collated = {**six_segment_mappings, **unique_segment_mappings}
        important_sector = self.discern_important_sector(collated)
        five_segment_mappings = self.discern_five_segment_digits(digits, collated, important_sector)
        return {
            **five_segment_mappings,
            **collated,
        }

    def discern_important_sector(self, collated: dict):
        """Discern the descending sector in the top right hand corner."""
        um = collated[8] - collated[6]
        return list(um)[0]

    def get_unique_segment_mappings(self, digits: List[str]) -> dict:
        """Discern the mappings for digits with unique segment numbers."""
        ONE_SEGMENT_COUNT = 2
        FOUR_SEGMENT_COUNT = 4
        SEVEN_SEGMENT_COUNT = 3
        EIGHT_SEGMENT_COUNT = 7
        unique_segment_map: Dict[int: int] = {
            ONE_SEGMENT_COUNT: 1,
            FOUR_SEGMENT_COUNT: 4,
            SEVEN_SEGMENT_COUNT: 7,
            EIGHT_SEGMENT_COUNT: 8,
        }
        mapping = {}
        for k, v in unique_segment_map.items():
            reading = next(digit for digit in digits if len(digit) == k)
            # formatted_reading = "".join(sorted(reading))
            reading_set = set(reading)
            mapping[v] = reading_set
        return mapping

    def discern_six_segment_digits(self, digits: List[str], mappings: Dict[int, set]) -> Dict[int, set]:
        """Discern the six segment digits based on the unique ones"""
        um = [
            {char for char in digit}
            for digit in digits
            if len(digit) == 6
        ]
        nine = next(digit for digit in um if mappings[4].issubset(digit))
        print(um)

        um.remove(nine)
        print(um)
        print(mappings[1].issubset(um[0]), mappings[1].issubset(um[1]))

        if mappings[1].issubset(um[0]):
            return {
                0: um[0],
                6: um[1],
                9: nine,
            }
        else:
            return {
                0: um[1],
                6: um[0],
                9: nine,
            }

    def discern_five_segment_digits(
            self,
            digits: List[str],
            mappings: Dict[int, set],
            important_sector: str
    ) -> Dict[int, set]:
        """Discern the five segment digits based on the unique ones"""
        um = [
            {char for char in digit}
            for digit in digits
            if len(digit) == 5
        ]
        three = next(digit for digit in um if mappings[1].issubset(digit))
        um.remove(three)

        if important_sector in um[0]:
            return {
                2: um[0],
                5: um[1],
                3: three,
            }
        else:
            return {
                2: um[1],
                5: um[0],
                3: three,
            }

print(SignalDecoder('input_data.txt').parse_readings())





# def extract_raw_data(path: str) -> List[str]:
#     """Extract the raw source data.."""
#     with open(path, 'r') as infile:
#         raw_data: list = infile.readlines()
#     return raw_data


# def handle_row(row: str) -> List[str]:
#     """Extract digits from a row of data"""
#     _, digits_string = row.split(" | ")
#     digits: List[str] = [digit.strip() for digit in digits_string.split(" ")]
#     return digits


# def count_unique_digits(digits: List[str]) -> int:
#     """Count digits with identifiable sector counts."""
#     UNIQUE_DIGIT_SEGMENT_COUNTS = (2, 4, 3, 7)
#     unique_segment_digits: int = sum(
#         1
#         for digit in digits
#         if len(digit) in UNIQUE_DIGIT_SEGMENT_COUNTS
#     )
#     return unique_segment_digits


# def get_unique_segment_counts(raw_data: list) -> int:
#     """Retrun count of readings with uniquely IDable segments counts."""
#     unique_segment_counts = 0
#     for row in raw_data:
#         digits: List[str] = handle_row(row)
#         unique_segment_digits: int = count_unique_digits(digits)
#         unique_segment_counts += unique_segment_digits
#     return unique_segment_counts


# data = extract_raw_data('input_data.txt')
# print(get_unique_segment_counts(data))