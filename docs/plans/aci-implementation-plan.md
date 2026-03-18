# ACI Implementation Plan for PantheonOS

## Overview

Based on the SWE-Agent paper's Agent-Computer Interface principles, this plan outlines what needs to be built to give PantheonOS agents the 64% performance improvement that comes from interface design, not model improvement.

**Reference:** [ACI Principles](../references/aci-principles.md)

---

## Priority 1: Output Capping Layer (HIGH LEVERAGE)

### Problem
Agents flood their own context with unbounded output from tools like `search_files`, `read_file`, terminal commands.

### Solution
Implement output capping at the tool layer:

**Search Results Cap**
- Max 50 results returned
- If exceeded: return count + "Narrow your query" message
- Include file paths only, not full content matches

**File Read Cap**
- Default 200 lines per read
- Explicit offset/limit required for large files
- "File has N total lines" metadata always included

**Terminal Output Cap**
- 10KB stdout cap (already exists in execute_code)
- Structured truncation with line count

### Implementation
```
/tools/output_capping.py
- CappedSearchResults(max_results=50)
- CappedFileRead(default_limit=200, max_limit=1000)
- TruncatedTerminal(max_bytes=10240)
```

### Files to Create/Modify
- `tools/output_governor.py` - Output capping middleware
- `tools/__init__.py` - Register capped tools
- `docs/references/output-capping-spec.md` - Specification

---

## Priority 2: Realm Bootstrapping with Isolated State

### Problem
Agents work on code without being able to verify it runs. No way to boot, inspect, or validate changes.

### Solution
Each realm gets:
- Git worktree isolation
- Bootable application instance
- Isolated state directory
- Lifecycle management (create → run → inspect → teardown)

### Implementation
```
realms/bootstrap.py
- create_worktree(realm_id, branch)
- boot_instance(realm_id, port)
- teardown(realm_id)

realms/isolation.py
- IsolatedRealm(realm_id)
  - state_dir: /tmp/pantheon/realms/{realm_id}
  - worktree: /tmp/pantheon/worktrees/{realm_id}
  - port: auto-assigned
```

### Files to Create
- `realms/__init__.py` - Realm isolation framework
- `realms/bootstrap.py` - Worktree + instance management
- `realms/isolation.py` - State isolation
- `docs/references/realm-isolation-spec.md`

---

## Priority 3: Observability Exposure

### Problem
Agents can only infer behavior from code. No access to logs, metrics, or traces.

### Solution
Per-realm observability:
- Structured logs via simple log aggregation
- Performance metrics (timing, resource usage)
- Trace correlation for multi-step operations

### Implementation (Phase 1 - Minimal)
```
observability/logger.py
- RealmLogger(realm_id)
- Structured JSON logs
- Log query interface

observability/metrics.py
- Simple counters and timers
- Exposed via /metrics endpoint
```

### Files to Create
- `observability/__init__.py` - Observability stack
- `observability/logger.py` - Structured logging
- `observability/metrics.py` - Basic metrics
- `docs/references/observability-spec.md`

---

## Priority 4: Browser/DOM Inspection

### Problem
No way to verify rendered UI, inspect DOM, or validate visual output.

### Solution
Chrome DevTools Protocol integration:
- DOM snapshots
- Element inspection
- Screenshot capture
- Navigation control

### Implementation (Phase 2)
```
browser/inspector.py
- CDPInspector(realm_id, port)
- get_dom_snapshot()
- screenshot()
- navigate(url)
- query_selector(selector)
```

### Files to Create
- `browser/__init__.py` - Browser inspection tools
- `browser/inspector.py` - CDP wrapper
- `browser/dom.py` - DOM manipulation
- `docs/references/browser-inspection-spec.md`

---

## Priority 5: Progressive Disclosure Engine

### Problem
Agents don't have structured way to discover what documentation exists and where to find it.

### Solution
Documentation index + navigation:
- Machine-readable doc catalog
- Dependency graph between docs
- Staleness detection
- Coverage tracking

### Implementation
```
disclosure/index.py
- DocIndex(docs_root)
- list_all() -> [{path, title, last_modified, dependencies}]
- find(query) -> ranked results
- check_staleness() -> [{path, days_stale}]

disclosure/navigator.py
- Navigator(agent_context)
- start() -> entry point doc
- next(current_doc) -> suggested next docs
- related(topic) -> all related docs
```

### Files to Create
- `disclosure/__init__.py` - Progressive disclosure engine
- `disclosure/index.py` - Documentation indexing
- `disclosure/navigator.py` - Guided navigation
- `docs/doc-index.yaml` - Machine-readable catalog
- `docs/references/progressive-disclosure-spec.md`

---

## Implementation Order

### Sprint 1: Foundation (Immediate Value)
1. **Output capping** - Prevent context flooding NOW
2. **Doc index** - Enable progressive disclosure

### Sprint 2: Isolation (Agent Autonomy)
3. **Realm bootstrapping** - Agents can verify their own work
4. **Basic observability** - Structured logging per realm

### Sprint 3: Verification (Full Loop)
5. **Browser inspection** - UI verification capability
6. **Advanced observability** - Metrics and tracing

---

## Success Metrics

### Quantitative
- Context window utilization: <60% average (down from overflow)
- Agent task completion rate: +40% improvement
- Verification steps per task: 0 → 3+ (self-verification)
- Time to locate relevant docs: <3 tool calls

### Qualitative
- Agents don't thrash on search results
- Agents self-verify changes before reporting
- Documentation stays current via staleness detection
- New agents productive within first session

---

## Anti-Patterns to Avoid

1. **Don't build one big instruction file** - Use progressive disclosure
2. **Don't return raw tool output** - Cap and summarize
3. **Don't share state between realms** - Full isolation
4. **Don't skip verification loops** - Boot, inspect, validate

---

*ACI Implementation Plan for PantheonOS*
*Created: 2026-03-18*
*Status: PLANNING*
