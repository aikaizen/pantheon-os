# Agent-Computer Interface (ACI) Principles

## Reference: SWE-Agent Paper & Industry Insights

*Compiled from analysis of the SWE-Agent paper and related agent architecture research.*

---

## Core Thesis

The interface between an agent and its environment is the primary determinant of agent performance. A carefully designed ACI produced a **64% relative improvement** in benchmark performance compared to the same model interacting through a standard Linux shell. Same model, same task, same compute budget. The only variable was the interface.

**64% is not a marginal gain. That is the difference between a tool that works and a tool that does not.**

---

## The Context Window Is Not a RAM Slot

### The Wrong Mental Model
- Treats context window like RAM: load data → process → output
- Assumes more context = better performance
- Assumes longer prompts = richer understanding

### The Correct Mental Model
- Context window = agent's **entire working consciousness** for a session
- Every token costs computation
- Every irrelevant piece of information competes with relevant information
- Models do **not** have selective attention that cleanly ignores noise
- Noise degrades reasoning quality

### Measurable Consequences
- Running `grep` returning 10,000 lines floods working memory
- Using `cat` on entire files when only 2 functions needed = firehose when drinking glass needed
- Context flooding degrades **every subsequent step** until context is cleared

### Documented Failure Modes (Standard Bash Interface)
1. Issue grep command → thousands of lines returned
2. Lose track of what was being searched for
3. Issue more grep commands
4. Gradually fill context with noise
5. Eventually produce wrong answer or stop making progress

**Problem was not model intelligence. Interface had no mechanism for protecting the agent from itself.**

### ACI Solution
- Build search tool that returns **capped, summarized** results
- If search returns >50 matches: suppress output, tell agent to narrow query
- Transforms context-flooding failure into **natural refinement loop**

---

## What an ACI Actually Is

### Definition
Abstraction layer between a language model agent and a computer environment. Analogy to HCI (Human-Computer Interface) is intentional.

### HCI vs ACI

| Human Cognitive Architecture | LM Cognitive Architecture |
|------------------------------|---------------------------|
| Visual pattern recognition | Sequential token processing |
| Spatial memory | Sensitivity to context order/formatting |
| Parallel attention across screen | Limited working memory |
| Ability to skim and selectively focus | Tendency to anchor on prominent information |

### Design Principle
Build around LM constraints, not against them.

---

## SWE-Agent ACI Components

### 1. Search and Navigation
Replaced standard `grep` and `find` with purpose-built tools:
- `find_file` - Locate files by pattern
- `search_file` - Search within specific files
- `search_dir` - Search across directories

**Key difference was not syntax. It was output control.**

### 2. Context Management
- Capped output lengths
- Summarization of large results
- Explicit "narrow your query" feedback loops

### 3. State Awareness
- Agents aware of what's already in context
- Avoid redundant data loading
- Progressive information disclosure

### 4. Feedback Loops
- Quality bounded by quality of feedback
- Direct observation > code inference
- Application legibility enables self-verification

---

## Application Legibility: Making Systems Agent-Verifiable

### The Verification Bottleneck
As code throughput increases, bottleneck shifts from generation to verification. Agents generate faster than humans can validate.

### Solutions Implemented

**Bootable Per Worktree**
- Each agent task gets isolated application instance
- Can launch, drive, and inspect the actual application
- Torn down after task completion

**Chrome DevTools Protocol Integration**
- DOM snapshots
- Screenshots
- Browser navigation
- Reproduce bugs, validate fixes, reason about UI

**Full Local Observability Stack**
- Logs via LogQL
- Metrics via PromQL
- Traces via TraceQL
- Each agent task has isolated observability data

### The Principle
Quality of agent's work is bounded by quality of feedback loops. If agent can see what user sees, and observe same metrics/logs as human engineer, it catches broader class of problems.

---

## Progressive Disclosure Pattern

### The "One Big AGENTS.md" Anti-Pattern

**Four Failure Modes:**
1. **Context scarcity** - Giant file crowds out task, code, and relevant docs
2. **Non-guidance** - Everything important = nothing important; agent pattern-matches locally
3. **Instant rot** - Monolithic manual becomes stale graveyard
4. **Verification difficulty** - Single blob can't be coverage-checked or cross-linked

### The Solution
- Structured `docs/` directory as system of record
- Short `AGENTS.md` (~100 lines) as **map** pointing to deeper sources
- Architecture docs provide top-level domain map
- Plans as first-class artifacts with progress logs

### Result
Agents reason about full domain from repository alone, without external context.

---

## Implications for PantheonOS

### Direct Applications
1. **Registry-as-ACI** - Our registries are already structured disclosure
2. **Realm isolation** - Each realm provides scoped context
3. **State engine** - Provides capped, relevant state snapshots
4. **HTML docs** - Progressive disclosure via linked documentation

### Gaps to Address
1. **No bootable application per worktree** - Agents can't self-verify
2. **No observability integration** - No LogQL/PromQL/TraceQL exposure
3. **No CDP integration** - Can't inspect rendered UI
4. **Output capping** - Need to implement in tool layer

### Build Priorities
1. Output capping on all agent tools (prevent context flooding)
2. Bootable realm instances with isolated state
3. Observability stack per agent session
4. Browser inspection tools for UI verification

---

*Reference material for PantheonOS ACI design.*
*Created: 2026-03-18*
