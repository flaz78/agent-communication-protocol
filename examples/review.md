# Esempio — modalità REVIEW

**Input:** handoff `examples/handoff.json` + diff `3f9c2a1..8b41d07`.

## Verifiche eseguite dal reviewer

| Verifica | Esito | Stato |
|---|---|---|
| Validazione schema handoff | valido | VERIFICATO |
| `pytest -q` | 48 passed | VERIFICATO (rieseguito) |
| `git diff 3f9c2a1..8b41d07 -- src/detector.py` | vuoto | VERIFICATO |
| Benchmark 1080p | — | NON ESEGUITO (GPU non disponibile) |

## Osservazioni

- [major] `src/pipeline/video.py:96` — Il tracker viene istanziato a ogni chiamata di `process_video()`: gli ID non sono stabili tra due chiamate sullo stesso stream.
  Evidenza: riga 96 `tracker = ByteTracker(cfg)` dentro la funzione.
  Azione: istanziare il tracker una volta per stream e aggiungere un test con due chiamate consecutive.

- [major] AC3 (25 fps su 1080p) — `not_verified` nell'handoff e non verificabile qui.
  Azione: eseguire il benchmark prima del merge o declassare AC3 a obiettivo non bloccante con conferma dell'utente.

- [minor] `config/tracking.yaml` — Parametri non documentati in `docs/usage.md` (già in I2).

- [nit] `src/tracking/bytetrack.py:12` — Import `math` non usato.

## Controlli senza osservazioni

Scope rispettato (solo file dichiarati); nessuna nuova dipendenza; API di Detector invariata; nessun segreto nel diff.

## Esito

**Approvato con riserve.** Nessun blocker. Due major da risolvere prima del merge.

Note: nessun punteggio numerico; ogni osservazione ha posizione, evidenza e azione.
