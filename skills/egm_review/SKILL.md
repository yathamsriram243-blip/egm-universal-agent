---
name: egm-review
license: Apache-2.0
disable-model-invocation: true
description: >-
  Orchestrates the EGM Goldfish Review Protocol. Used as part of the EGM
  process to perform design document reviews. Executes four review stages in strict sequence:
  Stage 1: Zoom Out, Stage 2: Comprehension, Stage 3: Critic, Stage 4: Readiness.
---

# EGM Review: Multi-Stage Verification Pipeline

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.

Orchestrates multi-stage design and code verification across specialized, stateless Goldfish personas.

## Delegation

A Goldfish runs in a fresh context with no conversation history. Spawn each
subagent with your harness's subagent tool (Antigravity: `invoke_subagent`;
Gemini CLI: subagents). Each subagent is defined in `agents/<file>.md`, and its
frontmatter `name` (for example `egm-zoom-out`) is the subagent type to request
where your harness registers named subagents. Otherwise spawn a general-purpose
subagent and tell it to read that persona file first. Pass the prompt verbatim
and wait for the report. If your harness cannot nest subagents,
use direct dispatch instead of the synthesizer. See `docs/harnesses.md`.

**Fallback Protocol**: If subagent execution is unavailable or unsupported on the
host harness, execute clearly labeled sequential reviews in the primary thread.
Never claim concurrency or independence that did not occur.

## Execution Constraints (CRITICAL)

1.  **Artifact-First Delivery (MANDATORY)**: You are **STRICTLY FORBIDDEN** from
    presenting large proposals, drafts, summaries, or plans directly in the chat
    pane. You **MUST** write them to the working directory (or your harness's
    artifact directory, if it has one) using your file-writing tool and then
    tell the user in chat the file path and ask for review.
2.  **Strict Stage Ordering (MANDATORY)**: The review stages MUST be executed in
    this strict topological sequence:
    *   **Stage 1: Zoom Out** (`egm-zoom-out`) — system boundaries, architecture, simplicity, YAGNI, reuse.
    *   **Stage 2: Comprehension** (`egm-comprehension`) — naive reader clarity, definitions, unstated assumptions.
    *   **Stage 3: Critic** (`egm-design`) — hostile adversarial stress-testing, edge cases, failure modes.
    *   **Stage 4: Readiness** (`egm-implementation-readiness`) — feasibility, dependencies, migration, testability.
3.  **Standard Finding Contract (11 Fields)**: All findings across all stages MUST conform to the
    Standard Review-Finding Contract defined in `resources/finding_contract.md`.
4.  **No False Approvals**: You MUST NOT mark a design approved merely because all stages completed.
    Approval requires an explicit `READY` verdict with zero unresolved critical/blocking findings.
5.  **Deduplication & Disagreement Preservation**: Deduplicate overlapping observations while
    preserving minority high-impact objections and conflicting recommendations.
6.  **Grounded Evidence**: Verify that all findings cite concrete file paths, line ranges, or symbol names.
7.  **Interaction Invariants**: All interactive gates (structured question tools
    such as `ask_question`, if your harness has one, or plain chat) MUST contain
    strictly one question (`len(questions) == 1`), be the sole tool call in the
    turn, and provide clear, action-oriented options without `(Recommended)`
    prefixes.

## Inputs

*   **`TargetFile`**: Absolute or relative path to the design document (Required).
*   **`GoldfishContext`** (Optional): Reading list to establish baseline knowledge for reviewers.
*   **`Step`** (Optional): Specific stage or preset to run (`interactive`, `uninterrupted`, `1`, `2`, `3`, `4`).

## Workflow

### Step 1: Intake & Validation

1.  **Verify TargetFile**: If missing, prompt the user in chat for the target file path.
2.  **Verify Context**: If `GoldfishContext` is omitted, default to reading files referenced directly in `TargetFile`.
3.  **Discover Semantic Boundary**: Scan `TargetFile` for the dividing header `## Detailed Implementation Plan` (or synonyms).
    *   `FeatureRange`: Lines covering Overview, Requirements, and Architecture (e.g. Lines 1 to split boundary - 1).
    *   `DetailedRange`: Lines covering Implementation Tasks, Rollout, and Testing (e.g. Split boundary to End).

