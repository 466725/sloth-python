"""
In this problem, we want to determine all possible combinations of k
numbers out of 1 ... n. We use backtracking to solve this problem.
Time complexity: O(C(n,k)) which is O(n choose k) = O((n!/(k! * (n - k)!)))
"""


def backtrack(
        increment: int,
        total_number: int,
        level: int,
        path: list[int],
        result_list: list[list[int]],
) -> None:
    if level == 0:
        result_list.append(path[:])
        return

    for i in range(increment, total_number - level + 2):
        path.append(i)
        backtrack(i + 1, total_number, level - 1, path, result_list)
        path.pop()


def generate_all_combinations(n: int, k: int) -> list[list[int]]:
    """
    >>> generate_all_combinations(n=4, k=2)
    [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    """
    combinations: list[list[int]] = []
    backtrack(
        increment=1,
        total_number=n,
        level=k,
        path=[],
        result_list=combinations,
    )
    return combinations


def print_all_state(print_list: list[list[int]]) -> None:
    """Print each combination on its own line."""
    for combination in print_list:
        print(*combination)


if __name__ == "__main__":
    total_list = generate_all_combinations(5, 3)
    print_all_state(total_list)
