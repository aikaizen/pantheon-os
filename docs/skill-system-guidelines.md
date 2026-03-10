# PromptEngines Skill System Guidelines

Date: 2026-03-10
Status: Draft v1
Purpose: Company-wide guideline for how Prompt Engines should design, test, maintain, and distribute agent skills.
Primary source integrated: Anthropic, "The Complete Guide to Building Skills for Claude"

## 1. Why this is now core

Prompt Engines should treat skills as a first-class operating primitive.

A skill is not just a prompt snippet.
A skill is a reusable unit of:
- workflow knowledge
- domain judgment
- trigger logic
- tool usage guidance
- quality control
- organizational memory

For Prompt Engines specifically, skills should become the main bridge between:
- constitutional grounding
- agent identity
- manifests / temporary org structure
- repeatable work
- tool / MCP / API connectivity

In practical terms:
- APIs and MCPs provide access
- skills provide reliable use
- constitution provides alignment
- memory provides continuity

All major agents in the company should operate with this model in mind.

## 2. Core principles adopted company-wide

### A. Progressive disclosure
Prompt Engines should build skills in three layers:
1. Frontmatter
   - enough for automatic triggering
2. SKILL.md body
   - enough for correct execution
3. linked files
   - references, scripts, assets, templates loaded only when needed

Reason:
- cheaper context use
- better triggering
- less clutter
- more modular skill libraries

### B. Start from use cases, not abstractions
Every skill should begin with 2–3 concrete use cases.

Bad:
- "helps with project management"

Good:
- "when asked to plan a sprint, fetch current project state, estimate capacity, create tasks, and produce a sprint plan"

At Prompt Engines, this means every skill should define:
- user/operator trigger
- desired outcome
- required steps
- required tools
- expected artifact/result

### C. Skills must be composable
No skill should assume it is the only capability in play.

Prompt Engines agents should be able to combine:
- company skills
- product-specific skills
- connector/MCP skills
- design / writing / engineering skills

### D. Skills should be portable
As much as possible, skills should work across:
- Claude / Hermes / Codex / other agent surfaces
- local Mac execution
- future API/agent orchestration surfaces

Prompt Engines should avoid building skills that are only understandable in one narrow environment unless there is clear leverage.

### E. Skills are the recipe layer above tools
Adopt the Anthropic framing explicitly:
- tools/MCP/connectors are the kitchen
- skills are the recipes

For Prompt Engines:
- Vercel, Supabase, Neon, GitHub, Notion, Linear, etc. are tool layers
- skills define how the company wants them used

## 3. Prompt Engines skill categories

Prompt Engines should standardize skills into these classes.

### 1. Creation skills
Used for:
- design output
- frontend generation
- copy / documents / presentations
- artifacts with consistent style

### 2. Workflow automation skills
Used for:
- repeatable multi-step operations
- onboarding
- release processes
- sprint/task workflows
- product launch checklists

### 3. Connector-enhancement skills
Used for:
- GitHub workflows
- Vercel deploy flows
- Supabase/Neon operational patterns
- any MCP/server integration guidance

### 4. Company OS skills
Used for:
- manifests
- sitreps
- revenue updates
- customer signal logging
- memory promotion
- constitutional update handling
- dashboard refresh workflows

### 5. Venture-specific skills
Used for:
- Kaizen operational work
- Storybook Studio launch/print pipelines
- Norbu curriculum workflows
- Video Terminal production/security workflows
- Flow Education experimentation workflows

## 4. Required skill structure

Every Prompt Engines skill should follow this structure:

skill-name/
- SKILL.md
- scripts/ (optional)
- references/ (optional)
- assets/ (optional)

Rules:
- folder name in kebab-case
- file must be exactly `SKILL.md`
- no README inside the skill folder itself
- top-level human-facing docs can exist outside the skill package if needed

## 5. Required frontmatter standard

Minimum required frontmatter:

---
name: skill-name
summary: one sentence about what it does
when_to_use: specific trigger conditions and phrases
owner: Prompt Engines / specific venture / specific agent
version: 1.0.0
status: draft|active|deprecated
category: creation|workflow|connector|company-os|venture
---

Prompt Engines additions recommended beyond Anthropic’s minimal standard:
- owner
- version
- status
- category
- dependencies
- required_connectors
- venture_scope
- review_cycle

## 6. Description and trigger rules

Every skill description must clearly state:
- what it does
- when it should trigger
- what kinds of requests or phrases imply use

Bad:
- "helps with dashboards"

