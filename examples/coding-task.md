# Esempio — modalità CODING (L2)

**Richiesta utente:** "Gli utenti vengono sloggati dopo 5 minuti invece di 30. Correggi."

## 1. Classificazione (interna, non mostrata all'utente)

- Modalità: CODING (auto).
- Livello: L2 — tocca l'autenticazione, componente condiviso; correzione circoscritta ma con rischio di regressione su login/cookie.

## 2. Task contract

Versione JSON validata: `task-contract.json`. Versione Markdown equivalente:

```markdown
OBJECTIVE: Correggere la scadenza prematura delle sessioni senza modificare il formato del cookie.
SCOPE: IN src/auth/session.py, src/config/loader.py, tests/auth/ | OUT formato cookie, DB, UI
INVARIANTI:
- INV1 login/logout invariati → pytest tests/auth/test_login.py tests/auth/test_logout.py
- INV2 formato cookie invariato → pytest tests/auth/test_cookie_format.py
ACCEPTANCE CRITERIA:
- AC1 test di regressione: fallisce prima, passa dopo
- AC2 pytest tests/auth → 0 failed
- AC3 timeout non numerico → errore esplicito all'avvio
```

## 3. Esecuzione (con strumenti disponibili)

1. Baseline: `pytest tests/auth` → registra l'esito **prima** di modificare.
2. Scrivi `tests/auth/test_session_timeout.py` → verifica che fallisca sul codice attuale.
3. Modifica mirata: conversione e validazione del tipo in `load_config()` (non una riscrittura del loader).
4. Riesegui test di regressione, invarianti e suite dell'area.
5. `git diff --stat` → solo file in scope.

## 4. Riepilogo finale atteso

```markdown
**Modifiche:** src/config/loader.py — `session_timeout` convertito in int con errore esplicito se non numerico (righe 31-38). Nuovo test tests/auth/test_session_timeout.py.
**Verifica:** `pytest tests/auth` → 23 passed (prima: 22 passed, 0 failed). Il nuovo test falliva sul commit base.
**Preservato:** INV1 e INV2 verificati dai test indicati.
**Aperto:** [IPOTESI] altri parametri numerici in settings.yaml potrebbero avere lo stesso problema; non verificato.
```

## 4-bis. Stesso task senza accesso al repository (T13)

```markdown
**Modifiche proposte:** (codice nel blocco sopra)
**Verifica:** NON ESEGUITO — nessun accesso al repository. Esegui: `pytest tests/auth`.
**Aperto:** la causa è un'IPOTESI basata sulla descrizione; confermala riproducendo il problema.
```

Il secondo riepilogo non contiene "testato" o "funziona".
