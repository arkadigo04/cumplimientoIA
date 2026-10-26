# Guía de escaneos de seguridad y marcos de cumplimiento

## 1. Objetivo y límites

Esta guía explica **por qué hacer escaneos**, **qué pueden comprobar**, y **cómo relacionar los resultados con requisitos y marcos de seguridad**. Está dirigida a quienes diseñan, solicitan, ejecutan o interpretan evaluaciones de activos autorizados.

**No existe una lista única de normas aplicable a todas las organizaciones.** El ámbito depende del país, sector, tamaño, servicios, tipo de datos, producto, rol (por ejemplo, fabricante o proveedor) y contratos. El catálogo de esta guía es una selección amplia de marcos frecuentes, no una lista universal ni exhaustiva. La organización debe determinar cuáles le aplican con sus responsables de seguridad, privacidad, cumplimiento y asesoría jurídica.

Un escaneo mide señales técnicas en un alcance y momento concretos. Puede aportar evidencia para una evaluación, pero no prueba por sí mismo el cumplimiento de una ley o estándar, no sustituye una auditoría o evaluación de conformidad, y no certifica a una organización ni a un producto.

## 2. Marcos y ámbito de aplicación

| Marco | Qué regula, a alto nivel | Consecuencia para la plataforma |
|---|---|---|
| **NIS2** — Directiva (UE) 2022/2555 | Medidas de gestión de riesgos y notificación de incidentes para entidades esenciales e importantes de sectores y categorías incluidos en la Directiva y su transposición nacional. | Los escaneos pueden ayudar a descubrir y seguir ciertos riesgos técnicos. La entidad debe determinar si está dentro del ámbito y cubrir también gobierno, respuesta, continuidad, personas, proveedores y otros controles. |
| **Reglamento de Ejecución (UE) 2024/2690** | Requisitos técnicos y metodológicos detallados para determinadas categorías de entidades digitales incluidas en NIS2. | Cuando aplique, las pruebas deben mapearse a sus requisitos concretos; no extrapolarlos a toda entidad NIS2 ni asumir que un escaneo cubre las medidas organizativas. |
| **CRA** — Reglamento (UE) 2024/2847 | Requisitos de ciberseguridad para productos con elementos digitales y obligaciones de fabricantes y otros actores definidos por el Reglamento. | Escanear un producto no convierte automáticamente a la plataforma en fabricante ni al producto en conforme. Si la plataforma es en sí un producto con elementos digitales, debe analizarse su propio papel y ámbito. |
| **Cybersecurity Act** — Reglamento (UE) 2019/881 | Marco europeo de certificación de ciberseguridad y mandato de ENISA. | Una evaluación automatizada puede aportar pruebas técnicas, pero no otorga una certificación europea ni sustituye el esquema de certificación aplicable. |
| **DORA** — Reglamento (UE) 2022/2554 | Resiliencia operativa digital de entidades financieras incluidas en el ámbito y determinados proveedores TIC. | La gestión de vulnerabilidades y pruebas técnicas pueden apoyar el programa de resiliencia; un escaneo no cubre gobierno TIC, incidentes, continuidad, pruebas avanzadas ni gestión contractual de terceros. |
| **RGPD** — Reglamento (UE) 2016/679 | Protección de datos personales tratados por la organización. | Los escaneos y evidencias deben minimizar datos personales, limitar accesos y retención, y proteger cualquier dato personal que se trate. La aplicabilidad concreta depende de los roles y del tratamiento. |
| **ENS** — Real Decreto 311/2022 (España) | Principios y requisitos de seguridad para sistemas del sector público español y los casos incluidos en su ámbito, como ciertos proveedores que prestan servicios o soluciones al sector público. | Las comprobaciones técnicas pueden aportar evidencia a algunas medidas, pero la categoría del sistema, la Declaración de Aplicabilidad y la conformidad requieren evaluación del sistema completo. |
| **CER** — Directiva (UE) 2022/2557 | Resiliencia de entidades críticas frente a riesgos más amplios, incluidos riesgos físicos y organizativos. | Escaneos digitales tienen un alcance limitado y no verifican la resiliencia física, continuidad integral ni todos los requisitos de la entidad crítica. |
| **PCI DSS** | Requisitos del sector de tarjetas para entidades que almacenan, procesan o transmiten datos de cuenta o pueden afectar al entorno de datos de tarjetas. | Un escaneo puede contribuir a comprobaciones técnicas; ciertos fines de validación externa requieren un proveedor ASV aprobado y procedimientos PCI específicos. |
| **Reglamento Delegado (UE) 2022/30 (RED)** | Requisitos de ciberseguridad para determinadas categorías de equipos radioeléctricos, sujeto a ámbito y fechas aplicables. | Evaluar un dispositivo conectado no equivale a la evaluación de conformidad del equipo ni de sus requisitos específicos. |
| **Reglamento de IA (UE) 2024/1689** | Obligaciones para sistemas y modelos de IA según categoría, rol y calendario de aplicación; incluye requisitos de ciberseguridad para ciertos sistemas de alto riesgo. | El escaneo puede verificar algunos controles técnicos del sistema desplegado; no clasifica jurídicamente el sistema ni comprueba el conjunto de obligaciones de IA. |
| **ISO/IEC 27001** | Norma de sistema de gestión de seguridad de la información, normalmente adoptada voluntariamente o por exigencia contractual. | Los resultados pueden alimentar un proceso de evaluación y mejora; un escaneo no equivale a implantar ni certificar un SGSI. |