Good:
- "builds and updates PromptEngines Company OS dashboards. Use when asked to create dashboard sections, wire metrics, add project drill-downs, or align UI with the Prompt Engines site design language."

Prompt Engines standard:
- vague skill descriptions are not allowed
- every active skill must be testable against trigger phrases

## 7. Company testing standard for skills

Every important skill should be tested in 3 ways.

### A. Trigger tests
- should trigger on obvious requests
- should trigger on paraphrased requests
- should not trigger on unrelated requests

### B. Functional tests
- does it actually complete the workflow?
- do the tool calls succeed?
- do expected artifacts appear?
- does error handling work?

### C. Performance / value tests
- fewer tool calls?
- fewer correction loops?
- fewer user clarifications?
- more consistent output?

Prompt Engines rule:
- no skill should become company-standard without at least light trigger + functional testing

## 8. Prompt Engines review checklist for any new skill

Before accepting a skill into the company library:
- clear use cases defined
- folder and naming correct
- frontmatter valid
- trigger description specific
- instructions actionable
- references separated from core instructions
- error handling included
- examples included
- tested for under-triggering
- tested for over-triggering
- tested with real company scenarios
- assigned owner and review cycle

## 9. How skills relate to the pantheon

The executive pantheon is unbounded.
Skills should not reduce executive agents to departments.

Instead, skills should do two things:
1. preserve archetypal identity
2. improve reliability of manifested work

So:
- Andy can use marketing, ops, launch, documentation, or coordination skills
- Hermetic_Demiurge can use architecture, security, product, or dashboard skills
- skills do not define the agent’s essence
- skills extend the agent’s operational precision

This is the key Prompt Engines adaptation.

## 10. How skills relate to constitution and memory

Prompt Engines should treat skills as constitutional and memory-linked assets.

Every mature skill should reference:
- relevant constitutional principles
- relevant venture scope
- relevant connector/tool assumptions
- known edge cases
- lessons learned from prior runs

That means skills should be updated when:
- a repeated failure pattern appears
- a new workflow is discovered
- a venture matures
- a connector changes
- the constitution changes in a way that affects behavior

## 11. Recommended company skill governance

### Global skill library
Create one shared company skill library with:
- company-os skills
- connector skills
- venture skills
- creation skills
- workflow skills

### Owners
Each skill has:
- an operational owner
- a venture scope or company scope
- a review interval

### Lifecycle
Each skill should have lifecycle state:
- draft
- active
- deprecated
- superseded

### Review cadence
Suggested:
- core company skills: monthly
- connector skills: on connector change or monthly
- venture skills: per active launch / per sprint / monthly

## 12. Recommended Prompt Engines skill patterns

The Anthropic guide identifies several patterns Prompt Engines should adopt directly.

### Pattern 1: Sequential workflow orchestration
Use for:
- launch checklists
- release flows
- onboarding
- dashboard refresh pipelines
- customer onboarding

### Pattern 2: Multi-connector coordination
Use for:
- GitHub + Vercel + Supabase workflows
- dashboard build + deploy + notify flows
- product launch sequences crossing multiple systems

### Pattern 3: Iterative refinement
Use for:
- copy generation
- design refinement
- deep-dive project reports
- investor/customer-facing docs

### Pattern 4: Context-aware tool selection
Use for:
- deciding whether something belongs in GitHub, local files, Notion, etc.
- deciding whether to use local or hosted paths

### Pattern 5: Domain-specific intelligence
Use for:
- constitutional reasoning
- product-specific launch logic
- education/curriculum logic
- AI safety / platform hardening / pricing workflows

## 13. Practical decisions for Prompt Engines right now

Going forward, Prompt Engines should:
- create a formal company skill registry
- require specific triggers in every company skill
- use progressive disclosure as the default skill design model
- test skills against real company tasks before declaring them standard
- keep skills portable and composable
- use skills as the main orchestration layer above tools/connectors
- treat skills as part of the company’s operational memory

## 14. Immediate next actions

1. Establish a `skills/` area in the Company OS / portal structure
2. Add a company skill template
3. Add a review checklist
4. Convert major repeatable company workflows into skills:
   - dashboard refresh
   - sitrep drafting
   - memory promotion
   - revenue/cross-venture update
   - venture launch review
5. Add a lightweight registry of active/deprecated skills

## 15. Final principle

Prompt Engines should not view skills as optional conveniences.
They should be treated as one of the company’s core operational substrates.

Constitution aligns agents.
Skills operationalize work.
Memory preserves what is learned.
Connectors provide access.

That is the correct stack.
