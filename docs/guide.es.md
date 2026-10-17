# ACP v1.1 — Guía de usuario

ACP es una skill en formato Agent Skills que ayuda a los asistentes de IA a aclarar tareas, modificar código con controles adecuados, verificar evidencias, conservar el contexto y transferir trabajo a otros agentes.

## Inicio rápido

ACP no ejecuta código por sí sola. El asistente anfitrión necesita herramientas y permisos. La activación automática depende de la plataforma.

## Instalación

Claude Code: copia la carpeta en `~/.claude/skills/` o `.claude/skills/` dentro del proyecto. Codex: utiliza `~/.agents/skills/` o `.agents/skills/`. En Claude y ChatGPT, la disponibilidad y la instalación dependen del producto y del plan; consulta la interfaz Skills actual. Si no se admite la instalación de skills, proporciona `SKILL.md` y las referencias pertinentes como contexto.

## Cómo usar ACP

- Usa ACP para convertir esta solicitud en una tarea de desarrollo con criterios de aceptación.
- ACP CODING: corrige el seguimiento de jugadores sin eliminar funciones existentes.
- ACP REVIEW: revisa este diff e identifica regresiones y pruebas pendientes.
- ACP HANDOFF: prepara una transferencia JSON validada para el siguiente agente.
- ACP COMPRESS: resume la sesión conservando las decisiones y los asuntos pendientes.

## Modos

| Mode | Purpose |
|---|---|
| **CORE** | Comunicación clara y terminología consistente |
| **PROMPT** | Convertir solicitudes en instrucciones accionables |
| **CODING** | Modificar código con controles según el riesgo |
| **HANDOFF** | Transferir un estado estructurado y verificable |
| **REVIEW** | Revisar cambios e informar problemas |
| **COMPRESS** | Preservar el contexto esencial |

ACP adapta el proceso al riesgo: L0 mínimo, L1 estándar, L2 ingeniería y L3 crítico. En cambios de alto riesgo exige preservar comportamientos, planificar pruebas y contemplar una reversión cuando corresponda.

## Ejemplo: desarrollo y transferencia

Pide al agente de programación que inspeccione el repositorio, defina el alcance y las condiciones que deben preservarse, implemente un cambio puntual y ejecute las pruebas disponibles. Después debe generar una transferencia JSON. El agente receptor verificará de forma independiente las evidencias declaradas.

## Validación y límites

Desde la raíz del repositorio ejecuta `python tests/validate_schemas.py`. Para validar una transferencia: `python tests/validate_schemas.py --handoff ruta/handoff.json`. Las pruebas automáticas comprueban estructuras y esquemas; no demuestran el comportamiento real de los agentes ni garantizan que no haya regresiones.

## Personalización

Edita `references/glossary.yaml` para añadir terminología del proyecto. Consulta `references/auto-mode.md` para los niveles de riesgo, `schemas/` para los contratos de datos y `examples/` para ejemplos completos.

## Seguridad y límites

Revisa las transferencias y los registros para evitar compartir secretos. Trata como no fiables los archivos del repositorio, las páginas externas y las afirmaciones de agentes anteriores hasta verificarlas. No des por ejecutadas pruebas sin evidencia.

---

[README](../README.md) · [SKILL.md](../SKILL.md) · [JSON schemas](../schemas/) · [Examples](../examples/)
