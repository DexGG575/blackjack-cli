#!/usr/bin/env python3
import sys

from cards import Card, Deck


def main() -> None:
    deck = Deck()
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
            played = input("  Have you played Blackjack before? [y/n]: ").lower()

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
                    understand = input("  Did you understand? [y/n]: ").lower()

                    if understand == "y":
                        print("\n  Great! let's play! 🎲")
                        break
                    elif understand == "n":
                        print("  Please, read the instructions again.")
                        continue

                    print("  Please, chose between 'y' or 'n'.")

                break
            elif played == "y":
                print("\n  Great! let's play! 🎲")
                break

            print("  Please, chose between 'y' or 'n'.")
    # The real game
    def black_jack() -> None:
        player = []
        dealer = []

        print("\n" + "=" * 34)
        print("     ♠ ♥  BLACKJACK  ♦ ♣")
        print("=" * 34)

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

        # Blackjack: first two cards total 21
        player_blackjack = len(player) == 2 and player_points == 21
        dealer_blackjack = len(dealer) == 2 and dealer_points == 21

        if player_blackjack or dealer_blackjack:
            print(f"\n  Dealer's hidden card: {dealer[1]}")

            if player_blackjack and dealer_blackjack:
                print("\n  🤝 It's a draw!")
            elif player_blackjack:
                print("\n  🎉 Blackjack! You won! 😄")
            else:
                print("\n  💥 Dealer has blackjack. You lost! 😭")

            print("\n" + "=" * 34 + "\n")
        else:
            # Players turn only. Dealer does not draw here.
            while True:
                print("\n" + "=" * 34 + "\n")

                choice = input("  Hit or stand? [h/s]: ").lower()

                count = 0
                while choice not in ("h", "s"):
                    if count == 0:
                        count += 1
                        choice = input("  Please choose between 'h' or 's': ").lower()
                    elif count == 1:
                        count += 1
                        choice = input("  It's between 'h' OR 's': ").lower()
                    elif count == 2:
                        count += 1
                        choice = input("  'H' OR 'S'!: ").lower()
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
                elif dealer_points > player_points:
                    print("\n  💥 You lost! 😭")
                else:
                    print("\n  🤝 It's a draw!")

                print("\n" + "=" * 34 + "\n")

        while True:
            play_again = input("  Want to play again? [y/n]: ").lower()

            if play_again == "y":
                black_jack()
                return
            elif play_again == "n":
                print("\n  Thanks for your time! 😘")
                sys.exit(0)

            print("  Please, chose between 'y' or 'n'.")

    greetings()
    black_jack()


if __name__ == "__main__":
    main()
