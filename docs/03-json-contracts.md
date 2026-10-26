# Contratos JSON

## 1. Propósito

Los contratos JSON definen la interfaz entre:
- API y workers,
- workers y almacenamiento,
- frontend y backend.

Su objetivo es:
- evitar ambigüedad,
- estandarizar comunicación,
- mantener compatibilidad,
- permitir versionado claro.

## 2. Principios

- todo contrato debe ir versionado,
- el consumidor debe validar el payload,
- la cola nunca debe sustituir la autorización,
- los secretos no deben viajar dentro del mensaje,
- los mensajes deben ser mínimos y explícitos.

## 3. Contrato de trabajo: scan job

### Ejemplo
```json
{
  "schema_version": 1,
  "event_id": "8d881f62-0d48-4df0-b7ee-83d6e5d20b7e",
  "scan_id": "12f58d0d-9689-4789-b2f7-13bce12d8110",
  "organization_id": "d0ef5ec6-1b9f-4d95-b77f-347df47014bd",
  "asset_id": "2cbee4a7-b7ba-43b5-b214-251aeedca6be",
  "modules": ["dns_email", "tls"],
  "created_at": "2026-10-23T12:00:00Z"
}
```

### Reglas
- `schema_version` es obligatorio.
- `event_id` debe ser único.
- `scan_id` debe existir y estar asociado a una evaluación real.
- `organization_id` y `asset_id` deben corresponder al mismo activo.
- `modules` debe ser una lista válida y permitida.
- no incluir JWT, tokens, secretos o instrucciones arbitrarias.

## 4. Contrato de hallazgo

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

### Campos recomendados
- `module`: módulo responsable
- `rule_id`: identificador único y estable
- `severity`: low / medium / high / critical
- `title`: resumen breve
- `description`: explicación humana
- `evidence`: estructura técnica validada
- `remediation`: recomendación concreta

## 5. Contrato de respuesta de API

```json
{
  "id": "12f58d0d-9689-4789-b2f7-13bce12d8110",
  "organization_id": "d0ef5ec6-1b9f-4d95-b77f-347df47014bd",
  "asset_id": "2cbee4a7-b7ba-43b5-b214-251aeedca6be",
  "status": "completed",
  "created_at": "2026-10-23T12:00:00Z",
  "updated_at": "2026-10-23T12:10:00Z",
  "modules": ["dns_email", "tls"],
  "summary": {
    "total_findings": 4,
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 1
  }
}
```

## 6. Versionado

Se recomienda:
- `schema_version` en mensajes de cola,
- versionado explícito de los contratos,
- compatibilidad hacia atrás cuando sea posible,
- nuevo `schema_version` si cambia el significado de un campo.

## 7. Reglas de compatibilidad

- no romper un campo existente sin versionado,
- no cambiar el tipo de un campo sin acordarlo,
- validar cada payload antes de persistirlo o enviarlo,
- mantener un formato estable de salida para frontend y clientes.

## 8. Validación

Cada payload debe validarse antes de:
- publicarse en cola,
- procesarse en el worker,
- almacenarse en PostgreSQL,
- entregarse al frontend.

Esto reduce errores de integración y facilita la observabilidad.
