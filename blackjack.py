#!/usr/bin/env python3
import math
import sys

from cards import Card, Deck


def main() -> None:
    deck = Deck()
    balance: float = 100.0
    gambling: bool = False

    # Deals with the A special case
    def hand_value(hand: list[Card]) -> int:
        total = sum(card.point() for card in hand)
        aces = sum(1 for card in hand if card.rank == "A")

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    # Welcome the player and explain the game to him
    def greetings() -> None:
        print("\n" + "=" * 34)
        print("     ♠ ♥  BLACKJACK  ♦ ♣")
        print("=" * 34)
        print("\n  Welcome to the table!")

        while True:
            played = input("  Have you played Blackjack before? [y/n]: ").strip().lower()

            if played == "n":
                print("\n  ── How to play ──────────────────────────")
                print("  • Goal: get closer to 21 than the dealer,")
                print("    without going over.")
                print("  • 2–10 are worth their face value.")
                print("  • J, Q, K are each worth 10.")
                print("  • A is worth 11, but drops to 1 if 11")
                print("    would bust your hand.")
                print("  • You and the dealer each get 2 cards.")
                print("    One of the dealer's cards stays hidden")
                print("    until your turn is over.")
                print("  • You always play first. Type:")
                print("        h  → hit   (take another card)")
                print("        s  → stand (stop drawing; dealer plays)")
                print("  • You can hit as many times as you like,")
                print("    but going over 21 is a bust, you lose.")
                print("  • Hitting 21 ends your turn automatically.")
                print("  • After you stand, the dealer reveals the")
                print("    hidden card and draws until reaching")
                print("    17 or higher, then stops.")
                print("  • A 2-card 21 is a Blackjack: it beats")
                print("    any other hand, unless the dealer also")
                print("    has one, then it's a draw.")
                print("  • Highest total wins. Equal totals drawn.")
                print("  ─────────────────────────────────────────\n")

                while True:
                    understand = input("  Did you understand? [y/n]: ").strip().lower()

                    if understand == "y":
                        print("\n  Great! let's play! 🎲")
                        break
                    elif understand == "n":
                        print("  Please, read the instructions again.")
                        continue

                    print("  Please, choose between 'y' or 'n'.")

                break
            elif played == "y":
                print("\n  Great! let's play! 🎲")
                break

            print("  Please, choose between 'y' or 'n'.")
    # Explains the gambling mode to the player and ask if he wants to play with it
    def gamble_mode() -> bool:
        print("\n  ── Gambling mode ────────────────────────")
        print("  • You start with $100.00.")
        print("  • A normal win pays 1:1.")
        print("  • A real Blackjack pays 3:2.")
        print("  • If the dealer's revealed card is an Ace,")
        print("    you may take a safe bet (insurance) for")
        print("    half of your bet. It pays 2:1 if the")
        print("    dealer makes a real Blackjack.")
        print("  • If you lose all your money, you are")
        print("    broke and the game ends.")
        print("  ─────────────────────────────────────────\n")

        while True:
            want = input("  Do you want to gamble? [y/n]: ").strip().lower()

            if want == "y":
                print("\n  💰 Gambling mode on. Good luck!")
                return True
            elif want == "n":
                print("\n  No problem, we'll play for fun then.")
                return False

            print("  Please, choose between 'y' or 'n'.")

    # The real game
    def blackjack() -> None:
        nonlocal balance

        player = []
        dealer = []

        print("\n" + "=" * 34)
        print("     ♠ ♥  BLACKJACK  ♦ ♣")
        print("=" * 34)

        bet = 0.0
        insurance = 0.0

        if gambling:
            print(f"\n  💰 Your balance: ${balance:.2f}")

            while True:
                raw = input(f"  Place your bet (0.00 - {balance:.2f}): $").strip()

                try:
                    bet = float(raw)
                except ValueError:
                    print("  Please, enter a valid number, like 5.78.")
                    continue

                if not math.isfinite(bet) or bet <= 0.0 or bet > balance:
                    print(f"  Your bet must be greater than 0.0 and at most ${balance:.2f}.")
                    continue

                bet = round(bet, 2)
                if bet <= 0.0:
                    print("  Your bet must be at least $0.01.")
                    continue

                break

            balance -= bet

        if deck.needs_reshuffle():
            deck.refill()
            print("\n  🔄 Dealer reshuffles the deck.")

        # Deal 2 cards each. Dealer's second card is hidden.
        player.append(deck.draw())
        dealer.append(deck.draw())
        player.append(deck.draw())
        dealer.append(deck.draw())

        player_points = hand_value(player)
        dealer_points = hand_value(dealer)

        print(f"\n  You received   : {player[0]}")
        print(f"  You received   : {player[1]}")
        print(f"  Your points    : {player_points}")
        print(f"  Dealer shows   : {dealer[0]}")

        # Safe bet (insurance) when the dealer shows an Ace.
        if gambling and dealer[0].rank == "A":
            print("\n  Dealer's revealed card is an Ace.")

            if balance >= bet / 2:
                while True:
                    safe = input(
                        "  Take a safe bet for half your bet? [y/n]: "
                    ).strip().lower()

                    if safe == "y":
                        insurance = bet / 2
                        balance -= round((insurance), 2)
                        print(f"  Insurance bet  : ${insurance:.2f}")
                        break
                    elif safe == "n":
                        print("  No insurance taken.")
                        break

                    print("  Please, choose between 'y' or 'n'.")
            else:
                print("  You can't afford the safe bet.")

        # Blackjack: first two cards total 21
        player_blackjack = len(player) == 2 and player_points == 21
        dealer_blackjack = len(dealer) == 2 and dealer_points == 21

        if player_blackjack or dealer_blackjack:
            print(f"\n  Dealer's hidden card: {dealer[1]}")

            if player_blackjack and dealer_blackjack:
                print("\n  🤝 It's a draw!")
                if gambling:
                    balance += bet
                    print(f"  Your bet of ${bet:.2f} is returned.")
            elif player_blackjack:
                print("\n  🎉 Blackjack! You won! 😄")
                if gambling:
                    payout = bet * 1.5
                    balance += round((bet + payout), 2)
                    print(f"  Blackjack pays 3:2. You won ${payout:.2f}!")
            else:
                print("\n  💥 Dealer has blackjack. You lost! 😭")
                if gambling:
                    print(f"  You lost ${bet:.2f}.")

            if gambling and insurance:
                if dealer_blackjack:
                    payout = insurance * 2
                    balance += round((insurance + payout), 2)
                    print(f"  Insurance pays 2:1. You won ${payout:.2f}!")
                else:
                    print(f"  Insurance lost: ${insurance:.2f}.")

            print("\n" + "=" * 34 + "\n")
        else:
            # Players turn only. Dealer does not draw here.
            while True:
                print("\n" + "=" * 34 + "\n")

                choice = input("  Hit or stand? [h/s]: ").strip().lower()

                count = 0
                while choice not in ("h", "s"):
                    if count == 0:
                        count += 1
                        choice = input("  Please choose between 'h' or 's': ").strip().lower()
                    elif count == 1:
                        count += 1
                        choice = input("  It's between 'h' OR 's': ").strip().lower()
                    elif count == 2:
                        count += 1
                        choice = input("  'H' OR 'S'!: ").strip().lower()
                    else:
                        print("  I HATE YOU! 🤬")
                        sys.exit(0)

                if choice == "s":
                    break

                player_card = deck.draw()
                player.append(player_card)
                player_points = hand_value(player)

                print(f"\n  You received   : {player_card}")
                print(f"  Your points    : {player_points}")
                print(f"  Dealer shows   : {dealer[0]}")

                if player_points > 21:
                    print("\n  💥 You busted! You lost! 😭")
                    if gambling:
                        print(f"  You lost ${bet:.2f}.")
                        if insurance:
                            print(f"  Insurance lost: ${insurance:.2f}.")
                    print("\n" + "=" * 34 + "\n")
                    break

                if player_points == 21:
                    print("\n  You have 21, it's the end of your turn.")
                    print("\n" + "=" * 34 + "\n")
                    break

            # Dealer only plays after player stand, and only if player didn't bust.
            if player_points <= 21:
                print(f"\n  Dealer reveals : {dealer[1]}")
                print(f"  Dealer points  : {dealer_points}")

                while dealer_points < 17:
                    dealer_card = deck.draw()
                    dealer.append(dealer_card)
                    dealer_points = hand_value(dealer)

                    print(f"  Dealer received: {dealer_card}")
                    print(f"  Dealer points  : {dealer_points}")

                if dealer_points > 21 or player_points > dealer_points:
                    print("\n  🎉 You won! 😄")
                    if gambling:
                        payout = bet
                        balance += round((bet + payout), 2)
                        print(f"  You won ${payout:.2f}!")
                elif dealer_points > player_points:
                    print("\n  💥 You lost! 😭")
                    if gambling:
                        print(f"  You lost ${bet:.2f}.")
                else:
                    print("\n  🤝 It's a draw!")
                    if gambling:
                        balance += round((bet), 2)
                        print(f"  Your bet of ${bet:.2f} is returned.")

                if gambling and insurance:
                    print(f"  Insurance lost: ${insurance:.2f}.")

                print("\n" + "=" * 34 + "\n")

        if gambling:
            print(f"  💰 Your balance: ${balance:.2f}")

            if balance <= 0:
                print("\n  💸 You're broke! No more money to gamble. 😭")
                sys.exit(0)

        while True:
            play_again = input("  Want to play again? [y/n]: ").strip().lower()

            if play_again == "y":
                blackjack()
                return
            elif play_again == "n":
                print("\n  Thanks for your time! 😘")
                sys.exit(0)

            print("  Please, choose between 'y' or 'n'.")

    greetings()
    gambling = gamble_mode()
    blackjack()


if __name__ == "__main__":
    main()
