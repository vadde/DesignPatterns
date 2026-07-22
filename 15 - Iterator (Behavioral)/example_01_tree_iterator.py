"""
============================================================
Example: Tree Traversals (DFS vs BFS)
Pattern: Iterator (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have a complex data structure: A Tree representing a company's
management hierarchy.

You want to allow other developers to loop over this tree easily:
`for employee in company_tree:`

But a tree isn't a flat list. Do we go deep first (Depth-First Search)? 
Or level by level (Breadth-First Search)? 

The Iterator pattern allows us to provide multiple ways to traverse 
the exact same data structure, completely hiding the complex algorithms 
from the client.

KEY INSIGHT:
------------
We will implement one iterator the "Hard Way" (using a Class with 
__iter__ and __next__) and one the "Pythonic Way" (using a generator 
with `yield`). Both fulfill the Iterator pattern!

============================================================
"""

from collections import deque
from typing import Any, Generator, Iterator


# ─── Node ──────────────────────────────────────────────

class Node:
    """A node in our tree."""
    def __init__(self, value: str) -> None:
        self.value = value
        self.children: list['Node'] = []
        
    def add(self, child: 'Node') -> None:
        self.children.append(child)


# ─── Iterator 1: The "Class" Way (Breadth-First) ───────

class BreadthFirstIterator(Iterator[Node]):
    """
    A classic class-based iterator.
    Implements BFS (Level Order Traversal) using a queue.
    """
    def __init__(self, root: Node) -> None:
        self._queue = deque([root]) if root else deque()
        
    def __iter__(self) -> Iterator[Node]:
        """Iterators must return themselves."""
        return self
        
    def __next__(self) -> Node:
        """The core logic to get the next element."""
        if not self._queue:
            # This is how Python knows the loop is finished!
            raise StopIteration
            
        current = self._queue.popleft()
        
        # Add children to the queue for later processing
        for child in current.children:
            self._queue.append(child)
            
        return current


# ─── The Collection (Iterable) ─────────────────────────

class CompanyTree:
    """
    The Iterable Collection.
    It holds the data and provides methods to get Iterators.
    """
    def __init__(self, root: Node) -> None:
        self.root = root
        
    def __iter__(self) -> Iterator[Node]:
        """
        Default iteration method (used by `for x in tree:`).
        We'll default to Breadth-First Search using our custom class.
        """
        return BreadthFirstIterator(self.root)
        
    def depth_first(self) -> Generator[Node, None, None]:
        """
        Iterator 2: The "Pythonic" Way (Generators).
        Using `yield` automatically creates an Iterator class behind the scenes!
        """
        if not self.root:
            return
            
        # DFS uses a stack (LIFO)
        stack = [self.root]
        
        while stack:
            current = stack.pop()
            yield current # Pause execution and return the value!
            
            # Add children to stack in reverse order so left is processed first
            for child in reversed(current.children):
                stack.append(child)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("ITERATOR PATTERN - Tree Traversals")
    print("=" * 60)
    
    # 1. Build the Tree
    #       CEO
    #      /   \
    #    VP1   VP2
    #   /   \     \
    # Dev1 Dev2   HR1
    
    ceo = Node("CEO")
    vp1 = Node("VP Engineering")
    vp2 = Node("VP HR")
    dev1 = Node("Dev 1")
    dev2 = Node("Dev 2")
    hr1 = Node("HR 1")
    
    vp1.add(dev1)
    vp1.add(dev2)
    vp2.add(hr1)
    ceo.add(vp1)
    ceo.add(vp2)
    
    company = CompanyTree(ceo)
    
    # 2. Iterate using the Default Iterator (BFS / Level Order)
    print("\n--- Default Iteration (Breadth-First via Class) ---")
    print("Expected: CEO -> VP Eng -> VP HR -> Dev 1 -> Dev 2 -> HR 1")
    for employee in company:
        print(f"  🏢 {employee.value}")
        
    # 3. Iterate using the Alternative Iterator (DFS / Pre-order)
    print("\n--- Alternative Iteration (Depth-First via Generator) ---")
    print("Expected: CEO -> VP Eng -> Dev 1 -> Dev 2 -> VP HR -> HR 1")
    for employee in company.depth_first():
        print(f"  🏢 {employee.value}")
        
    print("\n✅ Iterator pattern demonstrated successfully!")
