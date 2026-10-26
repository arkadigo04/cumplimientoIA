# Matriz de reglas de seguridad y cumplimiento

## 1. Objetivo

La plataforma debe aplicar una política explícita de seguridad para cada paso del flujo:
- autenticación,
- autorización,
- ejecución del trabajo,
- almacenamiento,
- presentación de resultados.

## 2. Dimensiones de control

| Área | Riesgo | Regla | Responsable |
|---|---|---|---|
| Autorización | Acceso no autorizado | Validar organización y permisos en cada request | API |
| Alcance | Escaneo fuera del dominio permitido | Recuperar alcance autorizado desde BD | Worker |
| Cola | Confianza indebida en mensajes | No usar el mensaje como autorización | API + Worker |
| Secretos | Exposición de credenciales | No incluir secretos en payload ni logs | API + Worker |
| Ejecución | Inyección o comandos arbitrarios | No concatenar entradas del usuario | Worker |
| Red | Conexiones fuera de alcance | Validar destinos y límites de red | Worker |
| Frecuencia | Abuso de recursos | Limitar peticiones, tiempo y concurrencia | API + Worker |
| Auditoría | Falta de trazabilidad | Registrar quién, qué y cuándo | API |
| Evidencia | Recolección innecesaria | Almacenar solo lo necesario | Worker |
| Resultado | Hallazgos inconsistentes | Normalizar y validar cada hallazgo | Worker |

## 3. Reglas por categoría

### 3.1 Autorización
- El usuario debe pertenecer a la organización del activo.
- La evaluación debe vincularse al activo correcto.
- `organization_id` no debe usarse como autoridad a partir del cliente.

### 3.2 Alcance y permisos
- El activo debe estar verificado.
- El módulo debe estar permitido para ese activo.
- El worker debe validar el alcance desde la base de datos.

### 3.3 Mensajes asíncronos
- la cola no sustituye la autorización,
- los mensajes deben ser mínimos,
- los consumidores deben validar contratualmente cada payload.

### 3.4 Ejecución segura
- no concatenar strings del usuario en comandos,
- no ejecutar instrucciones arbitrarias,
- limitar tiempo y concurrencia por módulo,
- ejecutar workers con permisos mínimos.

### 3.5 Evidencia
- guardar solo evidencia necesaria,
- evitar datos sensibles innecesarios,
- mantener consistencia en severidad, título y descripción.

## 4. Matriz funcional de seguridad

| Control | Tipo | Implementación | Evidencia |
|---|---|---|---|
| Verificación de titularidad | Preventivo | validación del dominio | registros de verificación |
| Control por organización | Preventivo | memberships + permisos | base de datos |
| Autorización por activo | Preventivo | validaciones en API y worker | scans + assets |
| Contrato versionado | Preventivo | schema_version | payload JSON |
| Idempotencia | Correctivo | scan_id + deduplicación | BD / job state |
| Outbox transaccional | Correctivo | outbox_events | base de datos |
| Alcance acotado | Preventivo | módulos y límites por activo | configuración y logs |
| Auditoría | Detectivo | user_id, asset_id, timestamps | trazas y BD |
| Hallazgos normalizados | Preventivo | formato estándar | findings table |

## 5. Política recomendada

La plataforma debe cumplir estas reglas:
- mínimo privilegio,
- validación explícita de permisos,
- separación entre dominio e infraestructura,
- reintentos seguros e idempotentes,
- trazabilidad completa,
- registros de auditoría y métricas.

## 6. Regla de no aceptación

Se debe rechazar cualquier flujo que:
- ejecute activos no verificados,
- permita módulos fuera de alcance,
- dependa de mensajes de cola como autorización,
- almacene secretos en logs o base de datos sin necesidad,
- mezcle reglas de negocio con ejecución de red o procesos del sistema.

## 7. Conclusión

La seguridad no es un añadido opcional; es una propiedad del diseño. Si la autorización, el alcance, la cola, la persistencia y la validación no están correctamente separadas, el sistema pierde integridad y confianza.

Si quieres, puedo hacer ahora el siguiente paso real: dejarte la estructura completa del backend en Python con FastAPI, incluyendo:
- carpetas,
- modelos,
- endpoints,
- puertos y adaptadores,
- workers de cola,
- y el primer flujo completo “crear evaluación → publicar job → procesar → guardar hallazgos”.