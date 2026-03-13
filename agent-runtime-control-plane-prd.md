# PRD — Agent Runtime Control Plane

## Product summary
A control plane for operating internal and client-facing agents safely across multiple workflows, environments, and teams.

## Problem
Once a consultancy runs multiple agents or automations for multiple clients, operations become fragile.

Common failures:
- no single place to see what agents are running
- unclear ownership of prompts, policies, connectors, and runtime versions
- weak approval paths for higher-risk actions
- poor auditability
- unclear model/runtime costs by client, workflow, or operator

The result is avoidable operational risk and weak trust.

## Target users
Primary users:
- founder / principal operator
- delivery lead
- solutions architect
- automation engineer

Secondary users:
- client-side approver
- operations manager
- security or compliance reviewer

## Jobs to be done
- show me every active agent, what it can do, and what it touched
- let me approve or block risky agent actions
- let me see costs, failures, and throughput by workspace or workflow
- let me manage versions of prompts, policies, connectors, and workflows
- let me isolate one client’s environment from another

## Product goals
- make agent operations legible
- reduce operational and reputational risk
- provide explicit governance over actions
- expose runtime and spend visibility
- improve client trust through auditability and control

## Non-goals
- not a full no-code automation builder in v1
- not a generalized model provider
- not a consumer chatbot surface

## Core use cases
### 1. Multi-client agent operations
A consultancy runs several agents across different clients and needs strict workspace isolation, visibility, and approvals.

### 2. Internal delivery orchestration
The consultancy’s own operators need a single place to monitor long-running workflows, failures, queues, and approvals.

### 3. Client-safe automation
A client wants automation, but only with explicit permission boundaries, logs, and cost controls.

## Functional requirements
### Workspace and tenancy
- separate workspace per client or internal program
- explicit user roles and permissions
- asset isolation by workspace

### Agent registry
- register each agent with name, purpose, owner, runtime, version, permissions, and linked workflows
- show whether agent is active, paused, draft, or deprecated

### Run visibility
- list active runs and recent runs
- show status: queued, running, blocked, failed, completed
- show linked workflow, workspace, owner, runtime, duration, and cost estimate

### Approval gates
- allow workflows or agents to require approval before risky actions
- support approval types such as deployment, send, publish, writeback, and budget escalation
- record approver, time, decision, and evidence

### Policy layer
- define action policies by workspace
- define allowed connectors, spending caps, write permissions, and escalation conditions

### Cost visibility
- show cost by workspace, workflow, agent, and period
- show forecast versus cap
- alert on spend anomalies

### Audit trail
- log every important action with actor, timestamp, object, outcome, and evidence
- searchable history across runs, approvals, failures, and edits

### Versioning
- version agents, prompts, workflows, and policies
- show current deployed version and change history

### Incident controls
- pause agent
- pause workflow
- disable connector
- kill stuck run
- roll back to prior version

## Non-functional requirements
- strong workspace isolation
- human-readable logs and audit trails
- fast enough to be used as an operational console
- framework-agnostic integration with multiple runtimes
- exportable evidence for client review

## UX / workflow
### Daily operator loop
1. open control plane
2. review active runs and blocked items
3. approve or reject queued actions
4. inspect failures and re-run or patch
5. review cost posture and anomalies

### Client approval loop
1. client approver receives approval request
2. sees action summary, risk level, and evidence
3. approves or rejects
4. event is logged and workflow continues or stops

## Core entities
- Workspace
- Agent
- Workflow
- Run
- Policy
- Approval
- Connector
- Incident
- Cost record
- Audit event

## Key metrics
- approval turnaround time
- failed run rate
- incident recovery time
- spend variance versus budget
- percent of risky actions routed through policy and approvals
- number of active workspaces using the platform weekly

## Risks
### Too much infrastructure, not enough user value
Mitigation:
- start with visibility + approvals + cost + audit trail

### Client distrust of autonomous systems
Mitigation:
- make approval gates and logs first-class

### Integration sprawl
Mitigation:
- support a narrow connector set in v1

## Phased roadmap
### Phase 1
- workspace model
- agent registry
- run console
- approvals
- audit trail
- basic cost dashboard

### Phase 2
- policy editor
- versioning and rollback
- incident controls
- client portal for approvals

### Phase 3
- advanced analytics
- SLA reporting
- automated anomaly detection
- deeper connector governance

## Launch criteria
- at least one internal workflow and one client workflow operated through the control plane
- all higher-risk actions route through approvals
- run history and cost history are visible and exportable
