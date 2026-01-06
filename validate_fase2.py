#!/usr/bin/env python3
"""
Validation script for FASE II CAMBIO 2.1 implementation.
Tests AsyncPostgresDb fixes and new endpoints.
"""

import sys
import asyncio
from pathlib import Path

# Add project to path
root_dir = str(Path(__file__).resolve().parent)
sys.path.insert(0, root_dir)

async def test_async_postgres_db():
    """Test AsyncPostgresDb with Agno-compatible method signatures."""
    from backend.core.async_postgres_db import AsyncPostgresDb
    
    print("\n🧪 Testing AsyncPostgresDb...")
    
    db = AsyncPostgresDb(
        db_url="postgresql://postgres:postgres@localhost:5434/maas",
        max_connections=20
    )
    
    # Check that the class has all required Agno-compatible methods
    required_methods = [
        'get_session',      # Fixed: now accepts session_type parameter
        'upsert_session',   # Fixed: new method added
        'delete_session',   # Fixed: new method added
        'get_sessions',     # Fixed: new method added
        'table_exists',     # New method added
        'create_tables',    # New method added
        'render_session',   # New helper method
        'render_sessions',  # New helper method
        'initialize',
        'close',
        'execute',
        'fetch',
        'fetchone',
        'insert',
        'update',
        'delete',
        'health_check',
        'get_pool_status'
    ]
    
    missing = []
    for method in required_methods:
        if not hasattr(db, method):
            missing.append(method)
    
    if missing:
        print(f"❌ Missing methods: {missing}")
        return False
    
    # Check method signatures
    import inspect
    
    # Check get_session signature
    sig = inspect.signature(db.get_session)
    params = list(sig.parameters.keys())
    if 'session_type' not in params:
        print(f"❌ get_session missing 'session_type' parameter. Has: {params}")
        return False
    
    # Check upsert_session exists and takes 'session' parameter
    sig = inspect.signature(db.upsert_session)
    params = list(sig.parameters.keys())
    if 'session' not in params:
        print(f"❌ upsert_session missing 'session' parameter. Has: {params}")
        return False
    
    print("✅ All required methods present with correct signatures")
    
    # Check instance attributes for Agno compatibility
    if not hasattr(db, 'id'):
        print("❌ Missing 'id' attribute for Agno ORM")
        return False
    
    if not hasattr(db, 'host'):
        print("❌ Missing 'host' attribute")
        return False
    
    if not hasattr(db, 'port'):
        print("❌ Missing 'port' attribute")
        return False
    
    if not hasattr(db, 'database'):
        print("❌ Missing 'database' attribute")
        return False
    
    print("✅ All Agno ORM compatibility attributes present")
    return True


def test_main_py_imports():
    """Test that main.py imports correctly."""
    print("\n🧪 Testing main.py imports...")
    try:
        from backend import main
        print("✅ main.py imports successfully")
        
        # Check for new endpoints
        endpoints = {
            '/health': 'health_check',
            '/api/agents': 'list_agents',
            '/api/agents/performance': 'agent_performance'
        }
        
        for path, func_name in endpoints.items():
            if hasattr(main, func_name):
                print(f"✅ Found endpoint function: {func_name}")
            else:
                print(f"⚠️ Endpoint function not found: {func_name}")
        
        return True
    except Exception as e:
        print(f"❌ Error importing main.py: {str(e)}")
        return False


def test_requirements():
    """Check if required packages are in requirements.txt."""
    print("\n🧪 Checking requirements.txt...")
    
    req_file = Path(__file__).parent / "backend" / ".." / "requirements.txt"
    if not req_file.exists():
        print(f"⚠️ requirements.txt not found at {req_file}")
        return False
    
    content = req_file.read_text()
    required_packages = [
        'opentelemetry-api',
        'opentelemetry-sdk',
        'openinference-instrumentation-agno',
        'aiofiles',
        'asyncpg'
    ]
    
    missing = []
    for pkg in required_packages:
        if pkg not in content:
            missing.append(pkg)
    
    if missing:
        print(f"⚠️ Missing packages in requirements.txt: {missing}")
        return False
    
    print("✅ All required packages listed in requirements.txt")
    return True


def test_fase_ii_plan():
    """Check if FASE_II_PLAN.md has Control Plane documentation."""
    print("\n🧪 Checking FASE_II_PLAN.md...")
    
    plan_file = Path(__file__).parent / "FASE_II_PLAN.md"
    if not plan_file.exists():
        print(f"⚠️ FASE_II_PLAN.md not found at {plan_file}")
        return False
    
    content = plan_file.read_text()
    
    required_sections = [
        'Control Plane',
        'AgentUI',
        'Chat Interface',
        'Tracing & Execution Flow',
        'Session Management',
        'Knowledge Management'
    ]
    
    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)
    
    if missing:
        print(f"⚠️ Missing sections in FASE_II_PLAN.md: {missing}")
        return False
    
    print("✅ Control Plane documentation added to FASE_II_PLAN.md")
    return True


async def main():
    """Run all validation tests."""
    print("=" * 60)
    print("🔍 FASE II CAMBIO 2.1 Implementation Validation")
    print("=" * 60)
    
    results = {
        "AsyncPostgresDb": await test_async_postgres_db(),
        "main.py Imports": test_main_py_imports(),
        "requirements.txt": test_requirements(),
        "FASE_II_PLAN.md": test_fase_ii_plan()
    }
    
    print("\n" + "=" * 60)
    print("📊 VALIDATION RESULTS")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All validations passed!")
        print("\nNext steps:")
        print("1. Start the backend: python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 7777")
        print("2. Test endpoints:")
        print("   - GET http://localhost:7777/health")
        print("   - GET http://localhost:7777/api/agents")
        print("   - GET http://localhost:7777/api/agents/performance")
        return 0
    else:
        print("\n⚠️ Some validations failed. Review the output above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
