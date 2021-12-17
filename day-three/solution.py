from functools import cached_property
from statistics import mode


class DiagnosticReport:

    """Class for handling submarine diagnostic data."""

    def __init__(self, infile_path: str):
        """Read infile and set against instance"""
        with open(infile_path, 'r') as infile:
            self.readings: list = infile.readlines()

    @cached_property
    def gamma_rate(self) -> str:
        """Calculate the gamma rate."""
        self._transposed_data = self._transpose_data(self.readings)
        most_commons: list = [mode(column) for column in self._transposed_data]
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
        gamma_rate_int: int  = self._binary_string_to_int(self.gamma_rate)
        epsilon_rate_int: int  = self._binary_string_to_int(self.epsilon_rate)
        power_consumption: int =  gamma_rate_int * epsilon_rate_int
        return power_consumption

    def _transpose_data(self, readings: list) -> list:
        """Transpose a 2D list."""
        transposed_data: list = list(zip(*readings))
        return transposed_data

    def _binary_string_to_int(self, binary_string: str) -> int:
        """Convert a binary string to its corresponging integer."""
        binary_as_int: int = int(binary_string, 2)
        return binary_as_int


print(DiagnosticReport('input_data.txt').power_consumption)
