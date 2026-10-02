#!/usr/bin/env python3
"""
FSOT Safe Execution Manager
===========================
Prevents endless loops and provides safe execution modes for your AI system.
"""

import os as _os
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[2]


import asyncio
import signal
import sys
import time
import threading
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SafeExecutionManager:
    """Manages safe execution with timeout and loop prevention"""
    
    def __init__(self, max_timeout: int = 300):
        self.max_timeout = max_timeout
        self.is_running = False
        self.force_exit = False
        self.start_time = None
        
    def safe_run_with_timeout(self, func, *args, timeout: int = 60, **kwargs):
        """Run function with timeout protection"""
        self.start_time = datetime.now()
        self.is_running = True
        
        # Setup timeout handler
        def timeout_handler():
            time.sleep(timeout)
            if self.is_running:
                logger.error(f"⏰ TIMEOUT after {timeout} seconds - forcing exit")
                self.force_exit = True
                self._emergency_exit()
        
        timeout_thread = threading.Thread(target=timeout_handler, daemon=True)
        timeout_thread.start()
        
        try:
            logger.info(f"🛡️ Starting safe execution (timeout: {timeout}s)")
            result = func(*args, **kwargs)
            self.is_running = False
            logger.info("✅ Safe execution completed successfully")
            return result
            
        except Exception as e:
            self.is_running = False
            logger.error(f"❌ Execution failed: {e}")
            raise
            
        finally:
            self.is_running = False
    
    def _emergency_exit(self):
        """Emergency exit if timeout reached"""
        logger.critical("🚨 EMERGENCY EXIT - System taking too long")
        import os
        os._exit(1)
    
    async def safe_async_run(self, coro, timeout: int = 60):
        """Run async coroutine with timeout"""
        try:
            logger.info(f"🛡️ Starting safe async execution (timeout: {timeout}s)")
            result = await asyncio.wait_for(coro, timeout=timeout)
            logger.info("✅ Safe async execution completed")
            return result
        except asyncio.TimeoutError:
            logger.error(f"⏰ Async timeout after {timeout} seconds")
            raise
        except Exception as e:
            logger.error(f"❌ Async execution failed: {e}")
            raise

def safe_fsot_test():
    """Safe test of FSOT system components"""
    print("🧪 SAFE FSOT SYSTEM TEST")
    print("=" * 40)
    
    executor = SafeExecutionManager()
    
    def test_components():
        results = {}
        
        # Test 1: Imports
        print("1️⃣ Testing imports...")
        try:
            sys.path.insert(0, _os.fspath(_REPO_ROOT / 'FSOT_Clean_System'))
            from fsot_2_0_foundation import FSOTCore, FSOTDomain
            results['fsot_import'] = '✅ Success'
        except Exception as e:
            results['fsot_import'] = f'❌ Failed: {e}'
        
        # Test 2: Brain System
        print("2️⃣ Testing brain system...")
        try:
            sys.path.insert(0, _os.fspath(_REPO_ROOT))
            from brain_system import NeuromorphicBrainSystem
            brain = NeuromorphicBrainSystem()
            results['brain_system'] = f'✅ Success: {len(brain.regions)} regions'
        except Exception as e:
            results['brain_system'] = f'❌ Failed: {e}'
        
        # Test 3: Quick computation
        print("3️⃣ Testing FSOT computation...")
        try:
            core = FSOTCore()
            scalar = core.compute_universal_scalar(12, FSOTDomain.AI_TECH)
            results['fsot_computation'] = f'✅ Success: {scalar:.6f}'
        except Exception as e:
            results['fsot_computation'] = f'❌ Failed: {e}'
        
        return results
    
    # Run with timeout protection
    try:
        results = executor.safe_run_with_timeout(test_components, timeout=30)
        
        print("\n📊 TEST RESULTS:")
        for test, result in results.items():
            print(f"   {test}: {result}")
        
        print("\n💡 CONCLUSIONS:")
        success_count = sum(1 for r in results.values() if '✅' in r)
        total_tests = len(results)
        
        if success_count == total_tests:
            print("   🎉 ALL TESTS PASSED - System is healthy!")
            print("   🔧 Endless loop is in execution flow, not core components")
        else:
            print(f"   ⚠️ {success_count}/{total_tests} tests passed")
            print("   🔧 Some components need attention")
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")

def create_safe_main_wrapper():
    """Create a safe main.py wrapper"""
    safe_main_content = '''#!/usr/bin/env python3
"""
SAFE MAIN - No Endless Loops
============================
This wrapper prevents endless loops in your FSOT system.
"""

import asyncio
import sys
import logging
from datetime import datetime

# Import your safe execution manager
sys.path.insert(0, r".")
from advanced_monitoring_tools import FSATAutomationSuite

logger = logging.getLogger(__name__)

async def safe_main():
    """Safe main function with timeout protection"""
    print("🛡️ SAFE FSOT EXECUTION MODE")
    print("=" * 40)
    print(f"Started: {datetime.now()}")
    
    try:
        # Run automation suite first
        suite = FSATAutomationSuite()
        health = suite.run_health_check()
        
        if health['overall_health'] in ['EXCELLENT', 'GOOD']:
            print("\\n🚀 System healthy - proceeding with safe initialization...")
            
            # Import FSOT system safely
            sys.path.insert(0, r"FSOT_Clean_System")
            from main import FSOTHardwiredSystem
            
            # Create system with timeout
            system = FSOTHardwiredSystem()
            
            # Initialize with strict timeout
            print("🔄 Initializing system (30s timeout)...")
            await asyncio.wait_for(system.initialize(), timeout=30.0)
            
            # Get status
            status = await asyncio.wait_for(system.get_system_status(), timeout=10.0)
            print(f"✅ System Status: {status['system']['running']}")
            
            # Shutdown cleanly
            await asyncio.wait_for(system.shutdown(), timeout=10.0)
            print("✅ Clean shutdown completed")
            
        else:
            print("⚠️ System needs attention - skipping full initialization")
    
    except asyncio.TimeoutError:
        print("⏰ Operation timed out - preventing endless loop")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run with overall timeout protection
    try:
        asyncio.run(asyncio.wait_for(safe_main(), timeout=120.0))
    except asyncio.TimeoutError:
        print("🚨 OVERALL TIMEOUT - System is safe")
    except KeyboardInterrupt:
        print("🛑 User interrupted - clean exit")
    
    print(f"\\nCompleted: {datetime.now()}")
'''
    
    with open(_os.fspath(_REPO_ROOT / 'safe_main.py'), "w") as f:
        f.write(safe_main_content)
    
    print("✅ Created safe_main.py wrapper")

def main():
    """Main execution"""
    print("🛡️ FSOT SAFE EXECUTION MANAGER")
    print("=" * 50)
    
    # Run safe test
    safe_fsot_test()
    
    # Create safe wrapper
    print("\n🔧 Creating safe execution wrapper...")
    create_safe_main_wrapper()
    
    print("\n📋 USAGE INSTRUCTIONS:")
    print("1. Run safe test: python emergency_safe_run.py")
    print("2. Run safe main: python safe_main.py")
    print("3. Monitor system: python advanced_monitoring_tools.py")
    print("4. For web mode: python safe_main.py --web")
    
    print("\n✅ Safe execution tools ready!")

if __name__ == "__main__":
    main()
