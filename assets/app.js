
const data = window.PANTHEON_OS_DATA;
const el = (tag, className, html) => { const node = document.createElement(tag); if (className) node.className = className; if (html !== undefined) node.innerHTML = html; return node; };
const money = (n) => `$${Number(n).toLocaleString()}`;
const niceDate = (value) => value.replace('T', ' ').replace('Z', '');
const badgeTone = (value) => {
  const lowered = String(value).toLowerCase();
  if (['approved', 'active', 'completed', 'strong', 'steady', 'scheduled'].includes(lowered)) return 'ok';
  if (['pending', 'in_review', 'building', 'upcoming', 'mixed', 'pre-launch'].includes(lowered)) return 'warn';
  if (['due', 'high', 'framing', 'mixed-signal'].includes(lowered)) return 'danger';
  return 'info';
};
function renderHeader() {
  document.getElementById('hero-title').textContent = data.meta.system_name;
  document.getElementById('hero-tagline').textContent = data.meta.tagline;
  document.getElementById('meta-version').textContent = data.meta.version;
  document.getElementById('meta-updated').textContent = niceDate(data.meta.updated_at);
}
function renderSummary() {
  const cards = [['Ventures', data.summary.venture_count], ['Open approvals', data.summary.open_approvals], ['Due heartbeats', data.summary.due_heartbeats], ['Active skills', data.summary.active_skills], ['Monthly budget', money(data.summary.monthly_budget)], ['Forecast spend', money(data.summary.monthly_forecast)]];
  const wrap = document.getElementById('summary-cards');
  cards.forEach(([label, value]) => { const card = el('div', 'summary-card'); card.append(el('div', 'label', label)); card.append(el('strong', '', value)); wrap.append(card); });
}
function renderVentures() {
  const wrap = document.getElementById('venture-grid');
  data.ventures.forEach((venture) => {
    const pct = Math.min(100, Math.round((venture.budget.spent / venture.budget.allocated) * 100));
    const card = el('article', 'venture-card');
    card.append(el('h4', '', venture.name));
    const meta = el('div', 'venture-meta');
    meta.append(el('span', `badge ${badgeTone(venture.stage)}`, venture.stage));
    meta.append(el('span', `badge ${badgeTone(venture.status)}`, venture.status));
    meta.append(el('span', `badge ${badgeTone(venture.health)}`, venture.health));
    card.append(meta);
    card.append(el('p', '', `<strong>Owner:</strong> ${venture.owner}`));
    card.append(el('p', '', `<strong>Domain:</strong> ${venture.domain}`));
    card.append(el('p', '', `<strong>Next:</strong> ${venture.next_action}`));
    card.append(el('div', 'money-row', `<span>Allocated ${money(venture.budget.allocated)}</span><span>Spent ${money(venture.budget.spent)}</span><span>Forecast ${money(venture.budget.forecast)}</span>`));
    const bar = el('div', 'bar'); bar.append(el('span', '', '')); bar.firstChild.style.width = `${pct}%`; card.append(bar); wrap.append(card);
  });
}
function renderGoalTree() {
  const wrap = document.getElementById('goal-tree'); wrap.className = 'goal-tree';
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
      taskList.forEach((task) => { const line = el('div', 'task-line'); line.innerHTML = `<strong>${task.title}</strong><br /><small>${task.status} · ${task.owner} · next: ${task.next_step}</small>`; tasksWrap.append(line); });
      node.append(tasksWrap);
    }
    const kids = childrenByGoal[goal.id] || [];
    if (kids.length) { const childWrap = el('div', 'goal-children'); kids.forEach((kid) => childWrap.append(renderGoal(kid))); node.append(childWrap); }
    return node;
  };
  (childrenByGoal.root || []).forEach((goal) => wrap.append(renderGoal(goal)));
}
function renderHeartbeats() {
  const wrap = document.getElementById('heartbeat-list'); wrap.className = 'list-stack';
  data.heartbeats.forEach((heartbeat) => { const card = el('div', 'heartbeat-card'); card.append(el('h4', '', heartbeat.name)); card.append(el('div', 'venture-meta', `<span class="badge ${badgeTone(heartbeat.status)}">${heartbeat.status}</span><span class="pill">${heartbeat.cadence}</span><span class="pill">${heartbeat.owner}</span>`)); card.append(el('p', '', heartbeat.expected_output)); card.append(el('p', 'tiny', `Last: ${niceDate(heartbeat.last_run)} · Next: ${niceDate(heartbeat.next_run)} · Runtime budget: ${heartbeat.budget_minutes} min`)); wrap.append(card); });
}
function renderApprovals() {
  const wrap = document.getElementById('approval-list'); wrap.className = 'list-stack';
  data.approvals.forEach((approval) => { const card = el('div', 'approval-card'); card.append(el('h4', '', approval.title)); card.append(el('div', 'venture-meta', `<span class="badge ${badgeTone(approval.status)}">${approval.status}</span><span class="badge ${badgeTone(approval.risk)}">risk: ${approval.risk}</span><span class="pill">approver: ${approval.approver}</span>`)); const list = el('ul'); approval.criteria.forEach((item) => list.append(el('li', '', item))); card.append(list); card.append(el('p', 'tiny', `Due: ${approval.due_date}`)); wrap.append(card); });
}
function renderBudgets() {
  const company = data.budgets.company;
  document.getElementById('budget-summary').innerHTML = `<div class="summary-card"><div class="label">Company runtime posture</div><strong>${money(company.spent)} / ${money(company.allocated)}</strong><div class="money-row"><span>Forecast ${money(company.forecast)}</span><span>Variance ${money(company.allocated - company.forecast)}</span></div></div>`;
  const wrap = document.getElementById('budget-breakdown'); wrap.className = 'budget-bar-grid';
  data.budgets.by_agent.forEach((row) => { const pct = Math.min(100, Math.round((row.spent / row.allocated) * 100)); const card = el('div', 'summary-card'); card.append(el('div', 'label', row.name)); card.append(el('strong', '', money(row.spent))); card.append(el('div', 'money-row', `<span>Allocated ${money(row.allocated)}</span><span>Forecast ${money(row.forecast)}</span>`)); const bar = el('div', 'bar'); bar.append(el('span', '', '')); bar.firstChild.style.width = `${pct}%`; card.append(bar); wrap.append(card); });
}
function renderSkills() {
  const wrap = document.getElementById('skill-list'); wrap.className = 'skill-grid';
  data.skills.forEach((skill) => { const card = el('div', 'skill-card'); card.append(el('h4', '', skill.name)); card.append(el('div', 'skill-meta', `<span class="badge ${badgeTone(skill.status)}">${skill.status}</span><span class="pill">${skill.owner}</span><span class="pill">${skill.review_cadence}</span>`)); const list = el('ul'); skill.use_cases.forEach((item) => list.append(el('li', '', item))); card.append(list); card.append(el('p', 'tiny', skill.path)); wrap.append(card); });
}
function renderAgents() {
  const wrap = document.getElementById('agent-list'); wrap.className = 'agent-grid';
  data.agents.forEach((agent) => { const card = el('div', 'agent-card'); card.append(el('h4', '', agent.name)); card.append(el('div', 'agent-meta', `<span class="badge ${badgeTone(agent.status)}">${agent.status}</span><span class="pill">${agent.type}</span><span class="pill">${agent.archetype}</span>`)); card.append(el('p', '', agent.role)); card.append(el('p', 'tiny', `Monthly budget: ${money(agent.monthly_budget)}`)); const list = el('ul'); agent.skills.forEach((item) => list.append(el('li', '', item))); card.append(list); wrap.append(card); });
}
function renderMemory() {
  const wrap = document.getElementById('memory-list'); wrap.className = 'memory-grid';
  data.memory.forEach((entry) => { const card = el('div', 'memory-card'); card.append(el('h4', '', entry.type)); card.append(el('p', '', entry.summary)); card.append(el('p', 'tiny', entry.at)); wrap.append(card); });
}
function renderGuidance() {
  const skills = document.getElementById('guidance-skills'); data.guidance.anthropic_skill_standard.forEach((item) => skills.append(el('li', '', item)));
  const paperclip = document.getElementById('guidance-paperclip');
  paperclip.append(el('li', '', `Reference value: ${data.guidance.paperclip_stance.reference_value}`));
  paperclip.append(el('li', '', `Direct v1 fit: ${data.guidance.paperclip_stance.direct_v1_fit}`));
  paperclip.append(el('li', '', data.guidance.paperclip_stance.adoption_recommendation));
  data.guidance.paperclip_elements_adopted.forEach((item) => paperclip.append(el('li', '', item)));
}
renderHeader(); renderSummary(); renderVentures(); renderGoalTree(); renderHeartbeats(); renderApprovals(); renderBudgets(); renderSkills(); renderAgents(); renderMemory(); renderGuidance();
