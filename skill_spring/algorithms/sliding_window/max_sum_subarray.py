"""
Maximum Sum Subarray of Size K — Sliding Window Technique
==========================================================
Given an array of integers and a window size k, find the maximum sum
of any contiguous subarray of length k.

Why sliding window?
-------------------
A naive approach checks every subarray → O(n * k).
With a sliding window we maintain a running sum:
  - Add the new right element entering the window
  - Subtract the old left element leaving the window
  → O(n) time, O(1) space

Visual example  (nums=[2, 1, 5, 1, 3, 2], k=3):
  Window        Sum
  [2, 1, 5]     8
  [1, 5, 1]     7
  [5, 1, 3]     9  ← maximum
  [1, 3, 2]     6
  Answer: 9
"""

from __future__ import annotations


def max_sum_subarray(nums: list[int], k: int) -> int:
    """Return the maximum sum of any contiguous subarray of length ``k``.

    Args:
        nums: List of integers (can be negative).
        k:    Window size; must satisfy 1 <= k <= len(nums).

    Returns:
        The maximum subarray sum.

    Raises:
        ValueError: If ``nums`` is empty or ``k`` is out of range.

    Examples:
        >>> max_sum_subarray([2, 1, 5, 1, 3, 2], 3)
        9
        >>> max_sum_subarray([1, 4, 2, 9, 7, 3, 8], 4)
        27
        >>> max_sum_subarray([-1, -3, -5, -2], 2)
        -4
        >>> max_sum_subarray([5], 1)
        5
        >>> max_sum_subarray([1, 2], 0)
        Traceback (most recent call last):
            ...
        ValueError: k must be between 1 and len(nums) (got k=0, len=2)
    """
    n = len(nums)
    if n == 0 or not (1 <= k <= n):
        raise ValueError(
            f"k must be between 1 and len(nums) (got k={k}, len={n})"
        )

    # Build the sum of the first window
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # Slide: add next element, drop leftmost element
    for right in range(k, n):
        window_sum += nums[right] - nums[right - k]
        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum


if __name__ == "__main__":
    test_cases = [
        ([2, 1, 5, 1, 3, 2], 3, 9),
        ([1, 4, 2, 9, 7, 3, 8], 4, 27),
        ([-1, -3, -5, -2], 2, -4),
        ([5], 1, 5),
    ]

    print("===== Max Sum Subarray of Size K (Sliding Window) =====")
    for nums, k, expected in test_cases:
        result = max_sum_subarray(nums, k)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] nums={nums}, k={k} → {result}  (expected {expected})")
    print("=======================================================")
