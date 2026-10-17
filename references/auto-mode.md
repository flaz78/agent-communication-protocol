# Auto Mode — selezione di modalità e livello

## Confine di attivazione

Auto Mode opera **dopo** che il sistema ospitante ha caricato la skill. La skill:

- non può garantire la propria attivazione automatica: dipende dal runtime (match della `description`, impostazioni, policy come `allow_implicit_invocation` in Codex);
- non deve comportarsi come se fosse attiva quando non è stata caricata;
- supporta sempre l'attivazione esplicita (vedi `platforms.md`).

## Algoritmo

```
1. explicit = modalità indicata dall'utente ("ACP CODING", "fai una review", ...)
   se presente → modes = [explicit]  (override, test T12)
2. altrimenti → modes = intenti rilevati (intent-detection.md), ordinati:
      PROMPT → CODING → REVIEW → HANDOFF → COMPRESS
   nessun intento ingegneristico → modes = [CORE]
3. level = max(rischio di ogni azione prevista)   (tabella sotto)
4. applica il set minimo di artefatti richiesto dal livello
5. durante l'esecuzione, se emerge un rischio maggiore → alza il livello e dichiaralo
```

L'override esplicito cambia la **modalità**, non abbassa i requisiti di sicurezza: un task ACP PROMPT che richiede di cancellare dati resta soggetto alle regole sulle azioni irreversibili.

## Livelli di rischio

| Livello | Segnali tipici | Artefatti richiesti |
|---|---|---|
| L0 Minimal | typo, rinomina locale, domanda semplice, riformulazione | Nessuno. Applica solo ACP Core. |
| L1 Standard | bugfix circoscritto, funzione nuova isolata, modifica a un file | Obiettivo implicito chiaro, vincoli pertinenti, verifica essenziale (test o esecuzione), riepilogo di 2–4 righe. |
| L2 Engineering | refactoring, feature multi-file, integrazione, modifica a moduli condivisi o API interne | Task contract (Markdown o JSON), invarianti, criteri di accettazione verificabili, test eseguiti, riepilogo finale con evidenze. |
| L3 Critical | migrazione dati/schema, cambi architetturali, cancellazioni, force push, deploy, modifiche a sicurezza/autenticazione/pagamenti | Tutto L2 + analisi d'impatto, piano di verifica, strategia di rollback, conferma esplicita per azioni irreversibili non già autorizzate. |

**Il rischio dipende dall'effetto, non dalla lunghezza.** "Elimina la tabella users in produzione" è breve ma L3. Un prompt di due pagine che chiede di correggere un refuso resta L0.

## Fattori che alzano il livello

- Codice condiviso da molti moduli o API pubbliche.
- Assenza di test nell'area modificata.
- Dati persistenti o stato esterno.
- Azioni non annullabili.
- Requisiti contraddittori o ambigui.
- Codice di sicurezza, autenticazione, pagamenti, privacy.

## Fattori che abbassano il livello

- Modifica coperta da test esistenti.
- Ambiente isolato (branch, sandbox, worktree).
- Richiesta esplicita di prototipo usa-e-getta.

## Combinazioni frequenti

| Richiesta | Sequenza |
|---|---|
| "Implementa X e prepara il lavoro per un altro agente" | CODING → REVIEW → HANDOFF |
| "Scrivimi il prompt per far fare X a Codex" | PROMPT (+ HANDOFF se serve contesto di repo) |
| "Controlla il lavoro dell'agente precedente e continua" | REVIEW → CODING |
| "Siamo a metà, salva lo stato" | COMPRESS (+ HANDOFF se cambia agente) |

Non produrre un handoff JSON per ogni piccola modifica: solo se richiesto o se il lavoro cambia agente/sessione.
