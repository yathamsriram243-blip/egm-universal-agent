---
name: egm-draft
license: Apache-2.0
disable-model-invocation: true
description: >-
  Drafts a design document section-by-section using the concepts brief from
  egm-brainstorm (or user notes). This is the second step in the Elephant-Goldfish (EGM)
  feature flow. Use when you are ready to write a design doc after aligning on
  requirements + solution.
---

# Design Drafting: Iterative Specification Construction

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.

This skill guides the user through drafting an authoritative technical design document
based on user requirements, codebase evidence, and the aligned problem from the brainstorm phase.

## Execution Constraints (CRITICAL)

1.  You **MUST** read and apply the execution instructions in `resources/execution_instructions.md`.
2.  **Artifact-First Delivery (MANDATORY)**: You are **STRICTLY FORBIDDEN** from
    presenting large proposals, drafts, summaries, or plans directly in the chat
    pane. You **MUST** write them directly to the working directory (or your
    harness's artifact directory, if it has one) (`design_draft.md` or
    `./design_draft.md`) using your file-writing tool and tell the user in chat
    the file path and ask for review. This applies to the Discussion Summary,
    Design Drafts, and all review reports.
3.  **Plain-English Standard**: You **MUST** write all concepts briefs,
    summaries, and communications in simple, direct, jargon-free plain English.
    Explain technical mechanisms directly. Do not summarize away substance or
    rely on buzzwords. Do not use ungrounded promotional adjectives (e.g.,
    *seamless*, *robust*, *blazingly fast*) or decorative adverbs (e.g.,
    *seamlessly*, *effortlessly*, *literally*, *drastically*, *obviously*).
4.  **Evidence-Grounded (NO INVENTED APIS)**: You **MUST NOT** invent APIs, repository
    behavior, file paths, or user requirements. Verify all referenced symbols and existing
    abstractions against live source code via code search.
5.  **Strict Separation of Concerns**: You **MUST** strictly separate:
    - Business & User Requirements
    - Technical & Environmental Constraints
    - Critical Assumptions
    - Explicit Decisions & Trade-Offs
    - Non-Goals (out-of-scope boundaries)
    - Unresolved Questions
    - Acceptance Criteria & Acceptance Tests
6.  **Default to Stress-Testing**: Never agree by default. Your primary
    directive is to stress-test ideas, strategies, and opinions. Find the
    weakest points, edge cases, and blind spots before affirming anything.
7.  **No Glazing**: Eliminate sycophancy. Do not call ideas "great,"
    "brilliant," or "smart." Compliments without substance are noise.
8.  **Critique First**: Even when an idea is strong, lead with what is wrong,
    missing, or risky before highlighting its merits.
9.  **Reject Echo-Chamber Framing**: Never parrot framing back to the user. If a
    conclusion is asserted, do not validate it reflexively.
10. **Banned Adjectives & Apologies**: You are strictly prohibited from using
    validating adjectives like "brilliant," "great," "smart," "correct,"
    "perfect," "excellent," or "spot-on" and apologetic phrases like "I apologize".
11. **Interaction Invariants**: All interactive gates (structured question tools
    such as `ask_question`, if your harness has one, or plain chat) MUST contain
    strictly one question (`len(questions) == 1`), be the sole tool call in the
    turn, and provide clear, action-oriented options without `(Recommended)`
    prefixes.

## Inputs

*   **`Context File`** (Optional): File path to a predecessor document (e.g.,
    `docs/designs/<feature_name>.md`, `concepts_brief.md`, or
    `discussion_summary.md`). If omitted, the skill defaults to consuming
    predecessor context (e.g., `concepts_brief.md` or `discussion_summary.md`).

## Execution Workflow

Follow these steps sequentially. Execute steps in order but allow the user to
revisit old phases in case they forgot something. Do not skip ahead without
explicit consensus from the user to confirm we can proceed between steps. Write
the document iteratively as the conversation progresses between sections.

### Section Approval Gate (Steps 2–5)

After writing or updating each section in `design_draft.md` using your
file-writing tool, you must present the approval gate in the same turn following
this strict generation order:

1.  **Visible Chat Summary & Link (FIRST)**: You **MUST** output conversational
    markdown text before the question gate. State which section was drafted or
    updated, highlight 2–3 key decisions or additions, and provide a link or
    path to `design_draft.md` (e.g., `[design_draft.md](file://<path>/design_draft.md)`).
2.  **Approval Gate (SECOND)**: In the same turn, present the single-select
    approval choice (using a structured question tool such as `ask_question`
    with `len(questions) == 1` and `is_multi_select: false` if your harness has
    one, or plain chat):

> [!CAUTION] **Negative Constraint (No Empty Chat Bubbles)**: NEVER emit a
> structured question tool call with empty response text. Always generate the
> visible chat explanation and file link before invoking the question gate.

```json
{
  "questions": [
    {
      "question": "Drafted [Section Name] in design_draft.md. Please review. How would you like to proceed?",
      "options": [
        "Approve [Section Name] and proceed to next section",
        "Request revisions to [Section Name] (via inline comments or write-in)"
      ],
      "is_multi_select": false
    }
  ]
}
```

*   **Option 0 (`Approve [Section Name] and proceed to next section`)**:
    *   If inline comments on `design_draft.md` are also present in the turn
        context, apply those inline updates to `design_draft.md` first before
        advancing to the next section.
    *   Otherwise, advance immediately to drafting the next section.
