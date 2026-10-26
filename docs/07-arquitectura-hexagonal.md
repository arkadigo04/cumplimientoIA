# Arquitectura hexagonal

Diagrama orientativo de la arquitectura propuesta para el MVP.

```mermaid
flowchart LR
    FE["Frontend"]
    HTTP["Adaptador de entrada<br/>API FastAPI"]

    subgraph APP["Aplicación"]
        UC1["Caso de uso<br/>Solicitar evaluación"]
        UC2["Caso de uso<br/>Procesar evaluación"]
        PDB["Puerto<br/>Guardar y consultar datos"]
        PQ["Puerto<br/>Publicar trabajo"]
        PC["Puerto<br/>Ejecutar comprobaciones"]
    end

    subgraph DOMAIN["Dominio"]
        RULES["Entidades y reglas<br/>Activos · permisos · evaluaciones · hallazgos"]
    end

    PG["Adaptador PostgreSQL"]
    DB[("PostgreSQL")]
    REDIS["Adaptador Redis"]
    QUEUE[("Cola Redis")]
    WC["Adaptador de entrada<br/>Consumidor del worker"]
    CHECK["Adaptadores de comprobación"]
    MODULES["Módulos permitidos"]

    FE -->|"HTTPS + JSON"| HTTP
    HTTP --> UC1
    UC1 --> RULES
    UC1 --> PDB
    UC1 --> PQ

    PDB -. "lo implementa" .-> PG
    PG --> DB

    PQ -. "lo implementa" .-> REDIS
    REDIS --> QUEUE
    QUEUE --> WC
    WC --> UC2

    UC2 --> RULES
    UC2 --> PDB
    UC2 --> PC
    PC -. "lo implementan" .-> CHECK
    CHECK --> MODULES