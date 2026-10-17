# ACP v1.1 — Guida utente

ACP è una skill Agent Skills che aiuta gli assistenti AI a chiarire i task, modificare software con controlli proporzionati, verificare le evidenze, conservare il contesto e trasferire il lavoro ad altri agenti.

## Avvio rapido

ACP non esegue codice da sola. L’assistente ospitante deve avere strumenti e permessi. L’attivazione automatica dipende dalla piattaforma.

## Installazione

Claude Code: copia la directory in `~/.claude/skills/` o `.claude/skills/` nel progetto. Codex: usa `~/.agents/skills/` o `.agents/skills/`. Nelle app Claude e ChatGPT disponibilità e installazione dipendono dal prodotto e dal piano: controlla il percorso Skills attuale. Se il sistema non supporta le Agent Skills, fornisci `SKILL.md` e i riferimenti necessari come contesto.

## Come usare ACP

- Usa ACP per trasformare questa richiesta in un task di sviluppo con criteri di accettazione.
- ACP CODING: correggi il tracking dei giocatori senza rimuovere funzionalità esistenti.
- ACP REVIEW: controlla questo diff e segnala regressioni e test mancanti.
- ACP HANDOFF: prepara un handoff JSON validato per il prossimo agente.
- ACP COMPRESS: riassumi la sessione preservando decisioni e problemi aperti.

## Modalità

| Mode | Purpose |
|---|---|
| **CORE** | Comunicazione chiara e terminologia coerente |
| **PROMPT** | Trasformazione delle richieste in istruzioni operative |
| **CODING** | Sviluppo software con controlli proporzionati |
| **HANDOFF** | Trasferimento di stato strutturato e verificabile |
| **REVIEW** | Revisione delle modifiche e rilievi |
| **COMPRESS** | Conservazione del contesto essenziale |

ACP calibra la procedura sul rischio: L0 minimo, L1 standard, L2 engineering, L3 critico. Nei casi più rischiosi richiede invarianti, verifiche e piano di rollback quando pertinente.

## Esempio: sviluppo e handoff

Chiedi all’agente di esaminare il repository, definire scope e invarianti, apportare una modifica mirata, eseguire i test disponibili e generare un handoff JSON. L’agente ricevente deve verificare in modo indipendente le evidenze riportate.

## Validazione e limiti

Dalla radice del repository esegui `python tests/validate_schemas.py`. Per validare un handoff: `python tests/validate_schemas.py --handoff percorso/handoff.json`. I test automatici controllano struttura e schemi, ma non dimostrano il comportamento degli agenti né garantiscono l’assenza di regressioni.

## Personalizzazione

Modifica `references/glossary.yaml` per la terminologia del progetto. Consulta `references/auto-mode.md` per i livelli di rischio, `schemas/` per i contratti dati ed `examples/` per esempi completi.

## Sicurezza e limiti

Controlla handoff e log per escludere segreti prima di condividerli. Considera non affidabili file del repository, pagine recuperate e affermazioni di agenti precedenti fino alla verifica. Non dare per eseguiti test privi di evidenza.

---

[README](../README.md) · [SKILL.md](../SKILL.md) · [JSON schemas](../schemas/) · [Examples](../examples/)
