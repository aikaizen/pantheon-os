
const data = window.PANTHEON_OS_DATA;
const el = (tag, className, html) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (html !== undefined) node.innerHTML = html;
  return node;
};
const money = (n) => `$${Number(n).toLocaleString()}`;
const niceDate = (value) => String(value).replace('T', ' ').replace('Z', '');
const badgeTone = (value) => {
  const lowered = String(value).toLowerCase();
  if (['approved','active','completed','strong','steady','wired','product'].includes(lowered)) return 'ok';
  if (['pending','in_review','building','upcoming','mixed','pre-launch','service','experiment','mvp'].includes(lowered)) return 'warn';
  if (['due','high','framing','mixed-signal','prototype','human-needed','discovery'].includes(lowered)) return 'danger';
  return 'info';
};
const groupOrder = ['platform','product','service','experiment','prototype','incubation','internal-system'];

function renderHeader() {
  document.getElementById('hero-title').textContent = data.meta.system_name;
  document.getElementById('hero-tagline').textContent = data.meta.tagline;
  document.getElementById('target-host').textContent = `Target: ${data.meta.target_host}`;
  document.getElementById('access-model').textContent = `Access: ${data.meta.access_mode} · ${data.meta.auth_provider}`;
  const heroMeta = document.getElementById('hero-meta');
  [
    ['Version', data.meta.version],
    ['Updated', niceDate(data.meta.updated_at)],
    ['Branch', data.meta.branch]
  ].forEach(([label, value]) => {
    const chip = el('div', 'stat-chip');
    chip.append(el('span', '', label));
    chip.append(el('strong', '', value));
    heroMeta.append(chip);
  });
}

function renderSummary() {
  const cards = [
    ['Ventures', data.summary.venture_count],
    ['Active', data.summary.active_count],
    ['Experiments', data.summary.experiment_count],
    ['Prototypes', data.summary.prototype_count],
    ['Wiring needed', data.summary.wiring_needed],
    ['Forecast spend', money(data.summary.monthly_forecast)]
  ];
  const wrap = document.getElementById('summary-cards');
  cards.forEach(([label, value]) => {
    const card = el('div', 'summary-card');
    card.append(el('div', 'label', label));
    card.append(el('strong', '', value));
    wrap.append(card);
  });
}

function renderPortfolio() {
  const wrap = document.getElementById('portfolio-groups');
  const legend = document.getElementById('stage-legend');
  const byCategory = {};
  data.ventures.forEach((venture) => {
    const key = venture.category;
    byCategory[key] ||= [];
    byCategory[key].push(venture);
  });
  groupOrder.filter((key) => byCategory[key]).forEach((key) => {
    const group = el('section', 'stage-group');
    group.append(el('h4', '', key.replaceAll('-', ' ')));
    const grid = el('div', 'venture-grid');
    byCategory[key].forEach((venture) => {
      const pct = Math.min(100, Math.round((venture.budget.spent / venture.budget.allocated) * 100));
      const card = el('article', 'venture-card');
      card.append(el('h4', '', venture.name));
      const meta = el('div', 'venture-meta');
      meta.append(el('span', `badge ${badgeTone(venture.stage)}`, venture.stage));
      meta.append(el('span', `badge ${badgeTone(venture.status)}`, venture.status));
      meta.append(el('span', `badge ${badgeTone(venture.health)}`, venture.health));
      meta.append(el('span', 'pill', venture.surface));
      card.append(meta);
      card.append(el('p', '', `<strong>Owner:</strong> ${venture.owner}`));
      card.append(el('p', '', `<strong>Repo:</strong> ${venture.repo}`));
      card.append(el('p', '', `<strong>Next:</strong> ${venture.next_action}`));
      card.append(el('p', 'tiny', `<strong>Wiring:</strong> ${venture.wiring}`));
      card.append(el('div', 'money-row', `<span>Allocated ${money(venture.budget.allocated)}</span><span>Spent ${money(venture.budget.spent)}</span><span>${venture.telemetry}</span>`));
      const bar = el('div', 'bar');
      bar.append(el('span', '', ''));
      bar.firstChild.style.width = `${pct}%`;
      card.append(bar);
      grid.append(card);
    });
    group.append(grid);
    wrap.append(group);
    legend.append(el('span', `badge ${badgeTone(key)}`, key.replaceAll('-', ' ')));
  });
}

function renderActivity() {
  const wrap = document.getElementById('activity-feed');
  data.activity.forEach((item) => {
    const card = el('div', 'activity-card');
    const meta = el('div', 'activity-meta');
    meta.append(el('span', 'pill', item.time));
    meta.append(el('span', 'pill', item.venture));
    meta.append(el('span', `badge ${badgeTone(item.type)}`, item.type));
    card.append(meta);
    card.append(el('h4', '', item.summary));
    card.append(el('p', 'tiny', `Actor: ${item.actor}`));
    wrap.append(card);
  });
}

