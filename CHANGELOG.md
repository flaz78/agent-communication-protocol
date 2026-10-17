# Changelog

## [1.1.0] — 2026-10-17

### Aggiunto
- Auto Mode: rilevazione dell'intento, override esplicito (`ACP <MODE>`), combinazione di modalità.
- Classificazione del rischio L0–L3 con artefatti proporzionati.
- Architettura a due livelli: ACP Core e ACP Engineering.
- Cinque modalità: PROMPT, CODING, HANDOFF, REVIEW, COMPRESS.
- `schemas/handoff.schema.json` con vincoli di onestà: test `passed`/`failed` richiedono `executed: true`; finding verificati e criteri `met` richiedono evidenze.
- `schemas/task.schema.json` con requisiti condizionali per L2 (invarianti) e L3 (analisi d'impatto, rollback).
- Controlli di coerenza semantica degli handoff (stato vs issue/criteri) e rilevazione di segreti.
- Glossario modificabile (`references/glossary.yaml`).
- Documentazione per piattaforma (`references/platforms.md`) e metadati Codex (`agents/openai.yaml`).
- Catalogo test T01–T15, 15 casi di valutazione LLM (`tests/evals.json`), protocollo di benchmark.

### Verifiche eseguite al rilascio
- `python tests/validate_schemas.py` → 7/7 controlli PASS, sia con il validatore interno sia con controllo incrociato `jsonschema` 4.26 (nessuna discordanza), sia senza `jsonschema` installato.
- 12/12 mutazioni non valide rifiutate, ciascuna per il motivo previsto.
- Validatore ufficiale `quick_validate.py` di skill-creator → "Skill is valid!".

### Non eseguito
- Valutazioni LLM T01–T10, T12–T15 (`tests/evals.json`): richiedono esecuzioni ripetute del modello con la skill caricata. Stato: NON ESEGUITE.
- Benchmark comparativo: solo protocollo; nessun dato empirico.
- Installazione effettiva su ChatGPT e Codex: non provata; istruzioni basate sulla documentazione pubblica di ottobre 2026.

### Public release documentation
- Replaced the repository README with an English landing page.
- Added user guides in English, Italian, French, German, Spanish, and Simplified Chinese.
- Added MIT LICENSE, CONTRIBUTING.md, .gitignore and schema-validation GitHub Actions workflow.
