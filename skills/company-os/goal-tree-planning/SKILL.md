---
name: goal-tree-planning
title: Goal Tree Planning
category: company-os
owner: Hermetic_Demiurge
version: 0.1.0
status: drafted
review_cadence: monthly
venture_scope: company + venture + project
triggers:
  - create goal hierarchy
  - break strategy into tasks
  - plan venture goals
use_cases:
  - Translate strategy into execution
  - Decompose a venture initiative
  - Expose blockers and dependencies
progressive_disclosure:
  - frontmatter for routing
  - SKILL.md body for execution
  - linked templates for concrete output shape
tests_required:
  - triggering
  - functional_success
  - workflow_improvement
---

# Goal Tree Planning


Concrete use cases:
- a company objective needs venture-level decomposition
- a venture has too much motion and not enough structure
- a project needs explicit tasks, dependencies, and gates

Execution:
1. Write the company-level intent in one sentence.
2. Break it into venture goals, then into project tasks.
3. Attach owners, due dates, dependencies, and approval links.
4. Keep the tree minimal: no orphan tasks, no vague buckets, no hidden blockers.
5. End with the immediate next three actions.

Verification:
- every task belongs to a goal
- every goal has an owner and target
- blockers are visible
- tasks are decomposed enough to execute

Linked assets:
- `templates/goal-tree-planning-template.md`
- `tests/acceptance.md`
