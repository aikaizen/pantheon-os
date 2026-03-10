---
name: venture-status-refresh
title: Venture Status Refresh
category: company-os
owner: Prometheus
version: 0.1.0
status: drafted
review_cadence: every 2 weeks
venture_scope: all ventures
triggers:
  - refresh venture status
  - update venture card
  - reconcile venture drift
use_cases:
  - Refresh a venture card
  - Update health and next action
  - Reconcile drift between sources
progressive_disclosure:
  - frontmatter for routing
  - SKILL.md body for execution
  - linked templates for concrete output shape
tests_required:
  - triggering
  - functional_success
  - workflow_improvement
---

# Venture Status Refresh


Concrete use cases:
- a venture card is stale
- the homepage, dashboard, and repo tell different stories
- a venture needs a fresh owner, health score, and next action

Execution:
1. Read the latest known signals: commits, docs, operator notes, and live product state.
2. Normalize the venture to one stage, one status, one health judgment, and one next action.
3. If the refresh implies deployment, publication, or budget change, emit an approval requirement.
4. Record the change in operational memory and schedule the next heartbeat.

Verification:
- the venture has owner, stage, status, health, and next action
- drift sources are named plainly
- any needed approval is explicit
- the next heartbeat is set

Linked assets:
- `templates/venture-status-refresh-template.md`
- `tests/acceptance.md`
