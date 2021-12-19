from typing import Generator


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
        is_horizontal: bool = start_x == end_x
        is_vertical: bool = start_y == end_y
        if is_horizontal:
            self._traverse_line(start_y, end_y, start_x, horizontal=True)
        elif is_vertical:
            self._traverse_line(start_x, end_x, start_y, horizontal=False)

    def _traverse_line(
            self,
            start: int,
            end: int,
            constant: int,
            horizontal: bool = True
    ) -> None:
        """Traverse from the start to end, updating the master co_ords dict."""
        start, end = sorted((start, end))
        for point in range(start, end + 1):
            co_ord_list: list = [constant , point]
            if horizontal:
                co_ord_list = reversed(co_ord_list)
            co_ord_key: tuple = tuple(co_ord_list)
            self._update_bed(co_ord_key)

    def _update_bed(self, co_ords: tuple) -> None:
        """Update the master bed data with the point."""
        if co_ords not in self.bed:
            self.bed.update({co_ords: 1})
        else:
            self.bed[co_ords] += 1


print(SeaBed('input_data.txt').calculate_dangerous_areas())
