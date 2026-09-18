"""
In this problem, we want to determine all possible subsequences
of the given sequence. We use backtracking to solve this problem
with a for loop.

Time complexity: O(2^n),
where n denotes the length of the given sequence.
"""


def generate_all_subsequences(sequence):
    backtrack(sequence, [], 0)


def backtrack(sequence, path, index):
    print(path)

    for i in range(index, len(sequence)):
        path.append(sequence[i])
        backtrack(sequence, path, i + 1)
        path.pop()


sequence = ["A", "B", "C"]
generate_all_subsequences(sequence)
