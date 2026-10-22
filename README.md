# Elephant-Goldfish Model (EGM) — Universal Agent Edition

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Upstream](https://img.shields.io/badge/Upstream-google%2Felephant--goldfish--model-orange.svg)](https://github.com/google/elephant-goldfish-model)
[![Universal Repo](https://img.shields.io/badge/GitHub-yathamsriram243--blip%2Fegm--universal--agent-green.svg)](https://github.com/yathamsriram243-blip/egm-universal-agent)
[![Tests](https://img.shields.io/badge/Tests-25%20Passed-brightgreen.svg)](tests/)

**Elephant-Goldfish Model (EGM)** is an open-source framework and methodology for **Spec-Driven Development (SDD)** with autonomous AI coding agents.

Originally developed by Google ([google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model)), this **Universal Agent Edition** ([yathamsriram243-blip/egm-universal-agent](https://github.com/yathamsriram243-blip/egm-universal-agent)) extends EGM into a single, canonical, cross-compatible standard supporting **Google Antigravity**, **Gemini CLI**, **Claude Code**, **OpenAI Codex**, **Cursor**, **Hermes (Nous Research)**, **VS Code GitHub Copilot**, **Windsurf (Cascade)**, and open-source agents (**OpenCode**, **Continue**, **Cline**, **Roo Code**, **OpenHands**).

---

## 🐘 The Philosophy

EGM coordinates two complementary memory models across the software development lifecycle:

* 🐘 **The Elephant (Deep Context & Institutional Memory):**
  Loaded with system history, repository architecture, component boundaries, and customer journeys. The Elephant leads structured brainstorming, probes operational limits, and incrementally compiles living Markdown specifications.
* 🐠 **The Goldfish (Zero-Context Stateless Auditors):**
  Isolated subagents operating with fresh context windows and zero conversational bias. The Goldfish swarm stress-tests specifications and source code across conflicting adversarial perspectives (Skeptical Architect, Naive Reader, Hostile Design Critic, Pragmatic Tech Lead, Codebase Quality Auditor, Structural Validator, and Technical Copy Editor).
* 🧑‍💻 **The Human Engineer (Owns Decisions & Outcomes):**
  AI serves as an exploratory partner and tireless automated auditor; the human developer retains final authority over architectural trade-offs, scope approval, and merge gates.

> For the foundational essay introducing this methodology, see Dave Rensin's article: [Elephants, Goldfish, and the New Golden Age of Software Engineering](https://medium.com/@drensin/elephants-goldfish-and-the-new-golden-age-of-software-engineering-c33641a48874).

---

## 🛠️ Canonical Skills & Slash Commands

| Skill | Slash Command | Core Purpose & Deliverable |
| :--- | :--- | :--- |
| **Brainstorm** | `/egm-brainstorm` | Zero-document ideation engine using a multi-lens Goldfish shootdown swarm to stress-test raw concepts into an actionable RFC (`concepts_brief.md`). |
| **Draft** | `/egm-draft` | Section-by-section living design document compiler grounded strictly in codebase facts without inventing APIs (`docs/designs/<feature>.md`). |
| **Review** | `/egm-review` | Multi-stage verification pipeline executing 4 stages in strict topological order: Zoom Out $\rightarrow$ Comprehension $\rightarrow$ Critic $\rightarrow$ Readiness (`consolidated_review_report.md`). |
| **Review Loop** | `/egm-review-loop` | Concurrent review-subagent dispatch engine supporting direct dispatch, hierarchical synthesizer offloading, and transparent sequential fallback. |
| **Resolve** | `/egm-resolve` | Interactive triage, taxonomy classification (`defect`, `valid improvement`, `duplicate`, `false positive`), minimal safe patch application, and regression test verification. |
| **Drift Report** | `/egm-drift-report` | Strictly read-only AST scanner detecting divergence between checked-in design specifications and live code (`{YYYY-MM-DD}_DRIFT_REPORT.md`). |
| **Bootstrap** | `/egm-bootstrap` | Recursive codebase documentation generator compiling package contracts (Peanuts) and repository blueprints (Hay) with a 15-directory safety gate. |

---

## 👥 Stateless Reviewer Personas (`agents/`)

Every persona is formally defined in `agents/<name>.md` with strict read-only mandates, explicit evidence requirements, and structured output schemas:

1. **`egm-zoom-out` (Skeptical Architect):** Evaluates system boundaries, high-altitude simplicity, YAGNI, and existing codebase reuse opportunities. Produces an explicit architecture verdict (`PASS`, `CONDITIONAL PASS`, `FAIL`).
2. **`egm-comprehension` (Naive Reader):** Evaluates clarity from the perspective of a newcomer with zero tribal context. Flags undefined acronyms, hidden dependencies, and reader questions.
3. **`egm-design` (Hostile Design Critic):** Aggressively stress-tests failure modes, adversarial scenarios, state corruption, security boundaries, and peak QPS / token budget ceilings.
4. **`egm-implementation-readiness` (Pragmatic Tech Lead):** Verifies that tasks are fully actionable without design guesswork. Produces prerequisites, work breakdown, acceptance test matrix, and a readiness verdict (`READY`, `NEEDS REVISION`, `NOT READY`).
5. **`egm-codebase-details` (Codebase Quality Auditor):** Verifies code-to-doc fidelity, error propagation, unstated assumptions, and existing library reuse opportunities.
6. **`egm-structural` (Layout & Structure Validator):** Enforces strict document hierarchy (H1 $\rightarrow$ H2 $\rightarrow$ H3), template compliance, and catches internal contradictions between sections.
7. **`egm-style` (Technical Copy Editor):** Strips marketing fluff, ungrounded promotional adjectives (*seamless*, *revolutionary*), and buzzwords while preserving 100% of technical semantics.
8. **`egm-synthesizer` (Swarm Aggregator):** Intermediate coordinator managing the Goldfish swarm, deduplicating findings, preserving minority dissenting opinions, and formatting deliverables.
9. **`egm-bootstrap-orchestrator` (Blueprint Orchestrator):** Manages recursive directory tree inspection, safe worker partitioning, and rollup blueprints without concurrent file write collisions.

---

## 📋 Universal Finding Contract (`RFC-001`)

All skills and personas report review observations using the 11-field Standard Review-Finding Contract defined in [`resources/finding_contract.md`](resources/finding_contract.md):

```markdown
### [[id]] [title]
* **Severity**: [critical | high | medium | low | informational]
* **Category**: [architecture | correctness | security | requirements | implementation | testing | documentation | style]
* **Location**: `[file path, symbol, section, or line range]`
* **Evidence**: [Observed facts or reproducible behavior]
* **Reasoning**: [Why this evidence constitutes a defect or risk]
* **Impact**: [Realistic operational, architectural, or user consequence]
* **Recommendation**: [Concrete proposed remediation or minimal patch]
* **Confidence**: [high | medium | low]
* **Status**: [open | accepted | rejected | deferred | fixed | unverifiable]
```

---

## 🚀 Universal Harness Setup & Installation

EGM maintains a **single source of truth** in `skills/` and `agents/`. Each AI coding agent discovers EGM through its native declarative configuration:

```
├── .claude-plugin/plugin.json       # Claude Code Plugin Descriptor
├── .claude/commands/*.md            # Claude Code Custom Slash Commands
├── .cursor/rules/egm.mdc            # Cursor Composer & Agent Mode Rules
├── .cursorrules                     # Cursor Project Rules
├── .github/copilot-instructions.md  # GitHub Copilot System Instructions
├── .windsurfrules                   # Windsurf (Cascade) Project Rules
├── .continue/rules.md               # Continue Extension Rules
├── .clinerules                      # Cline / Roo Code Rules
├── .roomodes                        # Roo Code Custom Roles
├── opencode.json                    # OpenCode Plugin Configuration
├── plugin.yaml                      # Hermes (Nous Research) Plugin Manifest
├── plugin.json                      # Google Antigravity Plugin Manifest
├── gemini-extension.json            # Gemini CLI Extension Manifest
└── AGENTS.md                        # OpenAI Codex & Universal Agent Guidance
```

### 1. Google Antigravity (Native Host)
* **Global Path:** Place at `C:\Users\<User>\.gemini\config\plugins\egm` or `~/.gemini/config/plugins/egm`.
* **Workspace Path:** Add to `.agents/plugins/egm` or reference in `plugins.json`.
* **Usage:** Type `/egm-brainstorm`, `/egm-draft`, or `/egm-review` directly in chat canvas.

### 2. Gemini CLI
* **Link Local Directory:**
  ```bash
  gemini extensions link C:\Users\<User>\.gemini\config\plugins\egm
  ```
* **Install from GitHub:**
  ```bash
  gemini extensions install https://github.com/yathamsriram243-blip/egm-universal-agent.git
  ```

### 3. Claude Code (Anthropic)
* **Native Discovery:** Claude Code discovers commands declared in `.claude/commands/`.
* **Usage:** Type `/egm-brainstorm`, `/egm-draft`, `/egm-review` inside the Claude Code CLI.

### 4. Cursor (Anysphere)
* **Composer / Chat:** Cursor automatically ingests `.cursor/rules/egm.mdc` and `.cursorrules`.
* **Usage:** Mention `@rules egm` or ask Cursor: *"Run EGM Review on docs/designs/my_feature.md"*.

### 5. Hermes (Nous Research)
* **Hermes Plugin:** Hermes automatically discovers `plugin.yaml` in plugin roots or `~/.hermes/plugins/egm`.
* **Usage:** Hermes routes skills directly from `plugin.yaml`.

### 6. GitHub Copilot (VS Code)
* **Workspace Integration:** GitHub Copilot Chat in VS Code reads `.github/copilot-instructions.md`.
* **Usage:** Instruct Copilot: *"Run /egm-review on the active specification following the 4 stages"*.

### 7. OpenAI Codex
* **Ingestion:** Codex automatically ingests `AGENTS.md` and `.codex/instructions.md`.

### 8. OpenCode, Continue, Cline, and Windsurf
* Native configurations (`opencode.json`, `.continue/rules.md`, `.clinerules`, `.roomodes`, `.windsurfrules`) ensure seamless rule activation across open-source IDE assistants.

---

## 🧪 Automated Testing & Verification

The universal test suite validates schema compliance, link integrity, routing matrices, and safety gates across all platforms:

```bash
python -m pytest tests -v
```

* **Persona Verification:** Ensures all 9 personas implement the 7 required sections and specific output deliverables.
* **Contract Verification:** Ensures strict 11-field compliance with `RFC-001`.
* **Pipeline Ordering:** Enforces Stage 1 Zoom Out $\rightarrow$ Stage 2 Comprehension $\rightarrow$ Stage 3 Critic $\rightarrow$ Stage 4 Readiness.
* **Safety Boundaries:** Enforces 15-directory thresholds, `.gitignore` exclusions, secrets blocking, and read-only drift operations.

---

## 🤝 Attribution & Upstream

* **Upstream Framework:** [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) (Copyright Google LLC, Apache 2.0).
* **Universal Agent Edition:** Maintained at [yathamsriram243-blip/egm-universal-agent](https://github.com/yathamsriram243-blip/egm-universal-agent.git).
* **Foundational Philosophy:** Dave Rensin's *Elephants, Goldfish, and the New Golden Age of Software Engineering*.

## 📄 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.
