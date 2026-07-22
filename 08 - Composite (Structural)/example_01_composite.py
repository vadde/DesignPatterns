"""
============================================================
Example: File System (Files and Directories)
Pattern: Composite (Structural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
A file system consists of Files (Leaves) and Directories (Composites).
A Directory can contain Files AND other Directories.
If you ask for the size of a File, it returns its size in bytes.
If you ask for the size of a Directory, it recursively asks all its
children for their sizes and adds them up.

KEY INSIGHT:
------------
The client just calls `get_size()` or `render()`. It does not need
to check `if isinstance(child, Directory)`. The polymorphism handles
the recursion naturally.

============================================================
"""

from typing import Protocol


# ─── Component Interface ───────────────────────────────

class FileSystemNode(Protocol):
    """The Component interface that both Leaves and Composites implement."""
    
    @property
    def name(self) -> str: ...
    
    def get_size(self) -> int:
        """Returns size in bytes."""
        ...
        
    def render(self, depth: int = 0) -> str:
        """Renders the node as a string for tree visualization."""
        ...


# ─── Leaf ──────────────────────────────────────────────

class File:
    """Leaf node. Represents an actual file with a size. Has no children."""
    
    def __init__(self, name: str, size: int) -> None:
        self._name = name
        self._size = size
        
    @property
    def name(self) -> str:
        return self._name
        
    def get_size(self) -> int:
        return self._size
        
    def render(self, depth: int = 0) -> str:
        indent = "  " * depth
        return f"{indent}📄 {self.name} ({self.get_size()} bytes)"


# ─── Composite ─────────────────────────────────────────

class Directory:
    """
    Composite node. Contains children (which can be Files or other Directories).
    Routes calls to its children.
    """
    
    def __init__(self, name: str) -> None:
        self._name = name
        self._children: list[FileSystemNode] = []
        
    @property
    def name(self) -> str:
        return self._name
        
    def add(self, node: FileSystemNode) -> None:
        self._children.append(node)
        
    def remove(self, node: FileSystemNode) -> None:
        self._children.remove(node)
        
    def get_size(self) -> int:
        """
        Recursively calculates the size of the directory.
        Notice there is NO type checking (isinstance). It just calls get_size()!
        """
        return sum(child.get_size() for child in self._children)
        
    def render(self, depth: int = 0) -> str:
        """Recursively renders the directory tree."""
        indent = "  " * depth
        lines = [f"{indent}📁 {self.name}/ (Total: {self.get_size()} bytes)"]
        for child in self._children:
            lines.append(child.render(depth + 1))
        return "\n".join(lines)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("COMPOSITE PATTERN - File System")
    print("=" * 60)
    
    # 1. Create Leaves (Files)
    file1 = File("readme.md", 1024)
    file2 = File("logo.png", 2048)
    file3 = File("script.py", 512)
    file4 = File("secret_key.pem", 256)
    
    # 2. Create Composites (Directories) and build the tree
    root = Directory("root")
    
    docs = Directory("docs")
    docs.add(file1)
    docs.add(file2)
    
    src = Directory("src")
    src.add(file3)
    
    # We can put a directory inside a directory!
    hidden = Directory(".hidden")
    hidden.add(file4)
    src.add(hidden)
    
    # Add directories to root
    root.add(docs)
    root.add(src)
    
    # 3. Client interacts with the tree
    print("\n  [Rendering the entire File System Tree]")
    print(root.render())
    
    print("\n  [Client interacting with individual nodes vs the root]")
    print(f"  Size of {file3.name}: {file3.get_size()} bytes")
    print(f"  Size of {docs.name} directory: {docs.get_size()} bytes")
    print(f"  Size of entire {root.name} directory: {root.get_size()} bytes")
    
    print("\n✅ Composite pattern demonstrated successfully!")
