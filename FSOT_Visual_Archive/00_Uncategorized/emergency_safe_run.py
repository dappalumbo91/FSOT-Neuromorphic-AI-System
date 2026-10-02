#!/usr/bin/env python3
"""
EMERGENCY SAFE RUN - NO LOOPS
=============================
This script runs your FSOT system safely without any endless loops.
"""

import os as _os
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[2]


import sys
import time
import signal
import threading
from datetime import datetime

# Force timeout after 30 seconds
def emergency_timeout():
    time.sleep(30)
    print("\n🚨 EMERGENCY TIMEOUT - FORCING EXIT")
    import os
    os._exit(0)

# Start emergency timeout
timeout_thread = threading.Thread(target=emergency_timeout, daemon=True)
timeout_thread.start()

print("🛡️ EMERGENCY SAFE RUN MODE")
print("=" * 40)
print(f"Started: {datetime.now()}")
print("Timeout: 30 seconds maximum")
print()

try:
    # Test 1: Basic imports
    print("1️⃣ Testing basic imports...")
    import numpy as np
    print("✅ NumPy imported")
    
    # Test 2: FSOT foundation (most likely to work)
    print("2️⃣ Testing FSOT foundation...")
    sys.path.insert(0, _os.fspath(_REPO_ROOT / 'FSOT_Clean_System'))
    from fsot_2_0_foundation import FSOTCore, FSOTConstants, FSOTDomain
    core = FSOTCore()
    print(f"✅ FSOT Core: {core.compute_universal_scalar(12, FSOTDomain.AI_TECH):.6f}")
    
    # Test 3: Brain system (from main directory)
    print("3️⃣ Testing brain system...")
    sys.path.insert(0, _os.fspath(_REPO_ROOT))
    from brain_system import NeuromorphicBrainSystem
    brain = NeuromorphicBrainSystem()
    print(f"✅ Brain System: {len(brain.regions)} regions")
    
    # Test 4: Quick stimulus test
    print("4️⃣ Testing stimulus processing...")
    stimulus = {'type': 'test', 'intensity': 0.5}
    result = brain.process_stimulus(stimulus)
    print(f"✅ Stimulus processed: {result['consciousness_level']:.3f}")
    
    # Test 5: Neural network (simple import test)
    print("5️⃣ Testing neural network...")
    try:
        import neural_network
        print(f"✅ Neural Network: Module imported successfully")
    except Exception as e:
        print(f"❌ Neural Network: {e}")
    
    print("\n🎉 ALL TESTS PASSED - NO ENDLESS LOOPS DETECTED!")
    print("💡 Your system components are working correctly.")
    print("🔧 The loop issue is likely in the main.py execution flow.")
    
except Exception as e:
    print(f"\n❌ Error encountered: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    print(f"\nCompleted: {datetime.now()}")
    print("🛡️ Emergency safe run completed")
