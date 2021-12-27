from collections import Counter
from typing import List


class PolymerBuilder:

    """Logic encapsulating building a polymer from a template."""

    RULE_DELIMITER = ' -> '

    def __init__(self, infile_path: str):
        """Read the template data."""
        with open(infile_path, 'r') as infile:
            raw_data: List[str] = infile.read().splitlines()
        delimiter: int = raw_data.index('')
        template, rules = raw_data[:delimiter], raw_data[delimiter + 1:]
        polymer: str = template[0]
        # Extract the rules
        self.rules: dict = {}
        for rule in rules:
            pattern, insertion = rule.split(self.RULE_DELIMITER)
            self.rules[pattern] = insertion
        # Extract the pairing of characrters and their overall counts based on
        # the input polymer
        self.pair_counter: Counter = Counter()
        self.char_counter: Counter = Counter()
        for index, char in enumerate(polymer):
            charset = polymer[index: index + 2]
            self.char_counter[char] += 1
            if len(charset) > 1:
                self.pair_counter[charset] += 1

    def get_polymer_count(self, steps: int) -> int:
        """Simulate the given number of steps on the polymer and get count."""
        self._build_polymer(steps)
        counts: List[int] = list(Counter(self.char_counter).values())
        max_count: int = max(counts)
        min_count: int = min(counts)
        return max_count - min_count

    def _build_polymer(self, steps: int) -> None:
        """Build the polymer based on the number of steps"""
        for _ in range(steps):
            new_counter: Counter = Counter()
            for countable, count in self.pair_counter.items():
                if countable in self.rules:
                    inserted: str = self.rules[countable]
                    new_counter[f'{countable[0]}{inserted}'] += count
                    new_counter[f'{inserted}{countable[1]}'] += count
                    self.char_counter[inserted] += count
                else:
                    new_counter[countable] = count
            self.pair_counter = new_counter


print(PolymerBuilder('input_data.txt').get_polymer_count(10))
print(PolymerBuilder('input_data.txt').get_polymer_count(40))
