# Modalità PROMPT — prompt contract

Obiettivo: trasformare una richiesta informale in istruzioni che un agente può eseguire e verificare.

## Sezioni disponibili

Usa **solo** le sezioni che aggiungono informazione. Ordine consigliato:

| Sezione | Contenuto | Quando ometterla |
|---|---|---|
| OBJECTIVE | Una o due frasi: il risultato atteso, non l'attività. | Mai. |
| CONTEXT | Fatti che l'agente non può dedurre: dominio, stato, perché serve. | Se ovvio dall'obiettivo. |
| SCOPE | Cosa è dentro e cosa è fuori. | Task L0. |
| CONSTRAINTS | Obblighi e divieti (MUST / MUST NOT / SHOULD). | Se non ci sono vincoli reali. |
| ACCEPTANCE CRITERIA | Condizioni verificabili di completamento. | Prompt non operativi. |
| VERIFICATION | Come verificare (comandi, test, controlli manuali). | Se coincide con i criteri. |
| DELIVERABLES | Formato e posizione degli output. | Se il formato è ovvio. |

## Regole

1. Non inventare requisiti. Se un requisito utile manca, aggiungilo come `[IPOTESI]` o domanda.
2. Distingui requisiti espliciti (dell'utente) da ipotesi (tue).
3. Criteri di accettazione osservabili: "il comando `pytest tests/auth` termina con 0 fallimenti", non "il login funziona bene".
4. Spiega il **perché** dei vincoli importanti: un agente generalizza meglio da una motivazione che da un ordine.
5. Adatta il prompt al destinatario (Claude, Codex, ChatGPT, sub-agente): stessa struttura, nessun comando specifico di piattaforma inventato.
6. Lunghezza proporzionata: un prompt L0 può essere una frase.

## Template compatto

```markdown
OBJECTIVE: <risultato atteso>
CONTEXT: <fatti necessari>  [IPOTESI] <ipotesi marcate>
SCOPE: IN: <...> | OUT: <...>
CONSTRAINTS:
- MUST: <...>
- MUST NOT: <...>
ACCEPTANCE CRITERIA:
- AC1: <condizione verificabile>
VERIFICATION: <comandi o controlli>
DELIVERABLES: <file, formato>
```

Esempi: `examples/simple-prompt.md`.
