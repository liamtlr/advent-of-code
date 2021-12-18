from typing import Tuple


class Navigator:

    """Class for navigating a submarine based on a set of movements"""

    DIRECTION_ADJUSTMENT_MAP: dict = {
        'forward': 1,
        'up': -1,
        'down': 1,
    }
    DIRECTION_MAP: dict = {
        'forward': 'horizontal',
        'up': 'aim',
        'down': 'aim',
    }

    def __init__(
            self,
            infile_location: str,
            start_depth: int=0,
            start_horizontal: int=0,
            start_aim: int=0,
    ):
        """Set the the instance variables."""
        with open(infile_location, 'r') as infile:
            self.movements: list = infile.readlines()
        self.net_values: dict = {
            'depth': start_depth,
            'horizontal': start_horizontal,
            'aim': start_aim,
        }

    def get_final_postion(self) -> Tuple[int, int]:
        """Apply movements to the depth and horizontal values."""
        for movement in self.movements:
            direction, value_str = movement.split(' ')
            value = int(value_str)
            self._handle_horizontal(direction, value)
            if direction == 'forward':
                self._handle_depth(value)
        return self.net_values['depth'], self.net_values['horizontal']

    def _handle_horizontal(self, direction: str, value: int):
        """Apply the horizontal / aim adjustment."""
        direction_dimension: str = self.DIRECTION_MAP[direction]
        target_value: int = self.net_values[direction_dimension]
        adjusted_value: int = value * self.DIRECTION_ADJUSTMENT_MAP[direction]
        target_value += adjusted_value
        self.net_values[direction_dimension] = target_value

    def _handle_depth(self, value: int):
        """Apply depth value."""
        depth_increase = self.net_values['aim'] * value
        self.net_values['depth'] += depth_increase


depth, horizontal = Navigator('input_data.txt').get_final_postion()
print(depth * horizontal)
