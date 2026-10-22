---
name: egm-drift-report
license: Apache-2.0
disable-model-invocation: true
description: >-
  Detects divergence between authoritative design specifications and live codebase implementation.
  Produces an actionable, structured drift report with file and symbol evidence without mutating code.
---

# EGM Drift Report: Specification-to-Code Drift Detector

## Overview

When specifications and codebase reality diverge, systems accumulate hidden debt and developer
confusion. This skill systematically audits checked-in design specifications, architecture
contracts, and READMEs against live source code to detect and report drift.

## Execution Constraints & Safety Rules

1.  **Read-Only Operations (STRICT)**: You are **STRICTLY FORBIDDEN** from modifying, patching,
    or refactoring code or documentation during drift detection. Report discrepancies only.
    Remediation is deferred to a separate, user-authorized `/egm-resolve` session.
2.  **Concrete Evidence Required**: Every reported drift MUST cite the exact specification file
    and section alongside the concrete source code file, class, function, or line range.
3.  **Distinguish Confirmed Drift from Uncertainty**: Distinguish between confirmed drift
    (explicit contract violation) and unconfirmed drift caused by incomplete context or dynamic dispatch.
4.  **Avoid Trivia**: Do not treat every minor internal implementation detail (e.g. local loop variables)
    as a design violation. Focus on architectural contracts, public APIs, models, data flows, and invariants.

## Inputs

*   **`DesignPath`**: Path to a specific design document or directory of design docs/READMEs (e.g. `docs/designs/`). If omitted, prompt the user.
*   **`SourceRoot`** (Optional): Path to the codebase root (defaults to workspace root).

## Execution Workflow

### Step 1: Discover Authoritative Specifications

1.  Locate all design documents and contract files in `DesignPath`.
2.  For each document, identify authoritative statements:
    *   Public APIs, endpoints, and method signatures.
    *   Data structures, models, schemas, and fields.
    *   Architectural component boundaries and interaction flows.
    *   Invariants, error handling rules, and acceptance criteria.

### Step 2: Source Code Verification

For each documented contract:
1.  **Locate Source Files**: Trace referenced files, classes, and symbols in the live repository using code search.
2.  **Verify Fidelity**:
    *   **Missing Features**: Documented API endpoints, methods, or CLI commands absent from code.
    *   **Incomplete Data Models**: Dataclasses, structs, or database models missing documented fields.
    *   **Logic Divergence**: Hardcoded values or stub implementations where dynamic logic was specified.
    *   **Contract Conflicts**: Parameter types, return types, or error conditions conflicting with the spec.
    *   **Undocumented Behavior**: Critical public methods or side effects present in code but missing from docs.

### Step 3: Classify & Structure Drift Findings

Every finding MUST follow the 11-field Standard Review-Finding Contract (`resources/finding_contract.md`)
and be classified by severity:
* **Critical**: Security breach, data corruption hazard, or completely broken public contract.
* **High**: Documented core feature missing or unhandled error state.
* **Medium**: Field name drift, type inconsistency, or outdated architectural diagram.
* **Low / Informational**: Minor nomenclature discrepancy or formatting inconsistency.

### Step 4: Generate Deliverable Drift Report

Write the report to `{YYYY-MM-DD}_DRIFT_REPORT.md` (e.g., `2026-10-23_DRIFT_REPORT.md`) in the working directory using your file-writing tool:

```markdown
# EGM Specification-to-Code Drift Report

**Audit Date:** [YYYY-MM-DD]
**Target Specifications:** `[DesignPath]`
**Codebase Root:** `[SourceRoot]`

## Executive Summary
* **Total Specifications Audited:** [N]
* **Confirmed Drifts:** [N] (Critical: [C], High: [H], Medium: [M], Low: [L])
* **Uncertain / Incomplete Evidence:** [N]

---

## Drift Findings by Affected Contract

### [[id]] [title]
* **Severity**: [critical | high | medium | low | informational]
* **Category**: correctness
* **Affected Specification**: `[spec_file.md#Lstart-Lend]`
* **Live Code Evidence**: `[src_file.py:Symbol#Lstart-Lend]`
* **Discrepancy Description**: [Factual divergence observed]
* **Reasoning**: [Why this drift causes operational, integration, or maintenance issues]
* **Impact**: [System defect, API breakage, developer confusion]
* **Recommended Correction**: [Update specification to reflect intentional change, or implement missing code]
* **Confidence**: [high | medium | low]
* **Status**: open
```

Notify the user in chat with the summary and report path.
