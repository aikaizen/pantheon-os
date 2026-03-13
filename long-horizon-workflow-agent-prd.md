# PRD — Long-Horizon Workflow Agent

## Product summary
An agent designed to manage workflows that take multiple weeks, involve several people and systems, and fail when follow-up, state tracking, and coordination drift.

## Problem
Most automation tools are good at immediate tasks but weak at long-running workflows.

Examples:
- onboarding and implementation
- client delivery programs
- audits and compliance work
- recruiting pipelines
- multi-stage sales cycles
- strategic projects with several milestones

These workflows break because:
- status is spread across tools
- next actions are unclear
- deadlines slip silently
- blockers are noticed too late
- ownership changes are not reflected in the system

## Target users
Primary users:
- delivery managers
- operators
- project leads
- client success teams

Secondary users:
- founders
- consultants
- client approvers

## Jobs to be done
- keep a multi-week workflow moving without constant manual supervision
- know what is blocked, late, at risk, or ready
- preserve continuity across handoffs
- prompt the right person at the right time
- provide a trustworthy status view for humans and clients

## Product goals
- reduce workflow drift
- improve on-time completion
- reduce missed follow-up
- give operators a reliable state machine for long-running work
- make multi-week coordination feel manageable

## Non-goals
- not a general-purpose chatbot
- not a pure task manager
- not a full PM suite replacement in v1

## Core use cases
### 1. Client onboarding
Track every stage from kickoff through implementation, approval, training, and handoff.

### 2. Managed service delivery
Coordinate recurring, milestone-based work with multiple stakeholders and dependencies.

### 3. Internal transformation program
Run a long, cross-functional operating initiative with explicit checkpoints and escalation logic.

## Product principles
- state must be explicit
- next action must always be visible
- every workflow needs owners, deadlines, blockers, and evidence
- human judgment remains available at key checkpoints
- follow-up should be proactive, not reactive

## Functional requirements
### Workflow templates
- create reusable workflow templates with stages, milestones, dependencies, and SLAs
- allow per-client customization without destroying standardization

### Workflow state model
- every workflow instance has explicit states such as planned, active, blocked, waiting, at-risk, completed, archived
- each stage has entry and exit criteria

### Next-action engine
- always compute the current next best action
- assign that action to a responsible person or agent
- show why the action is next

### Follow-up and reminders
- send reminders based on due dates, inactivity, missing inputs, and blocked dependencies
- escalate when thresholds are crossed

### Blocker management
- capture blockers with owner, severity, dependency, and resolution target
- surface blockers prominently in the workflow view

### Evidence and status notes
- attach notes, files, and decisions to milestones and workflow state changes
- maintain an auditable history of progress

### Check-ins
- support recurring workflow reviews
- auto-generate status snapshots for weekly or milestone reviews

### Handoffs
- summarize workflow state for a new owner
- show open issues, recent changes, and critical dependencies

### Client-safe visibility
- allow external or client viewers to see a filtered status surface when needed

## Non-functional requirements
- resilient long-duration state handling
- clear audit history
- notification reliability
- simple enough for operational teams to use every day

## UX / workflow
### Operator loop
1. open workflow dashboard
2. review at-risk and blocked workflows
3. inspect suggested next actions
4. approve or change assignments
5. send reminders or escalate blockers

### Workflow instance loop
1. instantiate template
2. set owners and due dates
3. system tracks progress and inactivity
4. reminders and escalations fire as needed
5. workflow closes with evidence and summary

## Core entities
- Workflow template
- Workflow instance
- Stage
- Milestone
- Dependency
- Blocker
- Next action
- Check-in
- Evidence item
- Status event

## Key metrics
- on-time completion rate
- blocker resolution time
- overdue milestone rate
- follow-up response time
- workflow reopening rate
- operator hours saved per workflow

## Risks
### Too complex for daily use
Mitigation:
- start with a narrow workflow template set
- prioritize next-action clarity over configuration depth

### Weak trust in agent recommendations
Mitigation:
- make reasoning and evidence visible
- allow human override everywhere

### Notification fatigue
Mitigation:
- focus on high-signal reminders and escalation rules

## Phased roadmap
### Phase 1
- workflow templates
- explicit state model
- next-action view
- reminders and blocker tracking
- weekly status snapshot

### Phase 2
- richer dependency management
- external/client visibility
- handoff summaries
- approvals at key milestones

### Phase 3
- predictive risk scoring
- optimization recommendations
- portfolio analytics across many workflows

## Launch criteria
- one real multi-week workflow runs end-to-end in the system
- overdue and blocked work is clearly surfaced
- operators report lower coordination overhead and fewer missed follow-ups
