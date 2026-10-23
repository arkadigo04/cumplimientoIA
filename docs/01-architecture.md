# Arquitectura del sistema

**Estado:** propuesta inicial para el MVP  
**Alcance:** plataforma B2B de evaluación de seguridad externa y seguimiento de cumplimiento.  
**Principio de seguridad:** solo se procesan activos cuya organización haya verificado y autorizado. Las comprobaciones son acotadas, no intrusivas y sujetas a límites de frecuencia y alcance.

## 1. Objetivos y decisiones

La arquitectura debe:

- Separar las reglas de negocio de la red, la base de datos y las librerías de escaneo.
- Responder rápidamente a las peticiones web y ejecutar las evaluaciones fuera del proceso HTTP.
- Mantener un formato común para los hallazgos de todos los módulos.
- Aislar los datos de cada organización.
- Permitir sustituir una cola, una base de datos o un adaptador sin reescribir el dominio.

### Decisiones iniciales

| Área | Propuesta para el MVP | Motivo |
|---|---|---|
| Backend y workers | Python con FastAPI, Pydantic y tipado estático | Desarrollo rápido y ecosistema de seguridad maduro |
| Persistencia | PostgreSQL | Datos relacionales, transacciones y soporte JSONB |
| Cola | Redis con una biblioteca de trabajos adecuada al MVP | Operación sencilla para empezar |
| Frontend | React y TypeScript | Ecosistema amplio para aplicaciones de panel |
| Ejecución | Contenedores separados para API y workers | Despliegue y escalado independientes |

La base de datos es la fuente de verdad para el estado de una evaluación. La cola transporta trabajos; no sustituye el registro persistente de evaluaciones.

## 2. Vista general

```text
[React + TypeScript]
        |
        | HTTPS / API
        v
[API FastAPI] -------> [PostgreSQL]
        |                    ^
        | publica trabajo    | resultados y estado
        v                    |
   [Cola Redis] ------> [Workers aislados]
                             |
                             v
                   [Adaptadores de comprobación]
```

La API y los workers comparten los contratos de comunicación, pero no tienen que compartir infraestructura interna. La API gestiona usuarios, organizaciones, permisos y solicitudes. Los workers ejecutan trabajos autorizados y persistien resultados mediante puertos definidos.

## 3. Arquitectura hexagonal

El núcleo de negocio no debe importar FastAPI, Redis, un ORM, librerías de red ni herramientas externas.

### Dominio

Contiene conceptos y reglas independientes de la infraestructura:

- Organización, usuario, activo y evaluación.
- Estados de evaluación: `queued`, `running`, `completed`, `failed` y `cancelled`.
- Hallazgos, severidad y reglas de evaluación.
- Reglas que convierten evidencia técnica en resultados de cumplimiento.

El dominio recibe datos y devuelve decisiones. No realiza conexiones de red ni guarda datos por sí mismo.

### Puertos

Interfaces que expresan lo que necesita el dominio o los casos de uso, por ejemplo:

- Repositorio de evaluaciones y hallazgos.
- Publicador de trabajos.
- Adaptador para realizar una comprobación de seguridad.
- Reloj o generador de identificadores, si fueran necesarios para pruebas deterministas.

### Adaptadores

Implementaciones concretas de esos puertos:

- Adaptador HTTP: endpoints FastAPI y validación de entrada.
- Adaptador PostgreSQL: persistencia y transacciones.
- Adaptador Redis: publicación y consumo de trabajos.
- Adaptadores de comprobación: consultas DNS, análisis de TLS u otras comprobaciones aprobadas.
- Adaptador frontend: cliente de la API.

Una librería externa debe quedar detrás del adaptador correspondiente. Así, cambiar una librería no altera las reglas del dominio.

## 4. Flujo de una evaluación

1. Un usuario autenticado solicita una evaluación de un activo asociado a su organización.
2. La API verifica que el usuario puede actuar sobre ese activo y que el activo está verificado y dentro del alcance permitido.
3. La API crea la evaluación en PostgreSQL con estado `queued`.
4. El trabajo se publica en la cola. Para evitar que una caída entre la transacción de base de datos y la publicación deje evaluaciones atascadas, se recomienda una **outbox transaccional**: registrar el evento junto con la evaluación y publicarlo mediante un proceso independiente.
5. Un worker toma el trabajo, valida el contrato y marca la evaluación como `running`.
6. El worker ejecuta únicamente los módulos permitidos y dentro de los límites establecidos.
7. Guarda hallazgos y evidencia estructurada; finalmente marca la evaluación como `completed` o `failed`, con un error operativo explícito cuando corresponda.
8. El frontend consulta el estado y presenta los resultados. La API puede añadir notificaciones en una fase posterior.

