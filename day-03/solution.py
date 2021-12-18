from functools import cached_property
from statistics import multimode, mode
from typing import Callable


class DiagnosticReport:

    """Class for handling submarine diagnostic data."""

    def __init__(self, infile_path: str):
        """Read infile and set against instance"""
        with open(infile_path, 'r') as infile:
            self.readings: list = infile.readlines()

    @cached_property
    def gamma_rate(self) -> str:
        """Calculate the gamma rate."""
        transposed_data: list = self._transpose_data(self.readings)
        most_commons: list = [mode(column) for column in transposed_data]
        gamma_rate: str = "".join(most_commons)
        return gamma_rate

    @cached_property
    def epsilon_rate(self) -> str:
        """Calculate the epsilon rate from the gamma rate."""
        least_commons: list = [
            '1' if bit == '0' else '0'
            for bit in self.gamma_rate
        ]
        epsilon_rate: str = "".join(least_commons)
        return epsilon_rate

    @cached_property
    def power_consumption(self) -> int:
        """Calculate the power consumption."""
        gamma_rate_int: int = self._binary_string_to_int(self.gamma_rate)
        epsilon_rate_int: int = self._binary_string_to_int(self.epsilon_rate)
        power_consumption: int =  gamma_rate_int * epsilon_rate_int
        return power_consumption

    @cached_property
    def o2_generator_rating(self) -> str:
        """Calculate the oxygen generator rating."""
        remaining: list = list(self.readings)
        rating: str = self._extract_rating(remaining, 0, self._o2_reducer)
        return rating

    @cached_property
    def co2_scrubber_rating(self) -> str:
        """Calculate the carbon dioxide scrubber rating."""
        remaining: list = list(self.readings)
        rating: str = self._extract_rating(remaining, 0, self._co2_reducer)
        return rating

    @cached_property
    def life_support_rating(self) -> int:
        """Calculate the life_support rating."""
        o2_gen_int: int = self._binary_string_to_int(self.o2_generator_rating)
        co2_scrub_int: int = self._binary_string_to_int(self.co2_scrubber_rating)
        life_support: int =  o2_gen_int * co2_scrub_int
        return life_support

    def _transpose_data(self, readings: list) -> list:
        """Transpose a 2D list."""
        transposed_data: list = list(zip(*readings))
        return transposed_data

    def _binary_string_to_int(self, binary_string: str) -> int:
        """Convert a binary string to its corresponging integer."""
        binary_as_int: int = int(binary_string, 2)
        return binary_as_int

    def _get_column(self, column: int, table: list) -> list:
        """Extract a column from a 2D list."""
        return [row[column] for row in table]

    def _extract_rating(
            self,
            readings: list,
            index: int,
            reducer: Callable
    ) -> str:
        """Extract a single rating from a set using a given reducer."""
        column: list = self._get_column(index, readings)
        target: str = reducer(column)
        selected: list = [
            reading for reading in readings
            if reading[index] == target
        ]
        if len(selected) == 1:
            return selected[0]
        else:
            return self._extract_rating(selected, index + 1, reducer)

    def _o2_reducer(self, column: list) -> str:
        """"Get the target value for discerning o2 data from readings."""
        most_common_list: list = multimode(column)
        most_common: str = max(most_common_list)
        return most_common

    def _co2_reducer(self, column: list) -> str:
        """Get the target value for discerning co2 data from readings."""
        most_common_list: list = multimode(column)
        if len(most_common_list) == 2:
            target_val: str = '0'
        else:
            target_val: str = '0' if most_common_list[0] == '1' else '1'
        return target_val


report = DiagnosticReport('input_data.txt')
print(report.power_consumption)
print(report.life_support_rating)
