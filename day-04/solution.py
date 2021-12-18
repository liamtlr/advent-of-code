from typing import Optional


class Winnable:

    """Logic encapsulating groups of numbers (i.e. rows or columns)."""

    def __init__(self, items: list, win_at: int = 5):
        """Set items against the instance."""
        self.available_numbers = {item for item in items}
        self.checked_count = 0
        self.win_at = win_at

    @property
    def has_won(self) -> bool:
        """Returns true if all numbers have been checked off."""
        return self.checked_count == self.win_at

    def handle_number(self, number: int) -> None:
        """Handle a number checked of the winnable."""
        if number in self.available_numbers:
            self.checked_count += 1
            self.available_numbers.remove(number)

    def get_score(self) -> int:
        """Get the row or columns's score."""
        return sum(number for number in self.available_numbers)


class Card:

    """Logic encapsulating a bingo card"""

    def __init__(self, data: list, cols: int = 5):
        """Set the number data"""
        self.items = set()
        self.lookups = {}
        self.raw_column_data = [[] for _ in range(cols)]
        for row_index, row in enumerate(data):
            self.rows = [Winnable(row) for row in data]
            for column_index, number in enumerate(row):
                self.items.add(number)
                self.lookups.update({
                    number: {'column': column_index, 'row': row_index}
                })
                self.raw_column_data[column_index].append(number)
        self.columns = [Winnable(column) for column in self.raw_column_data]

    @property
    def has_won(self) -> bool:
        """Returns if a card has a winning row or column."""
        return (
            any([row.has_won for row in self.rows])
            or any([column.has_won for column in self.columns])
        )

    def handle_number(self, number: int) -> None:
        """Check a card has this number and forward to winnables if so."""
        if number in self.items:
            lookups: dict = self.lookups[number]
            column_index, row_index = lookups['column'], lookups['row']
            column_winnable: Winnable = self.columns[column_index]
            row_winnable: Winnable = self.rows[row_index]
            column_winnable.handle_number(number)
            row_winnable.handle_number(number)

    def get_score(self) -> int:
        """Get the card's score."""
        return sum(row.get_score() for row in self.rows)


class BingoGame:

    """Logic encapsulating a game of bingo"""

    def __init__(self, infile_path: str):
        """Read the game data."""
        with open(infile_path, 'r') as infile:
            data: list = infile.readlines()
        self.numbers = data[0].split(',')
        self.winning_number: Optional[int] = None
        self.winning_card: Optional[Card] = None
        self.last_winning_number: Optional[int] = None
        self.last_winning_card: Optional[Card] = None
        cards: list = data[2:]
        start = 0
        CARD_STEP = 6
        ROWS_PER_CARD = 5
        self.cards: list = []
        for i in range(start, len(cards), CARD_STEP):
            card_data: list = cards[i:i + ROWS_PER_CARD]
            card_data = [self._extract_row_numbers(row) for row in card_data]
            self.cards.append(Card(card_data))

    @property
    def game_over(self) -> bool:
        """Returns true a card has won."""
        return any([card.has_won for card in self.cards])

    def play(self):
        """Play a game of bingo"""
        for number_str in self.numbers:
            number: int = int(number_str)
            self._handle_number(number)

    def get_winning_card_score(self) -> int:
        """Get the winning card's score."""
        winning_card_score: int = self.winning_card.get_score()
        return winning_card_score * self.winning_number

    def get_last_winning_card_score(self) -> int:
        """Get the last winning card's score."""
        last_winning_card_score: int = self.last_winning_card.get_score()
        return last_winning_card_score * self.last_winning_number

    def _extract_row_numbers(self, row_string: str) -> list:
        """Extract a list of numbers from a single string of spaced numbers."""
        number_list: list = row_string.strip().split(' ')
        filtered_list: list = [int(number) for number in number_list if number]
        return filtered_list

    def _handle_number(self, number: int) -> None:
        """Pass the number to the cards"""
        for card in self.cards:
            if not card.has_won:
                card.handle_number(number)
                if card.has_won:
                    self.last_winning_card = card
                    self.last_winning_number = number
                    if not self.winning_card:
                        self.winning_card = card
                        self.winning_number = number


game = BingoGame('input_data.txt')
game.play()
print(game.get_winning_card_score())
print(game.get_last_winning_card_score())
