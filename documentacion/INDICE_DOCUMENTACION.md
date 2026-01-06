# 📑 ÍNDICE DE DOCUMENTACIÓN - MAAS v4.0

## 🎯 ¿Por dónde empiezo?

### Si tienes 5 minutos:
→ Lee: **RESUMEN_EJECUTIVO.md**
- Qué es MAAS v4.0
- 6 agentes principales
- Flujo completo
- Características clave

### Si tienes 15 minutos:
→ Lee: **GUIA_RAPIDA.md**
- Configuración requerida
- Ejemplo práctico paso a paso
- Troubleshooting común
- Interpretación de scores

### Si tienes 30 minutos:
→ Lee: **ARQUITECTURA_VISUAL.md**
- 8 diagramas visuales
- Matriz de herramientas vs agentes
- Flujo de datos completo
- Ciclo de vida del backend

### Si tienes 60 minutos:
→ Lee: **ESPECIFICACION_BACKEND.md**
- Especificación técnica completa
- Cada archivo y su responsabilidad
- Detalle de herramientas
- Endpoints REST
- Esquemas Pydantic
- Configuración de BD

---

## 📚 DOCUMENTOS DISPONIBLES

### 1. **RESUMEN_EJECUTIVO.md** ⭐ EMPEZAR AQUÍ
**Audiencia**: Ejecutivos, stakeholders, usuarios finales  
**Duración de lectura**: 5-10 min  
**Contenido**:
- ¿Qué es MAAS v4.0?
- Objetivo principal
- Los 6 agentes (explicación simple)
- Flujo completo
- Plantillas SIC soportadas
- Métricas de rendimiento
- Capacidades de auditoría

### 2. **GUIA_RAPIDA.md** ⭐ PARA USAR EL SISTEMA
**Audiencia**: Desarrolladores, operadores  
**Duración de lectura**: 10-15 min  
**Contenido**:
- Configuración .env
- Estructura de archivos
- Flujo paso a paso
- Ejemplo práctico completo
- Verificación de que funciona
- Troubleshooting
- Interpretación de scores

### 3. **ARQUITECTURA_VISUAL.md** 🎨 PARA ENTENDER CÓMO FUNCIONA
**Audiencia**: Arquitectos, tech leads  
**Duración de lectura**: 20-30 min  
**Contenido**:
- Pirámide de dependencias
- Mapa de agentes y herramientas
- Matriz herramientas vs agentes
- Flujo de datos principal
- Diagrama de BD
- Ciclo de vida del backend
- Matriz de responsabilidades
- Casos de uso

### 4. **ESPECIFICACION_BACKEND.md** 📖 REFERENCIA TÉCNICA COMPLETA
**Audiencia**: Desarrolladores, arquitectos  
**Duración de lectura**: 45-60 min  
**Contenido**:
- Arquitectura general (modelo holónico)
- main.py: punto de entrada
- ContextBroker: gestión de datos
- custom_tools.py: todas las herramientas en detalle
- 6 agentes: responsabilidades y flujos
- schemas.py: validación Pydantic
- workflows.py: orquestación
- Endpoints REST
- PostgreSQL: estructura de BD
- Flujos de datos completos
- Configuración de autorización

### 5. **ESPECIFICACION_BACKEND.md** (continuación)
- Diagramas de secuencia
- Checklist de validación
- Referencias y tecnologías

### 6. **Este documento: INDICE_DOCUMENTACION.md**
**Propósito**: Guía de navegación  
**Contenido**:
- Mapa de documentos
- Cómo acceder a cada sección
- Búsqueda rápida

---

## 🔍 BÚSQUEDA RÁPIDA POR TÓPICO

### Quiero entender...

#### "¿Qué es MAAS v4.0?"
→ RESUMEN_EJECUTIVO.md - Sección "¿QUÉ ES MAAS v4.0?"

