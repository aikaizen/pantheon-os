# Pantheon OS MVP Wiring Checklist

This file lists the exact items still needed from the human side to move the MVP from mock data to a deployed, authenticated dashboard.

## dashboard.promptengines.com deployment target

- Status: human-needed
- Owner: A.I.
- Impact: High
- Needed from human side: Connect Vercel project/domain and confirm whether the MVP is internal-only or gated public.

## Auth boundary and session model

- Status: human-needed
- Owner: A.I.
- Impact: High
- Needed from human side: Choose auth provider and define who can see internal systems, budgets, and approvals.

## Live metrics adapters

- Status: human-needed
- Owner: Hermetic_Demiurge
- Impact: High
- Needed from human side: Provide Supabase/Neon/project secrets and confirm event schema for Kaizen, Storybook, Bible, and Flow.

## GitHub build stream and activity feed token

- Status: human-needed
- Owner: Golem
- Impact: Medium
- Needed from human side: Provide production token/secret path for authenticated build-stream sync.

## Canonical Flow status

- Status: human-needed
- Owner: Thoth
- Impact: Medium
- Needed from human side: Decide whether Flow should appear as active product, experiment, or coming soon.

## Static MVP data contract

- Status: wired
- Owner: Hermetic_Demiurge
- Impact: Low
- Needed from human side: None for demo; replace JSON with live adapters later.

