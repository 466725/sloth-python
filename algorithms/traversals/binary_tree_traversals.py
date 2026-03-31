"""
This is pure Python implementation of binary tree traversal algorithms.
"""

from __future__ import annotations

import queue


class TreeNode:
    def __init__(self, data: int):
        self.data = data
        self.right: TreeNode | None = None
        self.left: TreeNode | None = None


def build_tree() -> TreeNode | None:
    print("\n********Press N to stop entering at any point of time********\n")
    check = input("Enter the value of the root node: ").strip().lower() or "n"
    if check == "n":
        return None
    q: queue.Queue[TreeNode] = queue.Queue()
    tree_node = TreeNode(int(check))
    q.put(tree_node)
    while not q.empty():
        node_found = q.get()
        msg = "Enter the left node of %s: " % node_found.data
        check = input(msg).strip().lower() or "n"
        if check == "n":
            return tree_node
        left_node = TreeNode(int(check))
        node_found.left = left_node
        q.put(left_node)
        msg = "Enter the right node of %s: " % node_found.data
        check = input(msg).strip().lower() or "n"
        if check == "n":
            return tree_node
        right_node = TreeNode(int(check))
        node_found.right = right_node
        q.put(right_node)
    return tree_node


def pre_order(root: TreeNode | None) -> None:
    if not isinstance(root, TreeNode) or not root:
        return
    print(root.data, end=" ")
    pre_order(root.left)
    pre_order(root.right)


def in_order(root: TreeNode | None) -> None:
    if not isinstance(root, TreeNode) or not root:
        return
    in_order(root.left)
    print(root.data, end=" ")
    in_order(root.right)


def post_order(root: TreeNode | None) -> None:
    if not isinstance(root, TreeNode) or not root:
        return
    post_order(root.left)
    post_order(root.right)
    print(root.data, end=" ")


def level_order(root: TreeNode | None) -> None:
    if not isinstance(root, TreeNode) or not root:
        return
    q: queue.Queue[TreeNode] = queue.Queue()
    q.put(root)
    while not q.empty():
        node_dequeued = q.get()
        print(node_dequeued.data, end=" ")
        if node_dequeued.left:
            q.put(node_dequeued.left)
        if node_dequeued.right:
            q.put(node_dequeued.right)


def level_order_actual(root: TreeNode | None) -> None:
    if not isinstance(root, TreeNode) or not root:
        return
    q: queue.Queue[TreeNode] = queue.Queue()
    q.put(root)
    while not q.empty():
        next_level_nodes: list[TreeNode] = []
        while not q.empty():
            node_dequeued = q.get()
            print(node_dequeued.data, end=" ")
            if node_dequeued.left:
                next_level_nodes.append(node_dequeued.left)
            if node_dequeued.right:
                next_level_nodes.append(node_dequeued.right)
        print()
        for child in next_level_nodes:
            q.put(child)


# iteration version
def pre_order_iter(root: TreeNode | None) -> None:
    if not isinstance(root, TreeNode) or not root:
        return
    stack: list[TreeNode] = []
    current: TreeNode | None = root
    while current or stack:
        while current:  # start from root node, find its left child
            print(current.data, end=" ")
            stack.append(current)
            current = current.left
        # end of while means current node doesn't have left child
        current = stack.pop()
        # start to traverse its right child
        current = current.right


def in_order_iter(root: TreeNode | None) -> None:
    if not isinstance(root, TreeNode) or not root:
        return
    stack: list[TreeNode] = []
    current: TreeNode | None = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        print(current.data, end=" ")
        current = current.right


def post_order_iter(root: TreeNode | None) -> None:
    if not isinstance(root, TreeNode) or not root:
        return
    stack1: list[TreeNode] = []
    stack2: list[TreeNode] = []
    stack1.append(root)
    while stack1:  # to find the reversed order of post order, store it in stack2
        current = stack1.pop()
        if current.left:
            stack1.append(current.left)
        if current.right:
            stack1.append(current.right)
        stack2.append(current)
    while stack2:  # pop up from stack2 will be the post order
        print(stack2.pop().data, end=" ")


def prompt(s: str = "", width=50, char="*") -> str:
    if not s:
        return "\n" + width * char
    left, extra = divmod(width - len(s) - 2, 2)
    return f"{left * char} {s} {(left + extra) * char}"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(prompt("Binary Tree Traversals"))

    root = build_tree()
    print(prompt("Pre Order Traversal"))
    pre_order(root)
    print(prompt() + "\n")

    print(prompt("In Order Traversal"))
    in_order(root)
    print(prompt() + "\n")

    print(prompt("Post Order Traversal"))
    post_order(root)
    print(prompt() + "\n")

    print(prompt("Level Order Traversal"))
    level_order(root)
    print(prompt() + "\n")

    print(prompt("Actual Level Order Traversal"))
    level_order_actual(root)
    print("*" * 50 + "\n")

    print(prompt("Pre Order Traversal - Iteration Version"))
    pre_order_iter(root)
    print(prompt() + "\n")

    print(prompt("In Order Traversal - Iteration Version"))
    in_order_iter(root)
    print(prompt() + "\n")

    print(prompt("Post Order Traversal - Iteration Version"))
    post_order_iter(root)
    print(prompt())
