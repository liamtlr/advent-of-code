from typing import List, Tuple


class SeaBed:

    """Logic encapsulating a bed of the sea."""

    FLASH_THRESHOLD_ENERGY = 9
    REGULAR_GESTATION_PERIOD = 7

    def __init__(self, infile_path: str):
        """Read the octopus data."""
        self.flashes: int = 0
        self.just_flashed: set = set()
        with open(infile_path, 'r') as infile:
            raw_data: List[str] = infile.read().splitlines()
            self.data: List[list] = [
                [int(char) for char in row]
                for row in raw_data
            ]

    def flashes_after_n_steps(self, steps: int) -> int:
        """Get the number of flashes after the given number of steps."""
        for _ in range(steps):
            self.handle_step()
        return self.flashes

    def handle_step(self) -> None:
        """Handle a step on the octopus population."""
        self.just_flashed = set()
        for row_index, row in enumerate(self.data):
            for column_index, _ in enumerate(row):
                self._increment_at(row_index, column_index)

    def _increment_at(self, row_index: int, column_index: int) -> None:
        """Increment the valus at the given location"""
        octopus: int = self.data[row_index][column_index]
        if (row_index, column_index) in self.just_flashed:
            return
        octopus += 1
        if octopus > 9:
            octopus = 0
            self.data[row_index][column_index] = octopus
            self._handle_flash(row_index, column_index)
            return
        self.data[row_index][column_index] = octopus

    def _handle_flash(self, row_index: int, column_index: int) -> None:
        """Handle a flash event on the surrounding octopuses."""
        self.flashes += 1
        self.just_flashed.add((row_index, column_index))
        lookups: List[Tuple] = [
            # Row above
            (row_index - 1, column_index - 1),
            (row_index - 1, column_index),
            (row_index - 1, column_index + 1),
            # Same row
            (row_index, column_index - 1),
            (row_index, column_index + 1),
            # Row below
            (row_index + 1, column_index - 1),
            (row_index + 1, column_index),
            (row_index + 1, column_index + 1),
        ]
        for row, column in lookups:
            if row < 0 or column < 0:
                continue
            try:
                self._increment_at(row, column)
            except IndexError:
                continue


print(SeaBed('input_data.txt').flashes_after_n_steps(100))