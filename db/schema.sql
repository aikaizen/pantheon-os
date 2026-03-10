
-- Pantheon OS relational model

create table if not exists ventures (
  id text primary key,
  name text not null,
  domain text,
  repo text,
  stage text not null,
  status text not null,
  health text not null,
  owner text not null,
  next_action text,
  budget_allocated numeric default 0,
  budget_spent numeric default 0,
  budget_forecast numeric default 0,
  updated_at text default current_timestamp
);

create table if not exists agents (
  id text primary key,
  name text not null,
  type text not null,
  role text not null,
  archetype text,
  status text not null,
  monthly_budget numeric default 0,
  updated_at text default current_timestamp
);

create table if not exists skills (
  id text primary key,
  name text not null,
  category text not null,
  owner text not null,
  version text not null,
  status text not null,
  review_cadence text,
  venture_scope text,
  package_path text not null,
  updated_at text default current_timestamp
);

create table if not exists goals (
  id text primary key,
  parent_goal_id text references goals(id),
  scope text not null,
  title text not null,
  status text not null,
  owner text not null,
  target_metric text,
  target_date text,
  updated_at text default current_timestamp
);

create table if not exists goal_ventures (
  goal_id text not null references goals(id),
  venture_id text not null references ventures(id),
  primary key (goal_id, venture_id)
);

create table if not exists approvals (
  id text primary key,
  title text not null,
  related_type text not null,
  related_id text not null,
  risk text not null,
  approver text not null,
  status text not null,
  due_date text,
  criteria_json text,
  updated_at text default current_timestamp
);

create table if not exists heartbeats (
  id text primary key,
  name text not null,
  scope_type text not null,
  scope_id text not null,
  cadence text not null,
  owner text not null,
  last_run text,
  next_run text,
  status text not null,
  budget_minutes integer default 0,
  expected_output text,
  updated_at text default current_timestamp
);

create table if not exists tasks (
  id text primary key,
  goal_id text not null references goals(id),
  parent_task_id text references tasks(id),
  title text not null,
  status text not null,
  owner text not null,
  due_date text,
  risk text,
  approval_id text references approvals(id),
  heartbeat_id text references heartbeats(id),
  next_step text,
  blocked_by_json text default '[]',
  updated_at text default current_timestamp
);

create table if not exists budget_periods (
  id integer primary key autoincrement,
  entity_type text not null,
  entity_id text not null,
  period text not null,
  currency text not null default 'USD',
  allocated numeric default 0,
  spent numeric default 0,
  forecast numeric default 0,
  updated_at text default current_timestamp
);

create table if not exists memory_events (
  id integer primary key autoincrement,
  event_type text not null,
  summary text not null,
  related_type text,
  related_id text,
  captured_at text not null,
  captured_by text default 'Pantheon OS'
);
