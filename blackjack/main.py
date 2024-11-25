from blackjack.game import BlackjackGame
from blackjack.player import Player
from blackjack.player import Dealer
def get_players():
    players = []
    while True:
        name = input("Enter the player's name (or type 'done' to finish adding players): ").strip()
        if name.lower() == 'done':
            break
        while True:
            try:
                balance = int(input(f"Enter the starting balance for {name}: "))
                if balance <= 0:
                    print("Balance must be a positive amount. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        players.append(Player(name, balance))
    return players
def get_decks():
    while True:
        try:
            decks= int(input(f"Enter the number of decks to create: "))
            if decks <= 0:
                print("Number of decks must be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
    return decks
def main():
    print("Welcome to Blackjack!")
    players = get_players()
    decks = get_decks()
    game = BlackjackGame(players,decks)

    if not players:
        print("No players added. Exiting the game.")
        return

    while True:
        game.place_bets()
        game.play_round()
        for player in players:
            if player.balance == 0:
                print(f"{player.name} is out of money and has been removed from the game.")
                players.remove(player)
        if not players:
            print("All players are out of money. Game over!")
            break
        play_again = input("Do you want to play another round? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
