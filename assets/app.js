const summary = [
  { label: 'Live deployments', value: '1', note: 'PromptEngines is live now' },
  { label: 'Tracked surfaces', value: '15', note: 'Public, prototype, and internal' },
  { label: 'Active agents', value: '2', note: 'Canonical live roster only' },
  { label: 'Metric families', value: '6', note: 'Already defined in dashboard work' },
  { label: 'Visible company surfaces', value: '13', note: 'Public and prototype surfaces on the company map' },
  { label: 'Internal control surfaces', value: '2', note: 'Dashboard + terminal manager' },
];

const deployments = [
  {
    name: 'PromptEngines',
    stage: 'reference deployment',
    status: 'live',
    summary: 'Applied AI lab using Pantheon OS as its first real company operating system deployment.',
    metrics: [
      '13 visible company surfaces',
      '2 active agents + 1 human principal',
      '6 metric families defined',
      'Dashboard and terminal-manager split preserved',
    ],
  },
];

const metricFamilies = [
  {
    name: 'Growth',
    route: '/growth',
    description: 'Acquisition and retention across company and app surfaces.',
    metrics: ['Total users', 'New users', 'DAU / WAU / MAU', 'Stickiness', 'Retention cohorts'],
  },
  {
    name: 'Finance',
    route: '/finance',
    description: 'Commercial performance and cost visibility.',
    metrics: ['Revenue', 'Monthly revenue', 'Credits purchased / spent', 'COGS', 'Margin', 'Revenue by source'],
  },
  {
    name: 'Engagement',
    route: '/engagement',
    description: 'How deeply each product is actually used.',
    metrics: ['Avg session duration', 'Sessions per user', 'Actions per session', 'Activation rate', 'Top features'],
  },
  {
    name: 'Reliability',
    route: '/reliability',
    description: 'Operational quality and trustworthiness.',
    metrics: ['Success rate', 'Error rate', 'p50 / p95 / p99 latency', 'Status indicators'],
  },
  {
    name: 'Unit Economics',
    route: '/finance',
    description: 'Whether usage and growth compound or leak margin.',
    metrics: ['ARPU', 'Cost per user', 'Margin per user', 'LTV', 'Paying users'],
  },
  {
    name: 'User Profitability',
    route: '/users',
    description: 'Per-user value, cost, funnel, and retained behavior.',
    metrics: ['Plan', 'Funnel stage', 'Revenue vs cost', 'Credits balance', 'Payments', 'Recent activity'],
  },
];

