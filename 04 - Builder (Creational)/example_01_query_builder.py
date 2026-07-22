"""
============================================================
Example: SQL Query Builder with Fluent API
Pattern: Builder (Creational)
Framework: Pure Python (SQLAlchemy-inspired)
============================================================

REAL-WORLD SCENARIO:
--------------------
Building SQL queries programmatically. A query has many optional
parts (WHERE, ORDER BY, LIMIT, JOIN, GROUP BY). Using a builder
with method chaining makes construction readable and prevents
SQL injection through parameterized values.

KEY INSIGHT:
------------
Each method returns `self`, enabling fluent chaining:
QueryBuilder("users").select("name").where("active=true").limit(10).build()

============================================================
"""

from dataclasses import dataclass, field
from typing import Self


@dataclass
class Query:
    """The product — an immutable SQL query."""
    sql: str
    params: dict[str, object] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"SQL: {self.sql}\nParams: {self.params}"


class QueryBuilder:
    """
    Fluent SQL query builder.

    Each method returns `self` (using `Self` type hint from Python 3.11+)
    to enable method chaining. The build() method produces the final Query.
    """

    def __init__(self, table: str) -> None:
        self._table = table
        self._columns: list[str] = ["*"]
        self._conditions: list[str] = []
        self._order: list[str] = []
        self._limit: int | None = None
        self._offset: int | None = None
        self._joins: list[str] = []
        self._group_by: list[str] = []
        self._params: dict[str, object] = {}

    def select(self, *columns: str) -> Self:
        """Set columns to select."""
        self._columns = list(columns)
        return self

    def where(self, condition: str, **params: object) -> Self:
        """Add a WHERE condition with optional named parameters."""
        self._conditions.append(condition)
        self._params.update(params)
        return self

    def join(self, table: str, on: str) -> Self:
        """Add a JOIN clause."""
        self._joins.append(f"JOIN {table} ON {on}")
        return self

    def order_by(self, column: str, desc: bool = False) -> Self:
        """Add ORDER BY clause."""
        direction = "DESC" if desc else "ASC"
        self._order.append(f"{column} {direction}")
        return self

    def group_by(self, *columns: str) -> Self:
        """Add GROUP BY clause."""
        self._group_by = list(columns)
        return self

    def limit(self, n: int) -> Self:
        """Set LIMIT."""
        self._limit = n
        return self

    def offset(self, n: int) -> Self:
        """Set OFFSET."""
        self._offset = n
        return self

    def build(self) -> Query:
        """Assemble and return the final Query product."""
        parts = [f"SELECT {', '.join(self._columns)}"]
        parts.append(f"FROM {self._table}")

        if self._joins:
            parts.extend(self._joins)
        if self._conditions:
            parts.append(f"WHERE {' AND '.join(self._conditions)}")
        if self._group_by:
            parts.append(f"GROUP BY {', '.join(self._group_by)}")
        if self._order:
            parts.append(f"ORDER BY {', '.join(self._order)}")
        if self._limit is not None:
            parts.append(f"LIMIT {self._limit}")
        if self._offset is not None:
            parts.append(f"OFFSET {self._offset}")

        return Query(sql="\n".join(parts), params=self._params)


# ─── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("BUILDER — SQL Query Builder with Fluent API")
    print("=" * 60)

    # Simple query
    print("\n  --- Simple SELECT ---")
    q1 = QueryBuilder("users").select("id", "name", "email").build()
    print(f"  {q1.sql}")

    # Complex query with all options
    print("\n  --- Complex Query ---")
    q2 = (
        QueryBuilder("orders")
        .select("orders.id", "users.name", "orders.total")
        .join("users", "users.id = orders.user_id")
        .where("orders.status = :status", status="completed")
        .where("orders.total > :min_total", min_total=100)
        .order_by("orders.total", desc=True)
        .limit(20)
        .offset(0)
        .build()
    )
    print(f"  {q2}")

    # Aggregation query
    print("\n  --- Aggregation ---")
    q3 = (
        QueryBuilder("products")
        .select("category", "COUNT(*) as count", "AVG(price) as avg_price")
        .where("active = true")
        .group_by("category")
        .order_by("count", desc=True)
        .limit(5)
        .build()
    )
    print(f"  {q3.sql}")

    # Verify builder produces correct SQL
    assert "SELECT id, name, email" in q1.sql
    assert "JOIN users ON" in q2.sql
    assert "WHERE" in q2.sql
    assert "LIMIT 20" in q2.sql
    assert q2.params == {"status": "completed", "min_total": 100}
    assert "GROUP BY category" in q3.sql

    print("\n✅ Query Builder demonstrated successfully!")
