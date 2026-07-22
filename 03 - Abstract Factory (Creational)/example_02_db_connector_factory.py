"""
============================================================
Example: Database Connector Abstract Factory
Pattern: Abstract Factory (Creational)
Framework: SQLAlchemy-inspired
============================================================

REAL-WORLD SCENARIO:
--------------------
An ORM needs to support multiple databases (PostgreSQL, SQLite).
Each database requires matching components: connection, cursor,
and query compiler. Mixing a PostgreSQL connection with a SQLite
compiler would be catastrophic. Abstract Factory ensures all
components come from the same database family.

KEY INSIGHT:
------------
SQLAlchemy's dialect system IS an Abstract Factory. create_engine()
selects the right dialect, which then produces matching connections,
type objects, and SQL compilers.

============================================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ─── Abstract Products ─────────────────────────────

class Connection(ABC):
    @abstractmethod
    def connect(self) -> str: ...
    @abstractmethod
    def close(self) -> str: ...

class Cursor(ABC):
    @abstractmethod
    def execute(self, query: str) -> str: ...

class QueryCompiler(ABC):
    @abstractmethod
    def compile_select(self, table: str, columns: list[str]) -> str: ...
    @abstractmethod
    def compile_insert(self, table: str, data: dict) -> str: ...


# ─── PostgreSQL Family ─────────────────────────────

class PostgresConnection(Connection):
    def connect(self) -> str:
        return "  🐘 Connected to PostgreSQL on port 5432"
    def close(self) -> str:
        return "  🐘 PostgreSQL connection closed"

class PostgresCursor(Cursor):
    def execute(self, query: str) -> str:
        return f"  🐘 PG executing: {query}"

class PostgresCompiler(QueryCompiler):
    def compile_select(self, table: str, columns: list[str]) -> str:
        cols = ", ".join(columns)
        return f'SELECT {cols} FROM "{table}"'  # PG uses double quotes

    def compile_insert(self, table: str, data: dict) -> str:
        cols = ", ".join(data.keys())
        vals = ", ".join(f"'{v}'" for v in data.values())
        return f'INSERT INTO "{table}" ({cols}) VALUES ({vals}) RETURNING id'


# ─── SQLite Family ──────────────────────────────────

class SQLiteConnection(Connection):
    def connect(self) -> str:
        return "  💾 Connected to SQLite (file: ./app.db)"
    def close(self) -> str:
        return "  💾 SQLite connection closed"

class SQLiteCursor(Cursor):
    def execute(self, query: str) -> str:
        return f"  💾 SQLite executing: {query}"

class SQLiteCompiler(QueryCompiler):
    def compile_select(self, table: str, columns: list[str]) -> str:
        cols = ", ".join(columns)
        return f"SELECT {cols} FROM [{table}]"  # SQLite uses brackets

    def compile_insert(self, table: str, data: dict) -> str:
        cols = ", ".join(data.keys())
        vals = ", ".join(f"'{v}'" for v in data.values())
        return f"INSERT INTO [{table}] ({cols}) VALUES ({vals})"


# ─── Abstract Factory ──────────────────────────────

class DatabaseFactory(ABC):
    """Abstract factory for database component families."""

    @abstractmethod
    def create_connection(self) -> Connection: ...

    @abstractmethod
    def create_cursor(self) -> Cursor: ...

    @abstractmethod
    def create_compiler(self) -> QueryCompiler: ...


class PostgresFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return PostgresConnection()
    def create_cursor(self) -> Cursor:
        return PostgresCursor()
    def create_compiler(self) -> QueryCompiler:
        return PostgresCompiler()


class SQLiteFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return SQLiteConnection()
    def create_cursor(self) -> Cursor:
        return SQLiteCursor()
    def create_compiler(self) -> QueryCompiler:
        return SQLiteCompiler()


# ─── Engine (like SQLAlchemy's create_engine) ──────

def create_engine(url: str) -> DatabaseFactory:
    """
    Simulates SQLAlchemy's create_engine().

    The URL determines which abstract factory (dialect) to use.
    All components produced by that factory are guaranteed to
    be compatible with each other.
    """
    scheme = url.split("://")[0].lower()
    factories: dict[str, type[DatabaseFactory]] = {
        "postgresql": PostgresFactory,
        "postgres": PostgresFactory,
        "sqlite": SQLiteFactory,
    }
    if scheme not in factories:
        raise ValueError(f"Unsupported database: {scheme}")
    return factories[scheme]()


# ─── ORM-like Client ───────────────────────────────

def run_queries(factory: DatabaseFactory) -> None:
    """
    Client code — doesn't know if it's talking to PG or SQLite.
    All components come from the same family (abstract factory).
    """
    conn = factory.create_connection()
    cursor = factory.create_cursor()
    compiler = factory.create_compiler()

    print(conn.connect())

    # Compile and execute a SELECT
    select_sql = compiler.compile_select("users", ["id", "name", "email"])
    print(cursor.execute(select_sql))

    # Compile and execute an INSERT
    insert_sql = compiler.compile_insert("users", {"name": "Alice", "email": "alice@example.com"})
    print(cursor.execute(insert_sql))

    print(conn.close())


# ─── Demo ──────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("ABSTRACT FACTORY — Database Connector (SQLAlchemy-style)")
    print("=" * 60)

    for url in ["postgresql://localhost/myapp", "sqlite:///./app.db"]:
        print(f"\n  ═══ Engine: {url} ═══")
        engine = create_engine(url)
        run_queries(engine)

    # The SAME run_queries() function works with both databases
    # because it only depends on the abstract factory interface
    assert isinstance(create_engine("postgresql://x"), PostgresFactory)
    assert isinstance(create_engine("sqlite:///x"), SQLiteFactory)

    print("\n✅ Database Abstract Factory demonstrated successfully!")
