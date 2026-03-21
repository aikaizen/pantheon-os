async function loadState() {
  const sources = ['../../data/pantheon-os-state.json', './data/mock-state.json'];
  for (const source of sources) {
    try {
      const response = await fetch(source, { cache: 'no-store' });
      if (response.ok) {
        const data = await response.json();
        return { data, source };
      }
    } catch (_) {}
  }
  throw new Error('Could not load state data');
}

function makeStatus(status) {
  const cls = ['status'];
  if (status === 'planned' || status === 'unknown' || status === 'stale') cls.push('status--planned');
  if (status === 'critical' || status === 'blocked' || status === 'failed') cls.push('status--critical');
  return `<span class="${cls.join(' ')}">${status}</span>`;
}

function runtimeForAgent(agent, runtimes) {
  const binding = (agent.runtime_bindings || [])[0];
  if (!binding) return null;
  return runtimes.find((runtime) => runtime.id === binding.runtime_id) || null;
}

function channelForAgent(agent, channels) {
  const binding = (agent.channel_bindings || []).find((item) => item.status === 'active') || (agent.channel_bindings || [])[0];
  if (!binding) return null;
  return channels.find((channel) => channel.id === binding.channel_id) || null;
}

function renderSummary(summary) {
  const grid = document.getElementById('summary-grid');
  const cards = [
    ['agents', summary.agent_count],
    ['runtimes', summary.runtime_count],
    ['controllers', summary.controller_count],
    ['channels', summary.channel_count],
    ['deployments', summary.deployment_count],
    ['ventures', summary.venture_count],
  ];
  grid.innerHTML = cards
    .map(([label, value]) => `<div class="summary-card"><div class="label">${label}</div><strong>${value}</strong></div>`)
    .join('');
}

function renderPersonas(agents, runtimes, channels) {
  const target = document.getElementById('persona-list');
  const personas = agents.filter((agent) => agent.id !== 'ai-principal');
  document.getElementById('persona-count').textContent = String(personas.length);
  target.innerHTML = personas.map((agent) => {
    const runtime = runtimeForAgent(agent, runtimes);
    const channel = channelForAgent(agent, channels);
    const heartbeat = agent.heartbeat || {};
    return `
      <div class="item">
        <div class="item__meta">persona</div>
        <strong>${agent.name}</strong>
        <p>${agent.role}</p>
        ${makeStatus(heartbeat.status || agent.status || 'unknown')}
        <div class="item__row"><span>channel</span><span>${channel ? channel.name : 'unbound'}</span></div>
        <div class="item__row"><span>runtime</span><span>${runtime ? runtime.name : 'unbound'}</span></div>
      </div>`;
  }).join('');
}

function renderControllers(controllers) {
  const target = document.getElementById('controller-list');
  document.getElementById('controller-count').textContent = String(controllers.length);
  target.innerHTML = controllers.map((controller) => `
    <div class="item">
      <div class="item__meta">controller</div>
      <strong>${controller.name}</strong>
      <p>${controller.agent_system} · access: ${controller.access_level}</p>
      ${makeStatus((controller.heartbeat || {}).status || controller.status || 'unknown')}
      <div class="item__row"><span>manages</span><span>${(controller.manages || []).length} runtimes</span></div>
    </div>`).join('');
}

function renderRuntimes(runtimes) {
  const target = document.getElementById('runtime-list');
  document.getElementById('runtime-count').textContent = String(runtimes.length);
  target.innerHTML = runtimes.map((runtime) => `
    <div class="item">
      <div class="item__meta">runtime</div>
      <strong>${runtime.name}</strong>
      <p>${runtime.runtime_system} · ${runtime.kind} · ${runtime.branding_mode || 'native'}</p>
      ${makeStatus((runtime.heartbeat || {}).status || runtime.status || 'unknown')}
      <div class="item__row"><span>mode</span><span>${runtime.access_mode}</span></div>
      <div class="item__row"><span>deploy</span><span>${runtime.deployment_mode || '—'} · ${runtime.support_level || '—'}</span></div>
      <div class="item__row"><span>host</span><span>${runtime.host ? runtime.host.label : '—'}</span></div>
    </div>`).join('');
}

function renderChannels(channels) {
  const target = document.getElementById('channel-list');
  document.getElementById('channel-count').textContent = String(channels.length);
  target.innerHTML = channels.map((channel) => `
    <div class="item">
      <div class="item__meta">channel</div>
      <strong>${channel.name}</strong>
      <p>${channel.platform} · ${channel.kind}</p>
      ${makeStatus(channel.status || 'unknown')}
      <div class="item__row"><span>mode</span><span>${channel.access_mode}</span></div>
    </div>`).join('');
}

function renderVentures(ventures, deployment) {
  const target = document.getElementById('venture-list');
  const tier = (((deployment || {}).pilot_scope || {}).tier_1) || [];
  const filtered = ventures.filter((venture) => tier.includes(venture.id));
  document.getElementById('venture-count').textContent = String(filtered.length);
  target.innerHTML = filtered.map((venture) => `
    <div class="item">
      <div class="item__meta">venture</div>
      <strong>${venture.name}</strong>
      <p>${venture.domain || venture.repo || ''}</p>
      ${makeStatus(venture.status || 'unknown')}
      <div class="item__row"><span>next</span><span>${venture.next_action || '—'}</span></div>
    </div>`).join('');
}

async function boot() {
  const { data, source } = await loadState();
  const deployment = (data.deployments || [])[0] || {};
  document.getElementById('hero-lede').textContent = `Loaded ${source}. ${data.summary.runtime_count} runtimes, ${data.summary.controller_count} controllers, ${data.summary.channel_count} channels, ${data.summary.agent_count} agents.`;
  document.getElementById('deployment-name').textContent = deployment.name || 'PromptEngines';
  const runtimeLine = deployment.default_runtime_system ? `default runtime: ${deployment.default_runtime_system} (${deployment.default_branding_mode || 'native'})` : '';
  document.getElementById('deployment-mode').textContent = `modes: ${((deployment.modes || ['observe'])).join(' · ')}${runtimeLine ? ' · ' + runtimeLine : ''}`;

  renderSummary(data.summary);
  renderPersonas(data.agents || [], data.runtimes || [], data.channels || []);
  renderControllers(data.controllers || []);
  renderRuntimes(data.runtimes || []);
  renderChannels(data.channels || []);
  renderVentures(data.ventures || [], deployment);
}

boot().catch((error) => {
  document.getElementById('hero-lede').textContent = error.message;
});