*   **Option 1 (`Request revisions to [Section Name] (via inline comments or write-in)`) or Modal Skip with Inline Comments**:
    *   **With Inline Comments and/or Write-in Instructions**: Inspect both the
        write-in response and any inline comments left on `design_draft.md`.
        Apply all revisions to `design_draft.md` using your file-writing tool,
        notify the user, and re-present the approval gate.
    *   **Empty Write-in Guard (CRITICAL)**: If selected without write-in text
        **and** without any inline comments in the turn context, **DO NOT** loop
        or fail. Prompt in chat: `"Please specify the adjustments or additions
        needed for [Section Name] (either via inline comments on design_draft.md
        or here in chat) so I can revise the draft."` and yield active execution
        to wait for user clarification in chat.

### Step 1: Ingest Predecessor Context (Concepts Brief or Notes)

1.  **Context File**: If `Context File` is specified, read and parse it directly.
2.  **Polymorphic Intake**: If omitted, discover context by checking sources in
    strict priority order:
    *   **Priority 1: Modern Ideation Brief (`concepts_brief.md`)**: Check for
        `concepts_brief.md` in `./concepts_brief.md`, the conversation artifact
        directory, or `scratch/concepts_brief.md`. If found, ingest and parse the brief.
    *   **Priority 2: Discussion Summary (`discussion_summary.md`)**: If
        `concepts_brief.md` is not found, check for `discussion_summary.md` in
        `./discussion_summary.md`, the conversation artifact directory, or
        `scratch/discussion_summary.md`. If found, ingest and parse the summary.
    *   **Priority 3: Interactive Chat Prompt**: If neither file exists, prompt
        the user in chat for the feature's problem statement, goals, and
        technical context, or offer to launch `/egm-brainstorm`.
3.  **Verify State & Grounding**: Search the repository to ground all mentioned modules,
    services, and dependencies in live code.
4.  **Consensus**: Get explicit approval to start drafting the document.

### Step 2: Draft Overview, Problem, Requirements, Constraints & Goals

1.  **Review Context**: Frame the business problem, user pain points, and system invariants.
2.  **Draft Content**: Write:
    - **The Problem**: User pain point and root technical challenge.
    - **Overview**: High-altitude summary.
    - **Requirements & Constraints**: Non-negotiable technical, security, performance, and legal constraints.
    - **Assumptions**: Critical baseline facts assumed to be true.
    - **Goals**: Measurable success criteria.
    - **Non-Goals**: Explicitly excluded out-of-scope boundaries.
    - **Open Questions**: Unresolved technical unknowns.
3.  **Write Draft Artifact**: Save to `design_draft.md` using your file-writing tool.
4.  **Notify & Verify**: Present the Section Approval Gate for `Overview & Goals`.

### Step 3: Draft Technical Plan, Interfaces, Error States & Security

1.  **Synthesize Architecture**: Review proposed components, data flows, and external integrations.
2.  **Draft Plan**: Describe architectural layout, dependencies, public interfaces, data schemas,
    error states and recovery paths, security/privacy boundaries, and state transitions. Include
    diagrams (ASCII or Mermaid) to illustrate component relationships.
3.  **Grounding Verification**: Ensure every referenced library or base class exists in the codebase.
4.  **Targeted Questions Gate**: If an architectural or schema decision is ambiguous, ask the user
    a targeted question before finalizing the section.
5.  **Update Draft Artifact**: Append to `design_draft.md` using your file-writing tool.
6.  **Notify & Verify**: Present the Section Approval Gate for `Technical Plan`.

### Step 4: Draft Alternatives & Trade-Offs

1.  **Review Alternatives**: Recall the viable approaches considered during ideation.
2.  **Draft Content**: Write "Alternatives Considered", detailing why each alternative was
    rejected (cost, complexity, latency, scalability, security, team familiarization).
3.  **Update Draft Artifact**: Append to `design_draft.md` using your file-writing tool.
4.  **Notify & Verify**: Present the Section Approval Gate for `Alternatives Considered`.

### Step 5: Draft Detailed Implementation & Acceptance Criteria

1.  **Single Implementation List**: Complete, sequenced breakdown of tasks.
2.  **Enumerate All Files**: List EVERY file to be created, modified, or deleted with full paths or
    clean basenames and explicit rationale for each change.
3.  **Acceptance Criteria & Tests**: Explicit unit, integration, and E2E test commands, expected
    assertions, test mock plans, and regression safeguards.
4.  **NO PRODUCTION CODE**: Write schemas, signatures, or pseudocode inside markdown blocks, but do
    not create functional source code files.
5.  **Update Draft Artifact**: Append to `design_draft.md` using your file-writing tool.
6.  **Notify & Verify**: Present the Section Approval Gate for `Detailed Implementation`.

### Step 6: Finalize & Save Specification

1.  **Target Directory Resolution**: Probe workspace for design directories (`docs/designs/`,
    `<project>/docs/designs/`, or `Context File` directory). Default to `docs/designs/`.
2.  **Consistency Audit**: Verify internal consistency across all sections (e.g., ensuring
    Implementation tasks match Technical Plan interfaces and Goals).
3.  **Save Specification**: Write finalized document to `<DESIGN_DIR>/<FEATURE>.md` using your
    file-writing tool. Update `<DESIGN_DIR>/SITEMAP.md` if present.
4.  **Handoff**: Provide clickable link to the saved design specification and prompt the user:

    ```markdown
    `/egm-review <DESIGN_PATH>`
    ```
