from functools import lru_cache, reduce
from typing import Dict, List, Optional, Set, Tuple


class TransparentOrigami:

    """Logic encapsulating folding transparent paper."""

    DIMENSION_VALUE_MAP: Dict[str, int] = {
        'x': 0,
        'y': 1,
    }
    DIMENSION_SIZE_MAP: Dict[str, int] = {
        'x': 'width',
        'y': 'height',
    }

    def __init__(self, infile_path: str):
        """Read the dot/fold data."""
        with open(infile_path, 'r') as infile:
            raw_data: List[str] = infile.read().splitlines()
            delimiter: int = raw_data.index('')
            dot_data, fold_data = raw_data[:delimiter], raw_data[delimiter + 1:]
            self.dots: Set[tuple] = set()
            self.folds: List[tuple] = []
            all_x: Set[int] = set()
            all_y: Set[int] = set()
            for row in dot_data:
                x, y = row.split(',')
                x, y = int(x), int(y)
                self.dots.add((x, y))
                all_x.add(x)
                all_y.add(y)
            self.width = max(all_x)
            self.height = max(all_y)
            for fold in fold_data:
                data: str = fold.split('fold along ')[1]
                dimension, value = data.split('=')
                self.folds.append((dimension, int(value)))

    def fold(self) -> None:
        """Perform all folds."""
        for fold in self.folds:
            self.perform_fold(*fold)

    def print_paper(self) -> None:
        """Construct the paper based on current dot data and print."""
        paper: List[list] =  [
            ['.' for _ in range(self.width + 1)]
            for _ in range(self.height + 1)
        ]
        for column_index, row_index in self.dots:
            paper[row_index][column_index] = '#'
        for row in paper:
            print(row)
        return paper

    def perform_fold(self, dimension: str, line_value: int) -> None:
        """Simulate the effect of a fold."""
        size: int = getattr(self, self.DIMENSION_SIZE_MAP[dimension])
        from_fold_to_end: int = size - line_value
        overhang: int = max([from_fold_to_end - line_value, 0])
        new_new_dots: Set[tuple] = {
            self._reform_dot(dot, (dimension, line_value), overhang)
            for dot in self.dots
            if self._reform_dot(dot, (dimension, line_value), overhang) is not None
        }
        self.dots = new_new_dots

        new_size: int = (size - from_fold_to_end + overhang) - 1
        setattr(self, self.DIMENSION_SIZE_MAP[dimension], new_size)
        return len(self.dots)

    @lru_cache
    def _reform_dot(self, dot: tuple, fold: tuple, overhang: int) -> Tuple[int]:
        """Determine the row's now position given the fold."""
        dimension, line_value = fold
        lookup: int = self.DIMENSION_VALUE_MAP[dimension]
        value: int = dot[lookup]
        new_value: int = value
        if value == line_value:
            return None
        pre_fold: bool = value < line_value
        if pre_fold:
            if overhang:
                new_value = value + overhang
        else:
            difference: int = value - line_value
            new_value = line_value - difference
        if dimension == 'x':
            return new_value, dot[1]
        else:
            return dot[0], new_value


origami = TransparentOrigami('input_data.txt')
print(origami.perform_fold(*origami.folds[0]))

origami_2 = TransparentOrigami('input_data.txt')
origami_2.fold()
origami_2.print_paper()
