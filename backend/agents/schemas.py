from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# ==================== AGDR ARCHITECTURE MODELS ====================

class FinancialMetricsSchema(BaseModel):
    """
    Schema estricto para MetricExtractorAgent (AGDR v5.0).
    Forza la salida tipada para métricas críticas stored as JSON.
    """
    van_kusd: float = Field(..., description="Valor Actual Neto en KUSD")
    tir_percent: float = Field(..., description="Tasa Interna de Retorno (%)")
    payback_years: float = Field(..., description="Período de recuperación")
    capex_total: float = Field(..., description="CAPEX Total consolidado")
    op_costs_unit: float = Field(..., description="Costos operativos unitarios (USD/lb)")
    confidence_score: float = Field(..., ge=0, le=1, description="Nivel de confianza (0-1)")

class KeyValue(BaseModel):
    """Estructura clave-valor para metadatos (evita Dict en OpenAI Strict)"""
    key: str = Field(..., description="Nombre del parámetro")
    value: str = Field(..., description="Valor del parámetro")

class SIC_DTO(BaseModel):
    """
    DTO para los 22 SIC (AGDR v5.0).
    Excluye narrativa no esencial para mitigar Context Overflow.
    """
    sic_code: str = Field(..., description="Código SIC (01-22)")
    project_id: int = Field(..., description="ID del proyecto")
    metadata: List[KeyValue] = Field(..., description="Metadatos técnicos clave (Lista de pares clave-valor)")
    key_tables_markdown: str = Field(..., description="Tablas críticas extraídas en formato Markdown")
    summary_markdown: str = Field(..., description="Contenido completo de la sección en Markdown")

class FeedbackCritiqueSchema(BaseModel):
    """
    Schema para Maker-Checker Loop (JudgeAgent).
    Encapsula solo la Causa Raíz y la Recomendación Accionable.
    """
    root_cause: str = Field(..., description="Análisis Causal (Bow-Tie, 5 Whys, Ishikawa)")
    actionable_recommendation: str = Field(..., description="Formato Anexo CC/DD: (Recomendación), para reducir/evitar (PROBLEMA)")
    qc_score: float = Field(..., ge=0, le=100, description="Puntaje de calidad técnica")
    approved: bool = Field(..., description="Si el documento es aprobado o no")
    critical_gaps: List[str] = Field(..., description="Lista de puntos críticos faltantes")
    regulatory_compliance: bool = Field(..., description="Cumplimiento reglamentario NCC-24")

class ValidationResponse(FeedbackCritiqueSchema):
    """Alias for backwards compatibility if needed, now inheriting AGDR properties"""
    pass

class SystemDependency(BaseModel):
    """Representa una dependencia entre agentes"""
    source_agent_id: str = Field(..., description="ID del agente origen")
    target_agent_id: str = Field(..., description="ID del agente destino")
    dependency_type: str = Field(..., description="hard (bloqueante) o soft")
    data_required: List[str] = Field(..., description="Lista de DTOs requeridos")

# ==================== LEGACY / SUPPORT MODELS (REQUIRED BY TOOLS) ====================

class BaseSICMetric(BaseModel):
    """Modelo base para todos los datos SIC"""
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza del dato (0-1)")
    source: str = Field(..., description="Fuente del dato (Issue ID, Documento, etc)")
    evidence: Optional[str] = Field(..., description="Fragmento de texto que respalda el dato")

class SIC16Capex(BaseSICMetric):
    total_capex: float = Field(..., description="Costo de Capital Total en KUSD")
    contingency: float = Field(..., description="Monto de contingencia")
    currency: str = Field(..., description="Moneda")
    capex_kusd: Optional[float] = Field(..., description="Opcional: CAPEX en KUSD")
    contingency_percentage: Optional[float] = Field(..., description="Opcional: % Contingencia")
    validated: bool = Field(..., description="Estado de validación")

class SIC14Plazo(BaseModel):
    months: int = Field(..., description="Plazo de ejecución en meses")
    validated: bool = Field(..., description="Estado de validación")

class SIC14Schedule(BaseSICMetric):
    duration_months: int = Field(..., description="Duración total en meses")
    start_date: Optional[str] = Field(..., description="Fecha inicio")
    end_date: Optional[str] = Field(..., description="Fecha fin")

class SIC03Riesgo(BaseModel):
    etp_capex: float = Field(..., description="Exposición Total del Proyecto (ETP) para CAPEX (50%)")
    etp_plazo: float = Field(..., description="Exposición Total del Proyecto (ETP) para Plazo (88%)")
    risk_level: Optional[str] = Field(..., description="Nivel de riesgo")

class SIC03Risk(BaseSICMetric):
    risk_level: str = Field(..., description="Nivel de riesgo global (Alto, Medio, Bajo)")
    critical_risks: List[str] = Field(..., description="Lista de riesgos críticos identificados")

class ExtractedMetrics(BaseModel):
    """Contenedor genérico compatible con FinancialMetricsSchema"""
    sic_code: str = Field(..., description="Código SIC")
    financial_data: Optional[FinancialMetricsSchema] = Field(..., description="Datos financieros (Pydantic)")
    valid: bool = Field(..., description="Si la extracción es válida")
    missing_fields: List[str] = Field(..., description="Lista de campos no encontrados")

class DocumentSectionDraft(BaseModel):
    """Borrador generado por el AuthorAgent"""
    sic_code: str
    title: str
    content_markdown: str = Field(..., description="Contenido en Markdown")
    used_metrics: List[str] = Field(default=[])

# ==================== WORKFLOW ENTITIES ====================

class DocumentSection(BaseModel):
    section_id: str
    title: str
    content: Optional[str] = None
    status: str = "pending" # pending, in_progress, review, approved, failed
    dependencies: List[str] = []

class DocumentPlan(BaseModel):
    project_id: str
    sections: List[DocumentSection]
    dag_edges: List[tuple[str, str]] = []
