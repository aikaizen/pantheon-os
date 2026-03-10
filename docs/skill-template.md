# PromptEngines Skill Template

Use this template for any company, connector, venture, or workflow skill.

Folder structure:
- skill-name/
  - SKILL.md
  - scripts/ (optional)
  - references/ (optional)
  - assets/ (optional)

Suggested frontmatter:

---
name: skill-name
summary: One sentence about what the skill does.
when_to_use: Use when the user asks to [specific triggers and phrases].
owner: Prompt Engines / venture / named maintainer
version: 1.0.0
status: draft
category: company-os
venture_scope: company
required_connectors: []
review_cycle: monthly
---

Suggested SKILL.md body:

# Skill Name

## Purpose
Explain what this skill is for in concrete terms.

## Use cases
List 2–3 concrete use cases.

## Trigger phrases
List the kinds of phrases that should trigger the skill.

## Workflow
Step-by-step procedure.

## Inputs required
- what the agent needs before starting

## Outputs expected
- what the skill should produce

## Error handling
- common failure cases
- what to do when they occur

## Examples
Example 1:
- user asks:
- skill should do:
- expected result:

Example 2:
- user asks:
- skill should do:
- expected result:

## Review checklist
- trigger is specific
- instructions are actionable
- references are separated from main body when needed
- examples exist
- error handling exists
- tested on at least one real company task