### Step 2: Preset Selection Gate

If `Step` is unspecified, present the single-select execution mode gate:

```json
{
  "questions": [
    {
      "question": "Select review execution mode for this document:",
      "options": [
        "Interactive review (step-by-step with checkpoint gates between stages)",
        "Consolidated report (run all four stages uninterrupted and compile deliverable)",
        "Feature specification only (Stages 1-3: Zoom Out, Comprehension, Critic)",
        "Implementation readiness only (Stage 4: Implementation Readiness)"
      ],
      "is_multi_select": false
    }
  ]
}
```

### Step 3: Four-Stage Review Execution

#### Stage 1: Zoom Out Review (`egm-zoom-out`)
*   **Target Scope**: Full file.
*   **Standard Applied**: `resources/document_standards/zoom-out-standard.md`.
*   **Subagent**: Dispatch `egm-zoom-out` (or `egm-synthesizer` with `Reviewers: [egm-zoom-out]`).
*   **Deliverable**: Write findings to `zoom_out_report.md`.
*   **Checkpoint**: Present single-select gate to proceed to Stage 2, pause for manual edits, or resolve findings.

#### Stage 2: Comprehension Review (`egm-comprehension`)
*   **Target Scope**: `FeatureRange` and `DetailedRange`.
*   **Standard Applied**: `resources/document_standards/re-implementation-standard.md`.
*   **Subagent**: Dispatch `egm-comprehension`.
*   **Deliverable**: Write findings to `comprehension_report.md`.
*   **Checkpoint**: Present single-select gate to proceed to Stage 3, pause, or resolve findings.

#### Stage 3: Design Critique (`egm-design` supported by `egm-structural` and `egm-style`)
*   **Target Scope**: `FeatureRange`.
*   **Standard Applied**: `resources/document_standards/feature-spec-standard.md`.
*   **Subagents**: Dispatch `egm-design`, `egm-structural`, `egm-style`.
*   **Deliverable**: Write findings to `critic_report.md`.
*   **Remediation Option**: If critical findings exist, offer to launch `/egm-resolve` to triage and patch issues before proceeding to Stage 4.
*   **Checkpoint**: Present single-select gate to proceed to Stage 4, pause, or resolve findings.

#### Stage 4: Implementation Readiness (`egm-implementation-readiness` supported by `egm-codebase-details`)
*   **Target Scope**: `DetailedRange`.
*   **Standard Applied**: `resources/document_standards/implementation-readiness-standard.md`.
*   **Subagents**: Dispatch `egm-implementation-readiness`, `egm-codebase-details`, `egm-style`.
*   **Deliverable**: Write findings to `implementation_readiness_report.md`.
*   **Remediation Option**: If defects are discovered, offer to launch `/egm-resolve` to triage and apply approved fixes.

### Step 4: Consolidated Deliverable & Final Verdict

Compile all stage findings into `consolidated_review_report.md` using your file-writing tool.
The report MUST include:

```markdown
# EGM Consolidated Review Report

**Target:** `[TargetFile]`
**Status:** [READY | NEEDS REVISION | NOT READY]

## 1. Executive Summary & Readiness Verdict
* **Final Verdict:** [READY | NEEDS REVISION | NOT READY]
* **Severity Breakdown:** Critical: [N], High: [N], Medium: [N], Low: [N], Informational: [N]
* **Verdict Rationale:** [Clear causal explanation of whether the design is safe to implement.]

## 2. Stage-by-Stage Findings Summary
* **Stage 1 (Zoom Out):** [Pass / Findings count / Key architectural risks]
* **Stage 2 (Comprehension):** [Pass / Findings count / Key comprehension blockers]
* **Stage 3 (Critic):** [Pass / Findings count / Key adversarial objections]
* **Stage 4 (Readiness):** [Pass / Findings count / Prerequisites & actionability]

## 3. Unresolved Questions & Critical Assumptions
* [Open question 1 with affected scope and impact]
* [Open question 2 with affected scope and impact]

## 4. Prioritized Unique Findings (11-Field Contract)
[Formatted findings sorted by severity: Critical -> High -> Medium -> Low -> Informational]
```

Notify the user in chat with a clean link to `consolidated_review_report.md` and present the explicit readiness verdict.