#### "¿Cómo funciona el flujo completo?"
→ ESPECIFICACION_BACKEND.md - Sección "8. FLUJOS DE DATOS COMPLETOS"
→ ARQUITECTURA_VISUAL.md - Sección "4. FLUJO DE DATOS PRINCIPAL"

#### "¿Cuáles son los 6 agentes?"
→ RESUMEN_EJECUTIVO.md - Sección "🏗️ LOS 6 AGENTES"
→ ESPECIFICACION_BACKEND.md - Sección "4. AGENTES"

#### "¿Cómo se usan las herramientas?"
→ ESPECIFICACION_BACKEND.md - Sección "3. HERRAMIENTAS"
→ ARQUITECTURA_VISUAL.md - Sección "2. MAPA DE AGENTES Y SUS HERRAMIENTAS"

#### "¿Dónde se almacenan los datos?"
→ GUIA_RAPIDA.md - Sección "💾 ¿DÓNDE SE ALMACENAN LOS DATOS?"
→ ESPECIFICACION_BACKEND.md - Sección "8. BASE DE DATOS"

#### "¿Cómo audita el sistema?"
→ RESUMEN_EJECUTIVO.md - Sección "📊 CAPACIDADES DE AUDITORÍA"
→ ESPECIFICACION_BACKEND.md - Sección "4.4 ExpertJudgeAgent"

#### "¿Cómo llamo el API?"
→ GUIA_RAPIDA.md - Sección "🎯 EJEMPLO PRÁCTICO"
→ ESPECIFICACION_BACKEND.md - Sección "7. ENDPOINTS"

#### "¿Qué hacer si algo no funciona?"
→ GUIA_RAPIDA.md - Sección "🚨 TROUBLESHOOTING"

#### "¿Cómo se estructura el código?"
→ GUIA_RAPIDA.md - Sección "📊 ESTRUCTURA DE ARCHIVOS"
→ ESPECIFICACION_BACKEND.md - Sección "9. RELACIONES ENTRE ARCHIVOS"

#### "¿Qué plantillas SIC soporta?"
→ RESUMEN_EJECUTIVO.md - Sección "🎓 PLANTILLAS SIC SOPORTADAS"
→ ESPECIFICACION_BACKEND.md - Sección "4.3 GeneralAuthorAgent"

#### "¿Cómo interpretó los scores?"
→ GUIA_RAPIDA.md - Sección "📈 INTERPRETACIÓN DE SCORES"
→ ESPECIFICACION_BACKEND.md - Sección "4.4 ExpertJudgeAgent - Scoring System"

---

## 📊 MATRIZ DE DOCUMENTACIÓN

```
┌─────────────────────────────┬──────┬──────┬────────┬──────────┐
│ Aspecto                     │Exec  │Quick │Visual  │Technical │
├─────────────────────────────┼──────┼──────┼────────┼──────────┤
│ ¿Qué es MAAS?              │ ✅   │      │        │ ✅       │
│ Cómo usarlo                 │      │ ✅   │        │          │
│ Flujo completo              │      │      │ ✅     │ ✅       │
│ 6 Agentes                   │ ✅   │      │ ✅     │ ✅       │
│ Herramientas               │ ✅   │      │ ✅     │ ✅       │
│ Bases de datos             │      │ ✅   │        │ ✅       │
│ API REST                   │      │ ✅   │        │ ✅       │
│ Troubleshooting            │      │ ✅   │        │          │
│ Interpretación scores      │      │ ✅   │        │ ✅       │
│ Validación                 │      │ ✅   │        │ ✅       │
│ Diagramas                  │      │      │ ✅     │ ✅       │
│ Arquitectura detallada     │      │      │ ✅     │ ✅       │
│ Código específico          │      │      │        │ ✅       │
│ Configuración              │ ✅   │ ✅   │        │ ✅       │
└─────────────────────────────┴──────┴──────┴────────┴──────────┘

Leyenda:
✅ = Contenido disponible
Exec = RESUMEN_EJECUTIVO.md
Quick = GUIA_RAPIDA.md
Visual = ARQUITECTURA_VISUAL.md
Technical = ESPECIFICACION_BACKEND.md
```

