# Modalità CODING — guardrail

## Workflow

| Passo | Azione | Output minimo L1 | Output L2–L3 |
|---|---|---|---|
| 1 | Comprendi l'obiettivo | obiettivo in una frase | task contract |
| 2 | Ispeziona il repository (se accessibile) | file rilevanti letti | mappa componenti + dipendenze |
| 3 | Identifica comportamenti da preservare | — | elenco invarianti |
| 4 | Definisci criteri di accettazione | 1–3 criteri | criteri con metodo di verifica |
| 5 | Implementa le modifiche autorizzate | diff mirato | diff mirato, commit atomici se richiesti |
| 6 | Esegui le verifiche disponibili | test dell'area | suite pertinente + test nuovi + lint/typecheck |
| 7 | Riporta | riepilogo breve | riepilogo con evidenze e problemi aperti |

Per L3 aggiungi prima del passo 5: analisi d'impatto, piano di rollback, conferma per azioni irreversibili.

## Regole obbligatorie

| ID | Regola |
|---|---|
| G1 | Non rimuovere funzionalità senza autorizzazione. |
| G2 | Non introdurre regressioni intenzionali non approvate. |
| G3 | Non modificare contratti API (firme pubbliche, endpoint, formati di dati) se non richiesto. |
| G4 | Non sostituire componenti funzionanti senza motivazione dichiarata. |
| G5 | Non riscrivere moduli interi quando basta una modifica mirata. |
| G6 | Non dichiarare test superati se non sono stati eseguiti. |
| G7 | Non modificare file fuori scope senza dichiararlo e motivarlo. |
| G8 | Non nascondere problemi, warning o test falliti riscontrati. |
| G9 | Non disabilitare, saltare o indebolire test per farli passare. |
| G10 | Non aggiungere dipendenze non necessarie. |

## Protezione dalle regressioni (controlli eseguibili)

Preferisci, in ordine:

1. **Test esistenti** dell'area modificata: eseguili prima (baseline) e dopo.
2. **Test di caratterizzazione**: se un comportamento da preservare non è coperto, scrivi un test che lo fissi *prima* di modificare.
3. **Test di regressione** per il bug corretto: deve fallire prima della correzione e passare dopo.
4. **Controlli statici**: typecheck, lint, build.
5. **Diff review**: controlla che il diff contenga solo modifiche pertinenti (`git diff --stat`).

Se la baseline fallisce già prima della modifica, registralo: un fallimento preesistente non è una regressione introdotta, ma va riportato.

## Senza strumenti o repository

- Consegna codice e istruzioni di verifica.
- Stato delle verifiche: `NON ESEGUITO` con il comando da lanciare.
- Non scrivere "testato", "funziona", "verificato".

## Riepilogo finale (L1+)

```markdown
**Modifiche:** <file e cosa è cambiato>
**Verifica:** <comando> → <esito osservato> | NON ESEGUITO (<motivo>)
**Preservato:** <invarianti controllati>          (L2+)
**Aperto:** <problemi, limiti, ipotesi non verificate>
```

Schema JSON del task contract: `../schemas/task.schema.json`. Esempio: `../examples/coding-task.md`.
