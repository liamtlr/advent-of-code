from typing import Dict, List


class CaveTraverser:

    """Logic encapsulating traversing sea caves."""

    START_CAVE = 'start'
    END_CAVE = 'end'

    def __init__(self, infile_path: str):
        """Read the cave data."""
        self.small_caves: set = set()
        self.cave_network: Dict[str, set] = {}
        self.paths: List[list] = []
        with open(infile_path, 'r') as infile:
            raw_data: List[str] = infile.read().splitlines()
            for join in raw_data:
                ot, do = join.split('-')
                if self._is_small_cave(ot):
                    self.small_caves.add(ot)
                if self._is_small_cave(do):
                    self.small_caves.add(do)
                self._add_caves_to_network(ot, do)

    def find_paths(self) -> int:
        """Find paths from start to end."""
        preceding_data: dict = {'double_small_cave': False, 'preceders': set([])}
        self._build_path(self.START_CAVE, preceding_data)
        return len(self.paths)

    def _is_small_cave(self, cave: str) -> bool:
        """Discern whether the given cave is small."""
        return cave.lower() == cave

    def _add_caves_to_network(self, from_cave: str, to_cave: str) -> None:
        """Add the given caves to the cave network"""
        if from_cave not in self.cave_network:
            self.cave_network[from_cave] = {to_cave}
        else:
            self.cave_network[from_cave].add(to_cave)
        if to_cave not in self.cave_network:
            self.cave_network[to_cave] = {from_cave}
        else:
            self.cave_network[to_cave].add(from_cave)

    def _build_path(self, cave: str, preceders: dict) -> None:
        """Get the path to the end from the given cave."""
        connected_caves = self.cave_network[cave]
        for connected_cave in connected_caves:
            fresh_preceders: set = set(preceders['preceders'])
            fresh_bool: bool = preceders['double_small_cave']
            if connected_cave == self.START_CAVE:
                continue
            if (
                connected_cave in self.small_caves
                and connected_cave in fresh_preceders
                and fresh_bool
            ):
                continue
            elif (
                connected_cave in self.small_caves
                and connected_cave in fresh_preceders
                and not fresh_bool
            ):
                fresh_bool = True
            if connected_cave == self.END_CAVE:
                fresh_preceders.add(cave)
                fresh_preceders.add(connected_cave)
                self.paths.append(fresh_preceders)
                continue
            else:
                fresh_preceders.add(cave)
                preceder_dict: dict = {
                    'preceders': fresh_preceders,
                    'double_small_cave': fresh_bool
                }
                self._build_path(connected_cave, preceder_dict)


print(CaveTraverser('input_data.txt').find_paths())
