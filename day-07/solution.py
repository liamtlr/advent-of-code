from functools import partial, reduce
from statistics import mean
from typing import List


def extract_data(path: str) -> List[int]:
    """Extract the source data and convert to list of ints."""
    with open(path, 'r') as infile:
        raw_data: list = infile.readlines()
    raw_data: list = raw_data[0].split(',')
    data: list = [int(datum) for datum in raw_data]
    return data


def calculate_fuel_required(acc: int, curr: int, mean: int) -> int:
    """Calculate the fuel needed to reach the mean position."""
    diff: int = curr - mean
    if diff < 0:
        diff = diff * -1
    adjusted_diff = sum(range(diff + 1))
    acc += adjusted_diff
    return acc


def calculate_minimum_fuel(positions: List[int]) -> int:
    """Calculate minimum fuel for all subs to reach the same point."""
    mean_position: int = int(mean(positions))
    reducer = partial(calculate_fuel_required, mean=mean_position)
    reduced: int = reduce(reducer, positions, 0)
    return reduced


data = extract_data('input_data.txt')
print(calculate_minimum_fuel(data))