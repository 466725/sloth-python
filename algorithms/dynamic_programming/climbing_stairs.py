"""Count distinct ways to climb stairs using 1-step or 2-step moves.

https://www.jointaro.com/interviews/questions/climbing-stairs/?src=taro75

This uses an iterative dynamic-programming approach with O(1) extra space:
ways(step) = ways(step - 1) + ways(step - 2)

Examples:
	>>> climb_stairs(0)
	1
	>>> climb_stairs(2)
	2
	>>> climb_stairs(3)
	3
"""


def climb_stairs(steps: int) -> int:
    """Return the number of distinct ways to reach the top of ``steps`` stairs.

    For ``steps <= 1``, there is exactly one way (do nothing or one single step).
    """
    if steps < 0:
        raise ValueError("steps must be >= 0")

    if steps <= 1:
        return 1

    # Rolling DP (Fibonacci-like): current = previous_one + previous_two
    prev_two = 1
    prev_one = 1

    for _ in range(2, steps + 1):
        current = prev_one + prev_two
        prev_two = prev_one
        prev_one = current

    return prev_one


if __name__ == "__main__":
    test_cases = [0, 1, 2, 3, 4, 5, 8, 10, 20, 40]
    print("===== Climbing Stairs Tests =====")
    for n in test_cases:
        result = climb_stairs(n)
        print(f"n = {n} -> Ways = {result}")
    print("=================================")
