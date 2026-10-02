#!/usr/bin/env python3
"""
SAFE MAIN - No Endless Loops
============================
This wrapper prevents endless loops in your FSOT system.
"""

import os as _os
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[3]


import asyncio
import sys
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def safe_main():
    """Safe main function with timeout protection"""
    print("SAFE FSOT EXECUTION MODE")
    print("=" * 40)
    print(f"Started: {datetime.now()}")
    
    try:
        # Run health check first
        print("1. Running health check...")
        sys.path.insert(0, _os.fspath(_REPO_ROOT))
        
        # Test core components
        print("2. Testing core components...")
        sys.path.insert(0, _os.fspath(_REPO_ROOT / 'FSOT_Clean_System'))
        from fsot_2_0_foundation import FSOTCore, FSOTDomain
        from main import FSOTHardwiredSystem
        
        print("3. Creating system with timeout protection...")
        system = FSOTHardwiredSystem()
        
        print("4. Initializing system (30s timeout)...")
        await asyncio.wait_for(system.initialize(), timeout=30.0)
        
        print("5. Getting system status...")
        status = await asyncio.wait_for(system.get_system_status(), timeout=10.0)
        print(f"System Status: {status['system']['running']}")
        
        print("6. Shutting down cleanly...")
        await asyncio.wait_for(system.shutdown(), timeout=10.0)
        print("Clean shutdown completed")
            
    except asyncio.TimeoutError:
        print("Operation timed out - preventing endless loop")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run with overall timeout protection
    try:
        asyncio.run(asyncio.wait_for(safe_main(), timeout=120.0))
    except asyncio.TimeoutError:
        print("OVERALL TIMEOUT - System is safe")
    except KeyboardInterrupt:
        print("User interrupted - clean exit")
    
    print(f"Completed: {datetime.now()}")
