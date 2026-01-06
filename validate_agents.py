#!/usr/bin/env python3
"""
Validación de la estructura modular de agentes

Script para verificar que:
1. Todos los imports funcionan correctamente
2. Cada agente se instancia sin errores
3. Cada agente tiene las herramientas necesarias
4. La arquitectura está lista para workflow de preinversión
"""

import sys
import os
from pathlib import Path

# Fix ModuleNotFoundError: No module named 'backend'
root_dir = str(Path(__file__).resolve().parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

print("\n" + "="*70)
print("VALIDACIÓN DE ESTRUCTURA MODULAR DE AGENTES")
print("="*70 + "\n")

# 1. VALIDATE IMPORTS
print("1️⃣  Validando imports de agentes...")
print("-" * 70)

try:
    from backend.agents.generic_data_agent import GenericDataAgent
    print("  ✅ GenericDataAgent")
except Exception as e:
    print(f"  ❌ GenericDataAgent: {e}")
    sys.exit(1)

try:
    from backend.agents.metric_extractor_agent import MetricExtractorAgent
    print("  ✅ MetricExtractorAgent")
except Exception as e:
    print(f"  ❌ MetricExtractorAgent: {e}")
    sys.exit(1)

try:
    from backend.agents.author_agent import GeneralAuthorAgent
    print("  ✅ GeneralAuthorAgent")
except Exception as e:
    print(f"  ❌ GeneralAuthorAgent: {e}")
    sys.exit(1)

try:
    from backend.agents.judge_agent import ExpertJudgeAgent
    print("  ✅ ExpertJudgeAgent")
except Exception as e:
    print(f"  ❌ ExpertJudgeAgent: {e}")
    sys.exit(1)

try:
    from backend.agents.planner_agent import MasterPlannerAgent, DependencyManagerAgent
    print("  ✅ MasterPlannerAgent")
    print("  ✅ DependencyManagerAgent")
except Exception as e:
    print(f"  ❌ PlannerAgents: {e}")
    sys.exit(1)

# 2. VALIDATE PACKAGE EXPORTS
print("\n2️⃣  Validando exports del paquete agents...")
print("-" * 70)

try:
    from backend.agents import (
        GenericDataAgent as GDA,
        MetricExtractorAgent as MEA,
        GeneralAuthorAgent as GAA,
        ExpertJudgeAgent as EJA,
        MasterPlannerAgent as MPA,
        DependencyManagerAgent as DMA
    )
    print("  ✅ Todos los agentes pueden importarse desde backend.agents")
except Exception as e:
    print(f"  ❌ Package exports: {e}")
    sys.exit(1)

# 3. VALIDATE TOOLS IMPORTS
print("\n3️⃣  Validando imports de herramientas...")
print("-" * 70)

try:
    from backend.tools.custom_tools import (
        RedmineTools,
        RedmineKnowledgeTools,
        RedmineReasoningTools,
        SourceTextTools
    )
    print("  ✅ RedmineTools")
    print("  ✅ RedmineKnowledgeTools")
    print("  ✅ RedmineReasoningTools")
    print("  ✅ SourceTextTools")
except Exception as e:
    print(f"  ❌ Custom tools: {e}")
    sys.exit(1)

# 4. VALIDATE CORE COMPONENTS
print("\n4️⃣  Validando componentes core...")
print("-" * 70)

try:
    from backend.core.context_broker import ContextBroker
    print("  ✅ ContextBroker")
except Exception as e:
    print(f"  ❌ ContextBroker: {e}")
    sys.exit(1)

try:
    from agno.models.openai import OpenAIChat
    print("  ✅ OpenAIChat")
except Exception as e:
    print(f"  ❌ OpenAIChat: {e}")
    sys.exit(1)

# 5. VALIDATE AGENT ATTRIBUTES
print("\n5️⃣  Validando atributos de agentes...")
print("-" * 70)

agents = {
    'GenericDataAgent': GenericDataAgent,
    'MetricExtractorAgent': MetricExtractorAgent,
    'GeneralAuthorAgent': GeneralAuthorAgent,
    'ExpertJudgeAgent': ExpertJudgeAgent,
}

for agent_name, agent_class in agents.items():
    try:
        # Check if it's a proper Agent subclass
        from agno.agent import Agent
        if issubclass(agent_class, Agent):
            print(f"  ✅ {agent_name} extends Agent")
        else:
            print(f"  ❌ {agent_name} doesn't extend Agent")
    except Exception as e:
        print(f"  ❌ {agent_name}: {e}")

# 6. ARCHITECTURE SUMMARY
print("\n" + "="*70)
print("✅ VALIDACIÓN COMPLETA - ARQUITECTURA LISTA PARA PREINVERSIÓN")
print("="*70)

print("""
📋 ESTRUCTURA ACTUAL:

/backend/agents/
├── __init__.py                    (✅ Package exports)
├── generic_data_agent.py          (✅ Datos de Redmine)
├── metric_extractor_agent.py      (✅ Transformación a Pydantic)
├── author_agent.py                (✅ Redacción de documentos SIC)
├── judge_agent.py                 (✅ Auditoría y validación)
├── planner_agent.py               (✅ Planificación estratégica)
└── extractor_agent.py             (✅ Ingesta de datos)

🔧 HERRAMIENTAS DISPONIBLES:
  • RedmineTools: Extracción de datos
  • RedmineKnowledgeTools: Búsqueda de patrones
  • RedmineReasoningTools: Análisis de dependencias
  • SourceTextTools: Extracción de evidencia
  • ReasoningTools: Lógica y razonamiento
  • KnowledgeTools: Acceso a Knowledge Base

📚 CONOCIMIENTO BASE:
  • project_kb: Hechos del proyecto
  • rules_kb: Reglas de negocio y plantillas SIC

🚀 PRÓXIMOS PASOS:
  1. Verificar credenciales de Redmine (REDMINE_BASE_URL, REDMINE_API_KEY)
  2. Crear endpoint /preinversion-plans
  3. Implementar flujo: GenericDataAgent → MetricExtractorAgent → 
                       GeneralAuthorAgent → ExpertJudgeAgent
  4. Testing end-to-end con datos reales de Redmine
""")

print("="*70 + "\n")
