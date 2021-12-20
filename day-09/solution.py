from typing import List


class SmokeFlowModel:

    """Class for modeeling smoke flows and associated risk."""

    def __init__(self, infile_path):
        """Read, manipulate and cache the source data."""
        with open(infile_path, 'r') as infile:
            self.height_data: List[str] = [
                [int(char) for char in row.strip()]
                for row in infile.readlines()
            ]

    def calculate_risk(self) -> int:
        """Calculate the total risk for the model's height data."""
        low_points: List[int] = self._find_low_points()
        total_risk: int = self._get_total_risk_level(low_points)
        return total_risk

    def _find_low_points(self) -> List[int]:
        """Find the low points from height data."""
        low_points = []
        for row_index, row in enumerate(self.height_data):
            for column_index, point in enumerate(row):
                is_low: bool = self._is_low_point(point, row_index, column_index)
                if is_low:
                    low_points.append(point)
        return low_points

    def _is_low_point(
            self,
            point: int,
            row_index: int,
            column_index: int
    ) -> bool:
        """Discern whether a given point is lower than its adjacent points."""
        adjacents = []
        if column_index - 1 >= 0:
            left: str = self.height_data[row_index][column_index - 1]
            adjacents.append(left)
        try:
            right: str = self.height_data[row_index][column_index + 1]
            adjacents.append(right)
        except IndexError:
            pass
        try:
            top: str = self.height_data[row_index + 1][column_index]
            adjacents.append(top)
        except IndexError:
            pass
        if row_index - 1 >= 0:
            bottom: str = self.height_data[row_index - 1][column_index]
            adjacents.append(bottom)
        is_low: bool = int(point) < min(adjacents)
        return is_low

    def _get_total_risk_level(self, low_points: List[int]) -> int:
        """Determing the total risk level given a set of low points."""
        RISK_LEVEL_ADJUSTMENT = 1
        return sum([point + RISK_LEVEL_ADJUSTMENT for point in low_points])


print(SmokeFlowModel('input_data.txt').calculate_risk())