# Regole linguistiche — ACP Core

Questo file applica principi di linguaggio chiaro e di linguaggio tecnico controllato alle istruzioni destinate ad agenti AI.

**Fonti di ispirazione (non dichiarazioni di conformità):**
- ISO 24495-1 (Plain language): quattro principi — pertinenza, reperibilità, comprensibilità, usabilità. ACP **non** dichiara conformità formale alla norma.
- Principi generali del linguaggio tecnico controllato (come quelli divulgati per l'Italiano Tecnico Semplificato e per lo Simplified Technical English). ACP **non** riproduce regole proprietarie di alcun metodo: le regole sotto sono una sintesi generale.

## 1. I quattro principi applicati agli agenti

| Principio | Domanda di controllo | Applicazione |
|---|---|---|
| Pertinenza | Questa frase serve all'agente per agire? | Elimina storia, cortesie, ripetizioni. Mantieni vincoli e motivazioni utili. |
| Reperibilità | L'agente trova subito obiettivo e vincoli? | Obiettivo all'inizio. Sezioni con titoli stabili. Un tema per sezione. |
| Comprensibilità | Esiste una sola interpretazione ragionevole? | Termini definiti, riferimenti espliciti, niente pronomi ambigui. |
| Usabilità | L'agente sa quando ha finito? | Criteri di accettazione verificabili e modalità di verifica. |

## 2. Regole di scrittura

R1. **Un termine, un concetto.** Usa sempre lo stesso termine per lo stesso oggetto. Registra i termini nel glossario (`glossary.yaml`).

R2. **Istruzioni atomiche quando l'ordine conta.** Un'azione per passo numerato. Per indicazioni di contesto la prosa va bene.

R3. **Condizione prima dell'azione.** "Se il test fallisce, ripristina il file" — non "ripristina il file se magari qualcosa va storto".

R4. **Soggetto chiaro.** Indica chi agisce: l'agente, l'utente, il sistema CI, l'agente ricevente.

R5. **Verbi operativi.** Preferisci verbi verificabili: *crea, modifica, elimina, esegui, verifica, riporta, non modificare*. Evita *gestisci, sistema, migliora* senza un criterio.

R6. **Riferimenti non ambigui.** Percorsi di file completi, nomi di funzioni, ID di commit, numeri di riga. Evita "quel file", "la funzione di prima".

R7. **Forza normativa esplicita.**

| Forma | Significato |
|---|---|
| DEVI / MUST | Obbligo. La violazione rende il lavoro non accettabile. |
| NON DEVI / MUST NOT | Divieto. |
| DOVRESTI / SHOULD | Raccomandazione: deviare è possibile con motivo dichiarato. |
| PUOI / MAY | Facoltà. |

R8. **Fatti separati dalle ipotesi.** Marca le ipotesi con `[IPOTESI]` e le informazioni non ricontrollate con `[RIPORTATO]`.

R9. **Numeri e unità esplicite.** "Timeout 30 s", non "timeout breve".

R10. **Negazioni semplici.** Una negazione per frase. Evita doppie negazioni.

R11. **Frasi brevi nelle istruzioni.** Indicativamente una frase, un'idea. Non è un limite rigido di parole.

## 3. Rilevazione di contraddizioni

Prima di eseguire un task L1+, controlla le coppie di istruzioni:

- Stesso oggetto con obblighi opposti ("non toccare l'API" + "rinomina l'endpoint /users").
- Vincoli incompatibili ("nessuna nuova dipendenza" + "usa la libreria X" non installata).
- Criteri non soddisfacibili insieme ("latenza < 10 ms" + "chiamata sincrona a un servizio remoto").

Se trovi una contraddizione: **non sceglierne una in silenzio.** Elencala, proponi un'interpretazione, chiedi conferma se il task è L2–L3; per L0–L1 procedi con l'interpretazione più conservativa e dichiarala.

## 4. Esempio di riscrittura

Prima:
> Sistema un po' il login che ogni tanto non va, e già che ci sei rendilo più moderno.

Dopo:
> OBJECTIVE: Correggere il fallimento intermittente del login.
> CONTEXT: [RIPORTATO] Gli utenti segnalano errori occasionali. Causa sconosciuta.
> SCOPE: modulo di autenticazione. "Rendere più moderno" non è definito: [IPOTESI] escluso da questo task salvo conferma.
> ACCEPTANCE CRITERIA: causa identificata con evidenza; test che riproduce il problema e passa dopo la correzione; test esistenti del modulo verdi.
