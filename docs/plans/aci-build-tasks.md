# ACI Build Plan - Task Tracker

## Sprint 1: Foundation (Immediate Value)

### Output Capping Layer
- [ ] Design output governor middleware
- [ ] Implement CappedSearchResults (max 50)
- [ ] Implement CappedFileRead (default 200 lines)
- [ ] Integrate with existing search_files tool
- [ ] Integrate with existing read_file tool
- [ ] Test context overflow scenarios

### Documentation Index
- [ ] Create doc catalog schema (YAML)
- [ ] Build doc index generator
- [ ] Implement staleness detection
- [ ] Create navigation helper
- [ ] Index existing docs/ directory
- [ ] Test progressive disclosure flow

## Sprint 2: Isolation (Agent Autonomy)

### Realm Bootstrapping
- [ ] Design realm isolation framework
- [ ] Implement git worktree management
- [ ] Build realm lifecycle (create/run/teardown)
- [ ] Add port assignment for instances
- [ ] Create realm state directory structure
- [ ] Test multi-realm isolation

### Basic Observability
- [ ] Design structured logging format
- [ ] Implement RealmLogger
- [ ] Add log query interface
- [ ] Create per-realm log files
- [ ] Test log isolation between realms

## Sprint 3: Verification (Full Loop)

### Browser Inspection
- [ ] Evaluate CDP wrapper libraries
- [ ] Implement basic DOM snapshot
- [ ] Add screenshot capability
- [ ] Create navigation controls
- [ ] Test UI verification workflow

### Advanced Observability
- [ ] Implement basic metrics (counters/timers)
- [ ] Add timing instrumentation
- [ ] Create metrics query interface
- [ ] Test performance measurement

---

*Created: 2026-03-18*
*Status: ACTIVE*
