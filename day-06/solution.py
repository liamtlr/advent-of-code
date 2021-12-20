from typing import Dict, List


class SeaBed:

    """Logic encapsulating a bed of the sea."""

    NEWBORN_GESTATION_PERIOD = 9
    REGULAR_GESTATION_PERIOD = 7

    def __init__(self, infile_path: str):
        """Read the vent data."""
        self.day: int = 0
        self.total_fishes: int = 0
        self.birthing_plan: Dict[int, int] = {}
        with open(infile_path, 'r') as infile:
            raw_data: list = infile.readlines()
            data: list = raw_data[0].split(',')
            for fish in data:
                self._handle_newborns(1, int(fish))

    def fishes_after_n_days(self, days: int) -> int:
        """Get the number of fishes after the given number of days."""
        for day in range(days):
            self.day_passes(day)
            try:
                del self.birthing_plan[day]
            except KeyError:
                pass
        return self.total_fishes

    def day_passes(self, day: int) -> None:
        """Handle the passing of a day on the fish population."""
        try:
            fish_to_give_birth: int = self.birthing_plan[day]
            self._handle_newborns(fish_to_give_birth)
            self._handle_parents(fish_to_give_birth)
        except KeyError:
            self.day += 1
            return
        self.day += 1

    def _handle_newborns(
            self,
            newborn_count: int,
            days_till_birth: int = NEWBORN_GESTATION_PERIOD
    ) -> None:
        """Insert the newborn into the birthing plan."""
        due_date: int = self.day + days_till_birth
        self._insert_into_birthing_plan(newborn_count, due_date)
        self.total_fishes += newborn_count

    def _handle_parents(
            self,
            parent_count: int,
    ) -> None:
        """Re-insert the parents into the birthing plan."""
        due_date: int = self.day + self.REGULAR_GESTATION_PERIOD
        self._insert_into_birthing_plan(parent_count, due_date)

    def _insert_into_birthing_plan(self, count: int, due_date: int) -> None:
        """Insert the given number of pregnant fishes as per due date."""
        if due_date not in self.birthing_plan:
            self.birthing_plan[due_date] = count
        else:
            self.birthing_plan[due_date] += count


print(SeaBed('input_data.txt').fishes_after_n_days(256))