Los trabajos deben poder reintentarse de forma segura: procesar dos veces el mismo mensaje no debe duplicar hallazgos ni corromper el estado.

## 5. Contrato de trabajo

El contrato debe versionarse. Los identificadores y el alcance se verifican también contra la base de datos; no se confía en que un mensaje de cola sea autorización suficiente.

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

El worker recupera de la base de datos el activo y el alcance autorizado asociados a `asset_id`. El mensaje no debe contener tokens JWT, contraseñas, secretos ni instrucciones arbitrarias de ejecución.

Cada hallazgo debe seguir un formato común, aunque la evidencia específica de cada módulo pueda variar:

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

`evidence` es información técnica estructurada y validada. En PostgreSQL puede almacenarse como JSONB, conservando columnas relacionales para filtros, relaciones y consultas frecuentes.

## 6. Datos principales

El esquema definitivo se documentará por separado. Como mínimo, el modelo deberá contemplar:

- `organizations`: tenant y configuración.
- `users`: identidad y estado de cuenta.
- `organization_memberships`: relación usuario-organización y permisos.
- `assets`: activos registrados, titularidad, estado de verificación y alcance autorizado.
- `scans`: organización, activo, estado, fechas y versión del contrato.
- `findings`: evaluación, módulo, regla, severidad, descripción y evidencia JSONB.
- `outbox_events`: eventos pendientes de publicar, si se adopta el patrón outbox.

Las consultas de un usuario deben filtrar por la organización derivada de su sesión autenticada, no por un `organization_id` libremente elegido por el cliente. Puede añadirse Row-Level Security de PostgreSQL como defensa adicional, pero no sustituye la autorización correcta en la aplicación.

## 7. Organización de carpetas orientativa

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

Organizad el frontend por funcionalidades y los módulos de comprobación por adaptador o plugin. Evitad un único archivo que concentre todos los escáneres. La estructura es orientativa: debe seguir el tamaño real del proyecto, no convertirse en capas vacías creadas por anticipado.

## 8. Seguridad y operación

- Verificar la titularidad del dominio antes de habilitar evaluaciones sobre él; por ejemplo, mediante un desafío DNS TXT.
- Aplicar una lista explícita de activos y módulos autorizados, con límites de frecuencia, concurrencia y tiempo.
- Rechazar entradas que intenten ampliar el alcance. Validar los destinos de red en el worker y prevenir redirecciones fuera del activo autorizado.
- No construir comandos de shell concatenando datos del usuario. Preferir APIs de librería; si una herramienta externa fuese imprescindible, invocarla con argumentos separados y permisos mínimos.
- Ejecutar workers aislados, sin acceso entrante público, con recursos limitados y acceso de red estrictamente necesario.
- Mantener secretos fuera del repositorio y de los mensajes de cola.
- Registrar quién inició cada evaluación, sobre qué activo y cuándo; evitar guardar datos personales o evidencia innecesaria.
- Definir métricas y alertas para trabajos atascados, fallos repetidos y crecimiento de la cola.

## 9. Evolución por etapas

1. **Walking skeleton:** inicio de sesión, organización, activo verificado, una comprobación inocua, cola, persistencia y visualización del resultado.
2. **Módulos independientes:** incorporar nuevas comprobaciones con el mismo contrato de salida y alcance autorizado.
3. **Cumplimiento e histórico:** vincular hallazgos con controles versionados y comparar evaluaciones.
4. **Escalado:** medir primero; después separar colas, ajustar concurrencia o evaluar workers en Go si existe una necesidad demostrada.

## 10. Decisiones pendientes

- Elegir la biblioteca concreta de cola tras un prototipo pequeño y verificar reintentos, recuperación y observabilidad.
- Definir el esquema relacional y las políticas de retención de evidencia.
- Acordar los módulos exactos y los límites de comprobación permitidos para el MVP.
- Crear ADRs cuando una decisión estructural cambie de forma significativa.
```

Una precisión importante: **no asumiría que esta arquitectura ya está implementada**; es una propuesta inicial. Y cambiaría la promesa de “cero conflictos de código” por “reducir conflictos”: separar carpetas ayuda, pero las interfaces, los contratos y la coordinación siguen siendo necesarios.