---

## 🎓 CAMINOS DE APRENDIZAJE

### Camino 1: Ejecutivo (15 minutos)
```
1. Lee RESUMEN_EJECUTIVO.md completo
   ↓
2. Ve ARQUITECTURA_VISUAL.md - Sección 1 (Pirámide)
   ↓
3. Comprende: ¿Qué es? ¿Para qué sirve? ¿Cómo funciona?
   ↓
✅ Listo para aprobar presupuesto
```

### Camino 2: Usuario Operador (30 minutos)
```
1. Lee GUIA_RAPIDA.md secciones "TL;DR" y "Configuración"
   ↓
2. Sigue "Ejemplo práctico"
   ↓
3. Intenta generar un documento
   ↓
4. Si falla, consulta "Troubleshooting"
   ↓
✅ Listo para usar el sistema
```

### Camino 3: Desarrollador (60 minutos)
```
1. Lee GUIA_RAPIDA.md completamente
   ↓
2. Lee ARQUITECTURA_VISUAL.md completamente
   ↓
3. Lee ESPECIFICACION_BACKEND.md secciones 1-5
   ↓
4. Explora los archivos Python del backend
   ↓
5. Ejecuta validate_agents.py para confirmación
   ↓
✅ Listo para modificar/extender código
```

### Camino 4: Arquitecto/Tech Lead (90 minutos)
```
1. Lee todos los documentos en orden
2. Estudia los diagramas en ARQUITECTURA_VISUAL.md
3. Revisa ESPECIFICACION_BACKEND.md completo
4. Analiza relaciones entre archivos
5. Planifica mejoras y escalado
   ↓
✅ Listo para tomar decisiones arquitectónicas
```

---

## 🔗 REFERENCIAS CRUZADAS

### GenericDataAgent
- Responsabilidad: ESPECIFICACION_BACKEND.md - 4.1
- Herramientas: ARQUITECTURA_VISUAL.md - 2
- Flujo: ARQUITECTURA_VISUAL.md - 4
- En código: `backend/agents/generic_data_agent.py`

### MetricExtractorAgent
- Responsabilidad: ESPECIFICACION_BACKEND.md - 4.2
- Herramientas: ARQUITECTURA_VISUAL.md - 2
- Flujo: ARQUITECTURA_VISUAL.md - 4
- Schemas: ESPECIFICACION_BACKEND.md - 5
- En código: `backend/agents/metric_extractor_agent.py`

### GeneralAuthorAgent
- Responsabilidad: ESPECIFICACION_BACKEND.md - 4.3
- Plantillas: RESUMEN_EJECUTIVO.md - Plantillas SIC
- Flujo: ARQUITECTURA_VISUAL.md - 4
- En código: `backend/agents/author_agent.py`

### ExpertJudgeAgent
- Responsabilidad: ESPECIFICACION_BACKEND.md - 4.4
- Scoring: RESUMEN_EJECUTIVO.md - Capacidades de Auditoría
- Interpretación: GUIA_RAPIDA.md - Interpretación de Scores
- En código: `backend/agents/judge_agent.py`

### ContextBroker
- Detalles: ESPECIFICACION_BACKEND.md - 2
- Bases de datos: GUIA_RAPIDA.md - ¿Dónde se almacenan?
- Flujo startup: ARQUITECTURA_VISUAL.md - 6
- En código: `backend/core/context_broker.py`

### RedmineTools
- Uso: ESPECIFICACION_BACKEND.md - 3
- Qué hace: ARQUITECTURA_VISUAL.md - 2
- En código: `backend/tools/custom_tools.py` (primera parte)

### API Endpoints
- Detalles: ESPECIFICACION_BACKEND.md - 7
- Uso práctico: GUIA_RAPIDA.md - Ejemplo Práctico
- Flujo: ARQUITECTURA_VISUAL.md - 4

