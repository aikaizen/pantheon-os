# PromptEngines pilot rollout

Goal: move from repo readiness into real internal use without skipping safety and observability.

## Phase 0 — repo and topology readiness

- topology registries exist
- state engine observes personas, runtimes, controllers, channels
- onboarding docs exist for Connect Existing Setup and Start Fresh
- terminal docs reflect persona/controller/runtime distinctions

## Phase 1 — observe-only pilot

- enable PromptEngines deployment in `observe` mode
- principal sees persona lanes, controller lanes, runtime health, and summaries on one surface
- no automated message sending or runtime control yet
- confirm that missing adapters degrade gracefully

## Phase 2 — message-enabled pilot

- enable approved message-capable bindings
- send test messages into registered channels
- validate channel summaries and reply flows
- confirm audit trail for operator actions

## Phase 3 — controller-enabled pilot

- enable approved controller actions for runtime inspection and maintenance
- test restart / inspect / send-test-message workflows
- keep destructive actions behind explicit approval

## Phase 4 — daily internal use

- use PantheonOS during real PromptEngines operations for Tier 1 ventures
- review blockers, false signals, missing panes, and noisy telemetry
- refine before external packaging
