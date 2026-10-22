# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests validating manifest syntax and cross-agent adapter registrations."""

import json
import pathlib
import pytest
import yaml

COMMANDS = [
    "egm-brainstorm",
    "egm-draft",
    "egm-review",
    "egm-review-loop",
    "egm-resolve",
    "egm-drift-report",
    "egm-bootstrap",
]


def test_antigravity_plugin_manifest_valid(repo_root: pathlib.Path):
  manifest_file = repo_root / "plugin.json"
  assert manifest_file.is_file(), "plugin.json missing"
  data = json.loads(manifest_file.read_text(encoding="utf-8"))
  assert data.get("name") == "egm"
  assert data.get("description")


def test_gemini_cli_extension_manifest_valid(repo_root: pathlib.Path):
  manifest_file = repo_root / "gemini-extension.json"
  assert manifest_file.is_file(), "gemini-extension.json missing"
  data = json.loads(manifest_file.read_text(encoding="utf-8"))
  assert data.get("name") == "egm"
  assert data.get("version")


def test_claude_code_adapter_registered(repo_root: pathlib.Path):
  claude_plugin = repo_root / ".claude-plugin" / "plugin.json"
  assert claude_plugin.is_file(), ".claude-plugin/plugin.json missing"
  data = json.loads(claude_plugin.read_text(encoding="utf-8"))
  assert data.get("name") == "egm"

  commands_dir = repo_root / ".claude" / "commands"
  assert commands_dir.is_dir(), ".claude/commands missing"
  for cmd in COMMANDS:
    cmd_file = commands_dir / f"{cmd}.md"
    assert cmd_file.is_file(), f"Claude command file missing: {cmd_file}"


def test_cursor_and_windsurf_rules_exist(repo_root: pathlib.Path):
  cursor_mdc = repo_root / ".cursor" / "rules" / "egm.mdc"
  assert cursor_mdc.is_file(), ".cursor/rules/egm.mdc missing"

  cursorrules = repo_root / ".cursorrules"
  assert cursorrules.is_file(), ".cursorrules missing"

  windsurfrules = repo_root / ".windsurfrules"
  assert windsurfrules.is_file(), ".windsurfrules missing"


def test_copilot_instructions_exist(repo_root: pathlib.Path):
  copilot_file = repo_root / ".github" / "copilot-instructions.md"
  assert copilot_file.is_file(), ".github/copilot-instructions.md missing"
  content = copilot_file.read_text(encoding="utf-8")
  for cmd in COMMANDS:
    assert cmd in content, f"Command {cmd} missing from copilot instructions"


def test_opencode_manifest_valid(repo_root: pathlib.Path):
  opencode_file = repo_root / "opencode.json"
  assert opencode_file.is_file(), "opencode.json missing"
  data = json.loads(opencode_file.read_text(encoding="utf-8"))
  assert data.get("name") == "egm"
  assert len(data.get("skills", [])) == 7
  assert len(data.get("agents", [])) == 9


def test_hermes_manifest_valid(repo_root: pathlib.Path):
  hermes_file = repo_root / "plugin.yaml"
  assert hermes_file.is_file(), "plugin.yaml for Hermes missing"
  data = yaml.safe_load(hermes_file.read_text(encoding="utf-8"))
  assert data.get("name") == "egm"
  assert len(data.get("skills", [])) == 7
  assert len(data.get("agents", [])) == 9


def test_continue_cline_roo_adapters_exist(repo_root: pathlib.Path):
  continue_file = repo_root / ".continue" / "rules.md"
  assert continue_file.is_file(), ".continue/rules.md missing"

  cline_file = repo_root / ".clinerules"
  assert cline_file.is_file(), ".clinerules missing"

  roo_file = repo_root / ".roomodes"
  assert roo_file.is_file(), ".roomodes missing"
  roo_data = json.loads(roo_file.read_text(encoding="utf-8"))
  assert "customModes" in roo_data
