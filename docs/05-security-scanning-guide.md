# Guía de seguridad para los escaneos

## 1. Propósito y alcance

Esta guía establece cómo diseñar, ejecutar y operar las comprobaciones de seguridad de la plataforma. Complementa [la arquitectura](./01-architecture.md), [el esquema de base de datos](./02-database-schema.md), [los contratos JSON](./03-json-contracts.md) y [la matriz de reglas](./04-security-rules-matrix.md). Para relacionar estas capacidades con marcos como NIS2, CRA y RGPD, consulta el [mapa de cumplimiento](./06-regulatory-security-mapping.md).

El objetivo es evaluar únicamente activos cuya organización haya autorizado, mediante comprobaciones externas acotadas y no intrusivas. Una evaluación no constituye autorización para explotar vulnerabilidades, acceder a cuentas, alterar datos o degradar servicios.

Los controles de esta guía son requisitos de diseño y operación; no implican que todos estén ya implementados.

## 2. Principios que no se deben eludir

- **Autorización verificable:** la propiedad y el alcance deben estar aprobados y persistidos antes de ejecutar cualquier operación de red.
- **Cero confianza en la cola:** un mensaje válido identifica trabajo, pero nunca concede permiso. PostgreSQL es la fuente de verdad.
- **Mínimo alcance y mínimo privilegio:** probar únicamente el activo, protocolo, puerto y módulo autorizados; ejecutar workers con permisos mínimos.
- **No intrusividad:** preferir consultas de lectura y comprobaciones de bajo impacto. No explotar, forzar credenciales, inundar servicios ni modificar el activo.
- **Límites explícitos:** toda operación de red debe tener tiempo máximo, límites de peticiones y concurrencia, y un presupuesto total por evaluación.
- **Trazabilidad y minimización:** registrar lo necesario para auditar; conservar solo evidencia útil y no sensible.
- **Fallo seguro:** si no se puede confirmar autorización, alcance o destino, no se escanea.

## 3. Antes de programar una comprobación

Para cada módulo y regla, documentar:

1. **Finalidad:** qué requisito o configuración comprueba y qué respuesta se considera suficiente.
2. **Activo esperado:** tipo de activo y cómo se relaciona con el objetivo de red.
3. **Permiso necesario:** módulo autorizado y límites de alcance que debe consultar.
4. **Interacción de red:** protocolo, puerto, método/consulta y número máximo de solicitudes.
5. **Riesgo e impacto:** carga, datos que podrían recibirse y condiciones de aborto.
6. **Resultado:** `rule_id` estable, severidad, descripción y evidencia mínima del contrato común.
7. **Límites:** timeout, concurrencia, tamaño máximo de respuesta y presupuesto.
8. **Pruebas:** casos permitidos, denegados, límites, errores y reintentos.

Si una comprobación necesita permisos más amplios o una interacción potencialmente disruptiva, no debe incorporarse como escaneo automático predeterminado. Requiere una decisión de producto, autorización explícita y controles separados.

## 4. Autorización del trabajo y validación de alcance

### 4.1 Validación al solicitar el escaneo

La API debe autenticar al solicitante y comprobar su membresía y permisos en la organización propietaria del activo. No debe confiar en el `organization_id` enviado por el cliente. Antes de crear el trabajo, debe verificar que:

- el activo pertenece a esa organización y está activo;
- la titularidad está verificada (`owner_verified = TRUE`);
- los módulos solicitados están permitidos en `allowed_modules`;
- los objetivos y límites corresponden al `scope` aprobado;
- el usuario puede solicitar esa operación.

La creación del escaneo y de su evento outbox debe ser transaccional, según la arquitectura del sistema.

### 4.2 Segunda validación obligatoria en el worker

Antes de abrir conexiones de red, el worker debe validar el contrato y volver a leer en PostgreSQL el escaneo y el activo. Comprobar, como mínimo:

- que el `scan_id` existe, está en un estado procesable y corresponde al `asset_id` y `organization_id` del mensaje;
- que el activo sigue activo y tiene `owner_verified = TRUE`;
- que cada módulo pedido continúa en `allowed_modules`;
- que el alcance usado procede de la base de datos y cubre exactamente el objetivo;
- que el trabajo no está completado, cancelado o sustituido por un estado incompatible.

Si la autorización se revocó, el activo cambió o los datos no coinciden, el worker debe detener el trabajo sin hacer solicitudes de red y registrar un resultado operativo explícito. No debe completar campos ausentes con valores permisivos ni usar el JSON de la cola como sustituto del alcance persistido.

