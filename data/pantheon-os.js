window.PANTHEON_OS_DATA = {
  "meta": {
    "system_name": "Pantheon OS",
    "company": "Prompt Engines",
    "tagline": "Local-first company control room for a human principal and a pantheon of agents.",
    "version": "0.1.0",
    "updated_at": "2026-03-10T08:00:00Z",
    "compatibility_alias": "data/company-os.json",
    "north_star": "Make the company legible, controllable, and compounding without turning the lab into bureaucracy."
  },
  "summary": {
    "venture_count": 11,
    "active_count": 7,
    "prototype_count": 2,
    "experiment_count": 2,
    "open_approvals": 3,
    "due_heartbeats": 2,
    "active_skills": 5,
    "monthly_budget": 2450,
    "monthly_spent": 1465,
    "monthly_forecast": 2140
  },
  "principles": [
    "Constitution aligns agents.",
    "Skills operationalize repeatable work.",
    "Memory preserves learning and state transitions.",
    "Connectors provide access; skills remain the recipe layer above them.",
    "Every meaningful action routes through explicit ownership, approval, and budget awareness."
  ],
  "guidance": {
    "anthropic_skill_standard": [
      "Skills are first-class operational assets, not just prompt helpers.",
      "Every skill starts from concrete use cases, not vague abstractions.",
      "Progressive disclosure is mandatory: frontmatter for triggering, SKILL.md for execution, linked assets only when needed.",
      "Skills are composable across agents and sit above tools/connectors as the recipe layer.",
      "Important skills are tested for triggering, functional success, and workflow improvement.",
      "Skill governance tracks owner, version, status, review cadence, and venture scope."
    ],
    "paperclip_stance": {
      "reference_value": "high",
      "direct_v1_fit": "medium-low",
      "adoption_recommendation": "Borrow orchestration patterns without adopting Paperclip as the core substrate."
    },
    "paperclip_elements_adopted": [
      "Goal and task hierarchy across company, venture, and project layers.",
      "Heartbeat and recurring sitrep logic with runtime budgets.",
      "Governance and approval gates for higher-risk actions.",
      "Budget and cost visibility by venture and by agent."
    ]
  },
  "agents": [
    {
      "id": "ai-principal",
      "name": "A.I.",
      "type": "human",
      "role": "Principal direction and final approval",
      "archetype": "Principal",
      "status": "active",
      "monthly_budget": 0,
      "skills": [
        "weekly-operating-review",
        "decision-gate-review"
      ]
    },
    {
      "id": "hermetic-demiurge",
      "name": "Hermetic_Demiurge",
      "type": "agent",
      "role": "Builder, hardening, and shipping",
      "archetype": "Demiurge / Prometheus",
      "status": "active",
      "monthly_budget": 900,
      "skills": [
        "goal-tree-planning",
        "venture-status-refresh"
      ]
    },
    {
      "id": "thoth",
      "name": "Thoth",
      "type": "agent",
      "role": "Memory, documentation, and synthesis",
      "archetype": "Scribe",
      "status": "active",
      "monthly_budget": 420,
      "skills": [
        "build-stream-synthesis",
        "weekly-operating-review"
      ]
    },
    {
      "id": "prometheus",
      "name": "Prometheus",
      "type": "agent",
      "role": "Prototype ignition and venture acceleration",
      "archetype": "Fire-bringer",
      "status": "active",
      "monthly_budget": 560,
      "skills": [
        "goal-tree-planning",
        "venture-status-refresh"
      ]
    },
    {
      "id": "golem",
      "name": "Golem",
      "type": "agent",
      "role": "Scheduled operations and reliable repeatability",
      "archetype": "Executor",
      "status": "active",
      "monthly_budget": 310,
      "skills": [
        "decision-gate-review",
        "weekly-operating-review"
      ]
    }
  ],
  "ventures": [
    {
      "id": "promptengines-web",
      "name": "PromptEngines.com",
      "domain": "promptengines.com",
      "repo": "aikaizen/promptengines-main",
      "stage": "product",
      "status": "active",
      "health": "strong",
      "owner": "A.I.",
      "operators": [
        "Hermetic_Demiurge",
        "Thoth"
      ],
      "next_action": "Decide the public/private split for Pantheon OS before any internet-facing deployment.",
      "budget": {
        "allocated": 420,
        "spent": 245,
        "forecast": 390
      }
    },
    {
      "id": "lab-notes",
      "name": "Lab Notes",
      "domain": "lab.promptengines.com",
      "repo": "aikaizen/promptengines-main",
      "stage": "product",
      "status": "active",
      "health": "steady",
      "owner": "Thoth",
      "operators": [
        "Thoth"
      ],
      "next_action": "Route build-stream synthesis into a repeatable publishing skill.",
      "budget": {
        "allocated": 180,
        "spent": 92,
        "forecast": 140
      }
    },
    {
      "id": "kaizen",
      "name": "Kaizen",
      "domain": "kaizen.promptengines.com",
      "repo": "aikaizen/kaizen",
      "stage": "product",
      "status": "active",
      "health": "strong",
      "owner": "Prometheus",
      "operators": [
        "Prometheus",
        "Hermetic_Demiurge"
      ],
      "next_action": "Tighten telemetry, growth review, and operator-visible learning loops.",
      "budget": {
        "allocated": 280,
        "spent": 176,
        "forecast": 260
      }
    },
    {
      "id": "storybook-studio",
      "name": "Storybook Studio",
      "domain": "storybookstudio.promptengines.com",
      "repo": "aikaizen/storybookstudio",
      "stage": "product",
      "status": "pre-launch",
      "health": "building",
      "owner": "Hermetic_Demiurge",
      "operators": [
        "Hermetic_Demiurge",
        "Prometheus"
      ],
      "next_action": "Stabilize the print-ready storybook pipeline and approval gates for publishing.",
      "budget": {
        "allocated": 260,
        "spent": 149,
        "forecast": 230
      }
    },
    {
      "id": "flow",
      "name": "Flow",
      "domain": "flow.promptengines.com",
      "repo": "aikaizen/flow",
      "stage": "experiment",
      "status": "mixed-signal",
      "health": "mixed",
      "owner": "A.I.",
      "operators": [
        "Prometheus"
      ],
      "next_action": "Resolve source-of-truth drift between public homepage, registry, and live dashboard API.",
      "budget": {
        "allocated": 210,
        "spent": 124,
        "forecast": 190
      }
    },
    {
      "id": "video-terminal",
      "name": "Video Terminal",
      "domain": "videoterminal.promptengines.com",
      "repo": "aikaizen/videoterminal",
      "stage": "experiment",
      "status": "alpha",
      "health": "emerging",
      "owner": "Prometheus",
      "operators": [
        "Prometheus"
      ],
      "next_action": "Define the smallest shippable control surface and active build loop.",
      "budget": {
        "allocated": 170,
        "spent": 82,
        "forecast": 150
      }
    },
    {
      "id": "norbu",
      "name": "Norbu",
      "domain": "norbu.promptengines.com",
      "repo": "aikaizen/norbu",
      "stage": "product",
      "status": "active",
      "health": "steady",
      "owner": "Prometheus",
      "operators": [
        "Prometheus",
        "Thoth"
      ],
      "next_action": "Establish a recurring content and product heartbeat.",
      "budget": {
        "allocated": 150,
        "spent": 77,
        "forecast": 133
      }
    },
    {
      "id": "bible",
      "name": "Bible",
      "domain": "bible.promptengines.com",
      "repo": "aikaizen/bible",
      "stage": "product",
      "status": "active",
      "health": "steady",
      "owner": "Thoth",
      "operators": [
        "Thoth"
      ],
      "next_action": "Add product heartbeat and governance checks before broader publishing.",
      "budget": {
        "allocated": 120,
        "spent": 54,
        "forecast": 96
      }
    },
    {
      "id": "consulting",
      "name": "Consulting",
      "domain": "consulting.promptengines.com",
      "repo": "aikaizen/consulting",
      "stage": "service",
      "status": "active",
      "health": "strong",
      "owner": "A.I.",
      "operators": [
        "Thoth",
        "Hermetic_Demiurge"
      ],
      "next_action": "Install account brief, proposal, and client approval workflows.",
      "budget": {
        "allocated": 230,
        "spent": 178,
        "forecast": 240
      }
    },
    {
      "id": "flow-education",
      "name": "Flow Education",
      "domain": "prototype",
      "repo": "aikaizen/promptengines-main",
      "stage": "prototype",
      "status": "active-prototype",
      "health": "emerging",
      "owner": "Prometheus",
      "operators": [
        "Prometheus"
      ],
      "next_action": "Convert prototype lessons into a venture roadmap with explicit dependencies.",
      "budget": {
        "allocated": 150,
        "spent": 58,
        "forecast": 110
      }
    },
    {
      "id": "vajra-upaya",
      "name": "Vajra-Upaya",
      "domain": "prototype",
      "repo": "aikaizen/promptengines-main",
      "stage": "prototype",
      "status": "framing",
      "health": "emerging",
      "owner": "A.I.",
      "operators": [
        "Thoth",
        "Prometheus"
      ],
      "next_action": "Frame the precision tool-fitting offer and approval path before public positioning.",
      "budget": {
        "allocated": 130,
        "spent": 30,
        "forecast": 88
      }
    }
  ],
  "goals": [
    {
      "id": "g-company-legibility",
      "parent_id": null,
      "scope": "company",
      "title": "Make Prompt Engines legible and controllable from one operating surface.",
      "status": "in_progress",
      "owner": "A.I.",
      "target_metric": "Every venture has owner, stage, health, next action, heartbeat, and budget.",
      "target_date": "2026-03-31",
      "venture_ids": []
    },
    {
      "id": "g-pantheon-dashboard",
      "parent_id": "g-company-legibility",
      "scope": "company",
      "title": "Ship Pantheon OS as the canonical local-first control room.",
      "status": "in_progress",
      "owner": "Hermetic_Demiurge",
      "target_metric": "Local dashboard, registry, schema, and guidance all exist in one deliverable.",
      "target_date": "2026-03-12",
      "venture_ids": [
        "promptengines-web"
      ]
    },
    {
      "id": "g-skill-library",
      "parent_id": "g-company-legibility",
      "scope": "company",
      "title": "Treat skills as first-class operational assets across the company.",
      "status": "in_progress",
      "owner": "Thoth",
      "target_metric": "Five core skills are packaged, linked to templates, and testable.",
      "target_date": "2026-03-15",
      "venture_ids": []
    },
    {
      "id": "g-goal-ladder",
      "parent_id": "g-company-legibility",
      "scope": "company",
      "title": "Install a company-to-venture goal and task hierarchy.",
      "status": "in_progress",
      "owner": "Prometheus",
      "target_metric": "All active ventures roll up to explicit company goals.",
      "target_date": "2026-03-18",
      "venture_ids": [
        "kaizen",
        "storybook-studio",
        "consulting"
      ]
    },
    {
      "id": "g-kaizen-loop",
      "parent_id": "g-goal-ladder",
      "scope": "venture",
      "title": "Create a tighter telemetry and growth review loop for Kaizen.",
      "status": "in_progress",
      "owner": "Prometheus",
      "target_metric": "Weekly operator review shows growth and activation state for Kaizen.",
      "target_date": "2026-03-20",
      "venture_ids": [
        "kaizen"
      ]
    },
    {
      "id": "g-storybook-launch",
      "parent_id": "g-goal-ladder",
      "scope": "venture",
      "title": "Make Storybook Studio launch-ready with explicit approvals.",
      "status": "in_progress",
      "owner": "Hermetic_Demiurge",
      "target_metric": "Publishing, printing, and release decisions all route through gates.",
      "target_date": "2026-03-22",
      "venture_ids": [
        "storybook-studio"
      ]
    },
    {
      "id": "g-consulting-ops",
      "parent_id": "g-goal-ladder",
      "scope": "venture",
      "title": "Make consulting a repeatable workflow with briefs, approvals, and follow-up.",
      "status": "planned",
      "owner": "A.I.",
      "target_metric": "Every account has a brief, next action, and approval state.",
      "target_date": "2026-03-25",
      "venture_ids": [
        "consulting"
      ]
    }
  ],
  "tasks": [
    {
      "id": "t-rename-pantheon",
      "goal_id": "g-pantheon-dashboard",
      "parent_task_id": null,
      "title": "Rename the company operating system surface to Pantheon OS.",
      "status": "completed",
      "owner": "Hermetic_Demiurge",
      "due_date": "2026-03-10",
      "risk": "low",
      "approval_id": "ap-branding",
      "heartbeat_id": null,
      "next_step": "Propagate the name into registry, docs, and dashboard copy.",
      "blocked_by": []
    },
    {
      "id": "t-static-dashboard",
      "goal_id": "g-pantheon-dashboard",
      "parent_task_id": null,
      "title": "Ship a local static dashboard that shows ventures, goals, heartbeats, approvals, budgets, skills, and memory.",
      "status": "completed",
      "owner": "Hermetic_Demiurge",
      "due_date": "2026-03-10",
      "risk": "medium",
      "approval_id": null,
      "heartbeat_id": null,
      "next_step": "Use it as the base for a richer authenticated control room later.",
      "blocked_by": []
    },
    {
      "id": "t-registry-pack",
      "goal_id": "g-pantheon-dashboard",
      "parent_task_id": null,
      "title": "Create registry YAML, a JSON snapshot, a schema, and a SQL model for Pantheon OS.",
      "status": "completed",
      "owner": "Thoth",
      "due_date": "2026-03-10",
      "risk": "medium",
      "approval_id": null,
      "heartbeat_id": null,
      "next_step": "Keep JSON as the dashboard snapshot and YAML as human-editable registry inputs.",
      "blocked_by": []
    },
    {
      "id": "t-core-skills",
      "goal_id": "g-skill-library",
      "parent_task_id": null,
      "title": "Write the first five core company skills as real SKILL.md packages.",
      "status": "completed",
      "owner": "Thoth",
      "due_date": "2026-03-10",
      "risk": "low",
      "approval_id": null,
      "heartbeat_id": null,
      "next_step": "Run trigger and functional checks on the first two skills in real workflows.",
      "blocked_by": []
    },
    {
      "id": "t-goal-tree-model",
      "goal_id": "g-goal-ladder",
      "parent_task_id": null,
      "title": "Install company, venture, and project-level goals with task decomposition.",
      "status": "completed",
      "owner": "Prometheus",
      "due_date": "2026-03-10",
      "risk": "medium",
      "approval_id": null,
      "heartbeat_id": "hb-daily-loop",
      "next_step": "Add dependencies and evidence links as the system matures.",
      "blocked_by": []
    },
    {
      "id": "t-heartbeat-model",
      "goal_id": "g-pantheon-dashboard",
      "parent_task_id": null,
      "title": "Add recurring heartbeat logic for sitreps, refreshes, and wake cycles.",
      "status": "completed",
      "owner": "Golem",
      "due_date": "2026-03-10",
      "risk": "medium",
      "approval_id": "ap-agent-wake-cycles",
      "heartbeat_id": "hb-daily-loop",
      "next_step": "Connect heartbeat execution to cron-backed automation later.",
      "blocked_by": []
    },
    {
      "id": "t-governance-model",
      "goal_id": "g-pantheon-dashboard",
      "parent_task_id": null,
      "title": "Add explicit decision gates and approval pathways for higher-risk actions.",
      "status": "completed",
      "owner": "A.I.",
      "due_date": "2026-03-10",
      "risk": "high",
      "approval_id": null,
      "heartbeat_id": "hb-weekly-review",
      "next_step": "Define which actions can auto-execute versus require human signoff.",
      "blocked_by": []
    },
    {
      "id": "t-budget-model",
      "goal_id": "g-pantheon-dashboard",
      "parent_task_id": null,
      "title": "Add venture and agent budget visibility with monthly allocation, spend, and forecast.",
      "status": "completed",
      "owner": "Golem",
      "due_date": "2026-03-10",
      "risk": "medium",
      "approval_id": "ap-budget-caps",
      "heartbeat_id": "hb-budget-review",
      "next_step": "Backfill cost data from actual runtime and connector usage later.",
      "blocked_by": []
    },
    {
      "id": "t-public-deploy-decision",
      "goal_id": "g-pantheon-dashboard",
      "parent_task_id": null,
      "title": "Decide whether Pantheon OS remains local-first or gets a gated hosted surface.",
      "status": "pending_approval",
      "owner": "A.I.",
      "due_date": "2026-03-12",
      "risk": "high",
      "approval_id": "ap-public-deploy",
      "heartbeat_id": "hb-weekly-review",
      "next_step": "Approve only after auth boundaries and public/private data split are clear.",
      "blocked_by": [
        "ap-public-deploy"
      ]
    },
    {
      "id": "t-flow-reconcile",
      "goal_id": "g-goal-ladder",
      "parent_task_id": null,
      "title": "Reconcile Flow status drift across homepage, registry, and live dashboard.",
      "status": "in_progress",
      "owner": "Thoth",
      "due_date": "2026-03-14",
      "risk": "medium",
      "approval_id": null,
      "heartbeat_id": "hb-daily-loop",
      "next_step": "Choose one canonical source of truth for venture status.",
      "blocked_by": []
    },
    {
      "id": "t-consulting-briefs",
      "goal_id": "g-consulting-ops",
      "parent_task_id": null,
      "title": "Add account-brief style workflow assets to Consulting.",
      "status": "planned",
      "owner": "Thoth",
      "due_date": "2026-03-21",
      "risk": "low",
      "approval_id": null,
      "heartbeat_id": "hb-weekly-review",
      "next_step": "Package the workflow as a venture-specific skill.",
      "blocked_by": []
    }
  ],
  "heartbeats": [
    {
      "id": "hb-daily-loop",
      "name": "Daily operator loop",
      "scope_type": "company",
      "scope_id": "prompt-engines",
      "cadence": "daily 09:00",
      "owner": "Golem",
      "last_run": "2026-03-09T09:00:00Z",
      "next_run": "2026-03-10T09:00:00Z",
      "status": "due",
      "budget_minutes": 20,
      "expected_output": "SITREP covering what exists, what changed, what needs attention, and what is ready to ship."
    },
    {
      "id": "hb-build-stream",
      "name": "Build stream digest",
      "scope_type": "venture",
      "scope_id": "lab-notes",
      "cadence": "daily 23:55 UTC",
      "owner": "Thoth",
      "last_run": "2026-03-09T23:55:00Z",
      "next_run": "2026-03-10T23:55:00Z",
      "status": "scheduled",
      "budget_minutes": 18,
      "expected_output": "Draft cross-repo build stream article and operator notes."
    },
    {
      "id": "hb-weekly-review",
      "name": "Weekly operating review",
      "scope_type": "company",
      "scope_id": "prompt-engines",
      "cadence": "weekly Monday 10:00",
      "owner": "A.I.",
      "last_run": "2026-03-03T10:00:00Z",
      "next_run": "2026-03-10T10:00:00Z",
      "status": "upcoming",
      "budget_minutes": 45,
      "expected_output": "Portfolio review, decisions required, and next-week priorities."
    },
    {
      "id": "hb-kaizen-refresh",
      "name": "Kaizen status refresh",
      "scope_type": "venture",
      "scope_id": "kaizen",
      "cadence": "every 2 days",
      "owner": "Prometheus",
      "last_run": "2026-03-08T15:00:00Z",
      "next_run": "2026-03-10T15:00:00Z",
      "status": "upcoming",
      "budget_minutes": 15,
      "expected_output": "Updated venture health, growth signal, and next action."
    },
    {
      "id": "hb-storybook-gate",
      "name": "Storybook launch gate review",
      "scope_type": "venture",
      "scope_id": "storybook-studio",
      "cadence": "weekly Thursday 14:00",
      "owner": "Hermetic_Demiurge",
      "last_run": "2026-03-01T14:00:00Z",
      "next_run": "2026-03-08T14:00:00Z",
      "status": "due",
      "budget_minutes": 25,
      "expected_output": "Launch blocker review and approval prep."
    },
    {
      "id": "hb-budget-review",
      "name": "Monthly runtime and budget review",
      "scope_type": "company",
      "scope_id": "prompt-engines",
      "cadence": "monthly day 1 11:00",
      "owner": "Golem",
      "last_run": "2026-03-01T11:00:00Z",
      "next_run": "2026-04-01T11:00:00Z",
      "status": "scheduled",
      "budget_minutes": 30,
      "expected_output": "Spend versus forecast by venture and agent."
    }
  ],
  "approvals": [
    {
      "id": "ap-branding",
      "title": "Adopt Pantheon OS as the canonical internal system name.",
      "related_type": "task",
      "related_id": "t-rename-pantheon",
      "risk": "medium",
      "approver": "A.I.",
      "status": "approved",
      "due_date": "2026-03-10",
      "criteria": [
        "Name is reflected across dashboard, docs, registry, and constitution.",
        "Company OS alias remains available for continuity."
      ]
    },
    {
      "id": "ap-public-deploy",
      "title": "Approve any hosted or public-facing Pantheon OS deployment.",
      "related_type": "task",
      "related_id": "t-public-deploy-decision",
      "risk": "high",
      "approver": "A.I.",
      "status": "pending",
      "due_date": "2026-03-12",
      "criteria": [
        "Auth and visibility model is explicit.",
        "Public and private data are separated.",
        "Sensitive ops data is excluded or gated."
      ]
    },
    {
      "id": "ap-agent-wake-cycles",
      "title": "Approve budgeted recurring wake cycles for operators and maintenance agents.",
      "related_type": "task",
      "related_id": "t-heartbeat-model",
      "risk": "medium",
      "approver": "A.I.",
      "status": "in_review",
      "due_date": "2026-03-11",
      "criteria": [
        "Each heartbeat has a cadence, owner, expected output, and runtime cap.",
        "Auto-executed tasks exclude publication and deployment."
      ]
    },
    {
      "id": "ap-budget-caps",
      "title": "Approve initial monthly runtime caps per agent and venture.",
      "related_type": "task",
      "related_id": "t-budget-model",
      "risk": "medium",
      "approver": "A.I.",
      "status": "pending",
      "due_date": "2026-03-13",
      "criteria": [
        "Budgets are visible by agent and venture.",
        "Variance is reviewed monthly.",
        "High-cost loops require explicit signoff."
      ]
    }
  ],
  "budgets": {
    "currency": "USD",
    "period": "2026-03",
    "company": {
      "allocated": 2450,
      "spent": 1465,
      "forecast": 2140
    },
    "by_agent": [
      {
        "name": "Hermetic_Demiurge",
        "allocated": 900,
        "spent": 510,
        "forecast": 860
      },
      {
        "name": "Thoth",
        "allocated": 420,
        "spent": 240,
        "forecast": 395
      },
      {
        "name": "Prometheus",
        "allocated": 560,
        "spent": 355,
        "forecast": 520
      },
      {
        "name": "Golem",
        "allocated": 310,
        "spent": 172,
        "forecast": 265
      },
      {
        "name": "A.I.",
        "allocated": 260,
        "spent": 188,
        "forecast": 100
      }
    ]
  },
  "skills": [
    {
      "id": "weekly-operating-review",
      "name": "Weekly Operating Review",
      "category": "company-os",
      "owner": "Thoth",
      "version": "0.1.0",
      "status": "drafted",
      "review_cadence": "weekly",
      "venture_scope": "all",
      "path": "skills/company-os/weekly-operating-review/SKILL.md",
      "use_cases": [
        "Prepare portfolio sitrep",
        "Run leadership review",
        "Reset agent priorities for the coming week"
      ]
    },
    {
      "id": "venture-status-refresh",
      "name": "Venture Status Refresh",
      "category": "company-os",
      "owner": "Prometheus",
      "version": "0.1.0",
      "status": "drafted",
      "review_cadence": "every 2 weeks",
      "venture_scope": "all ventures",
      "path": "skills/company-os/venture-status-refresh/SKILL.md",
      "use_cases": [
        "Refresh a venture card",
        "Update health and next action",
        "Reconcile drift between sources"
      ]
    },
    {
      "id": "decision-gate-review",
      "name": "Decision Gate Review",
      "category": "company-os",
      "owner": "A.I.",
      "version": "0.1.0",
      "status": "drafted",
      "review_cadence": "monthly",
      "venture_scope": "all",
      "path": "skills/company-os/decision-gate-review/SKILL.md",
      "use_cases": [
        "Review a deployment gate",
        "Approve publication",
        "Approve a budget or external action"
      ]
    },
    {
      "id": "goal-tree-planning",
      "name": "Goal Tree Planning",
      "category": "company-os",
      "owner": "Hermetic_Demiurge",
      "version": "0.1.0",
      "status": "drafted",
      "review_cadence": "monthly",
      "venture_scope": "company + venture + project",
      "path": "skills/company-os/goal-tree-planning/SKILL.md",
      "use_cases": [
        "Translate strategy into execution",
        "Create company-to-venture task ladders",
        "Expose blockers and dependencies"
      ]
    },
    {
      "id": "build-stream-synthesis",
      "name": "Build Stream Synthesis",
      "category": "company-os",
      "owner": "Thoth",
      "version": "0.1.0",
      "status": "drafted",
      "review_cadence": "daily",
      "venture_scope": "portfolio",
      "path": "skills/company-os/build-stream-synthesis/SKILL.md",
      "use_cases": [
        "Turn commits into operator signal",
        "Draft a build-stream note",
        "Surface cross-repo patterns"
      ]
    }
  ],
  "memory": [
    {
      "at": "2026-03-10",
      "type": "decision",
      "summary": "Pantheon OS adopted as the canonical internal name; Company OS kept as a compatibility alias."
    },
    {
      "at": "2026-03-10",
      "type": "guidance",
      "summary": "Skills are treated as first-class operational assets with progressive disclosure and explicit governance."
    },
    {
      "at": "2026-03-10",
      "type": "architecture",
      "summary": "Paperclip patterns adopted selectively: goal hierarchy, heartbeats, governance, and budget visibility."
    },
    {
      "at": "2026-03-09",
      "type": "risk",
      "summary": "Dashboard auth and metrics integrity remain weak; public APIs and app registry drift need attention."
    },
    {
      "at": "2026-03-09",
      "type": "portfolio",
      "summary": "PromptEngines public surface includes Kaizen, Storybook Studio, Flow, Video Terminal, Norbu, Consulting, Vajra-Upaya, and Lab Notes."
    }
  ]
};
