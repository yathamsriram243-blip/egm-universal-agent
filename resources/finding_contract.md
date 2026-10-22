# Standard Review-Finding Contract (EGM-RFC-001)

This specification defines the universal, structured schema for all Elephant-Goldfish Model (EGM) review findings across skills, subagents, and host harnesses.

## 1. Finding Schema (11-Field Contract)

Every finding reported by an EGM reviewer subagent (`egm-zoom-out`, `egm-comprehension`, `egm-design`, `egm-implementation-readiness`, `egm-codebase-details`, `egm-structural`, `egm-style`), the `egm-synthesizer`, or aggregated in `/egm-review`, `/egm-review-loop`, and `/egm-resolve` MUST populate the following eleven fields:

| Field | Type | Allowed Values / Format | Description |
| :--- | :--- | :--- | :--- |
| **`id`** | `string` | Regex: `^[A-Z0-9_-]+$` (e.g., `EGM-ZOOM-001`, `EGM-DES-004`) | Stable, unique finding identifier. |
| **`title`** | `string` | 10–120 characters | Concise description of the issue. |
| **`severity`** | `enum` | `critical`, `high`, `medium`, `low`, `informational` | Impact severity level. |
| **`category`** | `enum` | `architecture`, `correctness`, `security`, `requirements`, `implementation`, `testing`, `documentation`, `style` | Technical taxonomy category. |
| **`location`** | `string` | File path, symbol, section header, or line range (e.g., `docs/designs/auth.md#L45-L60`, `src/auth.py:TokenValidator`) | Specific location in codebase or design doc. |
| **`evidence`** | `string` | Factual observed text, AST extract, or reproducible behavior | Concrete observed facts without conjecture. |
| **`reasoning`** | `string` | Technical causal explanation | Why the evidence constitutes a defect or risk. |
| **`impact`** | `string` | Operational, architectural, or developer impact | Realistic consequence if left unaddressed. |
| **`recommendation`** | `string` | Actionable remediation guidance | Concrete proposed change or alternative. |
| **`confidence`** | `enum` | `high`, `medium`, `low` | Reviewer certainty grounded in evidence. |
| **`status`** | `enum` | `open`, `accepted`, `rejected`, `deferred`, `fixed`, `unverifiable` | Finding lifecycle state. |

---

## 2. Structured Output Representations

### 2.1 JSON Schema Representation (for Structured Harness Outputs)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EGMFinding",
  "type": "object",
  "properties": {
    "id": { "type": "string", "pattern": "^[A-Z0-9_-]+$" },
    "title": { "type": "string" },
    "severity": { "type": "string", "enum": ["critical", "high", "medium", "low", "informational"] },
    "category": { "type": "string", "enum": ["architecture", "correctness", "security", "requirements", "implementation", "testing", "documentation", "style"] },
    "location": { "type": "string" },
    "evidence": { "type": "string" },
    "reasoning": { "type": "string" },
    "impact": { "type": "string" },
    "recommendation": { "type": "string" },
    "confidence": { "type": "string", "enum": ["high", "medium", "low"] },
    "status": { "type": "string", "enum": ["open", "accepted", "rejected", "deferred", "fixed", "unverifiable"] }
  },
  "required": [
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
    "status"
  ]
}
```

### 2.2 Markdown Representation (for Natural Language & Chat Harnesses)

Where native JSON structured outputs are unavailable or when delivering markdown report artifacts (`goldfish_review_report.md`), each finding MUST be rendered in standard Markdown:

```markdown
### [[id]] [title]
* **Severity**: [critical | high | medium | low | informational]
* **Category**: [architecture | correctness | security | requirements | implementation | testing | documentation | style]
* **Location**: `[file path, symbol, section, or line range]`
* **Evidence**: [Observed facts or reproducible behavior]
* **Reasoning**: [Why the observed evidence matters]
* **Impact**: [Realistic operational, architectural, or user consequence]
* **Recommendation**: [Concrete proposed action or patch]
* **Confidence**: [high | medium | low]
* **Status**: [open | accepted | rejected | deferred | fixed | unverifiable]
```

---

## 3. Status Lifecycle Matrix

```
   [open]
     ├──> [accepted] ────> [fixed]
     ├──> [rejected] (contested with evidence)
     ├──> [deferred] (future milestone / out of scope)
     └──> [unverifiable] (insufficient context / inaccessible code)
```

1. **`open`**: Initial state produced by a Goldfish reviewer.
2. **`accepted`**: The Elephant / user agrees the finding is a valid defect or improvement.
3. **`rejected`**: Contested by the Elephant with technical justification or false positive evidence.
4. **`deferred`**: Valid observation, but acknowledged as intentional non-goal or deferred to later phase.
5. **`fixed`**: Patch applied and verified via tests.
6. **`unverifiable`**: Cannot be verified due to missing dependencies, external services, or ambiguous specs.
