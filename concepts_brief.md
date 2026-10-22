# Universal Multi-Agent EGM Bridge (Universal Plugin Adapter)

* **Author:** EGM Universal Architecture Working Group
* **Date:** 2026-10-23
* **Status:** Approved RFC / Ready for Drafting

## 1. Concept Summary
The Universal Multi-Agent EGM Bridge extends the Elephant-Goldfish Model (EGM) from a Google-specific framework (Antigravity & Gemini CLI) into a universal Spec-Driven Development (SDD) standard compatible across all major commercial and open-source AI coding agents: Claude Code, OpenAI Codex, Cursor, Hermes (Nous Research), GitHub Copilot, Windsurf (Cascade), and OpenCode / Continue / Cline. It provides unified skill definitions, 11-field standard finding contracts (`RFC-001`), and native adapter manifests without duplicating or forking core skill logic.

## 2. Alternatives Explored
1. **Separate Per-Agent Forks / Repositories:**
   - *Pros:* Independent customization tailored to each tool's quirks.
   - *Cons:* Maintenance nightmare, documentation drift, and fragmented community.
   - *Rejection Reason:* Violates the EGM single-source-of-truth invariant.
2. **Generic System-Prompt-Only Paste:**
   - *Pros:* Zero filesystem footprint.
   - *Cons:* Context window bloat, loss of progressive disclosure, no slash command integration.
   - *Rejection Reason:* Unreliable agent adherence and high token costs.
3. **Universal Canonical Core with Multi-Harness Adapters (Selected Approach):**
   - *Pros:* Single source of truth in `skills/` and `agents/` with lightweight adapter configs (`plugin.json`, `gemini-extension.json`, `.claude-plugin/`, `.cursor/`, `plugin.yaml`, `opencode.json`).

## 3. Strongest Adversarial Objections & Challenges
* **`egm-zoom-out` (Skeptical Architect):**
  * *Objection:* Are we maintaining speculative adapters for agents that may change their manifest schema in three months?
  * *Resolution:* Limit adapters strictly to native standard declarative manifests without heavy runtime wrappers.
* **`egm-design` (Hostile Critic):**
  * *Objection:* How do single-threaded agents (e.g. standard Claude or Cursor) execute concurrent Goldfish swarms without lying to the user?
  * *Resolution:* Mandate explicit Sequential Fallback Protocol: run sequential passes, label them honestly, and never claim parallel execution when it did not occur.
* **`egm-comprehension` (Naive Reader):**
  * *Objection:* The distinction between the Elephant (deep context) and Goldfish (stateless) must be clearly explained in each harness's instructions.
  * *Resolution:* Provide explicit role briefs and clear setup instructions per harness in `README.md` and `docs/harnesses.md`.

## 4. Architectural, Security & Feasibility Risks
* **Risk 1 (Schema Skew):** Different harnesses expect different command registration schemas.
  * *Mitigation:* Automated unit test `test_manifests_and_adapters.py` validates all manifests in CI.
* **Risk 2 (Sensitive File Exposure):** Recursive scanners could leak secrets (`.env`, tokens).
  * *Mitigation:* Universal exclusion standard enforcing `.gitignore`, `.egmignore`, and credentials blocklists.

## 5. Practical Recommendation & Synthesis
Deploy the unified repository structure where `skills/` and `agents/` remain canonical, and all harness manifests (`plugin.json`, `gemini-extension.json`, `plugin.yaml`, `opencode.json`, `.cursorrules`, `.windsurfrules`, `.claude-plugin/`) point to the canonical definitions.

## 6. Smallest Useful Validation Experiment
Run the 25-test pytest suite and execute an end-to-end design doc creation and review using the 7 skills sequentially on a test feature specification.

## 7. Goals vs. Non-Goals
* **In-Scope Goals:**
  - Standardized slash commands across 8+ agent ecosystems.
  - 11-field Standard Review-Finding Contract.
  - Native manifest discovery for Antigravity, Gemini CLI, Claude, Cursor, Hermes, Copilot, Windsurf, OpenCode.
* **Out-of-Scope Non-Goals:**
  - Modifying proprietary agent runtimes or writing closed-source binaries.
  - Inventing non-standard extension formats.

## 8. Unresolved Questions & Key Decisions
* **Decision 1:** Universal repo will track upstream `https://github.com/google/elephant-goldfish-model` and push to `https://github.com/yathamsriram243-blip/egm-universal-agent.git`.
* **Decision 2:** All findings must format to `RFC-001` (11 fields).
