# GitHub Copilot Instructions for Elephant-Goldfish Model (EGM)

This repository implements the Elephant-Goldfish Model (EGM) framework for Spec-Driven Development.

## Workflows & Commands
When requested by the developer, execute the following EGM workflows:
- `/egm-brainstorm`: Zero-doc ideation; challenge assumptions; output concept summary, alternatives, objections, risks, recommendation, and validation experiment.
- `/egm-draft`: Section-by-section specification drafting; separate requirements, constraints, assumptions, decisions, non-goals, and questions.
- `/egm-review`: Strict 4-stage verification:
  1. Zoom Out (`agents/zoom_out.md`)
  2. Comprehension (`agents/comprehension.md`)
  3. Critic (`agents/design_critic.md`)
  4. Readiness (`agents/implementation_readiness.md`)
- `/egm-review-loop`: Concurrent or sequential review dispatch engine.
- `/egm-resolve`: Finding triage (`defect`, `valid improvement`, `duplicate`, `false positive`, `needs clarification`), safe patch application, and test verification.
- `/egm-drift-report`: Compare specifications against live code; report concrete discrepancies without mutating code.
- `/egm-bootstrap`: Map directory tree, respect `.gitignore` and sensitive files, generate package contracts and blueprints.

## Universal Review Contract
All findings must populate the 11 standard fields:
`id`, `title`, `severity`, `category`, `location`, `evidence`, `reasoning`, `impact`, `recommendation`, `confidence`, `status`
(defined in `resources/finding_contract.md`).
