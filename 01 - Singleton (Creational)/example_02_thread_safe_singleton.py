"""
============================================================
Example: Thread-Safe Singleton with Double-Checked Locking
Pattern: Singleton (Creational)
Framework: Pure Python (threading)
============================================================

REAL-WORLD SCENARIO:
--------------------
A connection pool manager in a multi-threaded web server. Multiple
request threads may try to create the pool simultaneously on startup.
Without thread safety, two pools could be created — wasting resources
and causing subtle bugs.

PATTERN PARTICIPANTS IN THIS EXAMPLE:
--------------------------------------
- Singleton → ConnectionPool (thread-safe __new__)
- _lock → threading.Lock (guards first creation)
- _instance → the single pool object

KEY INSIGHT:
------------
Double-checked locking: the outer check avoids the lock overhead on
every call (fast path), while the inner check prevents race conditions
during first creation (safe path).

============================================================
"""

import threading
import time


class ConnectionPool:
    """
    Thread-safe Singleton connection pool.

    Uses double-checked locking to minimize lock overhead:
    - Outer check: fast path — no lock acquired if instance exists
    - Inner check: safe path — prevents two threads from both creating
    """

    _instance: "ConnectionPool | None" = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, pool_size: int = 5) -> "ConnectionPool":
        if cls._instance is None:                  # Fast path (no lock)
            with cls._lock:                         # Acquire lock
                if cls._instance is None:           # Double-check (safe path)
                    instance = super().__new__(cls)
                    instance._initialized = False
                    cls._instance = instance
        return cls._instance

    def __init__(self, pool_size: int = 5) -> None:
        if self._initialized:
            return

        # Simulate expensive pool creation
        self.pool_size = pool_size
        self.connections: list[str] = [
            f"conn_{i}" for i in range(pool_size)
        ]
        self._initialized = True
        print(f"  🔗 ConnectionPool created with {pool_size} connections (thread: {threading.current_thread().name})")

    def get_connection(self) -> str:
        """Get a connection from the pool."""
        if self.connections:
            return self.connections.pop()
        raise RuntimeError("No connections available!")

    def return_connection(self, conn: str) -> None:
        """Return a connection to the pool."""
        self.connections.append(conn)

    @classmethod
    def _reset(cls) -> None:
        """For testing only."""
        cls._instance = None

    def __repr__(self) -> str:
        return f"ConnectionPool(size={self.pool_size}, available={len(self.connections)})"


def worker(worker_id: int, results: dict[int, int]) -> None:
    """Simulate a worker thread accessing the singleton."""
    pool = ConnectionPool(pool_size=10)
    results[worker_id] = id(pool)
    # Small sleep to increase chance of race condition in naive impl
    time.sleep(0.01)


# ─── Usage / Demo ──────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("THREAD-SAFE SINGLETON — Double-Checked Locking")
    print("=" * 60)

    # Launch 10 threads simultaneously — all should get the SAME instance
    results: dict[int, int] = {}
    threads = [
        threading.Thread(target=worker, args=(i, results), name=f"Worker-{i}")
        for i in range(10)
    ]

    print("\n  Launching 10 threads simultaneously...")
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Verify ALL threads got the same instance
    unique_ids = set(results.values())
    print(f"\n  Thread results (object IDs): {list(results.values())[:5]}...")
    print(f"  Unique instances created: {len(unique_ids)}")
    assert len(unique_ids) == 1, f"Thread safety violated! Got {len(unique_ids)} instances"
    print(f"  All 10 threads share the same instance ✅")

    # Verify the pool works
    pool = ConnectionPool()
    print(f"\n  Pool state: {pool}")
    conn = pool.get_connection()
    print(f"  Got connection: {conn}")
    pool.return_connection(conn)
    print(f"  Returned: {conn}")

    print("\n✅ Thread-Safe Singleton demonstrated successfully!")