---

## 🚀 PRIMERAS ACCIONES

### Si nunca has usado MAAS:
```
1. Lee RESUMEN_EJECUTIVO.md (5 min)
2. Lee GUIA_RAPIDA.md (10 min)
3. Ejecuta: curl http://localhost:7777/health
4. Intenta generar un documento
5. Interpreta el score usando GUIA_RAPIDA.md
```

### Si necesitas entender la arquitectura:
```
1. Lee ARQUITECTURA_VISUAL.md (20 min)
2. Lee ESPECIFICACION_BACKEND.md secciones 1-4 (30 min)
3. Mapea mentalmente: main.py → agents → tools → KB
4. Identifica flujos de datos principales
```

### Si tienes un problema:
```
1. Consulta GUIA_RAPIDA.md - Troubleshooting
2. Si no está ahí, busca en ESPECIFICACION_BACKEND.md
3. Revisa logs en backend.log
4. Ejecuta validate_agents.py
5. Si persiste, consulta developer
```

---

## 📞 ¿CÓMO NAVEGAR ESTE REPOSITORIO?

### Estructura:
```
MAAS3/
├── README.md ← Empieza aquí
├── INDICE_DOCUMENTACION.md ← Este archivo
├── RESUMEN_EJECUTIVO.md ← Para ejecutivos
├── GUIA_RAPIDA.md ← Para usuarios
├── ARQUITECTURA_VISUAL.md ← Para arquitectos
├── ESPECIFICACION_BACKEND.md ← Referencia técnica
├── BACKEND_STATUS.md ← Estado actual
├── backend/ ← Código fuente
└── ...
```

### Para acceder a cualquier documento:
1. Abre VS Code
2. Presiona Ctrl+P (Quick Open)
3. Escribe el nombre: `RESUMEN_EJECUTIVO.md`
4. Presiona Enter

---

## ✅ VALIDACIÓN DE COMPRENSIÓN

### Después de leer RESUMEN_EJECUTIVO.md, deberías poder responder:
- [ ] ¿Qué es MAAS v4.0?
- [ ] ¿Cuáles son los 6 agentes?
- [ ] ¿Cómo se llama el LLM usado?
- [ ] ¿Cuántas plantillas SIC hay?
- [ ] ¿Qué significa un score de 75?

### Después de leer GUIA_RAPIDA.md, deberías poder:
- [ ] Hacer un health check
- [ ] Generar un documento
- [ ] Interpretar un score
- [ ] Identificar y resolver un error común

### Después de leer ARQUITECTURA_VISUAL.md, deberías poder:
- [ ] Dibujar el flujo de datos
- [ ] Listar herramientas de cada agente
- [ ] Explicar qué hace el ContextBroker
- [ ] Describir el ciclo de vida del backend

### Después de leer ESPECIFICACION_BACKEND.md, deberías poder:
- [ ] Modificar código de un agente
- [ ] Agregar una nueva herramienta
- [ ] Explicar cada endpoint
- [ ] Entender la estructura Pydantic

---

## 🎉 CONCLUSIÓN

Esta documentación forma un corpus completo que cubre MAAS v4.0 desde:
- **Alto nivel** (Ejecutivos) → RESUMEN_EJECUTIVO.md
- **Nivel operacional** (Usuarios) → GUIA_RAPIDA.md
- **Nivel de diseño** (Arquitectos) → ARQUITECTURA_VISUAL.md
- **Nivel técnico** (Desarrolladores) → ESPECIFICACION_BACKEND.md

Usa este índice para navegar rápidamente al contenido que necesitas.

---

**Versión**: 4.0 Documentation  
**Fecha**: 3 Enero 2026  
**Última actualización**: 3 Enero 2026  
**Status**: ✅ Completo y Actualizado

🎓 **¡Happy Learning!**