const applications = [
  {
    id: 'promptengines-web',
    group: 'Company Surfaces',
    name: 'PromptEngines.com',
    stage: 'Product',
    status: 'active',
    detail: 'Primary company surface for portfolio framing, app routing, and company narrative.',
    northStar: 'Make the company legible and convert attention into qualified demand.',
    metrics: ['Visitors → signups', 'App clickthrough', 'Lead conversion', 'Site freshness'],
  },
  {
    id: 'lab-notes',
    group: 'Company Surfaces',
    name: 'Lab Notes',
    stage: 'Product',
    status: 'active',
    detail: 'Publishing and build-intelligence layer. Also the canonical public team page.',
    northStar: 'Turn active work into legible insight without losing freshness.',
    metrics: ['Articles shipped', 'Read depth', 'Build-stream freshness', 'Audience growth'],
  },
  {
    id: 'consulting',
    group: 'Company Surfaces',
    name: 'Consulting',
    stage: 'Service',
    status: 'active',
    detail: 'Applied AI consulting offer and delivery surface.',
    northStar: 'Convert inbound demand into healthy revenue and delivery margin.',
    metrics: ['Inbound leads', 'Proposal conversion', 'Booked revenue', 'Delivery margin'],
  },
  {
    id: 'kaizen',
    group: 'Products',
    name: 'Kaizen',
    stage: 'Active',
    status: 'active',
    detail: 'Closest product to a real dashboard adapter and one of the clearest telemetry reference points.',
    northStar: 'Grow active learners while keeping latency and generation cost bounded.',
    metrics: ['DAU / WAU / MAU', 'Credits purchased vs spent', 'Signup → first generation', 'Generation latency'],
  },
  {
    id: 'storybook-studio',
    group: 'Products',
    name: 'Storybook Studio',
    stage: 'Pre-Launch',
    status: 'prelaunch',
    detail: 'Creator product with print, checkout, and book-generation economics.',
    northStar: 'Turn creators into repeat book buyers with stable print-ready output.',
    metrics: ['Active creators', 'Book generations', 'Checkout conversion', 'Print margin'],
  },
  {
    id: 'video-terminal',
    group: 'Products',
    name: 'Video Terminal',
    stage: 'Alpha',
    status: 'alpha',
    detail: 'Node-based media tool with workflow, render, and export questions.',
    northStar: 'Prove a tight creation loop with reliable render success.',
    metrics: ['Active runs', 'Render success rate', 'Export rate', 'Render latency'],
  },
  {
    id: 'norbu',
    group: 'Products',
    name: 'Norbu',
    stage: 'Active',
    status: 'active',
    detail: 'Language-learning product with curriculum and retention questions.',
    northStar: 'Increase learner retention and paid conversion.',
    metrics: ['Weekly learners', 'Lesson completion', 'Paid conversion', 'Retention'],
  },
  {
    id: 'bible',
    group: 'Products',
    name: 'Bible',
    stage: 'Active',
    status: 'active',
    detail: 'Scripture product with community and notification loops already entering the dashboard model.',
    northStar: 'Grow repeat reading sessions and notification reliability.',
    metrics: ['Readers', 'Study sessions', 'Notification success', 'Retention'],
  },
  {
    id: 'flow',
    group: 'Products',
    name: 'Flow',
    stage: 'Mixed Signal',
    status: 'drift',
    detail: 'Publicly visible, but still needs canonical resolution versus Flow Education.',
    northStar: 'Clarify what Flow is before overstating maturity.',
    metrics: ['Pilot sessions', 'Completion rate', 'Feedback', 'Latency'],
  },
  {
    id: 'flow-education',
    group: 'Prototypes',
    name: 'Flow Education',
    stage: 'Prototype',
    status: 'planned',
    detail: 'Prototype education surface that belongs in the company map but not in the mature-product bucket.',
    northStar: 'Learn whether the teaching loop is strong enough to formalize.',
    metrics: ['Prototype sessions', 'Lesson completion', 'Curriculum coverage'],
  },
  {
    id: 'vajra-upaya',
    group: 'Prototypes',
    name: 'Vajra-Upaya',
    stage: 'Prototype',
    status: 'planned',
    detail: 'Tool-fitting service prototype currently visible on the public site.',
    northStar: 'Prove signal quality and fit before building the larger shell.',
    metrics: ['Fit interviews', 'Recommendation quality', 'Pilot conversion'],
  },
  {
    id: 'resources',
    group: 'Prototypes',
    name: 'Resources',
    stage: 'Support Prototype',
    status: 'planned',
    detail: 'Reference / API support surface.',
    northStar: 'Increase internal leverage and reuse.',
    metrics: ['Reusable utilities', 'Docs usefulness', 'Reference visits'],
  },
  {
    id: 'vibes',
    group: 'Prototypes',
    name: 'Vibes',
    stage: 'Support Prototype',
    status: 'planned',
    detail: 'Design support surface and aesthetic R&D lane.',
    northStar: 'Increase reusable taste across shipped surfaces.',
    metrics: ['Explorations', 'Adoption into shipped surfaces', 'Asset reuse'],
  },
  {
    id: 'pantheon-dashboard',
    group: 'Internal Surfaces',
    name: 'Pantheon Dashboard',
    stage: 'MVP',
    status: 'active',
    detail: 'Strategic command surface for company legibility, metrics, and agent state.',
    northStar: 'Let the principal steer the company from one page.',
    metrics: ['Surface coverage', 'Metric-family coverage', 'Unread blockers', 'Approval latency'],
  },
  {
    id: 'terminal-manager',
    group: 'Internal Surfaces',
    name: 'Pant OS Terminal Manager',
    stage: 'Wireframe',
    status: 'planned',
    detail: 'Tactical multi-pane operating surface, separate from the dashboard.',
    northStar: 'Let the operator supervise chats, terminals, sessions, and interventions in one control room.',
    metrics: ['Active sessions', 'Unread handoffs', 'Intervention time', 'Session health'],
  },
];

