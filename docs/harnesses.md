# Harnesses & Agent Compatibility Matrix

EGM is a single canonical set of seven skills and nine personas. This repository serves as the
authoritative plugin source across all supported host coding agents.

## 1. Supported & Adapted Harnesses

| Harness | Adapter Manifest / Config | Discovery Root | Subagent Mechanism | Concurrency Support |
| :--- | :--- | :--- | :--- | :--- |
| **Google Antigravity** | `plugin.json` | `~/.gemini/config/plugins/egm` or `.agents/` | `invoke_subagent` (native named personas) | Parallel Subagents + Hierarchical Nesting |
| **Gemini CLI** | `gemini-extension.json` | `~/.gemini/extensions/` | Subagents (named personas in `agents/`) | Parallel Subagents |
| **Claude Code** | `.claude-plugin/plugin.json`, `.claude/commands/` | `.claude-plugin/` or `.claude/` | Direct Dispatch / Subshell / Sequential | Parallel / Sequential Fallback |
| **Cursor** | `.cursor/rules/egm.mdc`, `.cursorrules` | Project root / `.cursor/rules/` | Cursor Agent Mode / Custom Prompts | Sequential Fallback |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.github/` | Chat Prompt Routing / Specialized Roles | Sequential Fallback |
| **OpenAI Codex** | `AGENTS.md` | Project root | Agent Prompt Ingestion | Sequential Fallback |
| **Windsurf** | `.windsurfrules` | Project root | Cascade Rule Ingestion | Sequential Fallback |
| **OpenCode** | `opencode.json` | Project root | OpenCode Skill & Agent Loader | Parallel / Sequential Fallback |

---

## 2. Installation & Configuration by Harness

### 2.1 Google Antigravity (Native Host)
* **Global Path**: `C:\Users\<User>\.gemini\config\plugins\egm`
* **Workspace Path**: `<workspace>/.agents/` or explicitly listed in `<workspace>/plugins.json`.
* **Registration**: Antigravity automatically discovers `plugin.json`, mounting skills from `skills/` and subagent personas from `agents/`.
* **Invocation**: Use slash commands in chat (e.g. `/egm-brainstorm`, `/egm-draft`, `/egm-review`) or let Antigravity dispatch personas via `invoke_subagent`.

### 2.2 Gemini CLI
* **Install Command**:
  ```bash
  gemini extensions install https://github.com/google/elephant-goldfish-model
  ```
* **Local Development Link**:
  ```bash
  gemini extensions link C:\Users\<User>\.gemini\config\plugins\egm
  ```
* **Invocation**: Run `gemini` in terminal and invoke commands `/egm-brainstorm`, `/egm-draft`, `/egm-review`.

### 2.3 Claude Code
* **Plugin Configuration**: Recognized via `.claude-plugin/plugin.json`.
* **Custom Slash Commands**: Discovered via `.claude/commands/` (`/egm-brainstorm`, `/egm-draft`, etc.).
* **Install**: Clone or copy into project root or link `.claude-plugin/`.

### 2.4 Cursor
* **Configuration**: Automatically loaded from `.cursor/rules/egm.mdc` and `.cursorrules`.
* **Invocation**: Type `/egm-review` or `@rules egm` in Cursor Composer or Chat. Cursor's agent mode adopts the EGM constraints, finding contract, and review stages.

### 2.5 GitHub Copilot (VS Code)
* **Configuration**: Located in `.github/copilot-instructions.md`.
* **Invocation**: In VS Code GitHub Copilot Chat, reference commands like `/egm-review` or ask Copilot to apply the EGM Review Protocol to an active design document.

### 2.6 OpenAI Codex
* **Configuration**: Discovered via repository root `AGENTS.md`.
* **Invocation**: Prompt Codex with specific workflow directives (e.g., "Run EGM Review on docs/designs/feature.md").

### 2.7 Windsurf (Cascade)
* **Configuration**: Automatically loaded via `.windsurfrules`.
* **Invocation**: Mention the command in Cascade chat (e.g. `/egm-brainstorm` or `/egm-review`).

---

## 3. Subagent Delegation & Fallback Protocol

Skills say *"spawn a subagent"* and designate a persona (`egm-zoom-out`, `egm-design`, etc.). Each harness maps this instruction according to its capabilities:

1. **Native Named Personas (Antigravity & Gemini CLI)**: Invokes the subagent tool specifying the persona name directly.
2. **Generic Subagents**: Where named personas are not natively registered, the orchestrator spawns a general-purpose subagent and instructs it to read the corresponding file in `agents/<name>.md` before auditing.
3. **Sequential Fallback**: Where subagent spawning or independent context windows are unsupported, the agent executes clearly labeled sequential review passes within the primary conversation. Concurrency or independence is never claimed if it was not physically executed.

---

## 4. Standard Review Finding Contract (RFC-001)

All review skills and personas adhere to the universal 11-field finding contract defined in [`resources/finding_contract.md`](../resources/finding_contract.md):
* `id`, `title`, `severity`, `category`, `location`, `evidence`, `reasoning`, `impact`, `recommendation`, `confidence`, `status`.
