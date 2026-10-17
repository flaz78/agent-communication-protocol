# Piattaforme: installazione e attivazione

Informazioni verificate a ottobre 2026 sulla documentazione pubblica disponibile. Le piattaforme cambiano: controlla la documentazione ufficiale corrente prima di distribuire.

**Principio:** installare la skill non significa che verrà attivata automaticamente in ogni ambiente. L'attivazione implicita dipende dal runtime, che confronta la richiesta con il campo `description`. L'attivazione esplicita è sempre il fallback.

## Formato comune

Agent Skills: una cartella con `SKILL.md` (frontmatter YAML con `name` e `description`) e file di supporto. `name` in kebab-case (max 64 caratteri); `description` max 1024 caratteri, senza parentesi angolari. Un solo `SKILL.md` per skill.

## Claude Code

- Utente: `~/.claude/skills/agent-communication-protocol/`
- Progetto: `.claude/skills/agent-communication-protocol/` (versionabile con il repository)
- Attivazione implicita: il modello carica la skill quando la richiesta corrisponde alla descrizione.
- Attivazione esplicita: `/agent-communication-protocol` oppure chiedere "usa la skill ACP".

## App Claude (web, desktop, mobile)

- Carica lo ZIP dalla sezione Skills delle impostazioni (la posizione esatta del menu può variare tra versioni e piani; per i piani organizzativi può servire l'abilitazione da parte di un amministratore).
- Lo ZIP deve contenere la cartella della skill con `SKILL.md` al suo interno.
- Attivazione: implicita tramite descrizione; esplicita chiedendo "usa la skill agent-communication-protocol" o scrivendo `ACP <MODE>`.

## OpenAI Codex (CLI, IDE)

- Repository: `.agents/skills/agent-communication-protocol/` (Codex cerca anche nelle cartelle padre fino alla root del repo)
- Utente: `~/.agents/skills/agent-communication-protocol/`
- Attivazione esplicita: `/skills` oppure `$agent-communication-protocol` nel prompt.
- Il file opzionale `agents/openai.yaml` incluso definisce nome visualizzato e la policy `allow_implicit_invocation`.
- Nota: se l'elenco delle skill supera il budget di contesto, Codex può accorciare le descrizioni o ometterne alcune; per questo la descrizione è concisa e mette i trigger principali all'inizio.

## ChatGPT

- La documentazione pubblica mostra le skill nella barra laterale Skills dell'app desktop e l'invocazione esplicita con `@` + nome skill; la distribuzione avviene tramite plugin o creazione nell'app. Non è documentata, a ottobre 2026, una procedura di upload dello ZIP equivalente a quella delle app Claude.
- Fallback universale: incolla il contenuto di `SKILL.md` (e i riferimenti necessari) nelle istruzioni personalizzate di un progetto o di un GPT.

## Altri runtime compatibili con Agent Skills

Molti framework multi-agente leggono `SKILL.md` dalla filesystem. In assenza di supporto:

- usa `SKILL.md` come prompt di sistema del sub-agente;
- usa `schemas/handoff.schema.json` come contratto tra agenti (validabile da qualsiasi libreria JSON Schema draft 2020-12).

## Cosa NON esiste

`ACP PROMPT`, `ACP CODING`, ecc. sono **modalità logiche** interpretate dal modello quando la skill è caricata, non comandi nativi di alcuna piattaforma.
