---
name: weekly-operating-review
title: Weekly Operating Review
category: company-os
owner: Thoth
version: 0.1.0
status: drafted
review_cadence: weekly
venture_scope: all
triggers:
  - prepare weekly operating review
  - summarize portfolio this week
  - run weekly sitrep
use_cases:
  - Prepare portfolio sitrep
  - Run leadership review
  - Reset agent priorities for the coming week
progressive_disclosure:
  - frontmatter for routing
  - SKILL.md body for execution
  - linked templates for concrete output shape
tests_required:
  - triggering
  - functional_success
  - workflow_improvement
---

# Weekly Operating Review


Concrete use cases:
- when the principal needs one clean view of the portfolio
- when multiple ventures have drifted and need a single reset
- when agents need the next-week priority stack before waking into work

Execution:
1. Gather current venture status, open approvals, due heartbeats, and budget variance.
2. Sort ventures into: strong, at-risk, blocked, and ready-to-ship.
3. For each venture, write one line for what changed, one line for what matters, and one next action.
4. Surface decisions required from A.I. explicitly. Do not bury them in narrative.
5. End with the next seven-day priority stack, capped at five priorities.

Verification:
- every active venture is represented
- decisions required are explicit
- there are no more than five next-week priorities
- open approvals and due heartbeats are visible

Linked assets:
- `templates/weekly-operating-review-template.md`
- `tests/acceptance.md`
