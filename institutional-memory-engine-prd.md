# PRD — Institutional Memory Engine

## Product summary
A structured memory system that captures, organizes, retrieves, and governs operational knowledge across client work, internal delivery, and product development.

## Problem
Consultancies lose leverage when knowledge stays trapped in:
- chat threads
- meeting notes
- docs no one can find
- consultants’ heads
- project files that never become reusable systems

This leads to repeated discovery, inconsistent delivery, and weak productization.

## Target users
Primary users:
- consultants
- delivery leads
- founders / operators
- agents that need reliable context

Secondary users:
- client success teams
- researchers
- product managers

## Jobs to be done
- preserve client and internal knowledge in a reusable form
- retrieve the right context quickly with citations
- prevent the same work from being rediscovered repeatedly
- give humans and agents the same source of truth
- distinguish what is global, client-specific, sensitive, or stale

## Product goals
- increase reuse across projects
- reduce repeated research and rediscovery
- improve output consistency
- make delivery and productization cumulative
- provide permission-aware retrieval for humans and agents

## Non-goals
- not a generic document dump
- not a consumer note-taking app
- not a replacement for all source systems

## Core use cases
### 1. Delivery reuse
Before a new engagement starts, the team can retrieve similar workflows, prior solutions, templates, objections, and lessons learned.

### 2. Client continuity
If a delivery lead changes, the next operator can quickly understand the client, the workflow history, key decisions, and unresolved issues.

### 3. Agent context
Agents can retrieve approved, structured memory objects instead of relying on raw prompts or brittle ad hoc context.

## Memory model
The engine should store memory as structured objects rather than only raw files.

Recommended object types:
- client profile
- workflow pattern
- decision record
- meeting synthesis
- deliverable template
- implementation note
- risk / failure mode
- reusable asset
- terminology / glossary item

Each memory object should include:
- title
- type
- summary
- body
- source links
- owner
- workspace / client scope
- sensitivity level
- freshness status
- tags
- created at / updated at

## Functional requirements
### Ingestion
- ingest docs, notes, transcripts, tickets, and deliverables
- support manual capture and automated ingestion
- extract candidate memory objects from unstructured material

### Structuring
- convert raw material into typed memory objects
- require human review for promoted memory when confidence is low or sensitivity is high

### Retrieval
- hybrid retrieval by keyword, tag, and semantic similarity
- always return cited sources and confidence signals
- support workspace-specific and global retrieval scopes

### Permissioning
- strict client/workspace boundaries
- role-based access controls
- ability to mark memory objects as private, client-scoped, or global reusable knowledge

### Freshness and governance
- mark memory as draft, active, stale, archived
- support review cycles
- surface stale but frequently used memory for refresh

### Agent interface
- allow agents to query structured memory safely
- return concise answer + citations + linked objects
- block access to disallowed scopes

### Human curation
- review queue for candidate memory objects
- merge duplicates
- promote a project note into reusable organizational memory

## Non-functional requirements
- fast search and retrieval
- clear provenance and citations
- strong data isolation for client material
- exportable memory packs for handoffs
- usable by non-technical operators

## UX / workflow
### Memory capture loop
1. work happens in meetings, docs, and delivery
2. important material is ingested
3. candidate memory objects are proposed
4. operator reviews and promotes the useful ones
5. memory becomes searchable and reusable

### Retrieval loop
1. user or agent asks a question
2. system retrieves the best objects within permission scope
3. answer is synthesized with citations
4. user can inspect the underlying memory objects

## Core entities
- Workspace
- Memory object
- Source document
- Citation
- Review task
- Tag
- Access policy
- Retrieval event

## Key metrics
- retrieval success rate
- average time to find needed context
- reuse rate of memory objects in delivery
- reduction in repeated research hours
- percent of answers returned with citations
- freshness coverage of active memory

## Risks
### Garbage in, garbage out
Mitigation:
- typed object model
- human review queues
- freshness and quality scoring

### Security and privacy concerns
Mitigation:
- strict tenant isolation
- granular permissions
- explicit client/global separation

### Low adoption
Mitigation:
- make ingestion lightweight
- integrate memory into actual delivery workflows
- optimize for retrieval value, not archival completeness

## Phased roadmap
### Phase 1
- ingest core files and notes
- create typed memory objects manually and semi-automatically
- workspace-scoped retrieval with citations
- review queue

### Phase 2
- automated extraction from transcripts and project artifacts
- freshness scoring
- better semantic retrieval
- agent query interface

### Phase 3
- memory analytics
- suggested cross-client reusable patterns
- automatic stale-memory refresh prompts
- packaged handoff/export workflows

## Launch criteria
- one consultancy team uses it weekly for active delivery
- retrieval returns cited, permission-safe answers
- team reports measurable reduction in rediscovery effort
