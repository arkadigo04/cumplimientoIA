# Arquitectura del sistema

Estado: propuesta inicial para el MVP
Alcance: plataforma B2B de evaluación de seguridad externa y seguimiento de cumplimiento
Principio de seguridad: solo se procesan activos cuya organización haya verificado y autorizado. Las comprobaciones son acotadas, no intrusivas y sujetas a límites de frecuencia, alcance y permisos.

## 1. Objetivo del sistema

La plataforma debe permitir a una organización:

- registrar activos digitales bajo su titularidad,
- solicitar evaluaciones de seguridad y cumplimiento,
- ejecutar comprobaciones autorizadas en esos activos,
- conservar evidencia estructurada y hallazgos normalizados,
- visualizar resultados de forma clara y auditable,
- separar la lógica de negocio de la infraestructura técnica.

El sistema no debe depender de librerías externas para decidir la lógica de negocio ni para autorizar evaluaciones. La evaluación de cumplimiento debe basarse en reglas explícitas, verificables y reproducibles.

## 2. Decisiones arquitectónicas del MVP

| Área | Decisión MVP | Motivo |
|---|---|---|
| Backend API | Python + FastAPI | Desarrollo rápido, validación sólida, ecosistema maduro |
| Validación y modelos | Pydantic | Serialización, validación y contratos claros |
| Persistencia | PostgreSQL | Relacional, transaccional, soporte JSONB para evidencia |
| Cola / trabajos | Redis + queue library | Sencillo para MVP y desacoplamiento entrante/saliente |
| Frontend | React + TypeScript | Panel analítico y dashboard de uso frecuente |
| Worker de escaneo | Procesos separados del API | Aislar la ejecución de comprobaciones y escalar de forma independiente |
| Lenguaje futuro | Go solo si la carga lo exige | Optimización real, no un cambio “de moda” |

Nota: la intención es construir primero el producto y validar la lógica de negocio. El cambio de lenguaje a Go puede ser una decisión posterior si se demuestra que la concurrencia o el throughput del worker requieren mejor rendimiento.

## 3. Principios de diseño

### 3.1 Separación de responsabilidades
La arquitectura debe separar claramente:

- Dominio: reglas, estado y decisiones de negocio
- Puertos: interfaces que define la aplicación
- Adaptadores: infraestructura concreta (HTTP, PostgreSQL, Redis, comprobaciones)
- Workers: ejecución asíncrona de evaluaciones

### 3.2 Fuente de verdad
PostgreSQL será la fuente de verdad del estado de las evaluaciones, activos, hallazgos y permisos. La cola de eventos transporta trabajo, pero no sustituye la persistencia.

### 3.3 Contratos versionados
La comunicación entre API y workers debe estar basada en contratos explícitos, versionados y validados. Esto evita que un cambio de implementación rompa una evaluación en producción.

### 3.4 Seguridad por defecto
No se deben aceptar atributos de la request como autoridad suficiente para ejecutar comprobaciones. Todas las decisiones críticas deben validarse con datos persistidos, permisos de organización y alcance autorizado.

## 4. Vista general de la arquitectura

```text
[Frontend React + TypeScript]
              |
              | HTTPS / API
              v
[API FastAPI]
      |  \
      |   \---> [PostgreSQL]
      |
      | publica trabajo
      v
[Queue / Redis]
      |
      v
[Workers de evaluación]
      |
      +--> [Adaptadores de comprobación]
      |
      +--> [Persistencia de hallazgos y estado]
```

La API gestiona autenticación, autorización, usuarios, organizaciones, activos y peticiones. Los workers son responsables de ejecutar evaluaciones autorizadas y almacenar resultados en base de datos. El dominio no debe conocer ni Redis ni HTTP ni bibliotecas de terceros.

## 5. Arquitectura hexagonal

### 5.1 Dominio
El dominio contiene la lógica central del negocio, incluyendo:

- organizaciones,
- usuarios y permisos,
- activos,
- evaluaciones,
- estados de ejecución,
- hallazgos,
- severidades,
- reglas de traducción de evidencia técnica a resultado de cumplimiento.

El dominio no debe:

- hacer llamadas HTTP,
- importar librerías de escaneo,
- accedir directamente a PostgreSQL,
- depender de FastAPI,
- mezclar infraestructura con lógica de negocio.

### 5.2 Puertos
Los puertos defininen las dependencias del dominio, por ejemplo:

- repositorio de evaluaciones,
- repositorio de hallazgos,
- repositorio de activos,
- publicador de trabajos,
- verificador de permisos,
- adaptador de comprobación,
- reloj / UUID generator si fuera necesario en pruebas.

### 5.3 Adaptadores
Los adaptadores implementan esas interfaces:

- adaptador HTTP: endpoints FastAPI
- adaptador PostgreSQL: persistencia transaccional
- adaptador Redis: cola de trabajos
- adaptadores de comprobación: DNS, TLS, encabezados HTTP, SSL, etc.
- adaptador frontend: cliente de la API

