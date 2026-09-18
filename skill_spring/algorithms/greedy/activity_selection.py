"""
Activity Selection — Greedy Algorithm
======================================
Given a list of activities with start and end times, select the maximum
number of non-overlapping activities that can be performed by a single
person (or machine).

Greedy choice: always pick the activity with the earliest finish time
that doesn't conflict with the last selected activity.

Why greedy works here?
----------------------
Choosing the activity that finishes earliest leaves the most room for
future activities — a locally optimal choice that is also globally optimal
(provable by an exchange argument).

Time complexity:  O(n log n)  — dominated by sorting on end time
Space complexity: O(n)        — for the result list

Visual example:
    Activities (start, end):
    A=(1,4), B=(3,5), C=(0,6), D=(5,7), E=(3,9), F=(5,9), G=(6,10), H=(8,11)

    Sorted by end:  A(1,4) B(3,5) C(0,6) D(5,7) E(3,9) F(5,9) G(6,10) H(8,11)

    Pick A(1,4) ← earliest end
    Skip B(3,5) ← 3 < 4, overlaps
    Skip C(0,6) ← 0 < 4, overlaps
    Pick D(5,7) ← 5 >= 4, no overlap
    Skip E(3,9) ← 3 < 7, overlaps
    Skip F(5,9) ← 5 < 7, overlaps
    Skip G(6,10) ← 6 < 7, overlaps
    Pick H(8,11) ← 8 >= 7, no overlap

    Result: [A, D, H]  → 3 activities
"""

from __future__ import annotations


def activity_selection(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return the maximum set of non-overlapping activities.

    Each activity is a ``(start, end)`` tuple where ``start < end``.
    Activities that share only an endpoint are considered non-overlapping
    (e.g. one ends at 5 and next starts at 5 is allowed).

    Args:
        activities: List of (start, end) tuples.

    Returns:
        A list of selected (start, end) tuples in order of finish time.

    Examples:
        >>> activity_selection([(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)])
        [(1, 4), (5, 7), (8, 11)]
        >>> activity_selection([(1, 2), (2, 3), (3, 4)])
        [(1, 2), (2, 3), (3, 4)]
        >>> activity_selection([(0, 10), (1, 2), (3, 4)])
        [(1, 2), (3, 4)]
        >>> activity_selection([(5, 9)])
        [(5, 9)]
        >>> activity_selection([])
        []
    """
    if not activities:
        return []

    # Sort by finish time (greedy criterion)
    sorted_activities = sorted(activities, key=lambda act: act[1])

    # Always select the first activity (earliest finish)
    selected = [sorted_activities[0]]
    last_end = sorted_activities[0][1]

    for start, end in sorted_activities[1:]:
        if start >= last_end:  # no overlap — greedy pick
            selected.append((start, end))
            last_end = end

    return selected


if __name__ == "__main__":
    test_cases = [
        (
            [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)],
            [(1, 4), (5, 7), (8, 11)],
        ),
        (
            [(1, 2), (2, 3), (3, 4)],
            [(1, 2), (2, 3), (3, 4)],
        ),
        (
            [(0, 10), (1, 2), (3, 4)],
            [(1, 2), (3, 4)],
        ),
        (
            [(5, 9)],
            [(5, 9)],
        ),
        (
            [],
            [],
        ),
    ]

    print("===== Activity Selection (Greedy) =====")
    for activities, expected in test_cases:
        result = activity_selection(activities)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] activities={activities}")
        print(f"        selected={result}  (expected {expected})")
    print("=======================================")
