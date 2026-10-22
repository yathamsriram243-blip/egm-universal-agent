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

"""Unit tests validating all nine EGM subagent personas."""

import pathlib
import re
from typing import Dict, List
import pytest
import yaml

EXPECTED_PERSONAS = {
    "egm-zoom-out": "zoom_out.md",
    "egm-comprehension": "comprehension.md",
    "egm-design": "design_critic.md",
    "egm-implementation-readiness": "implementation_readiness.md",
    "egm-codebase-details": "codebase_details.md",
    "egm-structural": "structural.md",
    "egm-style": "style.md",
    "egm-synthesizer": "synthesizer.md",
    "egm-bootstrap-orchestrator": "bootstrap_orchestrator.md",
}

REQUIRED_SECTIONS = [
    "Role",
    "Objectives",
    "Review Procedure",
    "Evidence Requirements",
    "Output Schema",
    "Limitations",
    "Completion Criteria",
]


def parse_persona_file(file_path: pathlib.Path) -> (Dict, str):
  content = file_path.read_text(encoding="utf-8")
  assert "---" in content, f"Missing frontmatter in {file_path}"
  parts = content.split("---", 2)
  assert len(parts) >= 3, f"Malformed frontmatter in {file_path}"
  frontmatter = yaml.safe_load(parts[1])
  body = parts[2]
  return frontmatter, body


def test_all_nine_subagent_personas_exist(repo_root: pathlib.Path):
  agents_dir = repo_root / "agents"
  assert agents_dir.is_dir(), f"Agents directory missing at {agents_dir}"
  for persona_name, filename in EXPECTED_PERSONAS.items():
    agent_file = agents_dir / filename
    assert agent_file.is_file(), f"Expected persona file missing: {agent_file}"
    frontmatter, _ = parse_persona_file(agent_file)
    assert frontmatter.get("name") == persona_name, (
        f"Persona name in {filename} ({frontmatter.get('name')}) does not match {persona_name}"
    )
    assert frontmatter.get("description"), f"Missing description in {filename}"


def test_personas_define_all_seven_mandatory_sections(repo_root: pathlib.Path):
  agents_dir = repo_root / "agents"
  for persona_name, filename in EXPECTED_PERSONAS.items():
    agent_file = agents_dir / filename
    _, body = parse_persona_file(agent_file)
    for section in REQUIRED_SECTIONS:
      pattern = re.compile(rf"##\s+\d*\.?\s*{re.escape(section)}", re.IGNORECASE)
      assert pattern.search(body), (
          f"Persona '{persona_name}' in {filename} is missing mandatory section: '## {section}'"
      )


def test_personas_produce_required_deliverables(repo_root: pathlib.Path):
  agents_dir = repo_root / "agents"

  # 1. zoom_out
  _, zoom_body = parse_persona_file(agents_dir / "zoom_out.md")
  assert "Architectural Risks" in zoom_body
  assert "Structural Alternatives" in zoom_body
  assert "Critical Assumptions" in zoom_body
  assert "Architecture Verdict" in zoom_body

  # 2. comprehension
  _, comp_body = parse_persona_file(agents_dir / "comprehension.md")
  assert "Comprehension Blockers" in comp_body
  assert "Ambiguous Passages" in comp_body
  assert "Missing Explanations" in comp_body
  assert "Reader Questions" in comp_body

  # 3. design_critic
  _, design_body = parse_persona_file(agents_dir / "design_critic.md")
  assert "Design Objections" in design_body
  assert "Adversarial Scenarios" in design_body or "Failure Modes" in design_body
  assert "Mitigations" in design_body

  # 4. implementation_readiness
  _, impl_body = parse_persona_file(agents_dir / "implementation_readiness.md")
  assert "Readiness Verdict" in impl_body
  assert "Implementation Prerequisites" in impl_body
  assert "Work Breakdown" in impl_body
  assert "Acceptance Test" in impl_body

  # 5. codebase_details
  _, code_body = parse_persona_file(agents_dir / "codebase_details.md")
  assert "Drift" in code_body or "Discrepancy" in code_body
  assert "Reuse Opportunities" in code_body or "Reuse" in code_body

  # 6. structural
  _, struct_body = parse_persona_file(agents_dir / "structural.md")
  assert "Missing" in struct_body
  assert "Contradictions" in struct_body
  assert "Correction Guidance" in struct_body

  # 7. style
  _, style_body = parse_persona_file(agents_dir / "style.md")
  assert "Fluff" in style_body or "Hyperbole" in style_body
  assert "Conciseness" in style_body or "Precision" in style_body

  # 8. synthesizer
  _, synth_body = parse_persona_file(agents_dir / "synthesizer.md")
  assert "Unresolved Disagreements" in synth_body
  assert "Coverage Limitations" in synth_body or "Limitations" in synth_body

  # 9. bootstrap_orchestrator
  _, boot_body = parse_persona_file(agents_dir / "bootstrap_orchestrator.md")
  assert "Repository Documentation Plan" in boot_body or "Plan" in boot_body
  assert "Unresolved Questions" in boot_body
  assert "Verification Report" in boot_body


def test_no_corrupted_encoding_in_agents(repo_root: pathlib.Path):
  agents_dir = repo_root / "agents"
  for filename in agents_dir.glob("*.md"):
    raw_bytes = filename.read_bytes()
    # Check for typical CP1252 mis-decoded emoji sequences
    assert b"dY\"'" not in raw_bytes, f"Corrupted encoding in {filename.name}"
    assert b"dYY" not in raw_bytes, f"Corrupted encoding in {filename.name}"