function renderGoalTree() {
  const wrap = document.getElementById('goal-tree');
  wrap.className = 'goal-tree';
  const tasksByGoal = data.tasks.reduce((acc, task) => { (acc[task.goal_id] ||= []).push(task); return acc; }, {});
  const childrenByGoal = data.goals.reduce((acc, goal) => { (acc[goal.parent_id || 'root'] ||= []).push(goal); return acc; }, {});
  const renderGoal = (goal) => {
    const node = el('div', 'goal-card');
    node.append(el('h4', '', goal.title));
    const meta = el('div', 'venture-meta');
    meta.append(el('span', `badge ${badgeTone(goal.scope)}`, goal.scope));
    meta.append(el('span', `badge ${badgeTone(goal.status)}`, goal.status));
    meta.append(el('span', 'pill', `Owner: ${goal.owner}`));
    node.append(meta);
    node.append(el('p', '', `<strong>Target:</strong> ${goal.target_metric}`));
    node.append(el('p', 'tiny', `<strong>Due:</strong> ${goal.target_date}`));
    const taskList = tasksByGoal[goal.id] || [];
    if (taskList.length) {
      const tasksWrap = el('div', 'task-list');
      taskList.forEach((task) => {
        const line = el('div', 'task-line');
        line.innerHTML = `<strong>${task.title}</strong><br /><small>${task.status} · ${task.owner} · next: ${task.next_step}</small>`;
        tasksWrap.append(line);
      });
      node.append(tasksWrap);
    }
    const kids = childrenByGoal[goal.id] || [];
    if (kids.length) {
      const childWrap = el('div', 'goal-children');
      kids.forEach((kid) => childWrap.append(renderGoal(kid)));
      node.append(childWrap);
    }
    return node;
  };
  (childrenByGoal.root || []).forEach((goal) => wrap.append(renderGoal(goal)));
}

function renderHeartbeats() {
  const wrap = document.getElementById('heartbeat-list');
  data.heartbeats.forEach((hb) => {
    const card = el('div', 'heartbeat-card');
    card.append(el('h4', '', hb.name));
    card.append(el('div', 'venture-meta', `<span class="badge ${badgeTone(hb.status)}">${hb.status}</span><span class="pill">${hb.cadence}</span><span class="pill">${hb.owner}</span>`));
    card.append(el('p', '', hb.expected_output));
    wrap.append(card);
  });
}

function renderApprovals() {
  const wrap = document.getElementById('approval-list');
  data.approvals.forEach((approval) => {
    const card = el('div', 'approval-card');
    card.append(el('h4', '', approval.title));
    card.append(el('div', 'venture-meta', `<span class="badge ${badgeTone(approval.status)}">${approval.status}</span><span class="badge ${badgeTone(approval.risk)}">risk: ${approval.risk}</span><span class="pill">${approval.approver}</span>`));
    card.append(el('p', 'tiny', `Due: ${approval.due_date}`));
    wrap.append(card);
  });
}

function renderBudgets() {
  const company = data.budgets.company;
  document.getElementById('budget-summary').innerHTML = `<div class="summary-card"><div class="label">Company runtime posture</div><strong>${money(company.spent)} / ${money(company.allocated)}</strong><div class="money-row"><span>Forecast ${money(company.forecast)}</span><span>Variance ${money(company.allocated - company.forecast)}</span></div></div>`;
  const wrap = document.getElementById('budget-breakdown');
  data.budgets.by_agent.forEach((row) => {
    const pct = row.allocated ? Math.min(100, Math.round((row.spent / row.allocated) * 100)) : 0;
    const card = el('div', 'summary-card');
    card.append(el('div', 'label', row.name));
    card.append(el('strong', '', money(row.spent)));
    card.append(el('div', 'money-row', `<span>Allocated ${money(row.allocated)}</span><span>Forecast ${money(row.forecast)}</span>`));
    const bar = el('div', 'bar');
    bar.append(el('span', '', ''));
    bar.firstChild.style.width = `${pct}%`;
    card.append(bar);
    wrap.append(card);
  });
}

function renderOperators() {
  const wrap = document.getElementById('operator-grid');
  data.agents.forEach((agent) => {
    const card = el('div', 'operator-card');
    card.append(el('h4', '', agent.name));
    card.append(el('div', 'operator-meta', `<span class="badge ${badgeTone(agent.status)}">${agent.status}</span><span class="pill">${agent.type}</span><span class="pill">${agent.archetype}</span>`));
    card.append(el('p', '', agent.role));
    card.append(el('p', 'tiny', `<strong>Ventures:</strong> ${agent.ventures.join(', ')}`));
    card.append(el('p', 'tiny', agent.notes));
    wrap.append(card);
  });
}

function renderWiring() {
  const wrap = document.getElementById('wiring-list');
  data.wiring.forEach((item) => {
    const card = el('div', 'wiring-card');
    card.append(el('h4', '', item.title));
    card.append(el('div', 'venture-meta', `<span class="badge ${badgeTone(item.status)}">${item.status}</span><span class="pill">Owner: ${item.owner}</span><span class="pill">Impact: ${item.impact}</span>`));
    card.append(el('p', '', item.needed_from_human));
    wrap.append(card);
  });
}

function renderGuidance() {
  const skillList = document.getElementById('guidance-skills');
  data.guidance.anthropic_skill_standard.forEach((item) => skillList.append(el('li', '', item)));
  const principles = document.getElementById('guidance-principles');
  data.guidance.principles.forEach((item) => principles.append(el('li', '', item)));
}

renderHeader();
renderSummary();
renderPortfolio();
renderActivity();
renderGoalTree();
renderHeartbeats();
renderApprovals();
renderBudgets();
renderOperators();
renderWiring();
renderGuidance();
