from typing import Dict, List, Optional

class BraceSyntaxError(Exception):
    """Custom exception for when a brace syntax error incurred"""
    pass

class SyntaxChecker:

    """Class for encapsulating brace syntax logic."""

    OPENERS = {'(', '{', '[', '<'}

    CLOSER_MAP: Dict[str, str] = {
        '{': '}',
        '[': ']',
        '(': ')',
        '<': '>',
    }
    POINTS_MAP: Dict[str, str] = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    def __init__(self, path: str) -> List[str]:
        """Extract the source data."""
        with open(path, 'r') as infile:
            self.data: List[str] = infile.read().splitlines()
        self.to_be_closed: List[str] = []
        self.to_be_closed_next: Optional[str] = None
        self.points: int = 0

    def calculate_syntax_errors(self) -> int:
        """Calculate syntax error scores."""
        for row in self.data:
            for char in row:
                if char in self.OPENERS:
                    self._handle_opening(char)
                else:
                    try:
                        self._check_closure(char)
                    except BraceSyntaxError:
                        break
        return self.points

    def _handle_opening(self, opener: str) -> None:
        """Handle a newly opened set of braces."""
        self.to_be_closed.append(self.to_be_closed_next)
        self.to_be_closed_next = opener

    def _check_closure(self, char: str) -> None:
        """Check braces have been close correctly."""
        closer: str = self.CLOSER_MAP[self.to_be_closed_next]
        if char != closer:
            self.points += self.POINTS_MAP[char]
            raise BraceSyntaxError
        else:
            self.to_be_closed_next = self.to_be_closed.pop()


print(SyntaxChecker('input_data.txt').calculate_syntax_errors())