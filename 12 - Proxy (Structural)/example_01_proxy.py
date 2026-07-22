"""
============================================================
Example: Virtual & Protection Proxy
Pattern: Proxy (Structural)
Framework: Pure Python
============================================================

REAL-WORLD SCENARIO:
--------------------
You have a highly sensitive, very resource-intensive `DatabaseDownloader`
object. 

1. It takes 3 seconds just to instantiate (establish connection).
2. It contains sensitive financial data.

We want to solve two problems:
- Don't establish the connection (instantiate) unless the user ACTUALLY
  requests data (Virtual Proxy / Lazy Loading).
- Don't allow the request if the user doesn't have the "admin" role
  (Protection Proxy).

KEY INSIGHT:
------------
The Proxy implements the exact same interface (`DownloaderProtocol`)
as the real object. The client has no idea it's talking to a proxy.

============================================================
"""

from typing import Protocol
import time

# ─── Subject (The Interface) ───────────────────────────

class DownloaderProtocol(Protocol):
    """The common interface for both the Real Subject and the Proxy."""
    def download_financial_report(self, user_role: str) -> str: ...


# ─── Real Subject (The Heavy, Sensitive Object) ────────

class RealDatabaseDownloader:
    """
    The RealSubject.
    It takes a long time to initialize and does the actual heavy lifting.
    """
    def __init__(self) -> None:
        print("  [RealSubject] ⏳ Initializing database connection (this is slow)...")
        time.sleep(1.5)  # Simulated heavy init
        print("  [RealSubject] ✅ Connection established!")
        
    def download_financial_report(self, user_role: str) -> str:
        # Note: The real subject doesn't check permissions.
        # It assumes whoever calls it is allowed. That's the Proxy's job!
        print("  [RealSubject] 💾 Downloading 500MB financial report...")
        return "FINANCIAL_REPORT_Q3_2026.pdf"


# ─── Proxy (The Gatekeeper) ────────────────────────────

class DatabaseProxy:
    """
    The Proxy.
    It acts as BOTH a Virtual Proxy (lazy loading) AND a Protection Proxy (security).
    """
    def __init__(self) -> None:
        # We DO NOT instantiate the real subject yet! (Virtual Proxy)
        self._real_downloader: RealDatabaseDownloader | None = None
        
    def check_access(self, role: str) -> bool:
        """Protection Proxy logic."""
        print(f"  [Proxy] Checking access for role '{role}'...")
        return role == "admin"
        
    def download_financial_report(self, user_role: str) -> str:
        # 1. Protection Proxy: Check permissions first
        if not self.check_access(user_role):
            print(f"  [Proxy] ❌ Access DENIED for role '{user_role}'.")
            return "ACCESS_DENIED"
            
        print(f"  [Proxy] 🔓 Access GRANTED for role '{user_role}'.")
        
        # 2. Virtual Proxy: Lazy-load the real subject
        if self._real_downloader is None:
            print("  [Proxy] First request! Creating the RealSubject now...")
            self._real_downloader = RealDatabaseDownloader()
        else:
            print("  [Proxy] RealSubject already exists. Using cached instance.")
            
        # 3. Delegation: Pass the request to the real subject
        return self._real_downloader.download_financial_report(user_role)


# ─── Client ────────────────────────────────────────────

def client_code(downloader: DownloaderProtocol, role: str) -> None:
    """
    The client operates against the interface.
    It doesn't know if 'downloader' is the RealSubject or the Proxy.
    """
    print(f"\n--- Client requesting report as '{role}' ---")
    result = downloader.download_financial_report(role)
    print(f"Client received: {result}")


# ─── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("PROXY PATTERN - Virtual & Protection Proxy")
    print("=" * 60)
    
    # Instantiate the proxy. Notice how FAST this is!
    # The expensive DB connection is NOT made yet.
    print("Instantiating proxy...")
    proxy = DatabaseProxy()
    print("Proxy instantiated (almost instantly).\n")
    
    # 1. Try as a guest (Protection Proxy blocks it)
    # The real subject is NEVER created! We saved 1.5 seconds.
    client_code(proxy, "guest")
    
    # 2. Try as an admin (Protection Proxy allows it)
    # The Virtual Proxy sees no real subject exists, so it creates it now.
    client_code(proxy, "admin")
    
    # 3. Try as an admin again
    # The Virtual Proxy reuses the existing real subject. Very fast!
    client_code(proxy, "admin")
    
    print("\n✅ Proxy pattern demonstrated successfully!")
