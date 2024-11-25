import random
class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, n_decks):
        self.n_decks = n_decks
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        self.cards = [Card(suit, rank, values[rank]) for suit in suits for rank in ranks] * n_decks
        self.shuffle()


    def shuffle(self):
        random.shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()