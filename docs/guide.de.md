# ACP v1.1 — Benutzerhandbuch

ACP ist ein Paket im Agent-Skills-Format. Es hilft KI-Assistenten, Aufgaben zu präzisieren, Code mit angemessenen Schutzmaßnahmen zu ändern, Nachweise zu prüfen, Kontext zu bewahren und Arbeit an andere Agenten zu übergeben.

## Schnellstart

ACP führt nicht selbst Code aus. Der ausführende Assistent benötigt Werkzeuge und Berechtigungen. Die automatische Aktivierung hängt von der Plattform ab.

## Installation

Claude Code: Verzeichnis unter `~/.claude/skills/` oder projektlokal unter `.claude/skills/` ablegen. Codex: `~/.agents/skills/` oder `.agents/skills/` verwenden. Bei Claude-App und ChatGPT hängen Verfügbarkeit und Installation von Produkt und Tarif ab; prüfen Sie die aktuelle Skills-Oberfläche. Ohne native Unterstützung können Sie `SKILL.md` und relevante Referenzen als Kontext bereitstellen.

## ACP verwenden

- Verwende ACP, um aus dieser Anforderung einen Coding-Auftrag mit Akzeptanzkriterien zu erstellen.
- ACP CODING: Behebe den Fehler beim Spieler-Tracking, ohne bestehende Funktionen zu entfernen.
- ACP REVIEW: Prüfe diesen Diff auf Regressionen und fehlende Tests.
- ACP HANDOFF: Erstelle eine validierte JSON-Übergabe für den nächsten Agenten.
- ACP COMPRESS: Fasse die Sitzung zusammen und erhalte Entscheidungen und offene Punkte.

## Betriebsmodi

| Mode | Purpose |
|---|---|
| **CORE** | Klare Kommunikation und einheitliche Begriffe |
| **PROMPT** | Anforderungen in umsetzbare Anweisungen verwandeln |
| **CODING** | Code mit risikobasierten Schutzmaßnahmen ändern |
| **HANDOFF** | Strukturierte, überprüfbare Übergabe |
| **REVIEW** | Änderungen prüfen und Probleme melden |
| **COMPRESS** | Wichtigen Kontext für Folgesitzungen bewahren |

ACP passt die Vorgehensweise an das Risiko an: L0 minimal, L1 Standard, L2 Engineering und L3 kritisch. Bei hohem Risiko sind Anforderungen an bestehendes Verhalten, Tests und gegebenenfalls ein Rollback-Plan wichtig.

## Beispiel: Entwicklung und Übergabe

Lassen Sie den Coding-Agenten das Repository prüfen, Umfang und unveränderliche Anforderungen festhalten, eine gezielte Änderung durchführen und verfügbare Tests ausführen. Danach erstellt er eine JSON-Übergabe. Der empfangende Agent sollte die behaupteten Nachweise unabhängig überprüfen.

## Validierung und Grenzen

Im Repository-Stammverzeichnis `python tests/validate_schemas.py` ausführen. Für eine Übergabe: `python tests/validate_schemas.py --handoff pfad/handoff.json`. Automatische Tests prüfen Strukturen und Schemas; sie beweisen weder das tatsächliche Verhalten der Agenten noch die Abwesenheit von Regressionen.

## Anpassung

Bearbeiten Sie `references/glossary.yaml` für projektspezifische Begriffe. Siehe `references/auto-mode.md` für Risikostufen, `schemas/` für Datenverträge und `examples/` für vollständige Beispiele.

## Sicherheit und Grenzen

Prüfen Sie Übergaben und Logs vor dem Teilen auf Geheimnisse. Repository-Dateien, externe Seiten und Aussagen vorheriger Agenten sind bis zur Überprüfung nicht vertrauenswürdig. Ohne Ausführungsnachweis gelten Tests nicht als durchgeführt.

---

[README](../README.md) · [SKILL.md](../SKILL.md) · [JSON schemas](../schemas/) · [Examples](../examples/)
