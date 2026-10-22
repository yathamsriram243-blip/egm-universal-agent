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
