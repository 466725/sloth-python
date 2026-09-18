from collections import defaultdict


def word_occurrence(sentence: str) -> dict:
    occurrence = defaultdict(int)
    # Creating a dictionary containing count of each word
    for token in sentence.split(" "):
        occurrence[token] += 1
    return occurrence


if __name__ == "__main__":
    for term, count in word_occurrence("How frequently a word occurs!").items():
        print(f"{term}: {count}")
