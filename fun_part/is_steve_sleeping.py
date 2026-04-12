# How can you ask a user for information?
# How can you include if and else into a question
def ask_steve_status():
    for _ in range(6):
        while True:
            response = input("Is Steve sleeping? (yes/no): ").strip().lower()

            if response in ("yes", "no", "ahh"):
                break
            print("Please enter yes or no.")

        if response in ("yes", "ahh"):
            print("Steve woke up 😢")
        else:
            print("Steve went to sleep 🙂")


if __name__ == "__main__":
    ask_steve_status()
