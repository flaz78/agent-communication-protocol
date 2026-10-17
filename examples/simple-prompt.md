# Esempi — modalità PROMPT e ACP Core

## Esempio 1 — L0: nessuna struttura aggiuntiva

**Richiesta:** "Rendi più chiaro: *controlla un po' i file e vedi se c'è qualcosa che non va*"

**Output atteso (breve):**
> Controlla i file in `src/` e segnala errori di sintassi, import non usati e funzioni senza test. Non modificare nulla: produci solo un elenco con percorso e riga.

Nota: nessun template OBJECTIVE/SCOPE/…: il task è semplice (test T02).

## Esempio 2 — L1/L2: prompt per un agente di coding

**Richiesta:** "Mi scrivi un prompt per far aggiungere a Codex l'export CSV nella mia app Flask? Non deve rompere l'export Excel che c'è già."

**Output atteso:**

```markdown
OBJECTIVE: Aggiungere l'export CSV dei report, accanto all'export Excel esistente.

CONTEXT:
- App Flask. Esiste già un export Excel (percorso da individuare nel repository).
- [IPOTESI] I dati esportati in CSV sono gli stessi dell'export Excel.

SCOPE:
- IN: modulo di export, route dei report, test relativi.
- OUT: export Excel (solo lettura), modello dati, UI oltre al pulsante di download.

CONSTRAINTS:
- MUST NOT: modificare il comportamento o l'output dell'export Excel.
- MUST NOT: aggiungere dipendenze (il modulo `csv` della standard library è sufficiente).
- SHOULD: riusare la funzione che prepara i dati per l'export Excel.

ACCEPTANCE CRITERIA:
- AC1: una nuova route restituisce un file CSV con le stesse colonne dell'export Excel.
- AC2: i test esistenti dell'export Excel passano senza modifiche.
- AC3: esiste almeno un test per l'export CSV (intestazioni + una riga).

VERIFICATION: esegui la suite di test del progetto e riporta il comando e l'esito. Se non puoi eseguirla, scrivi NON ESEGUITO.

DELIVERABLES: diff, nuovi test, riepilogo di 3–5 righe.
```

Punti da notare:
- L'ipotesi è marcata, non trasformata in requisito.
- Il vincolo dell'utente ("non rompere l'Excel") diventa un MUST NOT e un criterio verificabile (AC2).
- Nessun comando specifico di Codex inventato.
