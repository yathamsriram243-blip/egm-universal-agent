---
name: egm-review-loop
license: Apache-2.0
disable-model-invocation: true
description: >-
  Concurrent review-subagent dispatch engine for the Elephant-Goldfish Model (EGM).
  Coordinates isolated Goldfish reviewers across targeted scopes, aggregates findings,
  and handles both direct and hierarchical dispatch with sequential fallback.
---

# EGM Review Loop: Concurrent Subagent Dispatch Engine

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.

## Overview

This skill acts as the central orchestration engine driving the concurrent Goldfish
review loop. It coordinates two distinct agent memory models:

*   **The Goldfish (Adversarial Auditors)**: Subagents spawned in isolated,
    fresh context windows to audit documents without historical bias.
*   **The Elephant (Persistent Resolver)**: The primary agent context holding
    system history to evaluate findings, triage feedback, and apply approved repairs.

The engine manages scope intake, resolves personas and standards, dynamically
re-calculates line ranges before each cycle, selects suitable review lenses,
and executes concurrent dispatch with honest reporting of coverage.

## Delegation & Dispatch Modes

Spawn each subagent with your harness's subagent tool (Antigravity: `invoke_subagent`;
Gemini CLI: subagents).

1.  **Direct Dispatch (Flat Swarm)**: The orchestrator invokes individual review
    personas directly in parallel (`egm-zoom-out`, `egm-comprehension`, `egm-design`,
    `egm-implementation-readiness`, `egm-codebase-details`, `egm-structural`, `egm-style`).
    Best suited when the host supports flat concurrency and root token budgets permit.
2.  **Hierarchical Dispatch (Synthesizer)**: The orchestrator dispatches an intermediate
    coordinator (`egm-synthesizer` at `agents/synthesizer.md`), which manages the swarm,
    deduplicates raw feedback, offloads context, and writes the consolidated report artifact.
    Use this when the host supports subagent nesting to keep the primary conversation clean.
3.  **Sequential Fallback Protocol**: If subagent execution is unavailable or unsupported on
    the host, perform clearly labeled sequential reviews in the current context. Never claim
    concurrency or independence that did not occur.

## Inputs

The caller or user provides these parameters:

*   **`TargetFile`**: Absolute or relative path to the target document (Required).
*   **`SemanticTarget`**: Descriptive targeting string (e.g. *"Target the H2 block 'Architecture'"*) or `full file`.
*   **`Reviewers`**: List of reviewer names (shortnames or paths). Defaults to recommended personas for the document type.
*   **`Standards`**: Mapping of reviewer names to standard names in `resources/document_standards/`.
*   **`GoldfishContext`**: A reading list (source files, directories, or documentation) fed to reviewers.

## Reviewer Selection Matrix

Select suitable review personas instead of dispatching every agent unnecessarily:

| Document Type | Recommended Primary Reviewers | Standards Applied |
| :--- | :--- | :--- |
| **Concept Brief / RFC** | `egm-zoom-out`, `egm-design`, `egm-comprehension` | `resources/document_standards/zoom-out-standard.md`, `resources/document_standards/heilmeier-standard.md` |
| **Feature Specification** | `egm-zoom-out`, `egm-design`, `egm-structural`, `egm-style` | `resources/document_standards/feature-spec-standard.md`, `resources/document_standards/zoom-out-standard.md` |
| **Implementation Plan** | `egm-implementation-readiness`, `egm-codebase-details`, `egm-style` | `resources/document_standards/implementation-readiness-standard.md` |
| **Full Architecture Doc** | Full Swarm (Phased or Hierarchical) | All applicable standards |

## Execution Workflow

### Step 1: Intake & Targeted Scoping

1.  Inspect provided inputs (`TargetFile`, `SemanticTarget`, `Reviewers`, `Standards`, `GoldfishContext`).
2.  If `TargetFile` is missing, prompt the user in chat.
3.  Bind reviewer selection according to the Reviewer Selection Matrix. Display the consolidated
    plan and confirm with the user before launching workers.

### Step 2: The Concurrent Review Loop

#### 2.1 Unconditional Target Line Resolution
Before every iteration, read `TargetFile` and locate the `SemanticTarget` header or anchor
to determine updated absolute line numbers ($L_{start}..L_{end}$). This ensures 100% targeting
accuracy across editing iterations.

#### 2.2 Swarm Execution & Coverage Monitoring
1.  Launch the assigned review personas using either **Hierarchical Dispatch** or **Direct Dispatch**.
2.  Provide each reviewer with a focused assignment, the resolved line bounds, and relevant context.
3.  **Honest Coverage Reporting**: Monitor subagent completion. If a subagent times out, fails to spawn,
    or encounters an error, record the incident explicitly under Coverage Limitations. Never fabricate
    results for an agent that failed to run.

#### 2.3 Finding Ingestion & Schema Validation
All findings MUST adhere to the 11-field Standard Review-Finding Contract (`resources/finding_contract.md`):
* `id`, `title`, `severity`, `category`, `location`, `evidence`, `reasoning`, `impact`, `recommendation`, `confidence`, `status`.

#### 2.4 Aggregated Resolution Hand-Off
1.  Pass the validated findings list to **`/egm-resolve`** in the primary Elephant context.
2.  Present the interactive resolution gate to the user.
3.  Execute approved edits on `TargetFile` using your file-editing tool.

#### 2.5 Iteration Boundary & Turn Taking
After resolution, check if any unaddressed critical/high findings remain:
* If findings remain and user requests re-audit: Loop back to Step 2.1 (re-scan line bounds).
* If zero findings remain or user concludes: Exit cleanly to parent workflow or chat summary.

### Step 3: Completion Deliverable

Write findings report to `goldfish_review_report.md` using your file-writing tool and output:
* Subagents dispatched and dispatch mode (Direct, Hierarchical, or Sequential Fallback).
* Coverage limitations or agent failures (if any).
* Severity breakdown and link to `goldfish_review_report.md`.
