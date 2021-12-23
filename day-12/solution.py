from functools import reduce
from typing import Dict, List, Optional, Tuple


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

    def find_paths(self) -> List[Tuple]:
        """Find paths from start to end."""
        self._build_path(self.START_CAVE, [])
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

    def _build_path(self, cave: str, preceders: List[str]) -> Optional[List[str]]:
        """Get the path to the end from the given cave."""
        connected_caves = self.cave_network[cave]
        for connected_cave in connected_caves:
            fresh_preceders: List[str] = list(preceders)
            if connected_cave in self.small_caves and connected_cave in preceders:
                continue
            if connected_cave == self.END_CAVE:
                fresh_preceders.extend([cave, connected_cave])
                self.paths.append(fresh_preceders)
                continue
            else:
                fresh_preceders.append(cave)
                self._build_path(connected_cave, fresh_preceders)


print(CaveTraverser('input_data.txt').find_paths())
