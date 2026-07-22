"""
============================================================
Example: Object Adapter (Composition)
Pattern: Adapter (Structural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have a modern data analytics application that expects all
incoming data in JSON format. However, you need to integrate
a legacy third-party library that only exports data in XML.
You cannot change the analytics app (it expects a specific interface)
and you cannot change the 3rd party library (it's closed source).

You create an Adapter that wraps the legacy library, translates
the XML to JSON, and passes it to the analytics app.

KEY INSIGHT:
------------
This is the "Object Adapter" pattern, which uses composition.
The adapter holds a reference to the Adaptee (the legacy object).
This is generally preferred over Class Adapters (inheritance)
because it's more flexible and follows "Favor Composition over Inheritance".

============================================================
"""

from typing import Protocol
import json

# ─── Target (The interface the client expects) ─────────

class JSONProvider(Protocol):
    """The modern interface expected by our client."""
    def get_json_data(self) -> str: ...


# ─── Client (Our modern application) ───────────────────

class AnalyticsApp:
    """A modern app that only speaks JSON."""
    
    def process_data(self, provider: JSONProvider) -> None:
        print("  📊 AnalyticsApp is requesting data...")
        json_data = provider.get_json_data()
        
        # Parse the JSON just to prove it worked
        parsed = json.loads(json_data)
        print(f"  ✅ AnalyticsApp successfully processed: {parsed}")


# ─── Adaptee (The legacy / 3rd party component) ────────

class LegacyXMLAPI:
    """A legacy system that only speaks XML. We cannot modify this class."""
    
    def fetch_xml_records(self) -> str:
        print("  📻 LegacyXMLAPI generating XML...")
        return "<person><name>Alice</name><age>30</age></person>"


# ─── Adapter (The bridge between them) ─────────────────

class XMLToJSONAdapter:
    """
    Object Adapter using COMPOSITION.
    
    Implements the Target interface (JSONProvider) but routes
    the actual work to the wrapped Adaptee (LegacyXMLAPI).
    """
    
    def __init__(self, adaptee: LegacyXMLAPI) -> None:
        self._adaptee = adaptee
        
    def get_json_data(self) -> str:
        """Translate the Adaptee's interface into the Target interface."""
        print("  🔌 Adapter intercepting call to get_json_data()...")
        
        # 1. Call the adaptee
        xml_data = self._adaptee.fetch_xml_records()
        
        # 2. Translate the data (simulating XML parsing)
        print(f"  🔌 Adapter converting XML to JSON: {xml_data}")
        
        # Extremely simplified XML-to-JSON for demonstration purposes
        import re
        name_match = re.search(r"<name>(.*?)</name>", xml_data)
        age_match = re.search(r"<age>(.*?)</age>", xml_data)
        
        data_dict = {
            "name": name_match.group(1) if name_match else "Unknown",
            "age": int(age_match.group(1)) if age_match else 0
        }
        
        # 3. Return what the client expects
        return json.dumps(data_dict)


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("OBJECT ADAPTER (Composition)")
    print("=" * 60)
    
    # 1. We have our client
    app = AnalyticsApp()
    
    # 2. We have the incompatible legacy object
    legacy_api = LegacyXMLAPI()
    
    # app.process_data(legacy_api)  <-- THIS WOULD CRASH (AttributeError)
    
    # 3. We wrap the legacy object in the adapter
    adapter = XMLToJSONAdapter(legacy_api)
    
    # 4. Client happily processes data, unaware of the XML under the hood
    app.process_data(adapter)
    
    print("\n✅ Object Adapter demonstrated successfully!")
