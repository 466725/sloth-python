"""
In this problem, we want to determine all possible combinations of k
numbers out of 1 ... n. We use backtracking to solve this problem.
Time complexity: O(C(n,k)) which is O(n choose k) = O((n!/(k! * (n - k)!)))
"""


def create_all_state(
        increment: int,
        total_number: int,
        level: int,
        current_list: list[int],
        result_list: list[list[int]],
) -> None:
    """Build combinations recursively using backtracking.

    Args:
        increment: Next candidate value to consider.
        total_number: Upper bound of the source range [1.n].
        level: Number of remaining values needed to complete a combination.
        current_list: Current in-progress combination.
        result_list: Collector for all completed combinations.
    """
    if level == 0:
        result_list.append(current_list[:])
        return

    for i in range(increment, total_number - level + 2):
        current_list.append(i)
        create_all_state(i + 1, total_number, level - 1, current_list, result_list)
        current_list.pop()


def generate_all_combinations(n: int, k: int) -> list[list[int]]:
    """
    >>> generate_all_combinations(n=4, k=2)
    [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    """
    combinations: list[list[int]] = []
    create_all_state(
        increment=1,
        total_number=n,
        level=k,
        current_list=[],
        result_list=combinations,
    )
    return combinations


def print_all_state(print_list: list[list[int]]) -> None:
    """Print each combination on its own line."""
    for combination in print_list:
        print(*combination)


if __name__ == "__main__":
    total_list = generate_all_combinations(4, 2)
    print_all_state(total_list)
