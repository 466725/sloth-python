"""
In this problem, we want to determine all possible subsequences
of the given sequence. We use backtracking to solve this problem.

Time complexity: O(2^n),
where n denotes the length of the given sequence.
"""


def generate_all_subsequences(sequence):
    backtrack(sequence, [], 0)


def backtrack(sequence, path, index):
    if index == len(sequence):
        print(path)
        return

    backtrack(sequence, path, index + 1)
    path.append(sequence[index])
    backtrack(sequence, path, index + 1)
    path.pop()


sequence = ["A", "B", "C"]
generate_all_subsequences(sequence)
