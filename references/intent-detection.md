# Intent detection

Usa la comprensione linguistica del modello. Le tabelle sotto sono **segnali**, non regole a parole chiave: decide il significato della richiesta.

## Segnali per modalità

| Modalità | Segnali (IT) | Segnali (EN) | Oggetto tipico |
|---|---|---|---|
| PROMPT | scrivi/migliora un prompt, istruzioni per l'agente, rendi la richiesta chiara per Claude/Codex | write a prompt, system prompt, instructions for the agent | testo destinato a un modello |
| CODING | correggi, implementa, aggiungi, refactor, debug, migra, ottimizza, fai funzionare | fix, implement, add, refactor, debug, migrate | codice, repository, test |
| HANDOFF | passa a, prepara per Codex/Claude Code, consegna a un altro agente, continua domani | hand off, prepare for, transfer to | stato del lavoro |
| REVIEW | controlla, revisiona, è corretto?, è pronto per il merge?, valuta | review, check, audit, is this ready | diff, PR, output, prompt |
| COMPRESS | riassumi la sessione, checkpoint, stato attuale, contesto troppo lungo | summarize session, checkpoint, compact | conversazione |
| CORE | rendi più chiaro, riscrivi in modo preciso, elimina ambiguità | clarify, rewrite clearly | qualsiasi testo operativo |

## Casi ambigui

| Richiesta | Interpretazione | Motivo |
|---|---|---|
| "Rivedi questo codice" + diff | REVIEW | valutazione, non modifica |
| "Rivedi questo codice e sistemalo" | REVIEW → CODING | due azioni |
| "Scrivi il codice per X" senza repo né strumenti | CODING senza esecuzione | consegna codice + comandi di verifica, nessun test dichiarato |
| "Fai un prompt per correggere il bug Y" | PROMPT | l'utente vuole istruzioni, non la correzione |
| "Correggi il bug Y" con strumenti disponibili | CODING | esegui, non trasformarlo in prompt |
| "Riassumi questo articolo" | Nessuna modalità ACP | non è comunicazione tra agenti; ACP Core facoltativo |

## Override esplicito

Forme riconosciute: `ACP PROMPT`, `ACP CODING`, `ACP HANDOFF`, `ACP REVIEW`, `ACP COMPRESS`, `ACP AUTO`, oppure "usa la modalità review". Sono modalità logiche della skill, **non** comandi nativi delle piattaforme. `ACP AUTO` ripristina la selezione automatica.

## Quando non usare ACP

Chiacchiera, domande fattuali, scrittura creativa, traduzioni, riassunti di contenuti non operativi. In questi casi non aggiungere strutture ACP.
