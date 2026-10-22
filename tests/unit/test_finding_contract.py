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

"""Unit tests validating the universal Standard Review-Finding Contract (11 fields)."""

import json
import pathlib
import re
import pytest

MANDATORY_FIELDS = [
    "id",
    "title",
    "severity",
    "category",
    "location",
    "evidence",
    "reasoning",
    "impact",
    "recommendation",
    "confidence",
    "status",
]

SEVERITY_LEVELS = {"critical", "high", "medium", "low", "informational"}
CATEGORIES = {
    "architecture",
    "correctness",
    "security",
    "requirements",
    "implementation",
    "testing",
    "documentation",
    "style",
}
CONFIDENCE_LEVELS = {"high", "medium", "low"}
STATUS_VALUES = {
    "open",
    "accepted",
    "rejected",
    "deferred",
    "fixed",
    "unverifiable",
}


def test_finding_contract_document_defines_all_eleven_fields(repo_root: pathlib.Path):
  contract_file = repo_root / "resources" / "finding_contract.md"
  assert contract_file.is_file(), f"Missing finding contract document: {contract_file}"
  content = contract_file.read_text(encoding="utf-8")

  for field in MANDATORY_FIELDS:
    assert f"`{field}`" in content or f"**`{field}`**" in content, (
        f"Field '{field}' missing from contract document"
    )

  for sev in SEVERITY_LEVELS:
    assert sev in content, f"Severity '{sev}' missing from contract document"

  for status in STATUS_VALUES:
    assert status in content, f"Status '{status}' missing from contract document"


def test_finding_contract_json_schema_parses_valid_payload(repo_root: pathlib.Path):
  contract_file = repo_root / "resources" / "finding_contract.md"
  content = contract_file.read_text(encoding="utf-8")

  # Extract JSON schema block
  match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", content)
  assert match, "JSON schema code block not found in finding_contract.md"
  schema = json.loads(match.group(1))

  assert schema.get("type") == "object"
  required = set(schema.get("required", []))
  for field in MANDATORY_FIELDS:
    assert field in required, f"Field '{field}' must be required in schema"

  # Validate a mock finding against constraints
  sample_finding = {
      "id": "EGM-ZOOM-001",
      "title": "Redundant caching layer introduces cache invalidation complexity",
      "severity": "high",
      "category": "architecture",
      "location": "docs/designs/auth.md#L45-L60",
      "evidence": "Section proposes Redis cache without measured latency bottleneck.",
      "reasoning": "Premature optimization violating YAGNI and increasing maintenance surface.",
      "impact": "Stale token risks and operational cost overhead.",
      "recommendation": "Query database directly and benchmark before adding Redis.",
      "confidence": "high",
      "status": "open",
  }

  assert sample_finding["severity"] in SEVERITY_LEVELS
  assert sample_finding["category"] in CATEGORIES
  assert sample_finding["confidence"] in CONFIDENCE_LEVELS
  assert sample_finding["status"] in STATUS_VALUES
