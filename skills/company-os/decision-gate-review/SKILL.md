---
name: decision-gate-review
title: Decision Gate Review
category: company-os
owner: A.I.
version: 0.1.0
status: drafted
review_cadence: monthly
venture_scope: all
triggers:
  - review approval gate
  - approve deployment
  - approve publication
use_cases:
  - Deployment approval
  - Publication approval
  - Budget escalation approval
progressive_disclosure:
  - frontmatter for routing
  - SKILL.md body for execution
  - linked templates for concrete output shape
tests_required:
  - triggering
  - functional_success
  - workflow_improvement
---

# Decision Gate Review


Concrete use cases:
- a deployment is ready but should not go live without signoff
- a public article or launch message could create reputational risk
- a recurring automation or cost increase needs explicit permission

Execution:
1. State the action under review in one sentence.
2. Name the blast radius, the reversibility, and the risk level.
3. List the exact criteria that must be true before approval.
4. Make the approver, due date, and fallback plan explicit.
5. Return one of: approved, pending, in_review, rejected.

Verification:
- risk is named clearly
- criteria are testable, not vague
- approver and due date are set
- the resulting status is unambiguous

Linked assets:
- `templates/decision-gate-review-template.md`
- `tests/acceptance.md`
