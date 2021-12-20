from typing import List


class LanternFish:

    """Class encapsulation logic for a lanternfish"""

    REGULAR_GESTATION_PERIOD = 6

    def __init__(self, initial_days_till_birth: int):
        """Set the initial day till birth."""
        self.days_till_birth = initial_days_till_birth

    @property
    def ready_to_give_birth(self) -> bool:
        """Determiens whether the fish is ready to give birth"""
        return self.days_till_birth == 0

    def handle_day(self):
        """Handle the day in the life of a wee lanternfish."""
        if self.ready_to_give_birth:
            self.days_till_birth = self.REGULAR_GESTATION_PERIOD
        else:
            self.days_till_birth -= 1


class SeaBed:

    """Logic encapsulating a bed of the sea."""

    NEWBORN_GESTATION_PERIOD = 8

    def __init__(self, infile_path: str):
        """Read the vent data."""
        self.bed = {}
        with open(infile_path, 'r') as infile:
            raw_data: list = infile.readlines()
            data: list = raw_data[0].split(',')
            self.fishies: list[LanternFish] = [
                LanternFish(int(datum))
                for datum in data
            ]

    def fishes_after_n_days(self, days: int) -> int:
        """Get the number of fishes after the given number of days."""
        for _ in range(days):
            self.day_passes()
        return len(self.fishies)

    def day_passes(self) -> None:
        """Handle the passing of a day on the fish population"""
        newborn_fishies: List[LanternFish] = []
        for fish in self.fishies:
            if fish.ready_to_give_birth:
                newborn: LanternFish = LanternFish(self.NEWBORN_GESTATION_PERIOD)
                newborn_fishies.append(newborn)
            fish.handle_day()
        self.fishies.extend(newborn_fishies)



print(SeaBed('input_data.txt').fishes_after_n_days(256))