---
name: build-stream-synthesis
title: Build Stream Synthesis
category: company-os
owner: Thoth
version: 0.1.0
status: drafted
review_cadence: daily
venture_scope: portfolio
triggers:
  - summarize build stream
  - turn commits into operator signal
  - draft build stream note
use_cases:
  - Daily build digest
  - Cross-repo pattern review
  - Lab Notes draft generation
progressive_disclosure:
  - frontmatter for routing
  - SKILL.md body for execution
  - linked templates for concrete output shape
tests_required:
  - triggering
  - functional_success
  - workflow_improvement
---

# Build Stream Synthesis


Concrete use cases:
- multiple repos changed and someone needs the signal, not the raw log
- a build-stream post should come from actual work instead of vague updates
- operators need to see patterns, blockers, and likely next moves across the portfolio

Execution:
1. Collect changes across the portfolio for the target window.
2. Group them by venture, work type, and operator.
3. Extract the few patterns that actually matter.
4. Name blockers plainly and attach a next action to each pattern.
5. Output both an internal sitrep and a public-draft version when appropriate.

Verification:
- raw change volume is condensed into actionable signal
- the output distinguishes internal versus public language
- blockers and next actions are explicit
- cross-repo patterns are named, not implied

Linked assets:
- `templates/build-stream-synthesis-template.md`
- `tests/acceptance.md`
