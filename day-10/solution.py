from functools import reduce
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
    ERROR_POINTS_MAP: Dict[str, str] = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    COMPLETION_POINTS_MAP: Dict[str, str] = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4,
    }

    def __init__(self, path: str) -> List[str]:
        """Extract the source data."""
        with open(path, 'r') as infile:
            self.data: List[str] = infile.read().splitlines()
        self.to_be_closed: List[str] = []
        self.to_be_closed_next: Optional[str] = None
        self.points: int = 0
        self.to_complete: List[str] = []
        self._parse_rows()

    @property
    def syntax_errors(self) -> int:
        """Calculate syntax error scores."""
        return self.points

    @property
    def completion_score(self) -> int:
        """Calculate the completion score."""
        scores: List[int] = [
            reduce(
                lambda acc, curr: (acc * 5) + self.COMPLETION_POINTS_MAP[curr],
                unclosed,
                0
            )
            for unclosed in self.to_complete
        ]
        sorted_scores = sorted(scores)
        middle_score = len(scores) // 2
        return sorted_scores[middle_score]

    def _parse_rows(self):
        """Parse the data"""
        for row in self.data:
            self.to_be_closed_next = None
            self.to_be_closed = []
            for char in row:
                if char in self.OPENERS:
                    self._handle_opening(char)
                else:
                    try:
                        self._check_closure(char)
                    except BraceSyntaxError:
                        break
            else:
                self._handle_incompletion()

    def _handle_opening(self, opener: str) -> None:
        """Handle a newly opened set of braces."""
        if self.to_be_closed_next is not None:
            self.to_be_closed.append(self.to_be_closed_next)
        self.to_be_closed_next = opener

    def _check_closure(self, char: str) -> None:
        """Check braces have been close correctly."""
        closer: str = self.CLOSER_MAP[self.to_be_closed_next]
        if char != closer:
            self.points += self.ERROR_POINTS_MAP[char]
            raise BraceSyntaxError
        else:
            if self.to_be_closed:
                self.to_be_closed_next = self.to_be_closed.pop()
            else:
                self.to_be_closed_next = None

    def _handle_incompletion(self) -> None:
        """Handle the unclosed braces."""
        self.to_be_closed.append(self.to_be_closed_next)
        reversed_for_closure: List[str] = reversed(self.to_be_closed)
        self.to_complete.append(reversed_for_closure)


print(SyntaxChecker('input_data.txt').syntax_errors)
print(SyntaxChecker('input_data.txt').completion_score)