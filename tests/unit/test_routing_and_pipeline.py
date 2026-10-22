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

"""Unit tests validating command-to-subagent routing, review stage ordering, and fallback."""

import pathlib
import pytest
import yaml

EXPECTED_COMMANDS = {
    "egm-brainstorm": "egm_brainstorm",
    "egm-draft": "egm_draft",
    "egm-review": "egm_review",
    "egm-review-loop": "egm_review_loop",
    "egm-resolve": "egm_resolve",
    "egm-drift-report": "egm_drift_report",
    "egm-bootstrap": "egm_bootstrap",
}


def test_all_seven_commands_discovered(repo_root: pathlib.Path):
  skills_dir = repo_root / "skills"
  assert skills_dir.is_dir()
  for cmd_name, folder_name in EXPECTED_COMMANDS.items():
    skill_dir = skills_dir / folder_name
    assert skill_dir.is_dir(), f"Skill directory missing: {skill_dir}"
    skill_file = skill_dir / "SKILL.md"
    assert skill_file.is_file(), f"SKILL.md missing: {skill_file}"
    content = skill_file.read_text(encoding="utf-8")
    assert f"name: {cmd_name}" in content, f"Skill {cmd_name} missing name in frontmatter"


def test_review_skill_enforces_strict_four_stage_ordering(repo_root: pathlib.Path):
  review_skill = repo_root / "skills" / "egm_review" / "SKILL.md"
  content = review_skill.read_text(encoding="utf-8")

  # Stages must be listed in exact topological sequence
  pos_zout = content.find("Stage 1: Zoom Out")
  pos_comp = content.find("Stage 2: Comprehension")
  pos_crit = content.find("Stage 3: Critic")
  pos_read = content.find("Stage 4: Readiness")

  assert pos_zout != -1, "Stage 1: Zoom Out not found in egm-review"
  assert pos_comp != -1, "Stage 2: Comprehension not found in egm-review"
  assert pos_crit != -1, "Stage 3: Critic not found in egm-review"
  assert pos_read != -1, "Stage 4: Readiness not found in egm-review"

  assert pos_zout < pos_comp < pos_crit < pos_read, (
      "Review stages do not execute in required order (Zoom Out -> Comprehension -> Critic -> Readiness)"
  )

  # Check assigned subagents
  assert "egm-zoom-out" in content
  assert "egm-comprehension" in content
  assert "egm-design" in content
  assert "egm-implementation-readiness" in content


def test_skills_define_honest_sequential_fallback(repo_root: pathlib.Path):
  skills_to_check = ["egm_brainstorm", "egm_review", "egm_review_loop"]
  for skill_folder in skills_to_check:
    skill_file = repo_root / "skills" / skill_folder / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")
    assert "fallback" in content.lower(), (
        f"Skill {skill_folder} must document fallback protocol when subagents are unavailable"
    )
    assert "sequential" in content.lower(), (
        f"Skill {skill_folder} must mention sequential execution as fallback"
    )


def test_resolve_skill_classifies_findings(repo_root: pathlib.Path):
  resolve_skill = repo_root / "skills" / "egm_resolve" / "SKILL.md"
  content = resolve_skill.read_text(encoding="utf-8")

  taxonomies = ["defect", "valid improvement", "duplicate", "false positive", "needs clarification"]
  for tax in taxonomies:
    assert tax in content, f"Classification taxonomy '{tax}' missing from egm-resolve"

  # Verification requirement
  assert "test" in content.lower()
  assert "smallest safe fix" in content.lower()


def test_drift_report_is_read_only(repo_root: pathlib.Path):
  drift_skill = repo_root / "skills" / "egm_drift_report" / "SKILL.md"
  content = drift_skill.read_text(encoding="utf-8")
  assert "read-only" in content.lower() or "read only" in content.lower()
  assert "without mutating" in content.lower() or "do not modify" in content.lower() or "not modifying" in content.lower()