Una librería externa debe quedar detrás de un adaptador concreto. Así, cambiar la implementación no cambia la lógica del dominio.

## 6. Flujo de una evaluación

1. Un usuario autenticado solicita una evaluación de un activo de su organización.
2. La API valida que el usuario tiene permiso sobre la organización y sobre el activo.
3. La API comprueba que el activo esté verificado y dentro del alcance autorizado.
4. La API crea la evaluación en PostgreSQL con estado queued.
5. La API publica un evento de trabajo en la cola.
6. Un worker toma el mensaje, valida el contrato y marca la evaluación como running.
7. El worker recupera el activo y el alcance autorizado desde la base de datos.
8. Ejecuta solo los módulos permitidos.
9. Guarda evidencia y hallazgos en PostgreSQL.
10. Marca la evaluación como completed o failed, con error operativo explícito cuando corresponda.
11. El frontend consulta el estado y presenta los resultados.

La base de datos es la verdad. La cola solo transporta jobs.

## 7. Reintentos y idempotencia

Los trabajos deben poder reintentarse de forma segura. Un mensaje duplicado no debe:

- duplicar hallazgos,
- duplicar registros de evaluación,
- dejar un estado inconsistente.

La solución recomendada es:

- idempotencia por keys de negocio,
- guardado de eventos con identificadores únicos,
- estado de evaluación final consistente,
- comprobaciones de deduplicación por scan_id, asset_id y module.

## 8. Contrato de trabajo

El contrato debe ir versionado. El worker no debe confiar en el contenido del mensaje para autorizar el trabajo. Debe validar el activo y el alcance desde la base de datos.

```json
{
  "schema_version": 1,
  "event_id": "uuid",
  "scan_id": "uuid",
  "organization_id": "uuid",
  "asset_id": "uuid",
  "modules": ["dns_email", "tls"],
  "created_at": "2026-10-23T12:00:00Z"
}
```

Es importante que el mensaje no contenga:

- JWTs
- sesiones
- secretos
- credenciales
- parámetros arbitrarios de ejecución
- instrucciones de shell

## 9. Formato común de hallazgos

Cada hallazgo debe seguir un formato común, aunque la evidencia técnica puede variar por módulo.

```json
{
  "module": "tls",
  "rule_id": "tls.certificate.expiration",
  "severity": "medium",
  "title": "Certificado próximo a caducar",
  "description": "La comprobación encontró un certificado dentro del umbral definido.",
  "evidence": {
    "expires_at": "2026-11-10T00:00:00Z"
  },
  "remediation": "Renovar el certificado antes de su fecha de expiración."
}
```

Esto permite que la capa de resultados sea consistente para la UI, reportes y cumplimiento.

## 10. Datos principales

El esquema debe incluir, como mínimo:

- organizations
- users
- organization_memberships
- assets
- scans
- findings
- outbox_events

La autorización debe derivarse siempre de la sesión autenticada del usuario y de su pertenencia a una organización. El cliente no debe poder “elegir” libremente organization_id como autoridad.

## 11. Organización sugerida de carpetas

```text
backend/
  src/
    domain/
    application/
    ports/
    adapters/
      http/
      persistence/
      queue/
      checks/
    worker/
  tests/

frontend/
  src/
    features/
      assets/
      scans/
      findings/
      compliance/

contracts/
  scan-job.schema.json
  finding.schema.json
```

La estructura es orientativa, pero debe mantenerse modular y funcional. No conviene un único archivo que contenga todos los escáneres ni toda la lógica de cumplimiento.

## 12. Seguridad y operación

- Verificar la titularidad del dominio antes de permitir la evaluación.
- Aplicar listas explícitas de activos autorizados y módulos permitidos.
- Limitar frecuencia, concurrencia, tiempo máximo y alcance de cada comprobación.
- Validar los destinos de red y evitar redirecciones fuera del activo autorizado.
- Ejecutar workers aislados con permisos mínimos.
- No concatenar entradas del usuario en comandos de shell.
- No guardar secretos dentro de mensajes de cola ni en logs.
- Registrar quién inició cada evaluación, sobre qué activo y cuándo.
- Definir alertas para trabajos bloqueados, errores repetidos y crecimiento de la cola.

## 13. Evolución por etapas

1. Walking skeleton:
   - login
   - organización
   - activo verificado
   - una comprobación simple
   - persistencia
   - cola
   - visualización del resultado

2. Módulos independientes:
   - nuevos módulos con el mismo contrato de salida
   - alcance y permisos por módulo

3. Cumplimiento e historial:
   - comparación entre evaluaciones
   - control de versiones de reglas

4. Escalado:
   - medir primero
   - separar colas o workers
   - cambiar a Go solo si se demuestra necesidad real

## 14. Decisiones pendientes

- elegir la biblioteca exacta de cola tras pruebas pequeñas,
- definir el esquema relacional final,
- definir la política de retención de evidencia,
- establecer los módulos MVP exactos,
- crear ADRs cuando una decisión estructural cambie de forma significativa.

