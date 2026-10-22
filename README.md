# Elephant-Goldfish Model (EGM) — Universal Agent Edition

> **The Universal Spec-Driven Development (SDD) Framework & Adversarial Review Engine for AI Coding Agents**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Upstream](https://img.shields.io/badge/Upstream-google%2Felephant--goldfish--model-orange.svg)](https://github.com/google/elephant-goldfish-model)
[![Release](https://img.shields.io/badge/Release-v1.0.0--universal-green.svg)](https://github.com/yathamsriram243-blip/egm-universal-agent/releases)
[![Tests](https://img.shields.io/badge/Tests-44%20Passed-brightgreen.svg)](tests/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yathamsriram243-blip/egm-universal-agent/pulls)

---

## 🚀 Overview / What is EGM Universal Agent?

The **Elephant-Goldfish Model (EGM)** is an open-source methodology and framework for **Spec-Driven Development (SDD)** with autonomous AI coding agents. 

Originally engineered by Google ([google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model)) based on Dave Rensin's foundational architecture, EGM coordinates two opposing memory models across the software development lifecycle:

* 🐘 **The Elephant (Deep Context & Institutional Memory):**  
  A persistent conversational agent holding deep project history, component boundaries, and customer journeys. The Elephant leads structured brainstorming, probes operational limits, and iteratively drafts living Markdown specifications.
* 🐠 **The Goldfish (Zero-Context Stateless Reviewers):**  
  Isolated, fresh-context subagents with zero conversational bias. The Goldfish swarm subjects draft specifications to rigorous, adversarial stress-testing across conflicting perspectives (Skeptical Architect, Hostile Design Critic, Naive Reader, Pragmatic Tech Lead, and Codebase Auditor).
* 🧑‍💻 **The Human Engineer (Owns Outcomes):**  
  AI serves as a tireless exploration partner and adversarial auditor; the human engineer retains full authority over architectural trade-offs, scope approval, and merge gates.

### The Shift to the Universal Agent Edition
The upstream Google release focused primarily on Google Antigravity and Gemini CLI. However, modern engineering teams build with a diverse array of assistants: **Claude Code**, **Cursor**, **OpenAI Codex**, **Windsurf**, **VS Code GitHub Copilot**, **Hermes**, and open-source models (**OpenCode**, **Continue**, **Cline**, **Roo Code**, **OpenHands**). 

The **Universal Agent Edition** bridges this fragmentation into a single canonical core. Through declarative native adapters, it brings native **AI coding agent custom rules**, **Claude Code slash commands**, and **Cursor custom instructions** to every leading agent ecosystem without code forks or documentation drift.

---

## ✨ Key Features & Capabilities

### 🛠️ 7 Universal EGM Skills & Slash Commands
* **`/egm-brainstorm`**: Zero-document ideation tool. Dispatches a multi-lens Goldfish shootdown swarm to stress-test raw concepts, discover existing codebase reuse, challenge assumptions, and generate an RFC brief (`concepts_brief.md`).
* **`/egm-draft`**: Section-by-section living specification compiler. Enforces strict separation of requirements, constraints, assumptions, explicit trade-offs, non-goals, and acceptance criteria with interactive Section Approval Gates.
* **`/egm-review`**: Multi-stage verification pipeline orchestrator. Executes four verification stages in strict sequence:
  $$\text{Stage 1: Zoom Out} \longrightarrow \text{Stage 2: Comprehension} \longrightarrow \text{Stage 3: Critic} \longrightarrow \text{Stage 4: Readiness}$$
* **`/egm-review-loop`**: Concurrent review-subagent dispatch engine. Coordinates parallel Goldfish reviewers across targeted scopes with direct dispatch, hierarchical aggregation, and honest sequential fallback.
* **`/egm-resolve`**: Interactive finding triage and automated patch engine. Ingests structured findings, classifies dispositions (`defect`, `valid improvement`, `duplicate`, `false positive`, `needs clarification`), applies minimal surgical diffs, and runs automated regression tests.
* **`/egm-drift-report`**: Read-only specification-to-code divergence scanner. Compares checked-in design documents against live source files and AST symbols to surface undocumented behavior and stale contracts without modifying code.
* **`/egm-bootstrap`**: Bottom-up repository blueprint compiler. Recursively maps codebases into leaf package contracts (Peanuts) and parent blueprint indexes (Hay) protected by idempotent HTML sentinel blocks and a 15-directory safety gate.

### 🐠 9 Specialized Goldfish Subagent Personas (`agents/`)
1. **`egm-zoom-out` (Skeptical Architect)**: Challenges necessity, enforces YAGNI, detects speculative over-engineering, and identifies existing open-source and internal library reuse.
2. **`egm-comprehension` (Naive Reader)**: Audits documents with zero assumed institutional memory, flagging undefined terms, acronyms, ambiguous requirements, and comprehension blockers.
3. **`egm-design` (Hostile Design Critic)**: Attacks failure modes, single points of failure (SPOFs), concurrency hazards, quota ceilings, and resource economics.
4. **`egm-implementation-readiness` (Pragmatic Tech Lead)**: Verifies that every modified file is enumerated with concrete rationale, API signatures match code, and test plans exist.
5. **`egm-codebase-details` (Codebase Quality Auditor)**: Pedantic auditor verifying that referenced classes, types, interfaces, and directory paths exist on disk.
6. **`egm-structural` (Layout & Structure Validator)**: Enforces heading hierarchy symmetry, section sequencing, and document template compliance.
7. **`egm-style` (Technical Copy Editor)**: Enforces concise, direct prose, stripping corporate buzzwords, validating adjectives, marketing fluff, and conversational filler.
8. **`egm-synthesizer` (Swarm Aggregator)**: Coordinates parallel Goldfish reviewer fan-out, deduplicates overlapping critiques, and compiles deliverable report artifacts.
9. **`egm-bootstrap-orchestrator` (Blueprint Orchestrator)**: Partitions directory trees, coordinates child scout workers, and merges package contracts into repository blueprints.

### 📋 RFC-001 Standard Review-Finding Contract
Every critique across all 9 personas and 7 skills adheres to the universal 11-field finding contract:
`id`, `title`, `severity` (critical/high/medium/low/informational), `category`, `location`, `evidence`, `reasoning`, `impact`, `recommendation`, `confidence`, and `status`.

---

## 🛠️ Supported AI Coding Agents & IDEs

| Assistant / Ecosystem | Native Adapter Configuration | Discovery Path | Execution Mode |
| :--- | :--- | :--- | :--- |
| **Google Antigravity** | `plugin.json` | `~/.gemini/config/plugins/egm` or `.agents/` | Native multi-agent subagents (`invoke_subagent`) |
| **Claude Code & Cowork** | `.claude-plugin/plugin.json`, `.claude/commands/` | `.claude-plugin/` or `--plugin-dir` | Native slash commands, isolated `Agent` tools |
| **OpenAI Codex & ChatGPT** | `.codex-plugin/plugin.json`, `AGENTS.md` | `.agents/plugins/marketplace.json` | Native `spawn_agent` (`fork_turns: "none"`) |
| **Cursor** | `.cursor/rules/egm.mdc`, `.cursorrules` | Project root / `.cursor/rules/` | Custom rules, Composer & Chat ingestion |
| **Windsurf (Cascade)** | `.windsurfrules` | Project root | Cascade system rules & workflow routing |
| **GitHub Copilot (VS Code)** | `.github/copilot-instructions.md` | `.github/` | Copilot Chat instructions & persona routing |
| **Hermes (Nous Research)** | `plugin.yaml` | `~/.hermes/plugins/` or root | Declarative Hermes skills & agents manifest |
| **OpenCode** | `opencode.json` | Project root | Standard OpenCode skills & tools schema |
| **Continue, Cline, Roo Code** | `.continue/rules.md`, `.clinerules`, `.roomodes` | Project root | Custom system prompt rules & custom modes |
| **Gemini CLI** | `gemini-extension.json` | `~/.gemini/extensions/` | Subagent dispatch via `agents/` personas |

---

## 💻 Quick Start & Installation

Clone or link the repository into your preferred AI agent environment:

### Option 1: Claude Code (Anthropic)
Install EGM as a Claude Code plugin:
```bash
claude plugin add https://github.com/yathamsriram243-blip/egm-universal-agent.git
```
Or run directly from a local directory:
```bash
claude --plugin-dir /path/to/egm-universal-agent
```
Inside Claude Code, trigger skills via native slash commands:
```text
/egm-brainstorm
/egm-draft
/egm-review docs/designs/my_feature.md
```

### Option 2: Cursor (Anysphere)
Copy the pre-configured rules into your project root:
```bash
cp /path/to/egm-universal-agent/.cursorrules ./
mkdir -p .cursor/rules
cp /path/to/egm-universal-agent/.cursor/rules/egm.mdc .cursor/rules/
```
In Cursor Chat or Composer, mention:
```text
@rules egm Run /egm-review on docs/designs/auth_service.md
```

### Option 3: Windsurf (Cascade)
Add the cross-compatible rules to your workspace root:
```bash
cp /path/to/egm-universal-agent/.windsurfrules ./
```

### Option 4: OpenAI Codex & ChatGPT Work
Add the marketplace manifest to your Codex configuration:
```bash
mkdir -p .agents/plugins
cp /path/to/egm-universal-agent/.agents/plugins/marketplace.json .agents/plugins/
```

### Option 5: Google Antigravity
Link or clone EGM to your global plugin directory:
* **Windows**: `C:\Users\<User>\.gemini\config\plugins\egm`
* **macOS/Linux**: `~/.gemini/config/plugins/egm`

---

## ⚙️ Configuration & Custom Rules

EGM provides ready-to-use custom instruction files that you can drop into any active repository to immediately enable Spec-Driven Development:

### 1. Cursor Custom Instructions (`.cursor/rules/egm.mdc`)
Enforces the 4-stage review pipeline and RFC-001 finding contract whenever you edit design documents (`docs/designs/*.md`) or repository blueprints (`*README.md`, `*EGM.md`).

### 2. Cline Custom Instructions (`.clinerules`) & Roo Code (`.roomodes`)
Defines specialized modes (`EGM Architect`, `EGM Critic`, `EGM Resolver`) with strict tool execution limits (e.g., read-only tools for reviewers, file editing exclusively for the resolver).

### 3. VS Code GitHub Copilot (`.github/copilot-instructions.md`)
Instructs Copilot Chat to automatically route requests for brainstorming, drafting, or review through the corresponding EGM procedures.

---

## 🧪 Verification & Automated Testing

EGM includes an offline test suite validating schemas, link integrity, and routing rules:

```bash
# Install test dependencies
pip install pytest pyyaml

# Run offline unit test suite (44/44 tests)
pytest tests/unit -v
```

* **Persona Verification**: Asserts that all 9 personas implement the 7 mandatory sections without CP1252 character corruption.
* **Finding Contract**: Asserts JSON Schema parsing against the 11-field RFC-001 standard.
* **Pipeline Ordering**: Enforces Stage 1 Zoom Out $\rightarrow$ Stage 2 Comprehension $\rightarrow$ Stage 3 Critic $\rightarrow$ Stage 4 Readiness.
* **Safety Invariants**: Enforces read-only drift scanning and the 15-directory bootstrap safety gate.

---

## 🤝 Contributing & Community

Contributions are warmly welcomed! Please review [docs/getting_started.md](docs/getting_started.md) and [TESTING.md](TESTING.md) before submitting pull requests.

1. Fork the repository: [yathamsriram243-blip/egm-universal-agent](https://github.com/yathamsriram243-blip/egm-universal-agent)
2. Create a feature branch: `git checkout -b feat/my-new-feature`
3. Verify that all 44 unit tests pass: `pytest tests/unit`
4. Submit a Pull Request following `.github/PULL_REQUEST_TEMPLATE.md`

### Acknowledgments & Upstream Attribution
* **Upstream Foundation**: Originally created by Google LLC at [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) (Apache-2.0 License).
* **Foundational Essay**: Dave Rensin's *Elephants, Goldfish, and the New Golden Age of Software Engineering*.
* **Universal Agent Architecture**: Maintained by the EGM Universal Agent Working Group.

---

## 📄 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.
