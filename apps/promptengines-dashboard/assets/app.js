
async function boot() {
  const data = await fetch('./data/dashboard.json').then(r => r.json());
  document.getElementById('title').textContent = data.meta.title;
  document.getElementById('subtitle').textContent = data.meta.subtitle + ' — ' + data.meta.updated_at;
  document.getElementById('deployment-note').textContent = data.meta.deployment_note;
  document.getElementById('access-model').textContent = data.meta.access_model;

  const summaryGrid = document.getElementById('summary-grid');
  Object.entries(data.summary).forEach(([k, v]) => {
    const card = document.createElement('div');
    card.className = 'summary-card';
    card.innerHTML = `<div class="label">${k.replaceAll('_', ' ')}</div><strong>${v}</strong>`;
    summaryGrid.appendChild(card);
  });

  const surfaceGrid = document.getElementById('surface-grid');
  data.surfaces.forEach(surface => {
    const card = document.createElement('div');
    card.className = 'surface-card';
    card.innerHTML = `<div class="section-label">${surface.name}</div><p>${surface.description}</p><ul>${surface.items.map(i => `<li>${i}</li>`).join('')}</ul>`;
    surfaceGrid.appendChild(card);
  });

  const portfolio = document.getElementById('portfolio');
  data.portfolio.forEach(group => {
    const card = document.createElement('div');
    card.className = 'category-card';
    card.innerHTML = `<div class="category-head"><div><div class="section-label">${group.category}</div><h3>${group.category[0].toUpperCase() + group.category.slice(1)}</h3></div></div><div class="category-list">${group.items.map(item => `<div class="mini-card"><h4>${item.name}</h4><div class="state">${item.state}</div><p>${item.focus}</p></div>`).join('')}</div>`;
    portfolio.appendChild(card);
  });

  const operators = document.getElementById('operators');
  data.operators.forEach(op => {
    const card = document.createElement('div');
    card.className = 'operator-card';
    card.innerHTML = `<div class="section-label">${op.role}</div><h3>${op.name}</h3><span class="status">${op.status}</span>`;
    operators.appendChild(card);
  });

  const nowList = document.getElementById('now-list');
  data.now.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    nowList.appendChild(li);
  });

  const buildStream = document.getElementById('build-stream');
  data.build_stream.forEach(item => {
    const row = document.createElement('div');
    row.className = 'stream-item';
    row.innerHTML = `<small>${item.time} · ${item.type}</small><strong>${item.title}</strong>`;
    buildStream.appendChild(row);
  });

  const panels = document.getElementById('panels');
  data.panels.forEach(panel => {
    const card = document.createElement('div');
    card.className = 'panel-card';
    card.innerHTML = `<h3>${panel.title}</h3><p>${panel.body}</p>`;
    panels.appendChild(card);
  });
}
boot();
