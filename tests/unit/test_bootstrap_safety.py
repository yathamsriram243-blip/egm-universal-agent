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

"""Unit tests validating safety gates, exclusions, and sensitive-file boundaries in egm-bootstrap."""

import pathlib
import pytest


def test_bootstrap_defines_fifteen_directory_safety_gate(repo_root: pathlib.Path):
  bootstrap_file = repo_root / "skills" / "egm_bootstrap" / "SKILL.md"
  content = bootstrap_file.read_text(encoding="utf-8")
  assert "15" in content, "15-directory safety threshold not defined in egm-bootstrap"
  assert "safety gate" in content.lower() or "safety" in content.lower()


def test_bootstrap_defines_sensitive_file_and_secret_protections(repo_root: pathlib.Path):
  bootstrap_file = repo_root / "skills" / "egm_bootstrap" / "SKILL.md"
  content = bootstrap_file.read_text(encoding="utf-8")
  assert ".gitignore" in content
  assert ".egmignore" in content
  assert "secrets" in content.lower()
  assert "credentials" in content.lower() or "credentials*" in content


def test_bootstrap_forbids_functional_code_and_vcs_commits(repo_root: pathlib.Path):
  bootstrap_file = repo_root / "skills" / "egm_bootstrap" / "SKILL.md"
  content = bootstrap_file.read_text(encoding="utf-8")
  assert "No Code Generation" in content or "no functional source code" in content.lower()
  assert "git commit" in content
  assert "preserve user-authored" in content.lower() or "preserve user" in content.lower()
