from blackjack.card import Deck
from blackjack.player import Dealer
class BlackjackGame:
    def __init__(self, players,n_decks):
        """
        Initialize the Blackjack game with a list of players.
        """
        self.n_decks = n_decks
        self.deck = Deck(n_decks)
        self.players = players  # List of Player objects
        self.dealer = Dealer(balance=100000)  # Dealer starts with a bank balance
    ############
    # Bets methods
    #############
    def place_bets(self):
        """
        Players place their bets for the round.
        """
        for player in self.players:
            if player.balance > 0:  # Only allow betting if the player has money
                while True:
                    try:
                        bet = int(input(f"{player.name}, your balance is {player.balance}. Enter your bet: "))
                        player.place_bet(bet)
                        break
                    except ValueError as e:
                        print(e)
                    except Exception as ex:
                        print("Invalid bet. Please try again.")
            else:
                print(f"{player.name} has no balance left and cannot bet.")

    def resolve_bets(self, player):
        for i, hand in enumerate(player.hands):
            hand_value = player.get_hand_value(hand)  # Calculate hand value
            dealer_value = self.dealer.get_hand_value(self.dealer.hand)
            if hand_value > 21:  # Player busts
                print(f"Hand {i + 1} of ", f"{player.name} busts! Dealer wins.")
                player.lose_bet()
                self.dealer.hand = []

            elif player.get_hand_value(hand) == 21 and len(player.hand) == 2:
                print(f"Hand {i + 1} of ", f"{player.name} has Blackjack!")
                player.win_bet(blackjack=True)
                self.dealer.balance -= player.current_bet *1.5
                self.dealer.hand = []

            elif dealer_value > 21 or hand_value > dealer_value:  # Player wins
                print(f"Hand {i + 1} of ", f"{player.name} wins!")
                player.win_bet()  # Blackjack bonus
                self.dealer.balance -= player.current_bet
                self.dealer.hand = []

            elif hand_value == dealer_value:  # Push
                print(f"Hand {i + 1} of ", f"{player.name} and Dealer push!")
                player.push_bet()
                self.dealer.hand = []

            elif self.dealer.hand_value == 21 and len(self.dealer.hand) == 2:
                print(f"Dealer wins against ", f"Hand {i + 1} of ", f"{player.name}. Dealer has blackjack!")
                player.lose_bet()
                self.dealer.hand = []

            else:  # Dealer wins
                print(f"Dealer wins against {player.name}.")
                player.lose_bet()
                self.dealer.hand = []
        player.hands = []
        player.hand=[]







    ########
    # Game playing methods
    #######
    def check_deck(self):
        if len(self.deck.cards) < (len(self.players) + 1) * 2:  # Minimum cards for a new round
            self.deck.shuffle()

    def play_round(self):
        """
        Play one round of Blackjack with sequential dealing, insurance, and dealer hitting on soft 17.
        """
        self.check_deck()

        # Reset hands for players and the dealer
        for player in self.players:
            player.reset_hands()
        self.dealer.reset_hand()

        # Sequential initial deal (one card to each player, then the dealer, repeat)
        for _ in range(2):
            for player in self.players:
                if player.balance > 0:
                    card = self.deck.deal_one()
                    if len(player.hands) == 0:
                        player.add_hand([card], bet=player.bets)
                    else:
                        player.hands[0].append(card)
            self.dealer.add_card(self.deck.deal_one())

        # Display initial hands
        for player in self.players:
            if player.balance > 0:
                print(f"\n{player.name}'s initial hand: {', '.join(str(card) for card in player.hands[0])}")
                print("Your value:", player.get_hand_value(player.hands[0]))

        print("\nDealer's hand: [Hidden],", self.dealer.hand[0])
        print("\nDealer's value:", self.dealer.get_hand_value(self.dealer.hand, reveal_all=False))


        # **Insurance Option**
        if self.dealer.hand[0].rank == 'A':  # Offer insurance
            print("\nDealer shows an Ace. Insurance is available.")
            for player in self.players:
                if player.balance > 0:
                    while True:
                        try:
                            insurance_bet = float(input(
                                f"{player.name}, place an insurance bet (up to half your initial bet, or 0 for none): "))
                            if insurance_bet == 0:  # Player opts out of insurance
                                print(f"{player.name} chose not to place an insurance bet.")
                                break
                            elif 0 < insurance_bet <= player.bets[0] / 2:  # Valid insurance bet
                                player.balance -= insurance_bet
                                print(f"{player.name} placed an insurance bet of {insurance_bet}.")
                                if self.dealer.get_hand_value(self.dealer.hand, reveal_all=True) == 21:
                                    print(f"Dealer has Blackjack! {player.name} wins the insurance bet.")
                                    player.balance += insurance_bet * 3  # Insurance pays 2:1
                                else:
                                    print("Dealer does not have Blackjack. Insurance bet is lost.")
                                break
                            else:
                                print("Invalid insurance bet amount. Try again.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

        # Check if the dealer has Blackjack
        if self.dealer.get_hand_value(self.dealer.hand, reveal_all=True) == 21:
            print("\nDealer has Blackjack! ",self.dealer.display_hand())
            for player in self.players:
                if player.balance > 0:
                    player_total = player.get_hand_value(player.hands[0])
                    if player_total == 21:
                        print(f"{player.name} pushes with the dealer.")
                        player.balance += player.bets[0]  # Return the bet for a push
                    else:
                        print(f"{player.name} loses.")
            return  # End round if dealer has Blackjack

        # Player turns
        for player in self.players:
            if player.balance > 0:
                print(f"\n{player.name}'s turn:")
                for i, hand in enumerate(player.hands):
                    print(f"\nPlaying hand {i + 1}: {', '.join(str(card) for card in hand)}")
                    while player.get_hand_value(hand) < 21:
                        action = input("Do you want to hit, stand, split, or double? (h/s/sp/d): ").lower()
                        if action == 'h':
                            hand.append(self.deck.deal_one())
                            print("\nDealer's hand: [Hidden],", self.dealer.hand[0])
                            print("Your hand:", ', '.join(str(card) for card in hand))
                            print("Your value:", player.get_hand_value(hand))
                            print("Your cards: ",len(hand))
                        elif action == 'sp':
                            try:
                                player.split_hand(i)
                                hand.append(self.deck.deal_one())
                                player.hands[-1].append(self.deck.deal_one())
                                print(f"Hands after splitting for {player.name}:")
                                print(f"Hand {i + 1}:", ', '.join(str(card) for card in hand))
                            except ValueError as e:
                                print(e)
                                continue
                        elif action == 'd':
                            try:
                                player.double_down(hand)
                                hand.append(self.deck.deal_one())
                                print(f"Your hand after doubling down:", ', '.join(str(card) for card in hand))
                                print("Your value:", player.get_hand_value(hand))
                                break  # Player gets only one more card after doubling
                            except ValueError as e:
                                print(e)
                                continue
                        else:
                            break

        # Dealer's turn (Hits on soft 17)
        print("\nDealer's turn:")
        print("Dealer's hand:", self.dealer.display_hand())
        while True:
            dealer_value = self.dealer.get_hand_value(self.dealer.hand)
            print("\nDealer's value:", dealer_value)
            if dealer_value < 17 or (dealer_value == 17 and any(card.rank == 'A' for card in self.dealer.hand)):
                print("Dealer hits.")
                self.dealer.add_card(self.deck.deal_one())
                print("Dealer's hand:", self.dealer.display_hand())
            elif dealer_value > 21:
                print("Dealer Busts!")
                break
            else:
                print("Dealer stands.")
                break

        # Resolve bets
        for player in self.players:
            if player.balance > 0:
                self.resolve_bets(player)



