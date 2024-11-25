class Player:
    def __init__(self, name, balance):  # Default bank of 100
        self.name = name
        self.balance = balance  # Player's starting money
        self.bets = []
        self.hands = []
        self.hand_value = 0
        self.aces = 0
        self.max_splits = 4
        self.hand=[]
        self.current_bet=0 # Bet placed for the current round and bet
        self.doubled_hands=False

    def place_bet(self, bet_amount):
        if not isinstance(bet_amount, int):
            raise TypeError("Bet amount must be an integer.")
        if bet_amount > self.balance:
            raise ValueError(f"{self.name} does not have enough balance to place this bet.")
        self.bets.append(bet_amount)
        self.current_bet=bet_amount# Track the bet for this hand
        self.balance -= bet_amount

    def win_bet(self,blackjack=False):
        if blackjack:
            self.balance += self.current_bet * 2.5  # Blackjack pays 3:2
        else:
            self.balance += self.current_bet * 2  # Regular win

    def lose_bet(self):
        self.current_bet = 0
        return

    def push_bet(self):
        self.balance += self.current_bet  # Bet returned to the player

    def add_hand(self, hand, bet):
        if not self.hands[0]:
            del self.hands[0]
        if len(self.hands) < self.max_splits:
            self.hands.append(hand)
            self.bets.append(bet)
        else:
            raise ValueError("Maximum number of splits reached!")

    def reset_hands(self):
        self.hands = [[]]  # Reset hands to a single empty hand
        self.bets = []

    def add_card(self, card):
        self.hand.append(card)
        self.hand_value += card.value
        if card.rank == 'A':
            self.aces += 1
        self.adjust_for_aces()

    def display_hands(self):
        return [', '.join(str(card) for card in hand) for hand in self.hands]

    def split_hand(self, hand_index):
        """
        Splits a hand into two hands if valid.
        """
        if len(self.hands[hand_index]) == 2 and self.hands[hand_index][0].value == self.hands[hand_index][1].value:
            new_hand = [self.hands[hand_index].pop()]  # Remove one card to form a new hand
            self.hands.append(new_hand)  # Add the new hand
            original_bet = self.current_bet # Get the original bet for the hand
            self.place_bet(original_bet)  # Place a new bet for the new hand
        else:
            raise ValueError("Cannot split this hand.")

    def double_down(self, hand):
        """
        Double the bet for a specific hand.
        """
        current_bet = self.current_bet
        if current_bet > self.balance:
            raise ValueError(f"{self.name} does not have enough balance to double down.")
        if len(hand)>2:
            raise ValueError("Cannot double down after dealing one card.")
        self.balance -= current_bet  # Deduct the additional bet
        self.current_bet=current_bet * 2
        self.doubled_hands = True  # Mark the hand as doubled

    def adjust_for_aces(self):
        while self.hand_value > 21 and self.aces:
            self.hand_value -= 10
            self.aces -= 1

    def display_hand(self, reveal_all=True):
        """
        Returns a string representation of the hand.
        If `reveal_all` is False, only display the first card.
        """
        if reveal_all:
            return ', '.join(str(card) for card in self.hand)
        else:
            return f"{self.hand[0]}, [Hidden]"

    def reset_hand(self):
        self.hands = []
        self.hand_value = 0
        self.aces = 0

    def get_hand_value(self,hand, reveal_all=True):
        cards_to_consider= hand if reveal_all else [hand[0]]
        total = sum(card.value for card in cards_to_consider)
        has_ace = any(card.rank == 'A' for card in cards_to_consider)
        if has_ace and total > 21:
            total-=10
            return total
        if has_ace and total + 10 <= 21:
            return total + 10  # Soft hand
        return total # Hard hand

class Dealer(Player):
    def __init__(self, balance):
        super().__init__(name="Dealer", balance=balance)

    def must_hit(self):
        """
        Determines if the dealer must hit based on the rules:
        - Dealer hits on soft 17 or less.
        - Dealer stands on 17 or higher (except soft 17 where the dealer hits).
        """
        hand_value, is_soft = self.get_hand_value()
        return hand_value < 17 or (hand_value == 17 and is_soft)

    def take_insurance(self, player, amount):
        """
        Handles insurance payouts if the dealer has blackjack.

        Args:
            player (Player): The player taking insurance.
            amount (int): Insurance bet amount.
        """
        if self.get_hand_value()[0] == 21:  # Dealer has blackjack
            self.balance -= 2 * amount  # Insurance pays 2:1
            player.balance += 2 * amount
        else:
            self.balance += amount  # Dealer keeps the insurance bet
