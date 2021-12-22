from functools import cached_property, lru_cache
from math import prod
from typing import List, Optional, Tuple


class SmokeFlowModel:

    """Class for modeeling smoke flows and associated risk."""

    def __init__(self, infile_path):
        """Read, manipulate and cache the source data."""
        self.basin_data: dict = {}
        with open(infile_path, 'r') as infile:
            self.height_data: List[str] = [
                [int(char) for char in row.strip()]
                for row in infile.readlines()
            ]

    @cached_property
    def low_points(self) -> List[tuple]:
        """Determine the low points based on height data."""
        return self._find_low_points()

    def calculate_risk(self) -> int:
        """Calculate the total risk for the model's height data."""
        total_risk: int = self._get_total_risk_level(self.low_points)
        return total_risk

    def calculate_basin_sizes(self) -> int:
        """Calculate the size of low point basins."""
        basin_values: List[int] = []
        for x, y in self.low_points:
            value: int = self.height_data[y][x]
            self.basin_data[(x, y)] = True
            basin: int = self._calculate_basin(value, y, x)
            basin_values.append(basin)
        top_3: List[int] = sorted(basin_values, reverse=True)[:3]
        return prod(top_3)

    def _find_low_points(self) -> List[tuple]:
        """Find the low points from height data."""
        low_points = []
        for row_index, row in enumerate(self.height_data):
            for column_index, point in enumerate(row):
                is_low: bool = self._is_low_point(point, row_index, column_index)
                if is_low:
                    low_points.append((column_index, row_index))
        return low_points

    def _get_total_risk_level(self, low_points: List[int]) -> int:
        """Determing the total risk level given a set of low points."""
        RISK_LEVEL_ADJUSTMENT = 1
        low_point_values: List[int] = [
            self.height_data[y][x]
            for x, y in low_points
        ]
        return sum([point + RISK_LEVEL_ADJUSTMENT for point in low_point_values])

    def _calculate_basin(self, starter: int, row_index: int, column_index: int) -> int:
        """Calculate the basin around the given point."""
        lookups: Tuple[int] = [
            (column_index, row_index - 1),
            (column_index + 1, row_index),
            (column_index, row_index + 1),
            (column_index - 1, row_index)
        ]
        adjacent_counts: int = []
        for lookup in lookups:
            in_basin, height = self._check_basin_adjacent(lookup, starter)
            if in_basin:
                count = self._calculate_basin(height, lookup[1], lookup[0])
                adjacent_counts.append(count)
        return sum(adjacent_counts) + 1

    def _check_basin_adjacent(self, lookup: tuple, comparator: int) -> Tuple[bool, Optional[int]]:
        """Return the adjacent point's value, if it is part of the basin."""
        column_index, row_index = lookup
        value: Optional[int] = self._lookup_height(row_index, column_index)
        is_part_of_basin: bool = (
            value
            and value > comparator
            and value != 9
        )
        not_already_counted: bool = lookup not in self.basin_data
        if is_part_of_basin and not_already_counted:
            self.basin_data[lookup] = True
            return True, value
        else:
            return False, None

    @lru_cache
    def _is_low_point(
            self,
            point: int,
            row_index: int,
            column_index: int
    ) -> bool:
        """Discern whether a given point is lower than its adjacent points."""
        adjacents: List[int] = [
            point
            for point in self._look_around(row_index, column_index)
            if point is not None
        ]
        is_low: bool = int(point) < min(adjacents)
        return is_low

    @lru_cache
    def _look_around(self, row_index: int, column_index: int) -> Tuple[int]:
        """Access the elements at the point adjacent to the given indices."""
        return (
            self._lookup_height(row_index - 1, column_index),
            self._lookup_height(row_index, column_index + 1),
            self._lookup_height(row_index + 1, column_index),
            self._lookup_height(row_index, column_index - 1),
        )
    def _lookup_height(self, row_index: int, column_index: int) -> Optional[int]:
        """Look up the height at the given location, if exists"""
        # Prevent looking up the other end of the list
        if row_index < 0 or column_index < 0:
            return None
        try:
            return self.height_data[row_index][column_index]
        except IndexError:
            return None

print(SmokeFlowModel('input_data.txt').calculate_risk())
print(SmokeFlowModel('input_data.txt').calculate_basin_sizes())