# Blackjack-cli

A command-line Blackjack game written in Python featuring a 6-deck shoe, interactive tutorials, and an optional gambling mode with insurance side bets.

---
## Features

- **6-Deck Shoe:** Uses a 312-card shoe (`cards.py`) that automatically reshuffles when fewer than 25% (78 cards) remain.
- **Beginner-Friendly Tutorial:** Includes an optional in-game rules walkthrough before the first hand.
- **Two Game Modes:**
  - **Free Play:** Play casually without tracking money.
  - **Gambling Mode:** Start with a **$100.00** bankroll, place custom bets, and play until you cash out or go broke.
- **Casino Payout Rules:**
  - Standard wins pay **1:1**.
  - Natural Blackjacks (2-card 21) pay **3:2**.
  - **Insurance:** When the dealer's face-up card is an Ace, take a side bet for half your original wager (pays **2:1** if the dealer hits Blackjack).

--- 
## Requirements

* **Python 3.10+** (uses built-in type hints such as `list[Card]`)
* No external libraries required—uses only the Python standard library (`math`, `random`, `sys`).

---
## How to Run

1. Clone or download this repository and navigate to the project folder:
```bash
cd your-repository-folder

```

2. Run the game from your terminal:
```bash
python3 blackjack.py

```
*(On Windows, you may use `python blackjack.py`)*

---
## How to Play

* **`h`** — **Hit:** Draw another card.
* **`s`** — **Stand:** End your turn and let the dealer play (dealer draws until reaching 17 or higher).
* **`y` / `n**` — Answer prompts for tutorials, gambling mode, insurance, and replaying rounds.

