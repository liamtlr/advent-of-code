"""
Solution for day 5 of advent of code.

A note on the implementation. We construct a range object representing the
traversal across the x / y axes, and their intermediary points. Separately,
the range(s) are iterated through to construct the actual co ordinates, and
published these to the central data structure.

Whilst initially readability has been prioritised, these series iterations
could be merged into a single iteration for performance reasons. Range object
constructions for static points could be removed entirely.
"""

from typing import Generator, Iterable


class SeaBed:

    """Logic encapsulating a bed of the sea."""

    POINTS_DELIMITER = ' -> '
    CO_ORDS_DELIMITER = ','

    def __init__(self, infile_path: str):
        """Read the vent data."""
        self.bed = {}
        with open(infile_path, 'r') as infile:
            self.raw_data: list = infile.readlines()

    def calculate_dangerous_areas(self) -> int:
        """Determine the dangerous areas from the raw data."""
        for datum in self.raw_data:
            co_ords: tuple = self._extract_data(datum)
            self._plot_line(co_ords)
        return sum(1 for value in self.bed.values() if value > 1)

    def _extract_data(self, row: str) -> tuple:
        """Extract the vector data to co ordinate tuples."""
        co_ord_strings: list = row.strip().split(self.POINTS_DELIMITER)
        co_ords: tuple = tuple(
            self._unpack_co_ords(co_ords)
            for co_ords in co_ord_strings
        )
        return co_ords

    def _unpack_co_ords(self, co_ord_string: str) -> tuple:
        """Convert a comma separated string of co ords to a tuple of ints."""
        int_gen: Generator = (
            int(co_ord)
            for co_ord in co_ord_string.split(self.CO_ORDS_DELIMITER)
        )
        return tuple(int_gen)

    def _plot_line(self, co_ords: tuple) -> None:
        """Plot a line."""
        start, end = co_ords
        start_x, start_y = start
        end_x, end_y = end
        x_traversal: range = self._build_traversal_range(start_x, end_x)
        y_traversal: range = self._build_traversal_range(start_y, end_y)
        self._traverse_line(x_traversal, y_traversal)

    def _build_traversal_range(self, start: int, end: int) -> range:
        """Build the points along with axis."""
        if start > end:
            return range(start, end - 1, -1)
        return range(start, end+1)

    def _traverse_line(
            self,
            x_range: tuple,
            y_range: tuple,
    ) -> None:
        """Traverse from the start to end, updating the master co_ords dict."""
        co_ords: tuple = tuple()
        if len(x_range) == len(y_range):
            y_range_iterable: Iterable = iter(y_range)
            for x_point in x_range:
                y_point: int = next(y_range_iterable)
                co_ords = tuple([x_point, y_point])
                self._update_bed(co_ords)
        elif len(x_range) == 1:
            for y_point in y_range:
                co_ords = tuple([x_range[0], y_point])
                self._update_bed(co_ords)
        else:
            for x_point in x_range:
                co_ords = tuple([x_point, y_range[0]])
                self._update_bed(co_ords)

    def _update_bed(self, co_ords: tuple) -> None:
        """Update the master bed data with the point."""
        if co_ords not in self.bed:
            self.bed.update({co_ords: 1})
        else:
            self.bed[co_ords] += 1


print(SeaBed('input_data.txt').calculate_dangerous_areas())
