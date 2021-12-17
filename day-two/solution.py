from typing import Tuple


with open('input_data.txt', 'r') as infile:
    movements: list = infile.readlines()


def navigate(
        movements: list,
        start_depth: int=0,
        start_horizontal: int=0
) -> Tuple[int, int]:
    """Apply movements to the depth and horizontal values."""
    NET_VALUES = {
        'depth': start_depth,
        'horizontal': start_horizontal
    }
    DIRECTION_ADJUSTMENT_MAP: dict = {
        'forward': 1,
        'up': -1,
        'down': 1,
    }
    DIRECTION_MAP: dict = {
        'forward': 'horizontal',
        'up': 'depth',
        'down': 'depth',
    }

    for movement in movements:
        direction, value_str = movement.split(' ')
        direction_dimension: str = DIRECTION_MAP[direction]
        target_value: int = NET_VALUES[direction_dimension]
        adjusted_value: int = int(value_str) * DIRECTION_ADJUSTMENT_MAP[direction]
        target_value += adjusted_value
        NET_VALUES[direction_dimension] = target_value

    return NET_VALUES['depth'], NET_VALUES['horizontal']


depth, horizontal = navigate(movements=movements)
print(depth * horizontal)