const principal = {
  name: 'A.I.',
  role: 'Human Principal',
  note: 'Final authority, direction, approvals, and taste. Pantheon OS stays human-sovereign.',
};

const agents = [
  {
    id: 'andy-stable',
    name: 'Andy Stable 🦾',
    role: 'Operations & Execution',
    sitrep: 'Maintaining continuity and making sure the company surface matches reality.',
    current: 'Reconciling public PromptEngines surfaces with internal dashboard framing.',
    next: 'Tighten continuity, publish clearer operating state, and keep handoffs legible.',
    blockers: ['Needs a stronger portal-backed continuity layer.'],
    workingOn: ['PromptEngines.com', 'Lab Notes', 'Consulting', 'Company continuity'],
    route: 'terminal-manager://ops/andy-stable',
  },
  {
    id: 'hermetic-demiurge',
    name: 'Hermetic_Demiurge',
    role: 'Developer & Engineer',
    sitrep: 'Reworking the dashboard into a PromptEngines-first command surface and defining the terminal-manager wireframe.',
    current: 'Translating PromptEngines brand language and Pantheon operating logic into a sharper UI.',
    next: 'Move from static contract to live adapters and session-registry-backed control.',
    blockers: ['Needs real adapter coverage and terminal-manager backend wiring.'],
    workingOn: ['Pantheon Dashboard', 'Terminal Manager', 'Kaizen', 'Storybook Studio'],
    route: 'terminal-manager://build/hermetic-demiurge',
  },
];

const queue = [
  {
    to: 'Hermetic_Demiurge',
    priority: 'high',
    subject: 'Dashboard taste refresh',
    body: 'Make the dashboard feel like PromptEngines, not a generic rounded SaaS console.',
  },
  {
    to: 'Andy Stable 🦾',
    priority: 'medium',
    subject: 'Continuity pass',
    body: 'Keep the public company surface and internal dashboard contract aligned.',
  },
];

const principles = [
  {
    title: 'Human Sovereignty',
    body: 'The dashboard supports the principal. It does not replace the principal.',
  },
  {
    title: 'Truth Over Performance',
    body: 'If there is drift, ambiguity, or missing wiring, the UI should show it plainly.',
  },
  {
    title: 'Execution Over Chatter',
    body: 'State, ownership, blockers, next work, and intervention paths matter more than vanity numbers.',
  },
  {
    title: 'Boundaried Autonomy',
    body: 'Each active agent needs a lane, a mandate, a state summary, and a message route.',
  },
  {
    title: 'Portal Primacy',
    body: 'Shared state should survive sessions via explicit notes, tasks, approvals, and handoffs.',
  },
];

const surfaceSplit = [
  {
    title: 'Dashboard = strategic surface',
    body: 'Company map, metrics, activity, agent state, and portfolio legibility belong here.',
  },
  {
    title: 'Terminal Manager = tactical surface',
    body: 'Chats, shells, tmux-like panes, logs, interventions, and operator supervision belong there.',
  },
  {
    title: 'Message handoff is the bridge',
    body: 'The dashboard can send work into the terminal-manager lane without becoming the terminal itself.',
  },
];

const tabs = document.querySelectorAll('.nav-tab');
const tabPanels = document.querySelectorAll('.tab-panel');
let selectedSurface = applications[0].id;
let selectedAgent = agents[0].id;

