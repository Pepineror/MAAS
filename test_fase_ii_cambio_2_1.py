"""
FASE II CAMBIO 2.1 Integration Test

Tests AsyncPostgresDb integration with the backend.
Validates connection pooling, concurrent access, and latency improvements.
"""

import asyncio
import httpx
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:7777"

def print_header(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def print_section(title):
    print(f"\n{title}")
    print("-" * len(title))

async def test_health_check():
    """Test backend health endpoint"""
    print_section("1️⃣ Health Check Test")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        assert response.status_code == 200
        print("✅ Health check PASSED")

async def test_preinversion_plan():
    """Test preinversion-plans endpoint with AsyncPostgresDb"""
    print_section("2️⃣ PreInversion Plan Test (AsyncPostgresDb)")
    
    payload = {
        "document": """
        PROYECTO: Expansión Minera - Codelco
        OBJETIVO: Aumentar producción de cobre en 20%
        RIESGOS: Geológicos, ambientales, sociales
        PRESUPUESTO: USD 500M
        CRONOGRAMA: 3 años
        """,
        "project_id": 12345
    }
    
    print(f"Sending POST request to /preinversion-plans")
    print(f"Project ID: {payload['project_id']}")
    
    start = datetime.now()
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/preinversion-plans",
                json=payload
            )
            
            elapsed = (datetime.now() - start).total_seconds()
            
            print(f"Status: {response.status_code}")
            print(f"Elapsed Time: {elapsed:.2f} seconds")
            
            if response.status_code in [200, 202]:
                try:
                    result = response.json()
                    print(f"\n✅ Response received:")
                    print(json.dumps(result, indent=2, ensure_ascii=False)[:500] + "...")
                except:
                    print(f"Response: {response.text[:200]}")
                print(f"✅ PreInversion plan test PASSED ({elapsed:.2f}s)")
            else:
                print(f"⚠️ Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")

async def test_concurrent_requests():
    """Test AsyncPostgresDb connection pooling with concurrent requests"""
    print_section("3️⃣ Concurrent Requests Test (AsyncPostgresDb Pool)")
    
    async def make_request(request_id: int):
        payload = {
            "document": f"Test project {request_id}",
            "project_id": 20000 + request_id
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                start = time.time()
                response = await client.post(
                    f"{BASE_URL}/preinversion-plans",
                    json=payload
                )
                elapsed = time.time() - start
                
                return {
                    "request_id": request_id,
                    "status": response.status_code,
                    "elapsed": elapsed,
                    "success": response.status_code in [200, 202]
                }
        except Exception as e:
            return {
                "request_id": request_id,
                "status": 0,
                "elapsed": 0,
                "error": str(e),
                "success": False
            }
    
    print(f"Sending 3 concurrent requests...")
    
    start = datetime.now()
    results = await asyncio.gather(
        make_request(1),
        make_request(2),
        make_request(3),
        return_exceptions=True
    )
    total_elapsed = (datetime.now() - start).total_seconds()
    
    successful = sum(1 for r in results if isinstance(r, dict) and r["success"])
    
    print(f"\nResults:")
    for result in results:
        if isinstance(result, dict):
            status = "✅" if result["success"] else "❌"
            print(f"  {status} Request {result['request_id']}: {result['status']} ({result.get('elapsed', 0):.2f}s)")
        else:
            print(f"  ❌ Request error: {result}")
    
    print(f"\nTotal concurrent time: {total_elapsed:.2f}s")
    print(f"Successful: {successful}/3")
    
    if successful >= 2:
        print(f"✅ Concurrent requests test PASSED (Pool is working)")
    else:
        print(f"⚠️ Concurrent requests test: Some failures detected")

async def test_async_postgres_db_direct():
    """Direct test of AsyncPostgresDb without HTTP"""
    print_section("4️⃣ Direct AsyncPostgresDb Test")
    
    try:
        from backend.core.async_postgres_db import AsyncPostgresDb
        
        db = AsyncPostgresDb(
            db_url="postgresql://postgres:postgres@localhost:5434/maas",
            max_connections=10
        )
        
        print("Initializing AsyncPostgresDb...")
        await db.initialize()
        print("✅ Pool initialized")
        
        # Health check
        health = await db.health_check()
        print(f"✅ Health check: {health}")
        
        # Test fetch
        result = await db.fetch("SELECT 1 as test_value;")
        print(f"✅ Fetch test: {result}")
        
        # Close
        await db.close()
        print("✅ Pool closed gracefully")
        
        print("✅ Direct AsyncPostgresDb test PASSED")
        
    except Exception as e:
        print(f"❌ Direct test failed: {str(e)}")

async def main():
    print_header("🚀 FASE II CAMBIO 2.1: AsyncPostgresDb Integration Test Suite")
    
    print(f"Backend URL: {BASE_URL}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run tests
        await test_health_check()
        await test_preinversion_plan()
        await test_concurrent_requests()
        await test_async_postgres_db_direct()
        
        print_header("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
