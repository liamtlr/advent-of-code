from collections import Counter
from functools import partial, reduce
import re
from typing import Dict, Iterator, List, Optional


class PolymerBuilder:

    """Logic encapsulating building a polymer from a template."""

    RULE_DELIMITER = ' -> '

    def __init__(self, infile_path: str):
        """Read the template data."""
        with open(infile_path, 'r') as infile:
            raw_data: List[str] = infile.read().splitlines()
        delimiter: int = raw_data.index('')
        template, rules = raw_data[:delimiter], raw_data[delimiter + 1:]
        self.polymer: str = template[0]
        self.rules: Dict[str] = {}
        for rule in rules:
            pattern, insertion = rule.split(self.RULE_DELIMITER)
            self.rules[pattern] = insertion

    def apply_rules(self, acc, curr) -> Dict[int, list]:
        """Apply the rules and report where matches occur"""
        rule, insertion = curr
        matches: List[Iterator] = re.finditer(f'(?={rule})', self.polymer)
        for match in matches:
            insertion_point = match.span()[0] + 1
            acc[insertion_point] = insertion
        return acc

    def build_polymer(
        self,
        acc: List[str],
        curr: tuple,
        insertion_map: Dict[int, str]
    ) -> List[str]:
        """Reconstruct polymer, inserting the rule-based characers."""
        index, char = curr
        try:
            for_insertion: List[str] = insertion_map[index]
            chars = f'{for_insertion}{char}'
        except KeyError:
            chars: Optional[str] = char
        return f'{acc}{chars}'

    def discern_polymer(self, steps: int) -> str:
        """Simulate the given number of steps on the polymer."""
        for _ in range(steps):
            insertion_map: Dict[int, list] = reduce(
                self.apply_rules,
                self.rules.items(),
                {},
            )
            new_string_chars: List[str] = reduce(
                partial(self.build_polymer, insertion_map=insertion_map),
                enumerate(self.polymer),
                ''
            )
            self.polymer = new_string_chars
        counts: List[int] = list(Counter(self.polymer).values())
        max_count: int = max(counts)
        min_count: int = min(counts)
        return max_count - min_count


print(PolymerBuilder('input_data.txt').discern_polymer(20))
