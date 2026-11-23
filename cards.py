from random import shuffle


class Card:
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]  # noqa: RUF012
    SUITS = ["spades", "hearts", "diamonds", "clubs"]  # noqa: RUF012

    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def point(self) -> int:
        if self.rank in "KJQ":
            return 10
        if self.rank == "A":
            return 11   # The function to deal with A special case is in "blackjack.py"
        return int(self.rank)


class Deck:
    DECKS_IN_SHOE = 6   # Every deck is formed by 6 other decks
    RESHUFFLE_FRACTION = 4   # Reshuffle when fewer than 1/4 of the shoe remains

    def __init__(self) -> None:
        self.deck: list[Card] = []
        self.refill()

    def refill(self) -> None:
        self.deck = [
            Card(rank, suit)
            for i in range(self.DECKS_IN_SHOE)
            for suit in Card.SUITS
            for rank in Card.RANKS
        ]
        shuffle(self.deck)

    def needs_reshuffle(self) -> bool:
        return len(self.deck) < self.DECKS_IN_SHOE * 52 // self.RESHUFFLE_FRACTION

    def draw(self) -> Card:
        return self.deck.pop(-1)

    def __len__(self) -> int:
        return len(self.deck)

    def __repr__(self) -> str:
        return f"Deck({len(self)} cards remaining)"
