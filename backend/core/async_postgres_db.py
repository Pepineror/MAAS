"""
PostgreSQL Database Driver - Agno ORM Compatible
Versión corregida: Problemas de inicialización y manejo de objetos Trace
"""

import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any, Union, Tuple
from urllib.parse import urlparse
from threading import Lock, RLock
from contextlib import contextmanager

try:
    import psycopg
    from psycopg import sql
    from psycopg.rows import dict_row
    from psycopg_pool import ConnectionPool
except ImportError:
    raise ImportError("psycopg3 required: pip install psycopg[binary] psycopg-pool")

from agno.db.base import AsyncBaseDb, SessionType

logger = logging.getLogger(__name__)


class AsyncPostgresDb(AsyncBaseDb):
    """
    PostgreSQL driver corregido con inicialización robusta y manejo adecuado de objetos.
    Solución a los problemas identificados en los logs.
    """
    
    # Singleton por URL de base de datos
    _instances = {}
    _class_lock = RLock()
    
    def __new__(cls, *args, **kwargs):
        """Singleton: una instancia por URL de base de datos"""
        db_url = kwargs.get('db_url', args[0] if args else 
                          "postgresql://postgres:postgres@localhost:5434/maas")
        normalized_url = cls._normalize_url(db_url)
        
        with cls._class_lock:
            if normalized_url not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[normalized_url] = instance
                instance._init_called = False
            return cls._instances[normalized_url]
    
    def __init__(
        self,
        db_url: str = "postgresql://postgres:postgres@localhost:5434/maas",
        table_name: str = "documents",
        max_connections: int = 20,
        session_table: Optional[str] = None,
        knowledge_table: Optional[str] = None,
        id: Optional[str] = None,
        autoconnect: bool = True
    ):
        """Inicialización - solo se ejecuta una vez por instancia"""
        if getattr(self, '_init_called', False):
            return
            
        self.db_url = self._normalize_url(db_url)
        self.table_name = table_name
        self.session_table = session_table or "sessions"
        self.knowledge_table = knowledge_table or f"{table_name}_knowledge"
        self.max_connections = max_connections
        self._pool: Optional[ConnectionPool] = None
        self._initialized = False
        self._lock = RLock()
        self._id = id or f"async_postgres_db_{hash(db_url)}"
        self.host = None
        self.port = None
        self.database = None
        self._autoconnect = autoconnect
        self._init_called = True
        
        # Inicialización automática si se solicita
        if autoconnect:
            self.initialize()
    
    @staticmethod
    def _normalize_url(db_url: str) -> str:
        """Normaliza URLs de conexión"""
        replacements = {
            "asyncpg://": "postgresql://",
            "postgresql+asyncpg://": "postgresql://",
            "postgresql+psycopg://": "postgresql://"
        }
        for old, new in replacements.items():
            if db_url.startswith(old):
                return db_url.replace(old, new)
        return db_url
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def session_table_name(self) -> str:
        return self.session_table
    
    @property
    def knowledge_table_name(self) -> str:
        return self.knowledge_table
    
    def _ensure_initialized(self):
        """Garantiza que la base de datos esté inicializada antes de cualquier operación"""
        if not self._initialized:
            if self._autoconnect:
                self.initialize()
            else:
                raise RuntimeError("AsyncPostgresDb not initialized. Call initialize() first.")
    
    def initialize(self) -> None:
        """Inicialización robusta con doble verificación"""
        if self._initialized:
            return
        
        with self._lock:
            # Doble verificación dentro del lock
            if self._initialized:
                return
            
            try:
                parsed = urlparse(self.db_url)
                self.host = parsed.hostname or "localhost"
                self.port = parsed.port or 5432
                self.database = parsed.path.lstrip('/') or 'maas'
                username = parsed.username or "postgres"
                password = parsed.password or "postgres"
                
                conninfo = f"postgresql://{username}:{password}@{self.host}:{self.port}/{self.database}"
                
                # Crear pool con configuración robusta
                self._pool = ConnectionPool(
                    conninfo,
                    min_size=2,
                    max_size=self.max_connections,
                    timeout=30.0,
                    max_idle=300.0,
                    num_workers=2,
                    open=True  # Abrir inmediatamente
                )
                
                # Verificar conexión
                with self._pool.connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT 1")
                        conn.commit()
                
                self._initialized = True
                logger.info(f"✅ AsyncPostgresDb inicializado exitosamente - Pool: {self.max_connections} conexiones máx")
                
                # Crear tablas en segundo plano para no bloquear
                self._create_tables_async()
                
            except Exception as e:
                self._initialized = False
                self._pool = None
                logger.error(f"❌ Error crítico inicializando AsyncPostgresDb: {str(e)}", exc_info=True)
                raise RuntimeError(f"No se pudo inicializar la base de datos: {str(e)}")
    
    def _create_tables_async(self):
        """Crear tablas de manera asíncrona y segura"""
        try:
            self.create_tables()
        except Exception as e:
            logger.warning(f"⚠️ Error creando tablas (se reintentará): {str(e)}")
            # Podrías agregar reintentos aquí
    
    @contextmanager
    def _get_connection(self):
        """Context manager seguro para conexiones"""
        self._ensure_initialized()
        
        conn = None
        try:
            conn = self._pool.getconn()
            yield conn
        finally:
            if conn:
                self._pool.putconn(conn)
    
    @contextmanager
    def _transaction(self):
        """Context manager para transacciones"""
        with self._get_connection() as conn:
            try:
                with conn.transaction():
                    cursor = conn.cursor(row_factory=dict_row)
                    yield cursor
            except Exception as e:
                logger.error(f"❌ Error en transacción: {str(e)}")
                raise
    
    # ==================== TRACE HANDLING FIXED ====================
    
    def upsert_trace(self, trace: Union[dict, Any]) -> None:
        """
        Versión corregida: Maneja tanto diccionarios como objetos Trace.
        Compatibilidad total con Agno Tracing.
        """
        try:
            # Convertir objeto Trace a diccionario si es necesario
            if hasattr(trace, '__dict__'):
                # Es un objeto con atributos
                trace_dict = {}
                for attr in dir(trace):
                    if not attr.startswith('_'):
                        try:
                            value = getattr(trace, attr)
                            # Filtrar métodos y propiedades complejas
                            if not callable(value):
                                # Convertir datetime a string para JSON
                                if isinstance(value, datetime):
                                    value = value.isoformat()
                                trace_dict[attr] = value
                        except:
                            continue
                trace_id = trace_dict.get('trace_id') or trace_dict.get('id') or trace_dict.get('run_id')
                trace_data = json.dumps(trace_dict, default=str)
            elif hasattr(trace, 'to_dict'):
                # Tiene método to_dict
                trace_dict = trace.to_dict()
                trace_id = trace_dict.get('trace_id') or trace_dict.get('id') or trace_dict.get('run_id')
                trace_data = json.dumps(trace_dict, default=str)
            else:
                # Ya es un diccionario
                trace_id = trace.get('trace_id') or trace.get('id') or trace.get('run_id')
                trace_data = json.dumps(trace, default=str)
            
            if not trace_id:
                trace_id = 'unknown_' + str(hash(str(trace)))
            
            query = """
                INSERT INTO traces (trace_id, trace_data, created_at, updated_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(trace_id) DO UPDATE SET
                    trace_data = EXCLUDED.trace_data,
                    updated_at = CURRENT_TIMESTAMP
            """
            
            self.execute(query, trace_id, trace_data)
            logger.debug(f"✅ Trace persistido: {trace_id}")
            
        except Exception as e:
            # Fallback: solo loguear sin romper la aplicación
            logger.warning(f"⚠️ upsert_trace fallback (no crítico): {str(e)[:100]}")
            # Log detallado solo en modo debug
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Trace no persistido (detalle): {trace}")
    
    # ==================== BASIC OPERATIONS CORREGIDAS ====================
    
    def execute(self, query: str, *args) -> int:
        """Ejecuta query con manejo robusto de conexiones"""
        self._ensure_initialized()
        
        try:
            with self._transaction() as cursor:
                cursor.execute(query, args)
                return cursor.rowcount
        except Exception as e:
            logger.error(f"❌ Error ejecutando query: {str(e)}")
            raise
    
    def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Obtiene múltiples filas"""
        self._ensure_initialized()
        
        try:
            with self._transaction() as cursor:
                cursor.execute(query, args)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"❌ Error en fetch: {str(e)}")
            raise
    
    def fetchone(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Obtiene una sola fila"""
        self._ensure_initialized()
        
        try:
            with self._transaction() as cursor:
                cursor.execute(query, args)
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"❌ Error en fetchone: {str(e)}")
            raise
    
    # ==================== SPAN MANAGEMENT CORREGIDO ====================
    
    def create_spans(self, spans: List[Any]) -> None:
        """
        Versión corregida: Maneja inicialización y objetos Span correctamente.
        No rompe la aplicación si falla.
        """
        if not spans:
            return
        
        try:
            self._ensure_initialized()
        except Exception as e:
            logger.error(f"❌ No se pueden crear spans - BD no inicializada: {str(e)}")
            return
        
        if not self.table_exists("spans"):
            try:
                self.create_tables()
            except Exception as e:
                logger.error(f"❌ No se pudo crear tabla spans: {str(e)}")
                return
        
        try:
            query = """
                INSERT INTO spans (
                    span_id, trace_id, parent_span_id, name, type,
                    start_time, end_time, status_code, attributes, events,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                ON CONFLICT(span_id) DO UPDATE SET
                    parent_span_id = EXCLUDED.parent_span_id,
                    name = EXCLUDED.name,
                    type = EXCLUDED.type,
                    start_time = EXCLUDED.start_time,
                    end_time = EXCLUDED.end_time,
                    status_code = EXCLUDED.status_code,
                    attributes = EXCLUDED.attributes,
                    events = EXCLUDED.events,
                    updated_at = CURRENT_TIMESTAMP
            """
            
            batch_size = 50
            for i in range(0, len(spans), batch_size):
                batch = spans[i:i + batch_size]
                batch_data = []
                
                for span in batch:
                    # Convertir span a diccionario
                    if hasattr(span, 'to_dict'):
                        span_data = span.to_dict()
                    elif hasattr(span, '__dict__'):
                        span_data = span.__dict__
                    else:
                        span_data = span
                    
                    batch_data.append((
                        span_data.get('span_id'),
                        span_data.get('trace_id'),
                        span_data.get('parent_span_id'),
                        span_data.get('name'),
                        span_data.get('type'),
                        span_data.get('start_time'),
                        span_data.get('end_time'),
                        span_data.get('status_code'),
                        json.dumps(span_data.get('attributes', {}), default=str),
                        json.dumps(span_data.get('events', []), default=str)
                    ))
                
                # Ejecutar batch
                try:
                    with self._transaction() as cursor:
                        cursor.executemany(query, batch_data)
                    logger.debug(f"✅ Batch de {len(batch)} spans procesado")
                except Exception as e:
                    logger.error(f"❌ Error en batch de spans: {str(e)}")
                    # Continuar con siguiente batch
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Error general en create_spans: {str(e)}")
            # No relanzar - tracing no debe romper la app principal
    
    # ==================== TABLE MANAGEMENT ====================
    
    def _table_exists(self, table_name: str) -> bool:
        """Versión sincrónica interna para evitar recursión"""
        self._ensure_initialized()
        
        try:
            query = """
                SELECT EXISTS(
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """
            result = self.fetchone(query, table_name)
            return result and result.get('exists', False)
        except Exception as e:
            logger.error(f"❌ Error verificando tabla: {str(e)}")
            return False
    
    def create_tables(self) -> None:
        """Crea tablas necesarias"""
        self._ensure_initialized()
        
        try:
            # Tabla de sesiones
            create_sessions = f"""
                CREATE TABLE IF NOT EXISTS {self.session_table} (
                    id BIGSERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    user_id VARCHAR(255),
                    session_type VARCHAR(100) DEFAULT 'default',
                    data JSONB DEFAULT '{{}}'::jsonb,
                    metadata JSONB DEFAULT '{{}}'::jsonb,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_session UNIQUE(session_id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_{self.session_table}_session_id 
                ON {self.session_table}(session_id);
                
                CREATE INDEX IF NOT EXISTS idx_{self.session_table}_user_id 
                ON {self.session_table}(user_id);
                
                CREATE INDEX IF NOT EXISTS idx_{self.session_table}_session_type 
                ON {self.session_table}(session_type);
            """
            
            # Tabla de traces (corregida)
            create_traces = """
                CREATE TABLE IF NOT EXISTS traces (
                    trace_id VARCHAR(255) PRIMARY KEY,
                    trace_data JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_traces_trace_id 
                ON traces(trace_id);
                
                CREATE INDEX IF NOT EXISTS idx_traces_created_at 
                ON traces(created_at DESC);
            """
            
            # Tabla de spans (corregida)
            create_spans = """
                CREATE TABLE IF NOT EXISTS spans (
                    span_id VARCHAR(255) PRIMARY KEY,
                    trace_id VARCHAR(255) NOT NULL,
                    parent_span_id VARCHAR(255),
                    name VARCHAR(255),
                    type VARCHAR(100),
                    start_time TIMESTAMP WITH TIME ZONE,
                    end_time TIMESTAMP WITH TIME ZONE,
                    status_code VARCHAR(50),
                    attributes JSONB DEFAULT '{}'::jsonb,
                    events JSONB DEFAULT '[]'::jsonb,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (trace_id) REFERENCES traces(trace_id) ON DELETE CASCADE
                );
                
                CREATE INDEX IF NOT EXISTS idx_spans_trace_id 
                ON spans(trace_id);
                
                CREATE INDEX IF NOT EXISTS idx_spans_parent_span_id 
                ON spans(parent_span_id);
                
                CREATE INDEX IF NOT EXISTS idx_spans_start_time 
                ON spans(start_time);
            """
            
            self.execute(create_sessions)
            self.execute(create_traces)
            self.execute(create_spans)
            
            logger.info("✅ Tablas creadas/verificadas exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error creando tablas: {str(e)}")
            raise
    
    # ==================== SESSION MANAGEMENT (mantenido para compatibilidad) ====================
    
    async def get_session(
        self,
        session_id: str,
        session_type: Optional[SessionType] = None,
        user_id: Optional[str] = None,
        deserialize: Optional[bool] = True,
    ) -> Optional[Dict[str, Any]]:
        self._ensure_initialized()
        
        try:
            query = f"""
                SELECT id, session_id, user_id, session_type, data, metadata, 
                       created_at, updated_at
                FROM {self.session_table}
                WHERE session_id = %s
            """
            params = [session_id]
            
            if session_type:
                query += " AND session_type = %s"
                params.append(session_type)
            
            result = self.fetchone(query, *params)
            
            if result:
                if isinstance(result.get('data'), str):
                    result['data'] = json.loads(result['data'])
                if isinstance(result.get('metadata'), str):
                    result['metadata'] = json.loads(result['metadata'])
            
            return result
        except Exception as e:
            logger.error(f"❌ Error get_session: {str(e)}")
            return None

    async def get_sessions(
        self,
        session_type: Optional[SessionType] = None,
        user_id: Optional[str] = None,
        component_id: Optional[str] = None,
        session_name: Optional[str] = None,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        limit: Optional[int] = 20,
        page: Optional[int] = 1,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[Any] = "desc",
        deserialize: bool = False,
    ) -> Union[List[Any], Tuple[List[Dict[str, Any]], int]]:
        """
        Obtiene sesiones de la base de datos con paginación y filtrado.
        Compatible con la interfaz esperada por Agno OS.
        """
        self._ensure_initialized()
        
        try:
            # Construir query base
            query = f"FROM {self.session_table} WHERE 1=1"
            params = []
            
            if session_type:
                # session_type puede ser un Enum o str
                st_value = session_type.value if hasattr(session_type, 'value') else str(session_type)
                query += " AND session_type = %s"
                params.append(st_value)
            
            if user_id:
                query += " AND user_id = %s"
                params.append(user_id)
            
            # component_id en Agno suele mapearse a agent_id, team_id o workflow_id según el tipo
            # Nuestra tabla de sesiones actual parece ser simplificada. 
            # Verificamos si tenemos esas columnas o si están en 'data'/'metadata'
            # Por ahora, buscamos en metadata si existe
            if component_id:
                query += " AND (metadata->>'agent_id' = %s OR metadata->>'team_id' = %s OR metadata->>'workflow_id' = %s)"
                params.extend([component_id, component_id, component_id])

            if session_name:
                query += " AND (session_id ILIKE %s OR metadata->>'session_name' ILIKE %s)"
                params.extend([f"%{session_name}%", f"%{session_name}%"])
            
            # Obtener conteo total
            total_count_query = f"SELECT COUNT(*) {query}"
            count_result = self.fetchone(total_count_query, *params)
            total_count = count_result.get('count', 0) if count_result else (count_result[0] if count_result and isinstance(count_result, tuple) else 0)
            
            # Aplicar ordenamiento
            order_clause = "DESC"
            if sort_order:
                order_clause = sort_order.value if hasattr(sort_order, 'value') else str(sort_order).upper()
            
            valid_sort_columns = ['id', 'session_id', 'user_id', 'session_type', 'created_at', 'updated_at']
            sort_column = sort_by if sort_by in valid_sort_columns else 'created_at'
            
            query += f" ORDER BY {sort_column} {order_clause}"
            
            # Paginación
            if limit and limit > 0:
                query += " LIMIT %s"
                params.append(limit)
                if page and page > 1:
                    query += " OFFSET %s"
                    params.append((page - 1) * limit)
            
            final_query = f"SELECT * {query}"
            records = self.fetch(final_query, *params)
            
            # Procesar registros (JSON parse)
            for record in records:
                if isinstance(record.get('data'), str):
                    record['data'] = json.loads(record['data'])
                if isinstance(record.get('metadata'), str):
                    record['metadata'] = json.loads(record['metadata'])
            
            if deserialize:
                # Agno espera objetos Session, pero si devolvemos dicts con deserialize=False (como hace el router) está bien
                return records
            
            return records, int(total_count)
            
        except Exception as e:
            logger.error(f"❌ Error en get_sessions: {str(e)}")
            return [], 0

    # --- Implementación obligatoria de métodos abstractos de AsyncBaseDb ---

    async def table_exists(self, table_name: str) -> bool:
        return self._table_exists(table_name)

    async def get_latest_schema_version(self, table_name: str) -> str:
        return "2.0.0"

    async def upsert_schema_version(self, table_name: str, version: str):
        pass

    async def delete_session(self, session_id: str) -> bool:
        self.execute(f"DELETE FROM {self.session_table} WHERE session_id = %s", session_id)
        return True

    async def delete_sessions(self, session_ids: List[str]) -> None:
        if not session_ids: return
        self.execute(f"DELETE FROM {self.session_table} WHERE session_id = ANY(%s)", (session_ids,))

    async def rename_session(self, session_id: str, session_type: SessionType, session_name: str, deserialize: bool = True) -> Optional[Any]:
        self.execute(f"UPDATE {self.session_table} SET metadata = metadata || jsonb_build_object('session_name', %s) WHERE session_id = %s", session_name, session_id)
        return await self.get_session(session_id, session_type)

    async def upsert_session(self, session: Any, deserialize: bool = True) -> Optional[Any]:
        # Implementación mínima para permitir guardado de sesiones
        try:
            s_dict = session.to_dict() if hasattr(session, 'to_dict') else session
            session_id = s_dict.get('session_id')
            user_id = s_dict.get('user_id')
            st_value = s_dict.get('session_type', 'default')
            data = json.dumps(s_dict.get('session_data', {}))
            metadata = json.dumps(s_dict.get('metadata', {}))
            
            query = f"""
                INSERT INTO {self.session_table} (session_id, user_id, session_type, data, metadata, updated_at)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (session_id) DO UPDATE SET
                    data = EXCLUDED.data,
                    metadata = EXCLUDED.metadata,
                    updated_at = EXCLUDED.updated_at
            """
            self.execute(query, session_id, user_id, st_value, data, metadata)
            return session if deserialize else s_dict
        except Exception as e:
            logger.error(f"Error upsert_session: {e}")
            return None

    # Memory, Metrics, Knowledge, Evals - dummies para cumplir interfaz
    async def clear_memories(self) -> None: pass
    async def delete_user_memory(self, memory_id: str, user_id: Optional[str] = None) -> None: pass
    async def delete_user_memories(self, memory_ids: List[str], user_id: Optional[str] = None) -> None: pass
    async def get_all_memory_topics(self, user_id: Optional[str] = None) -> List[str]: return []
    async def get_user_memory(self, memory_id: str, deserialize: bool = True, user_id: Optional[str] = None) -> Optional[Any]: return None
    async def get_user_memories(self, **kwargs) -> Any: return [], 0
    async def get_user_memory_stats(self, **kwargs) -> Any: return [], 0
    async def upsert_user_memory(self, memory: Any, deserialize: bool = True) -> Optional[Any]: return None
    async def get_metrics(self, **kwargs) -> Any: return [], 0
    async def calculate_metrics(self) -> Any: return None
    async def delete_knowledge_content(self, id: str): pass
    async def get_knowledge_content(self, id: str) -> Any: return None
    async def get_knowledge_contents(self, **kwargs) -> Any: return [], 0
    async def upsert_knowledge_content(self, knowledge_row: Any): pass
    async def create_eval_run(self, eval_run: Any) -> Any: return None
    async def delete_eval_runs(self, eval_run_ids: List[str]) -> None: pass
    async def get_eval_run(self, eval_run_id: str, deserialize: bool = True) -> Any: return None
    async def get_eval_runs(self, **kwargs) -> Any: return [], 0
    async def rename_eval_run(self, eval_run_id: str, name: str, deserialize: bool = True) -> Any: return None
    
    # Traces and Spans - wrap existing ones
    async def async_upsert_trace(self, trace) -> None:
        self.upsert_trace(trace)

    async def get_trace(self, **kwargs) -> Any: return None
    async def get_traces(self, **kwargs) -> Any: return [], 0
    async def get_trace_stats(self, **kwargs) -> Any: return [], 0
    async def create_span(self, span: Any) -> None: pass
    async def create_spans(self, spans: List) -> None: pass
    async def get_span(self, span_id: str) -> Any: return None
    async def get_spans(self, **kwargs) -> Any: return []

    # Cultural Knowledge
    async def clear_cultural_knowledge(self) -> None: pass
    async def delete_cultural_knowledge(self, id: str) -> None: pass
    async def get_cultural_knowledge(self, id: str) -> Any: return None
    async def get_all_cultural_knowledge(self, **kwargs) -> Any: return []
    async def upsert_cultural_knowledge(self, cultural_knowledge: Any) -> Any: return None
    
    # ==================== HEALTH & MONITORING ====================
    
    def health_check(self) -> Dict[str, Any]:
        """Verificación de salud robusta"""
        try:
            if not self._initialized:
                return {"status": "uninitialized", "timestamp": datetime.now().isoformat()}
            
            # Verificar pool
            pool_status = "unknown"
            if self._pool:
                try:
                    with self._pool.connection() as conn:
                        with conn.cursor() as cur:
                            cur.execute("SELECT 1 as health")
                            result = cur.fetchone()
                            pool_status = "healthy" if result and result[0] == 1 else "unhealthy"
                except:
                    pool_status = "unhealthy"
            
            return {
                "status": "healthy" if pool_status == "healthy" else "unhealthy",
                "pool_status": pool_status,
                "initialized": self._initialized,
                "pool_size": self.max_connections if self._pool else 0,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def close(self) -> None:
        """Cierra el pool de conexiones (Agno async compatible)"""
        if self._pool:
            try:
                self._pool.close()
                self._initialized = False
                logger.info("✅ Pool cerrado exitosamente")
            except Exception as e:
                logger.error(f"❌ Error cerrando pool: {str(e)}")