---
name: egm-resolve
license: Apache-2.0
disable-model-invocation: true
description: >-
  The Elephant resolution skill. Ingests structured review findings, performs interactive
  triage and classification, proposes minimal safe patches, applies approved edits,
  and runs automated verification tests.
---

# EGM Resolve: Interactive Triage & Patch Verification Engine

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.

## Overview

This skill operates within the primary Elephant context window to parse review findings
from Goldfish subagents. It evaluates critiques against repository facts, classifies findings,
presents an interactive triage gate to the human engineer, proposes the smallest safe fix,
applies approved edits, and verifies changes using targeted tests.

## Context Strategy (Elephant Memory)

Run this skill in the persistent conversation session that generated the target document or
code (the Elephant). This preserves historical rationale, architectural context, and intent
needed to defend accurate design decisions and craft minimal, high-quality repairs.

## Inputs

*   **`TargetFile`**: Path to the target document or source file (Required).
*   **`LineRange`**: Target line numbers or `full file` (Required).
*   **`FindingsList`**: List of findings conforming to the 11-field Standard Review-Finding Contract (`resources/finding_contract.md`).

## Finding Classification Taxonomy

For every finding in `FindingsList`, the Elephant classifies its disposition:

1.  **`defect`**: Confirmed technical, structural, or logical flaw requiring a code or document fix.
2.  **`valid improvement`**: Sound suggestion that enhances clarity, performance, or simplicity.
3.  **`duplicate`**: Redundant observation already covered by another finding ID.
4.  **`false positive`**: Reviewer misunderstood codebase semantics, out-of-scope boundaries, or intentional design invariants. Defended with code evidence.
5.  **`needs clarification`**: Reviewer raised a valid ambiguity that requires human direction before a fix can be determined.

## Execution Constraints & Safety Rules

1.  **No Silent Discarding**: You MUST NOT silently ignore or delete disputed findings. Every finding
    must have an explicit disposition (`accepted`, `rejected`, `deferred`, `fixed`).
2.  **Smallest Safe Fix**: Propose the minimal surgical modification necessary to resolve the defect.
    Do not rewrite unrelated paragraphs or refactor adjacent code.
3.  **Preserve User Work**: Do not overwrite unrelated changes or revert concurrent human edits.
4.  **No Speculative Verification Claims**: You MUST NOT claim a fix is verified unless the relevant
    test command was executed and exited with code 0 in the shell tool.
5.  **Scope Boundary Enforcement**: Only apply patches to files and sections explicitly approved by the user.

## Execution Workflow

### Step 1: Ingest & Evaluate Findings

1.  Read `TargetFile` at `LineRange` and inspect all referenced source files using your file-reading tool.
2.  Evaluate each finding against live repository code and authoritative specs.
3.  Assign classification (`defect`, `valid improvement`, `duplicate`, `false positive`, or `needs clarification`).
4.  Formulate proposed minimal textual replacements or code edits for accepted items.

### Step 2: Compile Triage Report

Write the annotated triage report to `goldfish_review_report.md` in the working directory (or harness artifact directory) using your file-writing tool:

```markdown
# EGM Resolution & Triage Report

**Target:** `[TargetFile]` (`[LineRange]`)
**Date:** [YYYY-MM-DD]

## Finding-by-Finding Disposition

### [[id]] [title] - Severity: [Severity]
* **Category**: [Category] | **Location**: `[Location]`
* **Disposition**: [defect | valid improvement | duplicate | false positive | needs clarification]
* **Elephant Evaluation**: [Technical rationale defending or accepting the finding]
* **Proposed Action**: [CONTEST | PROPOSE FIX | DEFER]
* **Proposed Patch / Minimal Edit**:
  ```diff
  - [Original text / code to remove]
  + [Minimal replacement text / code to add]
  ```
* **Status**: [open | accepted | rejected | deferred | fixed]
```

### Step 3: Interactive Triage Gate

Present the triage gate to the user in chat:

*"I have compiled the audit triage into `goldfish_review_report.md`. Please choose how to proceed:
- **Auto accept**: Apply all proposed fixes for confirmed defects and valid improvements.
- **Interactive breakdown**: Walk through findings one-by-one to approve, reject, or adjust each fix.
- **Continue without changes**: Proceed without applying fixes (leave findings deferred).
- **Custom instruction**: Provide specific guidance or edits."*

Yield execution immediately by calling zero tools in this turn payload and wait for user response.

### Step 4: Patch Application & Safe Editing

Upon approval:
1. Apply approved diffs using your file-editing tool (`edit_file`).
2. Verify that edits apply cleanly without mangling surrounding text.

### Step 5: Automated Verification & Regression Testing

1.  Detect and execute the relevant test command for the project (e.g., `pytest`, `npm test`, `cargo test`, `go test ./...`).
2.  If tests fail, inspect the failure log, formulate a rollback or corrective patch, and alert the user.
3.  Record test execution command and exit status in the report.

### Step 6: Post-Resolution Sync & Output

Update `goldfish_review_report.md` with final statuses (`fixed`, `rejected`, `deferred`) and return:
1. Finding-by-finding disposition summary.
2. Applied patches.
3. Verification results and test output.
4. Remaining risks or unaddressed items.
