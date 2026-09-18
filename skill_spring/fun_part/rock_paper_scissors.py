import random

CHOICES = ("rock", "paper", "scissors")


def get_choice(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in CHOICES:
            return choice
        print("Invalid choice. Please enter rock, paper, or scissors.")


def determine_winner(p1, p2):
    if p1 == p2:
        return "tie"
    wins = {
        ("rock", "scissors"),
        ("scissors", "paper"),
        ("paper", "rock"),
    }
    return "p1" if (p1, p2) in wins else "p2"


def play_vs_computer():
    user = get_choice("Choose rock, paper, or scissors: ")
    computer = random.choice(CHOICES)

    print(f"You: {user} !!!")
    print(f"Computer: {computer} !!!")

    result = determine_winner(user, computer)
    if result == "tie":
        print("You tied!!!")
    elif result == "p1":
        print("You won!!!")
    else:
        print("You lost!!!")


def play_vs_player():
    user1 = get_choice("Player 1: choose rock, paper, or scissors: ")

    print("\n" * 20)  # simple screen clear

    user2 = get_choice("Player 2: choose rock, paper, or scissors: ")

    print(f"Player1: {user1} !!!")
    print(f"Player2: {user2} !!!")

    result = determine_winner(user1, user2)
    if result == "tie":
        print("You two tied!!!")
    elif result == "p1":
        print("Player1 won!!!")
    else:
        print("Player2 won!!!")


def play_vs_hacker():
    user = get_choice("Choose rock, paper, or scissors: ")

    # Hacker always wins 😈
    counter = {
        "rock": "paper",
        "paper": "scissors",
        "scissors": "rock",
    }
    hacker = counter[user]

    print(f"You: {user} !!!")
    print(f"Hacker: {hacker} !!!")
    print("You lost!!!")


def main():
    mode = input("Play against computer, another player, or hacker? ").strip().lower()

    if mode == "computer":
        play_vs_computer()
    elif mode == "another player":
        play_vs_player()
    elif mode == "hacker":
        play_vs_hacker()
    else:
        print("Invalid mode.")


if __name__ == "__main__":
    main()
