# Esempio — workflow combinato CODING → REVIEW → HANDOFF

**Richiesta utente:** "Implementa il tracking video e poi prepara tutto per far controllare il lavoro a un altro agente."

## Selezione

- Intenti: implementare (CODING) + far controllare (REVIEW + HANDOFF).
- Sequenza: CODING → REVIEW (auto-review del mittente) → HANDOFF.
- Livello: L2 (nuova funzionalità multi-file su pipeline condivisa).

## Passi

| # | Passo | Modalità | Output |
|---|---|---|---|
| 1 | Analizza il repository: pipeline, detector, test esistenti | CODING | mappa componenti |
| 2 | Definisci il task contract (vincoli: API Detector invariata, niente GPL) | CODING | contratto |
| 3 | Implementa `src/tracking/bytetrack.py` e integrazione | CODING | diff |
| 4 | Esegui `pytest -q` (baseline e dopo) | CODING | esiti reali |
| 5 | Auto-review: scope, regressioni, test mancanti, affermazioni senza evidenza | REVIEW | elenco problemi residui |
| 6 | Produci handoff JSON e validalo | HANDOFF | `examples/handoff.json` |

## Cosa dice il mittente all'utente (breve)

> Tracking aggiunto su `feature/bytetrack` (commit 8b41d07). Suite: 48 passed. Non ho potuto eseguire i test di integrazione (manca il video di esempio) né misurare le prestazioni 1080p. L'handoff per il reviewer è in `handoff.json` e passa la validazione dello schema.

## Cosa fa il ricevente (agente di review)

1. `python tests/validate_schemas.py --handoff handoff.json` → valido.
2. Ricontrolla le evidenze critiche: riesegue `pytest -q`, verifica che il diff non tocchi `src/detector.py`.
3. Tratta H1 (prestazioni) come ipotesi; esegue il benchmark se possibile.
4. Produce una review secondo `references/review-rules.md`.

## Variante: modifica piccola

Se la richiesta fosse "correggi il refuso nel log del tracker e fallo controllare", basta un riepilogo di due righe con il diff: **non** serve un handoff JSON completo.