Validar un mensaje incluye comprobar `schema_version`, UUID, tipos, campos requeridos, módulos conocidos y límites de tamaño. Rechazar versiones desconocidas o entradas malformadas de forma explícita.

## 5. Controles de red y prevención de SSRF

Un destino que parece un dominio autorizado puede resolver a una dirección no permitida. La comprobación debe validar el destino efectivo justo antes de conectar:

- Normalizar y validar nombres de dominio, IP, puerto y esquema contra el alcance guardado. Rechazar sintaxis ambigua, credenciales embebidas, nombres vacíos y formatos no admitidos.
- Aceptar únicamente destinos públicos explícitamente autorizados. Bloquear loopback, redes privadas, link-local, direcciones de metadatos, multicast, no especificadas y otros rangos especiales, tanto IPv4 como IPv6, salvo una política interna aprobada específica.
- Resolver el nombre y comprobar **todas** las direcciones devueltas. Si hay direcciones mixtas permitidas y prohibidas, fallar de forma cerrada.
- Evitar TOCTOU y DNS rebinding: conectar a una dirección que ya se validó, conservar el nombre autorizado para SNI/`Host` cuando aplique y volver a validar en cada conexión nueva. No validar una resolución y luego permitir que el cliente HTTP resuelva libremente otra vez.
- Deshabilitar proxies heredados del entorno salvo que exista un proxy de salida controlado y aprobado.
- Desactivar redirecciones automáticas o validar cada salto con los mismos controles de esquema, host, puerto, resolución y alcance. Limitar el número de saltos.
- Limitar puertos y protocolos mediante listas permitidas. No aceptar URLs, cabeceras, métodos ni opciones arbitrarias directamente desde el mensaje de trabajo.
- Aplicar reglas de salida de red en infraestructura como defensa adicional; la validación de aplicación no las sustituye.

No se debe ampliar el alcance a subdominios, direcciones resueltas, puertos o URLs solo porque sean accesibles desde el activo autorizado. Cada objetivo debe estar cubierto por la política de alcance.

## 6. Ejecución segura y de bajo impacto

- Preferir bibliotecas de protocolo mantenidas y llamadas acotadas frente a procesos del sistema.
- No construir comandos con datos de usuario ni ejecutar shell. Si una dependencia binaria resulta imprescindible, usar argumentos estructurados y `shell=False`, validar el destino igualmente y aplicar límites de proceso.
- Configurar timeout explícito de conexión y de lectura en cada operación; añadir un deadline total para módulo y evaluación. Un timeout individual no limita por sí solo una secuencia larga.
- Limitar concurrencia global, por organización, activo, host y módulo; aplicar rate limiting, pausas y backoff acotado. Los reintentos no deben superar el presupuesto de solicitudes.
- Limitar tamaño de respuesta, número de registros/resultados, profundidad de análisis y memoria/CPU. Cortar la lectura al alcanzar el máximo.
- Evitar consultas que puedan producir transferencia masiva o carga innecesaria. Por ejemplo, no realizar transferencias de zona DNS ni enumeraciones indiscriminadas.
- En comprobaciones HTTP, usar métodos de lectura previstos por el módulo, no enviar cuerpos ni credenciales, y no seguir redirecciones fuera de alcance.
- En TLS, verificar el nombre autorizado mediante SNI y registrar únicamente atributos necesarios del certificado y de la negociación. No deshabilitar validaciones para convertir errores de conexión en resultados positivos.
- Cancelar de forma cooperativa cuando el trabajo se cancele o exceda sus límites. El aislamiento del worker debe impedir acceso innecesario a la red interna, archivos, sockets y credenciales.

## 7. Secretos, privacidad y evidencia

- No incluir tokens, contraseñas, cookies, claves privadas ni credenciales en jobs, hallazgos, trazas o logs.
- No recoger contenido de páginas, datos personales o cuerpos completos de respuestas si basta con metadatos o una señal técnica.
- Redactar cabeceras y valores sensibles antes de registrar excepciones o respuestas de bibliotecas.
- Validar y acotar el tamaño y la estructura de `evidence` antes de persistirla. Tratar cualquier texto recibido del activo como dato no confiable.
- Guardar evidencia suficiente para justificar el hallazgo —por ejemplo, fechas y emisor de un certificado cuando sean relevantes—, no volcados completos de red.
- Escapar contenido no confiable al mostrarlo en la UI o incluirlo en informes; no interpretarlo como HTML, Markdown ejecutable ni instrucciones.
- Definir controles de acceso, retención, eliminación y exportación de evidencia acordes con la organización. No registrar datos sensibles en métricas ni etiquetas.