Fuentes oficiales:

- [Directiva NIS2 (UE) 2022/2555 — EUR-Lex](https://eur-lex.europa.eu/eli/dir/2022/2555/oj)
- [Reglamento CRA (UE) 2024/2847 — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- [Reglamento DORA (UE) 2022/2554 — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- [Reglamento General de Protección de Datos (UE) 2016/679 — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [Directiva CER (UE) 2022/2557 — EUR-Lex](https://eur-lex.europa.eu/eli/dir/2022/2557/oj)
- [Esquema Nacional de Seguridad, Real Decreto 311/2022 — BOE](https://www.boe.es/eli/es/rd/2022/05/03/311/con)
- [Reglamento Delegado RED (UE) 2022/30 — EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2022/30/oj)
- [PCI DSS — PCI Security Standards Council](https://www.pcisecuritystandards.org/standards/pci-dss/)
- [ISO/IEC 27001 — ISO](https://www.iso.org/standard/27001)

La NIS2 establece una fecha de transposición para los Estados miembros; para obligaciones concretas hay que consultar la norma nacional aplicable y las decisiones de la autoridad competente. El CRA tiene aplicación general desde el **11 de diciembre de 2027**; sus obligaciones de notificación del artículo 14 se aplican desde el **11 de septiembre de 2026**. Verificar siempre el texto consolidado y las disposiciones vigentes al realizar una evaluación.

## 3. Relación entre controles y capacidades del escáner

La siguiente correspondencia es orientativa: relaciona áreas de control con capacidades posibles, no afirma que una herramienta cubra íntegramente esos artículos.

| Área de control | NIS2 | CRA | Capacidad útil de la plataforma | Lo que no cubre el escaneo |
|---|---|---|---|---|
| Inventario y alcance | Contexto para el análisis de riesgos y la gestión de activos | Identificación de componentes y gestión de vulnerabilidades del producto | Inventario de activos autorizados; estado de verificación; módulos y alcance aprobados; historial de cambios | La exactitud del inventario corporativo, la clasificación jurídica del activo o la identificación completa de componentes del producto |
| Gestión de riesgos y medidas técnicas | Art. 21: medidas técnicas, operativas y organizativas proporcionales al riesgo | Art. 13 y anexo I: obligaciones del fabricante y requisitos esenciales de ciberseguridad del producto | Comprobaciones externas configuradas, resultados priorizados, evidencia y seguimiento de remediación | Evaluación integral de riesgos, proporcionalidad, aceptación de riesgo, políticas, responsabilidades y controles internos |
| Vulnerabilidades | Art. 21 incluye gestión y divulgación de vulnerabilidades | Art. 14 y anexo I, parte II: tratamiento de vulnerabilidades y obligaciones de notificación aplicables | Detectar señales técnicas en activos autorizados, registrar hallazgos, recomendar correcciones y volver a comprobar | Desarrollo seguro, triaje completo, coordinación de divulgación, suministro de actualizaciones y cumplimiento de plazos regulatorios |
| Seguridad de servicios y cambios TIC | DORA, entre otros, requiere gestión del riesgo TIC y capacidades de protección, prevención, detección y recuperación | El CRA exige seguridad del producto durante su ciclo de vida | Verificar configuraciones y superficies técnicas dentro del alcance, con historial y remediación | Gestión completa del riesgo TIC, aprobaciones de cambio, políticas internas y responsabilidades de producto |
| Incidentes | Art. 23: notificación de incidentes significativos por las entidades incluidas | Art. 14: notificación por los fabricantes de vulnerabilidades explotadas activamente e incidentes graves que afecten a la seguridad del producto | Mantener trazabilidad de hallazgos, fallos, tiempos y cambios; exportar información técnica necesaria para análisis | Determinar por sí solo si un evento es un incidente notificable, valorar impacto legal, notificar a autoridades o cumplir los plazos de respuesta |
| Continuidad y recuperación | Art. 21 contempla continuidad, gestión de crisis, copias de seguridad y recuperación | Requisitos de seguridad y gestión del producto durante su ciclo de vida | Evidencia puntual de configuración externa y tendencias entre evaluaciones | Planes de continuidad, copias de seguridad, ejercicios, recuperación y gestión de crisis |
| Accesos, personal y proveedores | Art. 21 contempla control de acceso, ciberhigiene, formación y seguridad de cadena de suministro | Obligaciones del fabricante y seguridad del producto en su ciclo de vida | Evaluar únicamente interfaces o activos expresamente incluidos en el alcance | Gestión de identidades, formación, contratos, debida diligencia de proveedores y controles internos |
| Eficacia y auditoría | Art. 21 incluye políticas para evaluar la eficacia de las medidas de gestión de riesgos | Evidencia técnica de pruebas y tratamiento de vulnerabilidades del producto | Informes reproducibles, historial, versión de reglas, alcance y resultados | Auditoría independiente, evidencia de gobierno, políticas aprobadas y evaluación global de eficacia |
| Privacidad y evidencia | La organización debe considerar sus obligaciones legales y de protección de datos | La evidencia puede contener información de usuarios o del producto | Minimización, redacción, control de acceso, retención y exportación limitada | Determinar roles de responsable/encargado, base jurídica, evaluaciones de impacto u otras obligaciones del RGPD |

Como guía para crear un crosswalk verificable (no una afirmación de conformidad):

| Requisito de referencia | Pregunta de evaluación | Prueba técnica posible | Evidencia complementaria necesaria |
|---|---|---|---|
| NIS2, art. 21(2)(e): seguridad en adquisición, desarrollo y mantenimiento, incluida gestión/divulgación de vulnerabilidades | ¿Hay vulnerabilidades técnicas conocidas en los activos/software incluidos y se gestionan? | Inventario/SBOM autorizado, correlación con avisos y comprobaciones no intrusivas. | Política y proceso de vulnerabilidades, responsables, SLA de corrección, divulgación coordinada y registros de parches. |
| NIS2, art. 21(2)(h): políticas y procedimientos para evaluar la eficacia de medidas | ¿Se mide y revisa el control técnico de forma repetible? | Escaneos programados con alcance, reglas y resultados comparables. | Metodología, revisión de falsos positivos, auditoría, acciones correctivas y aprobación del riesgo residual. |
| CRA, anexo I, parte II: gestión de vulnerabilidades del producto | ¿Se identifican componentes/vulnerabilidades y se corrigen durante el periodo de soporte? | Análisis de componentes y comprobaciones técnicas del producto, si el material está autorizado. | SBOM mantenido, proceso de recepción y triaje, actualizaciones, periodo de soporte y documentación técnica. |
| DORA, arts. 5–16 y 24–27 (según la obligación concreta) | ¿La entidad gestiona el riesgo TIC y prueba la resiliencia conforme a su perfil y rol? | Escaneos y pruebas técnicas seleccionadas y controladas. | Marco de gestión aprobado, inventario TIC, respuesta, continuidad, pruebas avanzadas que correspondan y gobierno de terceros. |
| RGPD, art. 32 | ¿Las medidas técnicas y organizativas proporcionan un nivel de seguridad adecuado al riesgo del tratamiento? | Evidencia de configuración técnica que afecte a la confidencialidad, integridad, disponibilidad o resiliencia. | Análisis de riesgo del tratamiento, controles organizativos, accesos, pruebas y evaluación de eficacia; el responsable debe valorar la adecuación. |
| ENS, RD 311/2022, anexo II | ¿Qué medidas concretas aplican a la categoría y sistema evaluado y qué evidencia exige cada una? | Solo las pruebas técnicas ligadas a medidas aplicables y al perfil del sistema. | Categorización, Declaración de Aplicabilidad, políticas, evidencias organizativas y auditoría prevista por ENS. |
| PCI DSS, requisitos 11.3 y 11.4 y demás requisitos aplicables | ¿Se realizaron análisis de vulnerabilidades y pruebas de penetración requeridos para el CDE y su alcance? | Escaneo conforme a alcance y metodología PCI; cuando aplique, escaneo externo por ASV aprobado. | Evidencia del alcance CDE, segmentación, cualificación del proveedor, procedimientos, remediación y demás requisitos PCI. |

Las referencias de artículos son puntos de partida; confirmar texto consolidado, ámbito, medidas nacionales y versión del estándar antes de usarlas como criterio formal.

## 4. Qué mirar en un escaneo y por qué es útil

El plan de escaneo debe seleccionar módulos a partir del objetivo, el tipo de activo y el alcance autorizado. No se debe ejecutar cada comprobación disponible por defecto.

| Área / módulo | Qué se puede observar de forma acotada | Para qué sirve | Qué no demuestra por sí solo |
|---|---|---|---|
| DNS y dominio | Resolución, registros DNS públicos, delegación y configuración publicada; controles de correo como SPF, DKIM y DMARC cuando estén en alcance. | Detectar configuraciones débiles, errores de publicación y señales de suplantación de correo. | Titularidad legal completa, ausencia de abuso, seguridad de todos los proveedores DNS o cumplimiento íntegro de controles de correo. |
| TLS y certificados | Cadena, nombres, fechas, protocolos y parámetros de negociación visibles desde el punto de prueba. | Encontrar certificados caducados o próximos a caducar y configuraciones criptográficas obsoletas. | Seguridad de sesiones de usuario, configuración interna no observable o conformidad criptográfica de todos los sistemas. |
| HTTP y cabeceras | Respuestas y cabeceras de seguridad en rutas expresamente autorizadas; redirecciones y exposición de información técnica. | Señalar configuraciones web que merecen revisión y mejorar defensas del navegador. | Seguridad completa de la aplicación, autorización de usuarios, lógica de negocio o ausencia de fallos explotables. |
| Puertos y servicios expuestos | Servicios accesibles en direcciones y puertos aprobados, con identificación prudente y de baja interacción. | Comparar exposición observada con el inventario y descubrir servicios inesperados. | Inventario completo, vulnerabilidad confirmada ni permiso para explotar o probar otros puertos. |
| Vulnerabilidades conocidas | Versiones o señales identificables, correlacionadas con fuentes de vulnerabilidades, con validación no intrusiva. | Priorizar actualización y análisis manual de componentes aparentemente afectados. | Que una versión identificada sea explotable en ese contexto, que un componente no identificado esté libre de fallos o que no existan vulnerabilidades desconocidas. |
| Aplicación web | Comprobaciones seguras y autenticadas solo si existe autorización y configuración específica; validación con referencias como OWASP ASVS. | Verificar requisitos técnicos concretos, por ejemplo configuración, autenticación o manejo seguro de datos, según las pruebas habilitadas. | Una prueba de penetración completa ni seguridad del código y procesos de desarrollo. Las pruebas autenticadas pueden acceder a datos: requieren cuentas de prueba y límites. |
| Configuración cloud y postura interna | Solo mediante integraciones y credenciales de lectura aprobadas, con permisos mínimos y alcance explícito. | Revisar controles que no son observables desde Internet, como determinadas configuraciones de almacenamiento o identidad. | Cobertura completa de la nube ni seguridad de las identidades si la integración no las evalúa. No se deben introducir credenciales en un escaneo externo. |
| Inventario de software y cadena de suministro | Componentes declarados (SBOM) y versiones, si se reciben como artefacto autorizado; dependencias directas y transitivas según cobertura. | Relacionar componentes con avisos conocidos y priorizar actualización. | Exactitud de un SBOM incompleto, ausencia de componentes en ejecución o seguridad del proveedor. |

Toda comprobación debe mantenerse dentro del alcance, evitar explotación y limitar tráfico, tiempo, concurrencia y tamaño de respuesta conforme a [la guía operativa de escaneos](./05-security-scanning-guide.md). Las pruebas activas, autenticadas, de carga o de explotación requieren autorización y un procedimiento aparte; no forman parte del escaneo externo seguro predeterminado.

### ¿Por qué es útil?

- Da una fotografía reproducible de la superficie técnica expuesta en una fecha concreta.
- Ayuda a encontrar errores de configuración y servicios no esperados antes de que se conviertan en incidentes.
- Permite priorizar correcciones, asignar responsables y verificar si una corrección cambió la señal observada.
- Aporta evidencia técnica fechada para gestión de riesgos, auditorías y seguimiento de medidas.
- Facilita comprobar tendencias, siempre que el alcance y las reglas se mantengan comparables.

Su utilidad depende de la cobertura, actualidad de las reglas, calidad del inventario y validación humana. «Sin hallazgos» significa únicamente que las pruebas ejecutadas no detectaron señales bajo esas condiciones; no significa «seguro» ni «cumple».

## 5. En qué se basa una evaluación de cumplimiento

La evaluación empieza por **requisitos de control**, no por una puntuación global del escáner:

1. **Determinar aplicabilidad.** Identificar jurisdicción, sector, entidad o producto, rol legal, datos tratados, contratos y fecha/versión de la norma. Documentar quién aprobó esta determinación. Una norma que no aplica no debe marcarse conforme: debe justificarse como «no aplicable».
2. **Elegir fuente y versión.** Registrar el nombre oficial, versión, artículos/controles y fecha de vigencia. No mezclar sin documentar ediciones de una norma o perfil.
3. **Definir alcance.** Relacionar cada requisito con sistemas, servicios, entornos, organizaciones y activos incluidos. Una evaluación no se extiende automáticamente a activos no probados.
4. **Definir el criterio de prueba antes de ejecutar.** Especificar qué condición observable satisface el control, qué evidencia cuenta, qué autenticación/permisos se necesitan y qué limita la conclusión. Un ejemplo: «el certificado presentado por este hostname coincide con el nombre autorizado, encadena a una raíz de confianza y no está caducado en la fecha de prueba».
5. **Recoger evidencia con procedencia.** Guardar resultado, activo, momento UTC, módulo, versión de regla, configuración relevante, alcance, limitaciones y referencia al control. No guardar secretos ni respuestas completas innecesarias.
6. **Asignar estado por control, no por escaneo.** Usar estados diferenciados:
   - **Conforme (verificado):** evidencia suficiente satisface el criterio definido para el alcance y fecha.
   - **No conforme (fallo observado):** evidencia válida contradice el criterio.
   - **Parcial:** algunos componentes o subrequisitos pasan y otros fallan o no están cubiertos.
   - **No evaluado / evidencia insuficiente:** no se ejecutó una prueba adecuada, hubo error o falta evidencia. No equivale a conforme.
   - **No aplicable:** responsable competente documenta por qué el control no aplica.
7. **Revisión humana y remediación.** El responsable valida falsos positivos, contexto, impacto, excepción/aceptación de riesgo, prioridad y acciones; después se vuelve a probar y se conserva la evidencia anterior.

La plataforma puede informar que una **comprobación técnica pasó o falló**. Solo una persona o proceso de cumplimiento autorizado puede aprobar el estado del requisito legal, aceptar una excepción o declarar conformidad. No sumar hallazgos ni convertir una puntuación técnica en un «porcentaje de cumplimiento» salvo que exista un método formal, aprobado, versionado y explícitamente limitado.

### Riesgo técnico y conformidad son cosas distintas

La severidad indica prioridad técnica, no el estado legal. CVSS puede ayudar a describir severidad de una vulnerabilidad; contexto de exposición, criticidad del activo, explotación conocida, controles compensatorios e impacto del negocio también influyen en el riesgo. Ningún CVSS, CVE, catálogo de amenazas ni ausencia de CVE acredita por sí solo cumplimiento. Registrar la fuente y fecha de cualquier inteligencia utilizada; permitir revisión contextual.

## 6. Catálogo orientativo de normas y marcos de referencia

No todos son leyes ni todos pueden comprobarse con un escáner. Antes de usarlos, verificar edición vigente, adopción contractual/nacional, alcance y requisitos de evaluación.

### Leyes y reglamentos (obligatorios cuando aplican)

| Marco | Ámbito típico | Aporte posible del escáner |
|---|---|---|
| NIS2 y transposición nacional | Entidades esenciales/importantes incluidas y sectores definidos. | Evidencia parcial sobre exposición, vulnerabilidades y seguimiento; no cubre gobierno, organización ni todos los controles del art. 21. |
| CRA | Productos con elementos digitales y obligaciones por rol, especialmente fabricantes. | Señales sobre activos/versiones y evidencia para el proceso de vulnerabilidades; no realiza la evaluación de conformidad del producto. |
| DORA | Entidades financieras y otros sujetos expresamente incluidos. | Evidencia de pruebas y vulnerabilidades TIC; no valida el marco de gestión de riesgo TIC, respuesta, continuidad, pruebas de resiliencia ni terceros completo. |
| RGPD | Tratamientos de datos personales. | Ayuda a detectar exposición técnica que podría afectar a datos; no determina base jurídica, roles, derechos, evaluación de impacto ni cumplimiento global. |
| ENS (España) | Sector público y supuestos incluidos en el ámbito del RD 311/2022. | Evidencia para medidas técnicas concretas; no determina categoría ni sustituye auditoría, declaración de aplicabilidad o evaluación de conformidad. |
| CER | Entidades críticas incluidas en la transposición nacional. | Aporte limitado a superficie digital; no evalúa resiliencia física, organizativa ni continuidad integral. |
| RED, Reglamento Delegado 2022/30 | Categorías de equipos radioeléctricos y requisitos aplicables según el Reglamento. | Puede aportar pruebas técnicas específicas autorizadas; no sustituye evaluación de conformidad del equipo. |

### Estándares, esquemas, normas sectoriales y marcos de buenas prácticas

| Marco | Tipo / utilidad | Qué puede probar un escáner |
|---|---|---|
| ISO/IEC 27001 y 27002 | Sistema de gestión de seguridad de la información y catálogo de controles. | Evidencia técnica de algunos controles seleccionados; no políticas, liderazgo, auditoría interna, análisis de riesgos ni certificación. |
| ISO/IEC 27017 y 27018 | Controles y privacidad para servicios cloud / datos personales en nube, según ámbito de la edición aplicable. | Señales técnicas en configuraciones cloud solo si hay integración autorizada; no contratos, responsabilidades compartidas ni controles organizativos. |
| ISO/IEC 27701 | Sistema de gestión de información de privacidad. | Aporte puntual a controles técnicos de privacidad; no verifica el sistema de gestión completo. |
| ISO 22301 | Gestión de continuidad de negocio. | Puede aportar señales de disponibilidad observada; no verifica análisis de impacto, planes, ejercicios ni recuperación. |
| IEC 62443 | Seguridad de sistemas de automatización y control industrial, con distintos estándares y roles. | Solo pruebas OT específicamente autorizadas, compatibles y de bajo impacto. Escaneos IT genéricos pueden afectar sistemas industriales; no ejecutar sin validación del operador. |
| PCI DSS | Estándar sectorial para entornos que manejan datos de tarjetas o pueden afectar a su seguridad. | Comprobaciones técnicas acotadas. Para validación formal de determinados escaneos externos puede exigirse un ASV y el proceso PCI correspondiente. |
| NIST CSF 2.0 y NIST SP 800-53 | Marcos voluntarios/de referencia para gobernar y seleccionar resultados y controles de ciberseguridad; uso regulatorio puede depender de contrato o sector. | Evidencia técnica asociable a controles elegidos; no implementación del programa completo. |
| CIS Controls v8.1 y CIS Benchmarks | Salvaguardas priorizadas y recomendaciones de configuración para tecnologías concretas. | Comprobación de configuraciones solo cuando el módulo y acceso tienen cobertura expresa; no asumir que una recomendación CIS es ley. |
| OWASP ASVS | Requisitos de verificación de seguridad de aplicaciones web y servicios. | Base concreta para pruebas de requisitos técnicos seleccionados; muchos requisitos requieren pruebas autenticadas, revisión de diseño/código o análisis manual. |
| OWASP Top 10 / OWASP API Security Top 10 | Listas de concienciación de riesgos frecuentes, no listas completas de requisitos de conformidad. | Orientar casos de prueba; no usar la ausencia de sus categorías como prueba de aplicación segura. |
| SOC 2 Trust Services Criteria | Criterios usados en informes de aseguramiento, normalmente mediante auditoría de un proveedor autorizado. No es una certificación legal universal. | Evidencia técnica complementaria; no produce un informe SOC 2 ni sustituye la auditoría independiente. |

### Referencias técnicas que no son normas de cumplimiento

- **CVE** identifica vulnerabilidades divulgadas; **CWE** clasifica debilidades; **CVSS** estima severidad técnica. Son referencias para priorizar, no leyes ni certificados.
- **MITRE ATT&CK** organiza tácticas y técnicas observadas de adversarios. Sirve para diseñar detección y pruebas defensivas, no para declarar cumplimiento normativo.
- **CISA Known Exploited Vulnerabilities (KEV)** y **EPSS** pueden ayudar a contextualizar priorización cuando la fuente y fecha se documenten; no sustituyen el análisis del activo ni imponen universalmente un estado legal.

## 7. Requisitos de producto derivados para la plataforma

Para que las evaluaciones sean utilizables en un programa de cumplimiento:

1. **Mantener un alcance auditable.** Guardar activo, organización, titularidad verificada, módulos permitidos, versión del alcance, solicitante, fechas y resultado. El worker debe volver a validar permisos desde PostgreSQL antes de conectar, como exige la [guía de seguridad para los escaneos](./05-security-scanning-guide.md).
2. **Describir cobertura y límites.** Cada informe debe indicar módulos ejecutados, activos incluidos, fecha, versión de reglas, comprobaciones omitidas, errores y limitaciones. No presentar la falta de hallazgos como prueba de ausencia de vulnerabilidades.
3. **Permitir tratamiento del riesgo.** Registrar prioridad, responsable, estado de remediación, justificación de aceptación y evidencia de reevaluación sin convertir una recomendación automática en una decisión legal.
4. **Separar hallazgo, vulnerabilidad e incidente.** Un hallazgo técnico es una observación; no implica automáticamente vulnerabilidad confirmada, explotación, incidente significativo ni obligación de notificación.
5. **Facilitar trazabilidad y exportación.** Proporcionar informes legibles y datos estructurados con procedencia, marcas de tiempo y versiones; restringir exportaciones a usuarios autorizados y registrar accesos relevantes.
6. **Proteger los datos.** Evitar capturar contenido innecesario, secretos y datos personales; aplicar retención y borrado configurables, protección de evidencia y controles por organización.
7. **No automatizar decisiones regulatorias sin revisión.** La clasificación de entidades, productos, incidentes, plazos y autoridades responsables requiere procesos y responsables definidos por la organización.

## 8. NIS2: aspectos que no debe ocultar un informe

El artículo 21 de NIS2 cubre un conjunto más amplio que la seguridad técnica observable desde Internet, entre otros: análisis de riesgos y políticas de seguridad, gestión de incidentes, continuidad y recuperación, seguridad de la cadena de suministro, seguridad en adquisición/desarrollo/mantenimiento, tratamiento y divulgación de vulnerabilidades, evaluación de eficacia, ciberhigiene y formación, criptografía, control de acceso y activos, y autenticación multifactor cuando proceda.

Por ello, un informe debe identificar claramente que sus resultados son **evidencia técnica parcial** y enlazarlos a los procesos internos de riesgo y remediación. La evaluación de si una entidad está sujeta a NIS2, qué medidas nacionales aplican y si un incidente debe notificarse corresponde a la entidad con asesoramiento competente.

Para incidentes significativos, el artículo 23 establece un proceso escalonado: alerta temprana dentro de las 24 horas desde que se tiene conocimiento, notificación del incidente dentro de las 72 horas e informe final, por regla general, dentro de un mes desde la notificación. La clasificación del incidente, el cómputo aplicable y el canal de comunicación deben verificarse con la autoridad competente y la transposición nacional.

## 9. CRA: aspectos específicos para fabricantes

El CRA se centra en productos con elementos digitales y asigna obligaciones según el rol de los actores y el ámbito del producto. Para el fabricante, el Reglamento incluye requisitos de ciberseguridad durante el ciclo de vida y tratamiento de vulnerabilidades; el anexo I aborda, entre otras materias, la identificación y documentación de vulnerabilidades y componentes, la gestión de vulnerabilidades y las actualizaciones de seguridad.

El artículo 14 introduce notificaciones para las categorías de vulnerabilidades e incidentes que define el propio texto. El escáner puede aportar observaciones y marcas de tiempo, pero no decide automáticamente si se alcanza el umbral legal, quién es el fabricante responsable, ni si una notificación es exigible. La organización debe disponer de un proceso de recepción, validación, escalado y notificación que cubra productos, roles y plazos aplicables.

El artículo 14 establece, para los casos incluidos en su ámbito, una alerta temprana dentro de las 24 horas y una notificación dentro de las 72 horas desde que el fabricante tiene conocimiento. El informe final tiene plazos diferenciados: hasta 14 días después de que esté disponible una medida correctiva o mitigadora para una vulnerabilidad explotada activamente, y hasta un mes después de la notificación para un incidente grave que afecte a la seguridad del producto. Confirmar los desencadenantes, destinatarios, canal y obligaciones vigentes con asesoramiento especializado.

No debe etiquetarse un producto como «CRA conforme» basándose únicamente en que no se encontraron hallazgos. La evaluación de conformidad, documentación técnica, obligaciones de fabricante, soporte del producto y demás requisitos quedan fuera del alcance de un escaneo externo puntual.

## 10. Uso de resultados en una evaluación de cumplimiento

Una organización puede usar los resultados de esta plataforma como entrada para:

- actualizar su inventario y análisis de riesgos;
- priorizar medidas correctivas y verificar su implantación;
- aportar evidencia técnica fechada a controles internos o auditorías;
- identificar activos que requieren pruebas adicionales o intervención del responsable;
- apoyar la evaluación de incidentes, siempre con análisis humano y proceso formal.

Al preparar una evidencia, conservar contexto suficiente para reproducirla (alcance autorizado, fecha, módulo y versión de reglas), pero excluir datos innecesarios. Relacionar cada hallazgo con el control interno aplicable solo cuando exista una correspondencia aprobada por la organización; evitar asignaciones automáticas que sugieran certificación o cumplimiento legal.

## 11. Fuentes y referencias operativas

- [Reglamento de Ejecución NIS2 (UE) 2024/2690 — EUR-Lex](https://eur-lex.europa.eu/eli/reg_impl/2024/2690/oj)
- [Cybersecurity Act (UE) 2019/881 — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2019/881/oj)
- [Reglamento de IA (UE) 2024/1689 — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [NIST Cybersecurity Framework 2.0 — NIST](https://www.nist.gov/cyberframework)
- [NIST SP 800-53 — NIST CSRC](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [CIS Critical Security Controls — CIS](https://www.cisecurity.org/controls)
- [OWASP ASVS — OWASP](https://owasp.org/www-project-application-security-verification-standard/)
- [IEC — ciberseguridad industrial y serie IEC 62443](https://www.iec.ch/cyber-security)
- [ISO/IEC 27001 — ISO](https://www.iso.org/standard/27001)
- [PCI DSS — PCI Security Standards Council](https://www.pcisecuritystandards.org/standards/pci-dss/)

- Para autorización, SSRF, límites de red, minimización y pruebas seguras, seguir [Guía de seguridad para los escaneos](./05-security-scanning-guide.md).
- Para los pasos del worker, consultar [Arquitectura del sistema](./01-architecture.md).
- Para estructura de evidencia y hallazgos, consultar [Contratos JSON](./03-json-contracts.md).
- Para titularidad, módulos permitidos y persistencia de resultados, consultar [Esquema de base de datos](./02-database-schema.md).

Revisar este mapa cuando cambien la normativa, la transposición nacional, el alcance del producto o las capacidades de escaneo. Antes de utilizarlo como matriz formal de cumplimiento, validarlo con las funciones jurídica, de privacidad y de seguridad responsables.
