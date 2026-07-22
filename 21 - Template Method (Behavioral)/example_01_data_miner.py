"""
============================================================
Example: Data Miner / ETL Pipeline
Pattern: Template Method (Behavioral)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You are building an ETL (Extract, Transform, Load) pipeline that 
reads data from different sources (CSV files, APIs), processes it,
and saves it to a database.

The sequence of steps is ALWAYS the same:
1. Extract data.
2. Clean data.
3. [Optional hook: Send notification].
4. Load into database.

By putting this sequence in a Base Class (`mine_data`), we guarantee
every data miner follows the exact same protocol.

KEY INSIGHT:
------------
Notice the Hollywood Principle: "Don't call us, we'll call you."
The `DataMiner` base class is in charge. It calls the subclass 
methods when it needs them. The subclass never calls the base class.

============================================================
"""

from abc import ABC, abstractmethod


# ─── Abstract Class (The Skeleton) ─────────────────────

class DataMiner(ABC):
    """
    The Base Class. It defines the Template Method and the primitive
    steps that subclasses must/can implement.
    """
    
    def mine_data(self, source: str) -> None:
        """
        THE TEMPLATE METHOD.
        This defines the skeleton of the algorithm. It is usually
        NOT overridden by subclasses (in languages with 'final', this
        method would be marked final).
        """
        print(f"\n--- Starting Data Mining for: {source} ---")
        
        # Step 1: Extract (Required)
        raw_data = self.extract(source)
        
        # Step 2: Clean (Required)
        clean_data = self.clean(raw_data)
        
        # Step 3: Hook (Optional)
        self.before_load_hook(clean_data)
        
        # Step 4: Load (Standard implementation in base class)
        self._load_to_database(clean_data)
        
        print("--- Mining Complete ---")
        
    
    # --- Primitive Operations ---
    
    @abstractmethod
    def extract(self, source: str) -> str:
        """Subclasses MUST implement how they extract data."""
        pass
        
    @abstractmethod
    def clean(self, raw_data: str) -> str:
        """Subclasses MUST implement how they clean data."""
        pass
        
    def before_load_hook(self, clean_data: str) -> None:
        """
        A HOOK.
        It has an empty default implementation. Subclasses CAN override 
        it if they want to inject behavior before saving to the DB.
        """
        pass
        
    def _load_to_database(self, data: str) -> None:
        """
        A base operation.
        It is fully implemented in the base class. Subclasses generally
        use this as-is and do not override it.
        """
        print(f"  💾 [Base] Saving '{data}' to central database...")


# ─── Concrete Classes (The Details) ────────────────────

class CSVMiner(DataMiner):
    """Mines data from CSV files."""
    
    def extract(self, source: str) -> str:
        print(f"  📄 [CSV] Opening CSV file {source} and reading rows...")
        return "row1,row2,row3"
        
    def clean(self, raw_data: str) -> str:
        print("  🧹 [CSV] Removing commas and bad rows...")
        return "clean_csv_data"


class APIMiner(DataMiner):
    """Mines data from a JSON API."""
    
    def extract(self, source: str) -> str:
        print(f"  🌐 [API] Making HTTP GET request to {source}...")
        return '{"data": "json_blob"}'
        
    def clean(self, raw_data: str) -> str:
        print("  🧹 [API] Parsing JSON and validating schema...")
        return "clean_json_data"
        
    def before_load_hook(self, clean_data: str) -> None:
        """
        Overriding the hook! We only want to notify slack for API data.
        """
        print("  🪝  [API Hook] Sending Slack notification about new API data!")


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("TEMPLATE METHOD PATTERN - ETL Pipeline")
    print("=" * 60)
    
    # We instantiate the subclasses, but we call the Template Method
    # inherited from the Base class!
    
    csv_miner = CSVMiner()
    csv_miner.mine_data("users_export.csv")
    
    api_miner = APIMiner()
    api_miner.mine_data("https://api.example.com/v1/users")
    
    print("\n✅ Template Method pattern demonstrated successfully!")
