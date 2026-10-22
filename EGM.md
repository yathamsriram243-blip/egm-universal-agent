# Elephant-Goldfish Model (EGM) Blueprint

## System Overview
The Elephant-Goldfish Model is a Spec-Driven Development (SDD) multi-agent framework providing unified skills and stateless review personas across major AI coding agent harnesses.

## Subdirectories & System Boundaries
- `skills/`: [Relative Link](./skills/egm_bootstrap/SKILL.md) - Contains the 7 canonical skills (`egm-brainstorm`, `egm-draft`, `egm-review`, `egm-review-loop`, `egm-resolve`, `egm-drift-report`, `egm-bootstrap`).
- `agents/`: [Relative Link](./agents/zoom_out.md) - Contains the 9 stateless Goldfish reviewer and orchestrator personas (`egm-zoom-out`, `egm-comprehension`, `egm-design`, `egm-implementation-readiness`, `egm-codebase-details`, `egm-structural`, `egm-style`, `egm-synthesizer`, `egm-bootstrap-orchestrator`).
- `resources/`: [Relative Link](./resources/finding_contract.md) - Universal Standard Review-Finding Contract (`RFC-001`), document standards, and execution rules.
- `docs/`: [Relative Link](./docs/harnesses.md) - Architectural documentation, FAQ, getting started, and multi-harness compatibility matrix.
- `tests/`: [Relative Link](./tests/unit/test_subagent_personas.py) - Pytest automated validation test suites.

## Global Invariants
- `skills/` and `agents/` are the single source of truth; never duplicated or diverged per harness.
- Stateless Goldfish reviewers run in isolated contexts with read-only access.
- All review findings conform to the 11-field Standard Review-Finding Contract (`RFC-001`).
- Fallback to transparent sequential execution when subagents are unsupported.

## System Verification
- Run: `pytest tests` (All 25 automated unit tests must pass).
