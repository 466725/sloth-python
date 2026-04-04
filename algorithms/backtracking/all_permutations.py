"""Generate and print all permutations of a sequence using backtracking.

Time complexity: O(n! * n), where n is the sequence length.
"""

from collections.abc import Sequence
from typing import Any


def generate_all_permutations(sequence: Sequence[Any]) -> None:
    """Entry point that initializes backtracking state."""
    used = [False] * len(sequence)
    backtrack(sequence, [], 0, used)


def backtrack(
        sequence: Sequence[Any],
        path: list[Any],
        depth: int,
        used: list[bool],
) -> None:
    if depth == len(sequence):
        print(path)
        return

    for i, value in enumerate(sequence):
        if used[i]:
            continue

        path.append(value)
        used[i] = True
        backtrack(sequence, path, depth + 1, used)
        used[i] = False
        path.pop()


if __name__ == "__main__":
    generate_all_permutations([3, 1, 2, 4])
    generate_all_permutations(["A", "B", "C"])
