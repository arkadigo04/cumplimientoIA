# Esquema de base de datos

## 1. Objetivo

La base de datos será la fuente de verdad del sistema. Tiene que guardar:
- identidad y permisos,
- tenancy por organización,
- activos verificables,
- evaluaciones y estados,
- hallazgos y evidencia,
- eventos de outbox para trabajos asíncronos.

## 2. Principios

- PostgreSQL es la fuente de verdad.
- La cola no reemplaza el almacenamiento persistente.
- Los datos complejos se almacenan en JSONB.
- Las columnas relacionales se usan para joins, filtros y consultas frecuentes.
- Todas las consultas deben filtrarse por la organización del usuario autenticado.

## 3. Entidades principales

### 3.1 organizations
```sql
CREATE TABLE organizations (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  settings JSONB NOT NULL DEFAULT '{}'
);
```

### 3.2 users
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT,
  display_name TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 3.3 organization_memberships
```sql
CREATE TABLE organization_memberships (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  user_id UUID NOT NULL REFERENCES users(id),
  role TEXT NOT NULL DEFAULT 'member',
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (organization_id, user_id)
);
```

### 3.4 assets
```sql
CREATE TABLE assets (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  name TEXT NOT NULL,
  asset_type TEXT NOT NULL,
  value TEXT NOT NULL,
  verification_status TEXT NOT NULL DEFAULT 'unverified',
  owner_verified BOOLEAN NOT NULL DEFAULT FALSE,
  allowed_modules JSONB NOT NULL DEFAULT '[]',
  scope JSONB NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 3.5 scans
```sql
CREATE TABLE scans (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  asset_id UUID NOT NULL REFERENCES assets(id),
  status TEXT NOT NULL DEFAULT 'queued',
  schema_version INT NOT NULL DEFAULT 1,
  requested_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  started_at TIMESTAMPTZ,
  finished_at TIMESTAMPTZ,
  error_message TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'
);
```

### 3.6 findings
```sql
CREATE TABLE findings (
  id UUID PRIMARY KEY,
  scan_id UUID NOT NULL REFERENCES scans(id),
  module TEXT NOT NULL,
  rule_id TEXT NOT NULL,
  severity TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  remediation TEXT,
  evidence JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 3.7 outbox_events
```sql
CREATE TABLE outbox_events (
  id UUID PRIMARY KEY,
  aggregate_type TEXT NOT NULL,
  aggregate_id UUID NOT NULL,
  event_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'pending'
);
```

## 4. Índices recomendados

```sql
CREATE INDEX idx_assets_organization_id ON assets(organization_id);
CREATE INDEX idx_assets_verification_status ON assets(verification_status);
CREATE INDEX idx_scans_organization_asset ON scans(organization_id, asset_id);
CREATE INDEX idx_scans_status ON scans(status);
CREATE INDEX idx_findings_scan_id ON findings(scan_id);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_outbox_status_created_at ON outbox_events(status, created_at);
```

## 5. JSONB y evidencia estructurada

El campo `evidence` de `findings` debe ser JSONB porque:
- cada módulo puede devolver estructuras distintas,
- la evidencia técnica puede cambiar con el tiempo,
- permite validación y consultas futuras,
- mantiene flexibilidad sin perder orden y trazabilidad.

Ejemplo:
```json
{
  "expires_at": "2026-11-10T00:00:00Z",
  "issuer": "Let's Encrypt",
  "serial_number": "ABC123"
}
```

## 6. Retención de datos

Se recomienda definir una política explícita:
- conservar registros operativos relevantes,
- limitar la evidencia innecesaria,
- eliminar o anonimizar información no exigida por la auditoría,
- separar datos de funcionamiento de datos de historial.

## 7. Restricciones de negocio

- Un activo solo puede pertenecer a una organización.
- Los usuarios solo pueden consultar resultados de su organización.
- Las evaluaciones deben estar vinculadas a un activo real.
- Cada módulo debe estar permitido según el alcance del activo.
- Las operaciones de creación de evaluación + outbox deben ir en la misma transacción.

## 8. Seguridad del esquema

- usar UUIDs como identificadores principales,
- no guardar secretos en columnas normales,
- no confiar en `organization_id` enviado por cliente,
- aplicar filtros por organización en todas las consultas,
- usar PostgreSQL Row-Level Security como defensa adicional si se necesita.