## 8. Hallazgos correctos e idempotencia

Cada adaptador debe devolver hallazgos conforme al contrato común de [03-json-contracts.md](./03-json-contracts.md). `module` y `rule_id` deben ser estables; la severidad debe pertenecer al conjunto acordado; la evidencia debe ser JSON validado y mínima. Distinguir un hallazgo negativo de un error de comprobación: un timeout o una respuesta inválida no demuestra que el control sea seguro.

Los reintentos y mensajes duplicados no deben duplicar hallazgos para la misma combinación `(scan_id, module, rule_id)`. Implementar deduplicación en persistencia con una restricción única adecuada y escritura idempotente (por ejemplo, upsert); no depender solo de una comprobación previa en memoria. Si una regla necesita varios elementos, definir cómo agruparlos en el hallazgo o ajustar explícitamente la clave y el contrato antes de implementarla.

Actualizar el estado del escaneo y persistir hallazgos de forma consistente. Registrar errores operativos sin convertirlos en hallazgos de seguridad engañosos ni ocultar fallos como éxito.

## 9. Aislamiento y operación de workers

- Separar workers de la API y ejecutar con usuario no privilegiado, sistema de archivos mínimo y límites de CPU, memoria, procesos y tiempo.
- Aplicar segmentación de red y política de salida restrictiva. Los workers no necesitan acceso general a servicios internos.
- Mantener credenciales fuera del código y de la cola; conceder acceso a PostgreSQL/Redis con permisos mínimos y rotación apropiada.
- Mantener dependencias de comprobación actualizadas, fijar versiones en despliegues y revisar cambios que afecten protocolos o comportamiento de red.
- Supervisar profundidad/antigüedad de cola, duración, timeouts, denegaciones de alcance, errores y límites activados. Usar métricas agregadas sin datos del objetivo como etiquetas de alta cardinalidad.
- Alertar sobre repetición de fallos, comportamiento anómalo y cambios de política. Proporcionar cancelación y capacidad operativa para pausar un módulo o workers.
- Registrar quién solicitó el escaneo, activo, módulos, instante, resultado y motivo de denegación. Restringir el acceso a auditoría y protegerla contra alteraciones.

## 10. Pruebas mínimas antes de habilitar un módulo

Comprobar automáticamente que:

- un activo no verificado, inactivo o fuera de alcance no produce ninguna conexión;
- un módulo no permitido y una discrepancia entre mensaje, escaneo y activo se rechazan;
- cambiar o revocar el alcance después de encolar el trabajo bloquea la ejecución;
- direcciones privadas, loopback, link-local, metadata, IPv6 especiales, DNS con respuestas mixtas y redirecciones fuera de alcance se bloquean;
- DNS rebinding, timeouts, respuestas grandes, conexiones lentas y límites de concurrencia no eluden los presupuestos;
- cancelaciones y fallos de red no dejan el escaneo en estado incoherente;
- mensajes duplicados y reintentos no duplican `(scan_id, module, rule_id)`;
- salidas, errores y evidencia no contienen secretos ni datos fuera de lo necesario;
- los casos válidos producen el contrato exacto, y errores de comprobación no se presentan como ausencia de riesgo.

Las pruebas de red deben ejecutarse en entornos controlados y con destinos de prueba propios; no usar activos ajenos como objetivos de validación.

## 11. Lista de verificación para revisión

Antes de aprobar código o habilitar un módulo, responder **sí** a todo:

- [ ] ¿La API y el worker verifican autorización desde PostgreSQL?
- [ ] ¿El objetivo se deriva del alcance aprobado y no de parámetros arbitrarios de la cola?
- [ ] ¿Se valida la IP efectiva y cada redirección antes de conectar?
- [ ] ¿Hay timeouts, límites de tamaño, concurrencia, frecuencia y presupuesto total?
- [ ] ¿La comprobación es no intrusiva y usa permisos mínimos?
- [ ] ¿Los errores son explícitos y no se confunden con resultados seguros?
- [ ] ¿La evidencia se valida, minimiza y protege?
- [ ] ¿La persistencia es idempotente y auditable?
- [ ] ¿Hay pruebas de denegación, casos límite y ausencia de tráfico fuera de alcance?

Si alguna respuesta es **no** o desconocida, el módulo no debe ejecutarse en producción hasta resolverlo.
