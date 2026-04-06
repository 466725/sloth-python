"""
Two Sum on a Sorted Array — Two-Pointer Technique
==================================================
Given a sorted (ascending) list of integers and a target value, find the
indices (1-based) of the two numbers that add up to the target.

Why two pointers?
-----------------
Because the array is sorted we can use a left pointer (start) and a right
pointer (end) and move them intelligently:
  - sum < target → move left pointer right  (need a bigger number)
  - sum > target → move right pointer left  (need a smaller number)
  - sum == target → found the pair

Time complexity:  O(n)   — single pass
Space complexity: O(1)   — no extra data structure

Example:
    numbers = [2, 7, 11, 15], target = 9
    left=0 (2), right=3 (15) → sum=17 > 9 → move right
    left=0 (2), right=2 (11) → sum=13 > 9 → move right
    left=0 (2), right=1 (7)  → sum=9  == 9 → return [1, 2]
"""

from __future__ import annotations


def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    """Return 1-based indices [left, right] of the two numbers that sum to target.

    The input list must be sorted in non-decreasing order.
    Raises ValueError if no valid pair exists.

    Args:
        numbers: A sorted list of integers.
        target:  The desired sum.

    Returns:
        A list with two 1-based indices, e.g. [1, 2].

    Examples:
        >>> two_sum_sorted([2, 7, 11, 15], 9)
        [1, 2]
        >>> two_sum_sorted([2, 3, 4], 6)
        [1, 3]
        >>> two_sum_sorted([-3, -1, 0, 2, 4], 1)
        [1, 5]
        >>> two_sum_sorted([1, 2], 3)
        [1, 2]
        >>> two_sum_sorted([1, 2, 3], 10)
        Traceback (most recent call last):
            ...
        ValueError: No two-sum pair found for target=10
    """
    left = 0
    right = len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == target:
            return [left + 1, right + 1]  # convert to 1-based indices
        elif current_sum < target:
            left += 1  # need a larger value
        else:
            right -= 1  # need a smaller value

    raise ValueError(f"No two-sum pair found for target={target}")


if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9, [1, 2]),
        ([2, 3, 4], 6, [1, 3]),
        ([-3, -1, 0, 2, 4], 1, [1, 5]),
        ([1, 2], 3, [1, 2]),
    ]

    print("===== Two Sum Sorted (Two Pointers) =====")
    for numbers, target, expected in test_cases:
        result = two_sum_sorted(numbers, target)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] numbers={numbers}, target={target} → {result}")
    print("==========================================")
