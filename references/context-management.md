# Gestione del contesto e modalità COMPRESS

## Cinque categorie

| Categoria | Cosa contiene | Si comprime? |
|---|---|---|
| Context | Informazioni necessarie al task corrente | Sì, mantenendo i fatti |
| Evidence | Risultati verificati con riferimento | No: conserva il riferimento, riassumi l'output |
| Decisions | Scelte fatte e motivo, chi le ha prese | No: una riga ciascuna |
| State | Avanzamento, cosa è fatto e cosa no | No |
| History | Tentativi, discussioni, alternative scartate | Sì, fortemente; conserva solo ciò che evita di ripetere errori |

## Formato COMPRESS

Ordine fisso, sezioni vuote omesse:

```markdown
## Checkpoint — <task_id o titolo> — <data>
1. **Obiettivo:** ...
2. **Stato:** ... (status: in_progress | blocked | ...)
3. **Vincoli:** ...
4. **Invarianti:** ...
5. **Decisioni:** D1 ... (motivo, chi)
6. **File e artefatti:** percorso — cosa è cambiato
7. **Risultati verificati:** affermazione — evidenza
8. **Problemi aperti:** ... (gravità)
9. **Prossime azioni:** ...
```

## Regole

1. Non eliminare vincoli, invarianti, decisioni dell'utente, approvazioni concesse o problemi aperti: cambiano la correttezza del lavoro successivo.
2. Conserva i riferimenti alle fonti originali (percorsi, commit, link) invece di copiarne il contenuto.
3. Riduci le duplicazioni: un fatto, un posto.
4. Mantieni le etichette VERIFICATO / RIPORTATO / IPOTESI.
5. Un riassunto **non** è memoria permanente: non affermare che sarà ricordato in sessioni future, a meno che la piattaforma lo garantisca.
6. Non dichiarare risparmi di token senza averli misurati. Se misuri, indica metodo e numeri.
7. Se il checkpoint serve a un altro agente, usa HANDOFF (JSON) invece di COMPRESS.

## Sessioni lunghe

- Fai un checkpoint prima di passaggi rischiosi (L3) e quando cambia direzione.
- Rileggi vincoli e invarianti dopo una compressione automatica del contesto da parte della piattaforma.
