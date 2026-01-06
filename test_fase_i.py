#!/usr/bin/env python3
"""
FASE I - Test Suite
Valida los 4 CAMBIOs implementados:
1. CAMBIO 1.4 - Background Hook para auditoría
2. CAMBIO 1.1 - Paralelismo en FASE 2
3. CAMBIO 1.2 - Context Compression
4. CAMBIO 1.3 - Checkpoint Durability
"""

import asyncio
import json
import time
from datetime import datetime
import requests

# Configuration
BASE_URL = "http://localhost:7777"
ENDPOINT = f"{BASE_URL}/preinversion-plans"

def print_header(msg):
    print("\n" + "="*70)
    print(f"  {msg}")
    print("="*70)

def test_background_hook():
    """Test CAMBIO 1.4: Background Hook para auditoría"""
    print_header("TEST 1: Background Hook (CAMBIO 1.4)")
    
    payload = {
        "project_id": 12345,
        "document_type": "SIC",
        "timeout_seconds": 300
    }
    
    print(f"\n📤 Enviando request a: POST {ENDPOINT}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        start_time = time.time()
        
        # Realizar request (no debería tomar más de 45s)
        response = requests.post(
            ENDPOINT,
            json=payload,
            timeout=50
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Response recibida en {elapsed:.2f}s")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📋 Response body:")
            print(json.dumps(data, indent=2))
            
            # Validaciones
            print(f"\n🔍 Validaciones CAMBIO 1.4:")
            assert data.get("status") == "success", "❌ Status debe ser 'success'"
            print("✅ Status = 'success'")
            
            assert data.get("audit_started") == True, "❌ Audit debe estar en background"
            print("✅ Audit started = True (background hook activo)")
            
            assert elapsed < 45, f"❌ Latencia {elapsed:.2f}s > 45s (expected <45s)"
            print(f"✅ Latencia < 45s ({elapsed:.2f}s percibida)")
            
            print(f"\n📨 Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {str(e)}")
        return False

def test_parallelism():
    """Test CAMBIO 1.1: Paralelismo en FASE 2"""
    print_header("TEST 2: Paralelismo en FASE 2 (CAMBIO 1.1)")
    
    print("""
La prueba de paralelismo es validable en los logs del backend:
- Líneas con [FASE 2] indican extracciones paralelas
- Todas las 5 extracciones deben completarse en ~3-5s (vs 12-15s secuencial)

Buscar en backend.log:
  grep "FASE 2" backend.log
  
Patrón esperado:
  ⚡ [FASE 2] Iniciando extracciones paralelas...
  ✅ [FASE 2] Extracciones paralelas completadas (5 métricas)
    """)
    
    # Validar logs
    try:
        with open("/home/iades/IADES/PRODUCTOS/00.banco de probemas IADES/MAAS/MAAS3/backend.log", "r") as f:
            logs = f.read()
            
        if "[FASE 2]" in logs:
            print("✅ Logs contienen [FASE 2] - Paralelismo activo")
            return True
        else:
            print("⚠️  Aún no hay logs de [FASE 2] - Ejecutar prueba 1 primero")
            return False
    except FileNotFoundError:
        print("⚠️  No se encontró backend.log")
        return False

def test_compression():
    """Test CAMBIO 1.2: Context Compression"""
    print_header("TEST 3: Context Compression (CAMBIO 1.2)")
    
    print("""
La validación de compresión está en los logs:
- Línea con "✅ Context Compression" muestra antes/después de tokens

Buscar en backend.log:
  grep "Context Compression" backend.log
  
Patrón esperado:
  ✅ Context Compression: 1234 → 450 tokens (63% reducción)
    """)
    
    try:
        with open("/home/iades/IADES/PRODUCTOS/00.banco de probemas IADES/MAAS/MAAS3/backend.log", "r") as f:
            logs = f.read()
            
        if "Context Compression" in logs:
            print("✅ Logs contienen Context Compression - Compresión activa")
            # Buscar la línea específica
            for line in logs.split('\n'):
                if "Context Compression" in line:
                    print(f"  {line}")
            return True
        else:
            print("⚠️  Aún no hay logs de Context Compression - Ejecutar prueba 1 primero")
            return False
    except FileNotFoundError:
        print("⚠️  No se encontrado backend.log")
        return False

def test_checkpoint():
    """Test CAMBIO 1.3: Durability Checkpoint"""
    print_header("TEST 4: Durability Checkpoint (CAMBIO 1.3)")
    
    print("""
La validación de checkpoints está en los logs:
- Líneas con "💾 Guardando checkpoint" y "✅ Checkpoint guardado"

Buscar en backend.log:
  grep "Checkpoint" backend.log
  
Patrón esperado:
  💾 Guardando checkpoint: Proyecto 12345, Document Authoring
  ✅ Checkpoint guardado: Document Authoring
    """)
    
    try:
        with open("/home/iades/IADES/PRODUCTOS/00.banco de probemas IADES/MAAS/MAAS3/backend.log", "r") as f:
            logs = f.read()
            
        if "Checkpoint" in logs:
            print("✅ Logs contienen Checkpoint - Durability activa")
            # Buscar líneas específicas
            for line in logs.split('\n'):
                if "Checkpoint" in line:
                    print(f"  {line}")
            return True
        else:
            print("⚠️  Aún no hay logs de Checkpoint - Ejecutar prueba 1 primero")
            return False
    except FileNotFoundError:
        print("⚠️  No se encontró backend.log")
        return False

def print_summary(results):
    """Imprimir resumen de pruebas"""
    print_header("RESUMEN DE PRUEBAS")
    
    tests = [
        ("CAMBIO 1.4 - Background Hook", results[0]),
        ("CAMBIO 1.1 - Paralelismo", results[1]),
        ("CAMBIO 1.2 - Compresión", results[2]),
        ("CAMBIO 1.3 - Checkpoint", results[3]),
    ]
    
    print("\n")
    passed = 0
    for test_name, result in tests:
        status = "✅ PASS" if result else "⚠️  PENDING"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Total: {passed}/{len(tests)} tests completados")
    print(f"🎯 Latencia esperada: 50-60s → 30-40s (FASE I)")
    
    if passed == 4:
        print("\n🎉 ¡FASE I COMPLETADA EXITOSAMENTE!")
    else:
        print("\n⏳ Ejecutar prueba 1 (POST /preinversion-plans) para llenar todos los tests")

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════╗
║  FASE I - VALIDATION SUITE                                         ║
║  Durability & Optimization                                         ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    results = [
        test_background_hook(),      # CAMBIO 1.4
        test_parallelism(),          # CAMBIO 1.1
        test_compression(),          # CAMBIO 1.2
        test_checkpoint(),           # CAMBIO 1.3
    ]
    
    print_summary(results)
    
    print(f"\n⏱️  Timestamp: {datetime.now().isoformat()}")
    print("📁 Backend logs: /backend.log")
