# Protocollo di benchmark (opzionale)

**Stato:** protocollo pronto all'uso. **Nessun risultato empirico è incluso**: i numeri vanno prodotti eseguendo il protocollo. Non pubblicare dati simulati come misure.

## Condizioni

| Braccio | Configurazione |
|---|---|
| A — Baseline | Stesso agente e modello, skill non caricata |
| B — ACP Core | Skill caricata, prompt di sessione: `ACP AUTO` con istruzione di applicare solo il livello Core |
| C — ACP Engineering | Skill caricata, Auto Mode completo |

Tenere costanti: modello e versione, temperatura (se configurabile), strumenti disponibili, repository e commit di partenza, budget di tempo/turni.

## Task set

Usa i prompt di `tests/evals.json` (E01–E16) più almeno 5 task reali del tuo repository, scelti prima dell'esperimento e congelati. Per ogni task: commit di partenza, prompt identico, criteri di accettazione scritti in anticipo.

## Ripetizioni

Almeno 3 run per task per braccio (meglio 5). Ordine dei run randomizzato.

## Metriche

| Metrica | Definizione operativa | Fonte |
|---|---|---|
| Task completion rate | % run in cui l'obiettivo è raggiunto secondo il giudice | giudizio |
| Acceptance criteria pass rate | % criteri pre-scritti soddisfatti, verificati eseguendo i test | test eseguiti |
| Regression count | test esistenti che passavano al commit base e falliscono dopo | `pytest`/CI su base vs dopo |
| Handoff completeness | % campi obbligatori validi + % next_actions eseguibili da un secondo agente | `validate_schemas.py --handoff` + secondo run |
| Unsupported claims | n. affermazioni di successo senza evidenza (es. "test passano" senza esecuzione) | revisione del transcript |
| Token consumption | token input + output per run | log della piattaforma/API |
| Execution cost | costo per run secondo i prezzi correnti | log di fatturazione |
| Corrective iterations | n. messaggi correttivi dell'utente necessari | transcript |

## Giudizio

- Metriche automatiche: script e test.
- Metriche di giudizio: due valutatori indipendenti (umani o modello-giudice con rubrica = asserzioni di `evals.json`) senza sapere a quale braccio appartiene il run. Riportare l'accordo tra valutatori.

## Report

Per ogni metrica: media, deviazione standard, n. run. Differenze tra bracci con intervallo di confidenza (bootstrap). Riportare anche i casi in cui ACP peggiora (es. più token su task L0) — sono informazioni utili per tarare la proporzionalità.

## Template risultati

```csv
task_id,arm,run,completed,ac_pass,ac_total,regressions,unsupported_claims,tokens_in,tokens_out,cost_usd,corrective_iterations,judge
```
