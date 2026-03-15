---
name: skill-self-improvement
description: Run the cognee cycle on the shared skill pool — inspect observation logs, identify failing or underperforming skills, propose and apply amendments, evaluate results.
title: Skill Self-Improvement
category: company-os
owner: Dzambhala
version: 0.1.0
status: drafted
review_cadence: weekly
venture_scope: company
triggers:
  - review shared skills
  - run skill improvement cycle
  - inspect skill observations
  - improve underperforming skills
  - run cognee cycle
use_cases:
  - Weekly skill pool health check
  - Fix a skill that keeps failing
  - Improve trigger descriptions for under-used skills
progressive_disclosure:
  - frontmatter for routing
  - SKILL.md body for execution
  - linked protocol at _protocols/self-improvement.md for governance rules
tests_required:
  - triggering
  - functional_success
  - workflow_improvement
---

# Skill Self-Improvement

Concrete use cases:
- the observation log shows repeated failures for a specific skill
- a skill exists but is never triggered because its description is too vague
- a new capability has emerged that should be encoded as a reusable skill
- the weekly skill improvement heartbeat is due

Execution:
1. Read `_observations/execution_log.jsonl`. Group entries by skill name.
2. Identify patterns: failures > 2 for same skill, skills with zero invocations in the last 7 days, partial outcomes that suggest missing steps.
3. For each candidate skill, read its SKILL.md and compare the procedure to the observed failure mode.
4. Propose a specific patch. State: what changed, why, and what outcome is expected.
5. Check ownership in `_registry/agents.json` or skill frontmatter. If the skill is owned by another agent, log the proposal but do not apply it — flag for review.
6. If owned by self or unowned, apply via `skill_manage(action='patch')`. Increment the version.
7. Log the amendment to `_observations/execution_log.jsonl` with `skill: "self-improvement"`.
8. On the next invocation of the amended skill, compare outcome to prior failures. If worse, revert.

Ownership rules:
- Own skill or unowned skill: amend freely
- Another agent's skill: propose only, flag for their next heartbeat
- A.I.-owned skill (e.g., decision-gate-review): never amend without human approval

Verification:
- every proposed amendment has a stated reason
- ownership is checked before applying
- the observation log has a corresponding entry
- version is incremented on behavioral changes

Linked assets:
- `_protocols/self-improvement.md` — full governance protocol
- `_observations/execution_log.jsonl` — runtime evidence
- `_registry/agents.json` — agent roster and ownership lookup
