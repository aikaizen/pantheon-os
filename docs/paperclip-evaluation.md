# Paperclip Evaluation for Prompt Engines

Date: 2026-03-10
Repo evaluated: https://github.com/paperclipai/paperclip
Homepage: https://paperclip.ing
Repo description: "Open-source orchestration for zero-human companies"

## 1. Short verdict

Paperclip is strong as a reference system and potentially useful as an optional downstream orchestration layer.

It is not a good fit as the core substrate for Prompt Engines Company OS v1.

Prompt Engines should borrow ideas from it, but should not replace its own local-first constitutional operating system with Paperclip.

## 2. What Paperclip is

Paperclip is a fairly large Node.js + React control plane for running teams of agents as companies.

From the repo and README, it appears to include:
- org charts
- task/ticket system
- budgets / cost controls
- heartbeats
- goal alignment
- governance / approvals
- multi-company support
- audit trail concepts
- multiple agent runtime support
- a UI control plane

It is conceptually ambitious and clearly aimed at full agent-company orchestration.

## 3. What is good about it

### A. High conceptual overlap
Paperclip is thinking in the right direction on several themes that matter to Prompt Engines:
- companies as orchestration systems
- agent teams rather than one-off bots
- governance
- budgets
- goal hierarchy
- auditability
- organization-level control surfaces

### B. Multi-agent / multi-runtime orientation
Paperclip explicitly supports multiple agent surfaces and runtimes.
That is aligned with Prompt Engines’ model-mesh and multi-agent reality.

### C. It already treats skills seriously
The repo includes multiple skills and even `.claude/skills` structure.
This is useful because Prompt Engines now wants skills to become a core organizational substrate.

### D. Real implementation effort and community signal
At time of inspection:
- ~14k stars
- large TypeScript codebase
- many docs, packages, UI/server/CLI structure

This means it is not vapor. It is a serious project worth studying.

## 4. Why it is not the right core for Prompt Engines v1

### A. It is too heavy for the current Prompt Engines operating mode
Prompt Engines v1 needs:
- local-first
- Mac-native
- lean
- easy to inspect
- easy to change
- easy to deploy from a simple working directory

Paperclip is a larger, heavier server product.
It uses:
- Node.js server
- React UI
- embedded or external Postgres patterns
- larger package structure and operational complexity

That is a mismatch with the current need for a lightweight company OS living close to the operator.

### B. Its ontology is not quite our ontology
Paperclip’s public framing is “orchestration for zero-human companies.”
Prompt Engines is not that.

Prompt Engines is:
- human-principal-led
- constitution-grounded
- executive-pantheon-based
- manifest-driven rather than department-driven

That is a materially different worldview.
Paperclip’s organization model looks more like:
- jobs
- bosses
- employees
- hierarchical roles

Prompt Engines needs:
- stable archetypal identity
- dynamic manifested org charts
- constitutional alignment before departmentalization

So even if Paperclip can technically model some of this, it is not natively shaped around the same assumptions.

### C. Constitution and archetypal grounding do not appear central
Prompt Engines needs constitution-first operation.
The executive archetype layer and shared grounding bundle are core.
Paperclip seems stronger on:
- governance
- tasks
- budgets
- heartbeats
- agent management

It appears weaker, at least from the visible surface, on:
- archetypal identity as first-class design
- constitutional grounding as runtime substrate
- fluid pantheon manifestation logic

### D. It risks dragging us into platform adoption instead of company design clarity
If Prompt Engines adopts Paperclip too early, we risk bending the company to fit the tool.
That is the wrong order.

Prompt Engines should define:
- its ontology
- its constitution
- its registry
- its memory model
- its dashboard model

Then selectively integrate external systems only where they help.

## 5. What Prompt Engines should borrow from Paperclip

Prompt Engines should study and possibly borrow these concepts:

### 1. Goal/task hierarchy
Good for:
- company goals
- venture goals
- project goals
- task decomposition

### 2. Heartbeat / recurring check-in logic
Good for:
- periodic sitreps
- recurring refresh/build tasks
- budgeted agent wake cycles

### 3. Governance / approvals
Good for:
- explicit decision gates
- higher-risk action approvals
- deployment or publication approval paths

### 4. Budget/cost visibility
Good for:
- model/runtime budgets
- per-agent/per-project cost awareness
- 24/7 automation constraints

### 5. Audit trail mentality
Good for:
- handoffs
- messages
- decision tracking
- action provenance

These ideas are useful even if we never run Paperclip itself.

## 6. Recommended Prompt Engines posture toward Paperclip

### Near-term recommendation
Do not adopt Paperclip as the base platform.

Instead:
- continue building Prompt Engines Company OS locally and constitution-first
- keep the current local dashboard + build-time data architecture
- preserve the pantheon/manifests model as primary

### Medium-term recommendation
Treat Paperclip as one of three things:
1. reference implementation
2. pattern library
3. possible optional adapter target later

That means Prompt Engines could later build:
- a Paperclip export/import adapter
- a sync layer between our manifests and Paperclip tasks
- a way to use Paperclip for some autonomous execution loops without making it our source of truth

### Long-term recommendation
Only consider deeper adoption if:
- it can respect our constitution-first model
- it can operate as a thin execution layer beneath our Company OS
- it does not force a rigid org model onto the pantheon

## 7. Practical conclusion

Prompt Engines should not ask:
- “Should we switch to Paperclip?”

It should ask:
- “Which orchestration patterns from Paperclip are worth importing into our own system?”

That is the correct framing.

## 8. Final verdict

Paperclip evaluation:
- reference value: high
- conceptual overlap: high
- direct v1 fit: medium-low
- operational weight: too heavy for current needs
- ontology fit: partial, not full
- recommended action: study, borrow patterns, do not replace our core Company OS with it

Prompt Engines Company OS should remain:
- local-first
- constitution-first
- pantheon-aware
- manifest-driven
- connector-flexible

Paperclip can be useful later as an optional orchestration backend or integration target, but not as the core truth layer.
