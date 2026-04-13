from collections import Counter
import string


def analyze_text():
    text = input("Input numbers and sentences: ")

    counts = Counter(text)

    print("\nCharacter counts:")

    # Letters (case-sensitive)
    for ch in string.ascii_letters:
        if counts[ch] > 0:
            print(f"{ch}: {counts[ch]}")

    # Digits
    for digit in string.digits:
        if counts[digit] > 0:
            print(f"{digit}: {counts[digit]}")

    print(f"\nTotal characters: {len(text)}")


if __name__ == "__main__":
    analyze_text()
