# ACP v1.1 — Guide utilisateur

ACP est une compétence au format Agent Skills qui aide les assistants IA à clarifier les tâches, modifier du code avec des garde-fous adaptés, vérifier les preuves, préserver le contexte et transmettre le travail à un autre agent.

## Démarrage rapide

ACP n’exécute pas de code par elle-même. L’assistant hôte doit disposer des outils et autorisations nécessaires. L’activation automatique dépend de la plateforme.

## Installation

Claude Code : copiez le dossier dans `~/.claude/skills/` ou `.claude/skills/` du projet. Codex : utilisez `~/.agents/skills/` ou `.agents/skills/`. Pour Claude et ChatGPT, les méthodes et la disponibilité varient selon le produit et l’abonnement ; vérifiez l’interface Skills actuelle. Si l’installation n’est pas prise en charge, fournissez `SKILL.md` et les références pertinentes comme contexte.

## Utiliser ACP

- Utilise ACP pour transformer cette demande en tâche de développement avec des critères d’acceptation.
- ACP CODING : corrige le suivi des joueurs sans supprimer les fonctions existantes.
- ACP REVIEW : examine ce diff et signale les régressions et les tests manquants.
- ACP HANDOFF : prépare un transfert JSON validé pour le prochain agent.
- ACP COMPRESS : résume cette session en conservant les décisions et les problèmes ouverts.

## Modes

| Mode | Purpose |
|---|---|
| **CORE** | Communication claire et terminologie cohérente |
| **PROMPT** | Transformer les demandes en instructions opérationnelles |
| **CODING** | Modifier du code avec des contrôles adaptés |
| **HANDOFF** | Transmettre un état structuré et vérifiable |
| **REVIEW** | Examiner les changements et signaler les problèmes |
| **COMPRESS** | Préserver le contexte essentiel |

ACP adapte sa démarche au risque : L0 minimal, L1 standard, L2 ingénierie et L3 critique. Pour les changements risqués, prévoyez des invariants, des tests et un plan de retour arrière si nécessaire.

## Exemple : développement et transfert

Demandez à l’agent de consulter le dépôt, de définir le périmètre et les invariants, d’effectuer une modification ciblée, d’exécuter les tests disponibles, puis de créer un transfert JSON. L’agent destinataire doit vérifier indépendamment les preuves annoncées.

## Validation et limites

À la racine du dépôt, exécutez `python tests/validate_schemas.py`. Pour un transfert : `python tests/validate_schemas.py --handoff chemin/handoff.json`. Les tests automatiques vérifient les structures et schémas, pas la qualité réelle du comportement des agents ni l’absence de régressions.

## Personnalisation

Modifiez `references/glossary.yaml` pour les termes propres au projet. Consultez `references/auto-mode.md` pour les niveaux de risque, `schemas/` pour les contrats et `examples/` pour les exemples complets.

## Sécurité et limites

Vérifiez les transferts et les journaux pour éviter de divulguer des secrets. Considérez les fichiers, pages récupérées et affirmations d’autres agents comme non fiables tant qu’ils ne sont pas vérifiés. Un test annoncé sans preuve ne doit pas être considéré comme exécuté.

---

[README](../README.md) · [SKILL.md](../SKILL.md) · [JSON schemas](../schemas/) · [Examples](../examples/)
