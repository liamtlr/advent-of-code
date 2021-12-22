from typing import Dict, List


class SignalDecoder:

    """Class for discerning sector mappings from raw data."""

    ONE_SEGMENT_COUNT = 2
    FOUR_SEGMENT_COUNT = 4
    SEVEN_SEGMENT_COUNT = 3
    EIGHT_SEGMENT_COUNT = 7

    UNIQUE_SEGMENT_MAP: Dict[int, int] = {
        ONE_SEGMENT_COUNT: 1,
        FOUR_SEGMENT_COUNT: 4,
        SEVEN_SEGMENT_COUNT: 7,
        EIGHT_SEGMENT_COUNT: 8,
    }

    def __init__(self, path: str):
        """Extract the raw dara from the given path."""
        with open(path, 'r') as infile:
            self.raw_data: list = infile.readlines()

    def parse_readings(self) -> List[int]:
        """Get a list of readings from the source data"""
        readings = []
        for row in self.raw_data:
            input_data, output_reading = self.handle_row(row)
            data_by_sector_count: Dict[int, list] = self.get_input_data_by_sector_count(input_data)
            mappings = self.get_mapping(data_by_sector_count)
            reverse_mappings: Dict[str, int] =  self.reverse_mapping(mappings)
            reading: int = self.calculate_reading_number(output_reading, reverse_mappings)
            readings.append(reading)
        return sum(readings)

    def get_unique_segment_counts(self) -> int:
        """Retrun count of readings with uniquely IDable segments counts."""
        unique_segment_counts = 0
        for row in self.raw_data:
            _, digits  = self.handle_row(row)
            unique_segment_digits: int = self.count_unique_digits(digits)
            unique_segment_counts += unique_segment_digits
        return unique_segment_counts

    def count_unique_digits(self, digits: List[str]) -> int:
        """Count digits with identifiable sector counts."""
        unique_segment_digits: int = sum(
            1
            for digit in digits
            if len(digit) in self.UNIQUE_SEGMENT_MAP.keys()
        )
        return unique_segment_digits

    def get_input_data_by_sector_count(
            self,
            input_data: List[str]
    ) -> Dict[int, set]:
        """Group the readings by a count of its segments."""
        output_dict: dict = {}
        for reading in input_data:
            segments = len(reading)
            reading_set = {char for char in reading}
            if segments in output_dict:
                output_dict[segments].append(reading_set)
            else:
                output_dict[segments] = [reading_set]
        return output_dict

    def handle_row(self, row: str) -> List[str]:
        """Extract digits from a row of data"""
        zero_to_ten, reading = row.split(" | ")
        digits: List[str] = [digit.strip() for digit in zero_to_ten.split(" ")]
        reading_segments: List[str] = [
            "".join(sorted(digit.strip()))
            for digit in reading.split(" ")
        ]
        return digits, reading_segments

    def get_mapping(self, digit_data: Dict[int, list]) -> dict:
        """Get a mapping of digits to their underlying segments."""
        unique_segment_mappings: Dict[int, set] = self.get_unique_segment_mappings(digit_data)
        six_segment_mappings: Dict[int, set] = self.discern_six_segment_digits(
            digit_data,
            unique_segment_mappings
        )
        collated = {**six_segment_mappings, **unique_segment_mappings}
        important_sector = self.discern_important_sector(collated)
        five_segment_mappings: Dict[int, set] = self.discern_five_segment_digits(
            digit_data,
            collated,
            important_sector
        )
        return {
            **five_segment_mappings,
            **collated,
        }

    def reverse_mapping(self, mapping: Dict[int, str]) -> Dict[str, int]:
        """Reverse the mapping to be look up-able by the string of sectors."""
        return {"".join(sorted(list(v))): k for k, v in mapping.items()}

    def calculate_reading_number(
            self,
            output_reading: List[str],
            mapping: Dict[str, int]
    ) -> int:
        """Calculate the actual reading from the illuminated segments"""
        reading_numbers: List[str] = [
            str(mapping[segment])
            for segment in output_reading
        ]
        reading_proper: str = "".join(reading_numbers)
        return int(reading_proper)

    def discern_important_sector(self, collated: dict):
        """Discern the descending sector in the top right hand corner."""
        discerning_sector_set: set = collated[8] - collated[6]
        return list(discerning_sector_set)[0]

    def get_unique_segment_mappings(self, digits: Dict[int, list]) -> dict:
        """Discern the mappings for digits with unique segment numbers."""
        mapping: Dict[int, set] = {
            v: digits[k][0]
            for k, v in self.UNIQUE_SEGMENT_MAP.items()

        }
        return mapping

    def discern_six_segment_digits(
            self,
            digits: Dict[int, list],
            mappings: Dict[int, set]
    ) -> Dict[int, set]:
        """Discern the six segment digits based on the unique ones"""
        six_seg_digits: List[set] = digits[6]
        nine: set = self.get_digit_by_subset(six_seg_digits, mappings[4])
        six_seg_digits.remove(nine)
        if mappings[1].issubset(six_seg_digits[0]):
            return {
                0: six_seg_digits[0],
                6: six_seg_digits[1],
                9: nine,
            }
        else:
            return {
                0: six_seg_digits[1],
                6: six_seg_digits[0],
                9: nine,
            }

    def discern_five_segment_digits(
            self,
            digits: Dict[int, list],
            mappings: Dict[int, set],
            important_sector: str
    ) -> Dict[int, set]:
        """Discern the five segment digits based on the unique ones"""
        five_seg_digits: List[set] = digits[5]
        three: set = self.get_digit_by_subset(five_seg_digits, mappings[1])
        five_seg_digits.remove(three)

        if important_sector in five_seg_digits[0]:
            return {
                2: five_seg_digits[0],
                5: five_seg_digits[1],
                3: three,
            }
        else:
            return {
                2: five_seg_digits[1],
                5: five_seg_digits[0],
                3: three,
            }

    def get_digit_by_subset(self, potentials: List[set], subset: set) -> set:
        """Find the digit which ithe the superset of a given subset"""
        return next(digit for digit in potentials if subset.issubset(digit))


print(SignalDecoder('input_data.txt').parse_readings())
print(SignalDecoder('input_data.txt').get_unique_segment_counts())