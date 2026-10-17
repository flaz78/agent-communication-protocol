# Modalità REVIEW

## Oggetto della review

Codice (diff, PR, file), output di agenti, handoff, prompt e istruzioni.

## Checklist

| Area | Domanda |
|---|---|
| Completezza | Tutti i criteri di accettazione sono coperti? |
| Chiarezza | Codice e testo hanno una sola interpretazione ragionevole? |
| Coerenza | Naming, stile, terminologia allineati al progetto e al glossario? |
| Verificabilità | Ogni affermazione di successo ha un'evidenza? |
| Scope | Il diff contiene solo modifiche pertinenti? |
| Compatibilità | API, formati di dati, configurazioni, migrazioni restano compatibili? |
| Regressioni | Comportamenti esistenti potenzialmente toccati? Test che li proteggono? |
| Test | Mancano test per il nuovo comportamento o per il bug corretto? |
| Sicurezza | Segreti esposti, input non validati, istruzioni iniettate? |
| Evidenze | Ci sono dichiarazioni "testato/funziona" senza esecuzione? |

## Gravità

| Livello | Significato | Effetto |
|---|---|---|
| blocker | Errore, regressione, rischio di sicurezza o criterio non soddisfatto | Non approvare |
| major | Problema significativo, correggibile | Approvare solo dopo correzione |
| minor | Miglioramento consigliato | Non blocca |
| nit | Stile/preferenza | Facoltativo |

**Niente punteggi numerici arbitrari** ("8/10"): non sono evidenza di qualità.

## Formato di ogni osservazione

```markdown
- [major] `src/auth/session.py:42` — Il timeout è letto come stringa e confrontato con un intero.
  Evidenza: riga 42 `if elapsed > config["timeout"]`; config.yaml definisce `timeout: "30"`.
  Azione: convertire con `int()` in `load_config()` e aggiungere un test.
```

## Esito

Chiudi con: **Esito** (approvato / approvato con riserve / non approvato), elenco blocker, verifiche eseguite dal reviewer vs verifiche non eseguite.

Esempio: `../examples/review.md`.