function stateClass(value) {
  const lower = String(value).toLowerCase();
  if (['active', 'live', 'good'].includes(lower)) return 'state-good';
  if (['alpha', 'prelaunch', 'planned', 'prototype', 'support prototype', 'wireframe'].includes(lower)) return 'state-warn';
  if (['mixed signal', 'drift', 'blocked'].includes(lower)) return 'state-danger';
  return 'state-good';
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderSummary() {
  document.getElementById('summary-grid').innerHTML = summary.map((item) => `
    <article class="kpi-card">
      <div class="metric-key">${escapeHtml(item.label)}</div>
      <strong>${escapeHtml(item.value)}</strong>
      <p>${escapeHtml(item.note)}</p>
    </article>
  `).join('');
}

function renderDeployments() {
  document.getElementById('deployments-grid').innerHTML = deployments.map((item) => `
    <article class="deployment-card">
      <div class="deployment-head">
        <div>
          <div class="item-meta">${escapeHtml(item.stage)}</div>
          <h3>${escapeHtml(item.name)}</h3>
        </div>
        <span class="state-chip ${stateClass(item.status)}">${escapeHtml(item.status)}</span>
      </div>
      <p>${escapeHtml(item.summary)}</p>
      <div class="metric-row">
        ${item.metrics.map((metric) => `<span class="metric-chip">${escapeHtml(metric)}</span>`).join('')}
      </div>
    </article>
  `).join('');
}

function renderMetricFamilies() {
  document.getElementById('metric-families').innerHTML = metricFamilies.map((item) => `
    <article class="metric-family">
      <div class="item-meta">route ${escapeHtml(item.route)}</div>
      <h4>${escapeHtml(item.name)}</h4>
      <p>${escapeHtml(item.description)}</p>
      <ul>${item.metrics.map((metric) => `<li>${escapeHtml(metric)}</li>`).join('')}</ul>
    </article>
  `).join('');
}

function renderPortfolio() {
  const groups = [...new Set(applications.map((item) => item.group))];
  document.getElementById('portfolio-groups').innerHTML = groups.map((group) => {
    const items = applications.filter((item) => item.group === group);
    return `
      <section class="portfolio-group">
        <div class="portfolio-group-head">
          <h3>${escapeHtml(group)}</h3>
          <span class="metric-chip">${items.length} surfaces</span>
        </div>
        <div class="portfolio-grid">
          ${items.map((item) => `
            <button class="surface-card ${selectedSurface === item.id ? 'is-selected' : ''}" data-surface-id="${item.id}">
              <div class="card-head">
                <div>
                  <div class="item-meta">${escapeHtml(item.group)}</div>
                  <h4>${escapeHtml(item.name)}</h4>
                </div>
                <span class="state-chip ${stateClass(item.stage)}">${escapeHtml(item.stage)}</span>
              </div>
              <p>${escapeHtml(item.detail)}</p>
              <ul>${item.metrics.slice(0, 3).map((metric) => `<li>${escapeHtml(metric)}</li>`).join('')}</ul>
            </button>
          `).join('')}
        </div>
      </section>
    `;
  }).join('');

  document.querySelectorAll('[data-surface-id]').forEach((button) => {
    button.addEventListener('click', () => {
      selectedSurface = button.dataset.surfaceId;
      renderPortfolio();
      renderSurfaceDetail();
    });
  });
}

function renderSurfaceDetail() {
  const item = applications.find((app) => app.id === selectedSurface);
  if (!item) return;

  document.getElementById('surface-title').textContent = item.name;
  document.getElementById('surface-detail').innerHTML = `
    <div class="detail-block">
      <div class="item-meta">stage</div>
      <div class="surface-meta-row">
        <span class="state-chip ${stateClass(item.stage)}">${escapeHtml(item.stage)}</span>
        <span class="state-chip ${stateClass(item.status)}">${escapeHtml(item.status)}</span>
      </div>
    </div>
    <div class="detail-block">
      <h4>Why it belongs here</h4>
      <p>${escapeHtml(item.detail)}</p>
    </div>
    <div class="detail-block">
      <h4>North star</h4>
      <p>${escapeHtml(item.northStar)}</p>
    </div>
    <div class="detail-block">
      <h4>Metric focus</h4>
      <ul>${item.metrics.map((metric) => `<li>${escapeHtml(metric)}</li>`).join('')}</ul>
    </div>
  `;
}

function renderAgents() {
  document.getElementById('principal-panel').innerHTML = `
    <div class="item-meta">Human principal</div>
    <h3>${escapeHtml(principal.name)}</h3>
    <p>${escapeHtml(principal.note)}</p>
  `;

  document.getElementById('agent-list').innerHTML = agents.map((agent) => `
    <button class="agent-list-card ${selectedAgent === agent.id ? 'is-selected' : ''}" data-agent-id="${agent.id}">
      <div class="agent-head">
        <div>
          <div class="item-meta">active agent</div>
          <h3>${escapeHtml(agent.name)}</h3>
        </div>
        <span class="state-chip state-good">active</span>
      </div>
      <p class="agent-copy">${escapeHtml(agent.role)}</p>
    </button>
  `).join('');

  document.querySelectorAll('[data-agent-id]').forEach((button) => {
    button.addEventListener('click', () => {
      selectedAgent = button.dataset.agentId;
      renderAgents();
      renderAgentDetail();
      syncMessageTarget();
    });
  });
}

function renderAgentDetail() {
  const agent = agents.find((item) => item.id === selectedAgent);
  if (!agent) return;

  document.getElementById('agent-detail').innerHTML = `
    <div class="panel-head">
      <div>
        <span class="panel-kicker">Selected agent</span>
        <h3>${escapeHtml(agent.name)}</h3>
      </div>
      <span class="state-chip state-good">${escapeHtml(agent.role)}</span>
    </div>
    <div class="detail-block">
      <h4>Sitrep</h4>
      <p>${escapeHtml(agent.sitrep)}</p>
    </div>
    <div class="detail-block">
      <h4>What they are working on now</h4>
      <p>${escapeHtml(agent.current)}</p>
    </div>
    <div class="detail-block">
      <h4>What they are working on next</h4>
      <p>${escapeHtml(agent.next)}</p>
    </div>
    <div class="detail-block">
      <h4>Focus surfaces</h4>
      <div class="agent-focus-row">${agent.workingOn.map((item) => `<span class="mini-chip">${escapeHtml(item)}</span>`).join('')}</div>
    </div>
    <div class="detail-block">
      <h4>Blockers</h4>
      <ul>${agent.blockers.map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
    </div>
    <div class="detail-block">
      <h4>Terminal-manager route</h4>
      <p>${escapeHtml(agent.route)}</p>
    </div>
  `;
}

function renderPrinciples() {
  document.getElementById('principles-list').innerHTML = principles.map((item, index) => `
    <article class="principle-item ${index === 0 ? 'accent' : ''}">
      <div class="item-meta">principle</div>
      <h4>${escapeHtml(item.title)}</h4>
      <p>${escapeHtml(item.body)}</p>
    </article>
  `).join('');

  document.getElementById('surface-split-list').innerHTML = surfaceSplit.map((item, index) => `
    <article class="surface-split-item ${index === 0 ? 'accent' : ''}">
      <div class="item-meta">surface boundary</div>
      <h4>${escapeHtml(item.title)}</h4>
      <p>${escapeHtml(item.body)}</p>
    </article>
  `).join('');
}

function syncMessageTarget() {
  const agent = agents.find((item) => item.id === selectedAgent);
  if (!agent) return;
  document.getElementById('message-to').value = agent.name;
}

function renderQueue() {
  const queueNode = document.getElementById('message-queue');
  if (!queue.length) {
    queueNode.innerHTML = '<div class="empty-state">No queued handoffs.</div>';
    return;
  }

  queueNode.innerHTML = queue.map((item) => `
    <article class="queue-item ${item.priority}">
      <div class="queue-head">
        <div>
          <div class="item-meta">to ${escapeHtml(item.to)}</div>
          <h4>${escapeHtml(item.subject)}</h4>
        </div>
        <span class="queue-priority">${escapeHtml(item.priority)}</span>
      </div>
      <p>${escapeHtml(item.body)}</p>
    </article>
  `).join('');
}

document.getElementById('message-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const to = document.getElementById('message-to').value.trim();
  const priority = document.getElementById('message-priority').value.trim();
  const subject = document.getElementById('message-subject').value.trim();
  const body = document.getElementById('message-body').value.trim();

  if (!to || !subject || !body) return;

  queue.unshift({ to, priority, subject, body });
  renderQueue();
  event.target.reset();
  document.getElementById('message-priority').value = 'medium';
  syncMessageTarget();
});

tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    const target = tab.dataset.tab;
    tabs.forEach((item) => item.classList.toggle('is-active', item === tab));
    tabPanels.forEach((panel) => panel.classList.toggle('is-active', panel.id === `tab-${target}`));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});

renderSummary();
renderDeployments();
renderMetricFamilies();
renderPortfolio();
renderSurfaceDetail();
renderAgents();
renderAgentDetail();
renderPrinciples();
syncMessageTarget();
renderQueue();
