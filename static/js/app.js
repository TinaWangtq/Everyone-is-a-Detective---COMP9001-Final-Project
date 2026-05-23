/* =========================================================
   THE RAVENWOOD MANOR MYSTERY — Frontend Controller
   ========================================================= */

const CFG = window.GAME_CONFIG;
const stage = () => document.getElementById('stage');

// ---- Global state (lightweight; truth lives in the Python server) ----
let STATE = null;
let SELECTED_GENDER = 'Detective';
let ASSET_PRESENCE = { images: {}, audio: {} };
let ACCUSE_CULPRIT = null;
let ACCUSE_EVIDENCE = null;
let SOUND_ON = false;
let NOTEBOOK_FILTER = 'all';

// =========================================================
// API helper
// =========================================================
async function api(path, method = 'GET', body = null) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed: ${res.status}`);
  return data;
}

// =========================================================
// Asset presence check
// =========================================================
async function loadAssetPresence() {
  try {
    ASSET_PRESENCE = await api('/api/assets');
  } catch (_) { /* ignore */ }
}

// =========================================================
// AUDIO
// =========================================================
function setupAudio() {
  // Set src for each audio tag (file may not exist; <audio> handles that silently)
  const map = {
    'audio-ambient':   CFG.audioMap.ambient,
    'audio-click':     CFG.audioMap.click,
    'audio-page':      CFG.audioMap.page,
    'audio-discovery': CFG.audioMap.discovery,
    'audio-success':   CFG.audioMap.success,
    'audio-failure':   CFG.audioMap.failure,
  };
  for (const [id, file] of Object.entries(map)) {
    const el = document.getElementById(id);
    if (el && file) el.src = `${CFG.staticBase}audio/${file}`;
    if (el) el.addEventListener('error', e => e.preventDefault());
  }
}

function playSound(key) {
  if (!SOUND_ON) return;
  const ids = {
    click: 'audio-click', page: 'audio-page',
    discovery: 'audio-discovery',
    success: 'audio-success', failure: 'audio-failure',
  };
  const el = document.getElementById(ids[key]);
  if (!el || !el.src) return;
  try { el.currentTime = 0; el.play().catch(() => {}); } catch (e) {}
}

function toggleSound() {
  SOUND_ON = !SOUND_ON;
  const btn = document.getElementById('sound-toggle');
  btn.textContent = SOUND_ON ? '♫ Sound: On' : '♫ Sound: Off';
  btn.classList.toggle('active', SOUND_ON);
  const ambient = document.getElementById('audio-ambient');
  if (SOUND_ON) {
    ambient.volume = 0.35;
    ambient.play().catch(() => toast('Click to allow audio in your browser.'));
  } else {
    ambient.pause();
  }
}

// =========================================================
// BACKGROUND CONTROL
// =========================================================
function setBackground(sceneKey) {
  const file = CFG.imageMap[sceneKey];
  const layer = document.getElementById('bg-layer');
  if (!file) { layer.style.backgroundImage = ''; return; }
  const url = `${CFG.staticBase}images/${file}`;
  // Probe whether the image exists; if it does, set it
  const probe = new Image();
  probe.onload = () => { layer.style.backgroundImage = `url('${url}')`; };
  probe.onerror = () => { layer.style.backgroundImage = ''; };
  probe.src = url;
}

// =========================================================
// IMAGE PLATE with fallback
// =========================================================
function imagePlate(category, filename, label, portrait = false) {
  const folder = category;  // 'suspects' | 'items' | 'scenes'
  const url = `${CFG.staticBase}images/${folder}/${filename}`;
  const cls = portrait ? 'image-plate portrait' : 'image-plate';
  const fallbackLabel = (label || '').toUpperCase();
  // Try loading the image; show fallback if missing
  const id = 'plate_' + Math.random().toString(36).slice(2, 9);
  setTimeout(() => {
    const probe = new Image();
    probe.onload = () => {
      const el = document.getElementById(id);
      if (el) el.innerHTML = `<img src="${url}" alt="${escapeXML(label)}">`;
    };
    probe.src = url;
  }, 0);
  return `<div class="${cls}" id="${id}">
    <div class="image-fallback">
      ${escapeXML(fallbackLabel)}
      <small>— illustration not loaded —</small>
    </div>
  </div>`;
}

// =========================================================
// RENDERING
// =========================================================
function render(html) {
  stage().innerHTML = `<div class="panel">${html}</div>`;
}

function escapeXML(s) {
  return String(s).replace(/[<>&'"]/g, c =>
    ({ '<':'&lt;', '>':'&gt;', '&':'&amp;', "'":'&apos;', '"':'&quot;' }[c]));
}

function capitalize(s) {
  if (!s) return s;
  return s[0].toUpperCase() + s.slice(1);
}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 2400);
}

// =========================================================
// SCREEN: HOME
// =========================================================
function screenHome() {
  setBackground('manor');
  render(`
    <h1 class="title">Everyone is a Detective</h1>
    <div class="subtitle">— A Mystery in Three Acts —</div>
    <div class="divider">❦</div>

    <div class="prose" style="text-align:center;">
      <p class="lead">The case before you: <em>The Ravenwood Manor Mystery</em>.</p>
      <p>Before we begin, who shall be on the case?</p>
    </div>

    <div class="divider">✦ ENTER YOUR PARTICULARS ✦</div>

    <div class="field">
      <label for="name-input">Detective Name</label>
      <input type="text" id="name-input" maxlength="20"
             placeholder="Sherlock Holmes" autocomplete="off">
    </div>
    <div class="field">
      <label>Address</label>
      <div class="radio-group" id="gender-row"></div>
    </div>
    <div class="center-buttons">
      <button class="btn" id="begin-btn">Begin the Investigation</button>
    </div>
  `);

  // Build gender pills
  const row = document.getElementById('gender-row');
  CFG.genders.forEach(g => {
    const opt = document.createElement('div');
    opt.className = 'radio-opt' + (g === SELECTED_GENDER ? ' selected' : '');
    opt.dataset.g = g;
    opt.textContent = g;
    opt.addEventListener('click', () => {
      document.querySelectorAll('.radio-opt').forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      SELECTED_GENDER = g;
      playSound('click');
    });
    row.appendChild(opt);
  });

  document.getElementById('begin-btn').addEventListener('click', async () => {
    const name = document.getElementById('name-input').value.trim();
    if (!name) { toast('Please enter a name.'); return; }
    try {
      const data = await api('/api/start', 'POST',
                             { name, gender: SELECTED_GENDER });
      STATE = data.state;
      updateNotebook();
      playSound('page');
      screenPrologue(data.prologue);
    } catch (e) {
      toast(e.message);
    }
  });
}

// =========================================================
// SCREEN: PROLOGUE
// =========================================================
function screenPrologue(prologueData) {
  setBackground('manor');
  render(`
    <h2 class="section-title">Prologue</h2>
    ${imagePlate('scenes', CFG.imageMap.manor.replace('scenes/', ''), 'Ravenwood Manor')}
    <div class="prose" style="white-space:pre-wrap;">
      ${prologueData.prologue.map(p => p === '' ? '<p>&nbsp;</p>' : `<p>${escapeXML(p)}</p>`).join('')}
    </div>
    <div class="divider">❦</div>
    <div class="center-buttons">
      <button class="btn" id="continue-btn">Travel to Ravenwood Manor</button>
      <button class="btn back" id="quit-btn">Perhaps another day</button>
    </div>
  `);
  document.getElementById('continue-btn').addEventListener('click', () => {
    playSound('page');
    screenWatson(prologueData);
  });
  document.getElementById('quit-btn').addEventListener('click', async () => {
    await api('/api/reset', 'POST');
    screenHome();
  });
}

// =========================================================
// SCREEN: WATSON GREETING
// =========================================================
function screenWatson(prologueData) {
  setBackground('drawing');
  render(`
    <h2 class="section-title">Arrival at Ravenwood Manor</h2>
    ${imagePlate('scenes', CFG.imageMap.drawing.replace('scenes/', ''), 'The Drawing Room')}
    <div class="prose">
      ${prologueData.watson_intro.map(p => p === '' ? '<p>&nbsp;</p>' : `<p>${escapeXML(p)}</p>`).join('')}
    </div>
    <div class="divider">❦</div>
    <div class="center-buttons">
      <button class="btn" id="hub-btn">Begin the Investigation</button>
    </div>
  `);
  document.getElementById('hub-btn').addEventListener('click', () => {
    playSound('page');
    screenHub();
  });
}

// =========================================================
// SCREEN: HUB (action menu in icon-card row)
// =========================================================
async function screenHub() {
  setBackground('drawing');
  await refreshState();
  const name = STATE.player.name;

  render(`
    <h2 class="section-title">Detective ${escapeXML(name)}, what is your next move?</h2>

    <div class="hub-status">
      <div>Clues examined:<strong>${STATE.items_examined} / ${STATE.items_total}</strong></div>
      <div>Questions asked:<strong>${STATE.questions_asked} / ${STATE.questions_total}</strong></div>
    </div>

    <div class="hub-cards">
      <div class="hub-card" data-action="suspects">
        <span class="icon">⚖</span>
        <div class="label">Question Suspects</div>
        <span class="sub">Three witnesses await</span>
      </div>
      <div class="hub-card" data-action="scene">
        <span class="icon">🔍</span>
        <div class="label">Examine the Scene</div>
        <span class="sub">Inspect every detail</span>
      </div>
      <div class="hub-card" data-action="matrix">
        <span class="icon">▦</span>
        <div class="label">Deduction Board</div>
        <span class="sub">Survey your progress</span>
      </div>
      <div class="hub-card urgent" data-action="accuse">
        <span class="icon">⚜</span>
        <div class="label">Make Accusation</div>
        <span class="sub">When you are certain</span>
      </div>
    </div>
  `);

  document.querySelectorAll('.hub-card').forEach(c => {
    c.addEventListener('click', () => {
      playSound('click');
      const a = c.dataset.action;
      if (a === 'suspects') screenSuspectList();
      else if (a === 'scene') screenSceneList();
      else if (a === 'matrix') screenMatrix();
      else if (a === 'accuse') screenAccuseConfirm();
    });
  });
}

async function refreshState() {
  STATE = await api('/api/state');
  updateNotebook();
}

// =========================================================
// SCREEN: SUSPECT LIST
// =========================================================
function screenSuspectList() {
  setBackground('drawing');
  const buttons = STATE.suspects.map(s => {
    const asked = s.questions.filter(q => q.asked).length;
    return `<button class="btn" data-name="${escapeXML(s.name)}">
      ${escapeXML(s.name)}
      <span style="float:right; font-size:0.75rem; opacity:0.75; letter-spacing:0;">
        ${asked}/${s.questions.length} asked
      </span>
    </button>`;
  }).join('');

  render(`
    <h2 class="section-title">Whom Shall You Question?</h2>
    <div class="prose" style="text-align:center;">
      <p>The three guests await your interview in the drawing room.</p>
    </div>
    <div class="center-buttons">
      ${buttons}
      <button class="btn back" id="back-hub">Back to the Hall</button>
    </div>
  `);

  stage().querySelectorAll('button[data-name]').forEach(b => {
    b.addEventListener('click', () => {
      playSound('click');
      screenSuspect(b.dataset.name);
    });
  });
  document.getElementById('back-hub').addEventListener('click', () => {
    playSound('click');
    screenHub();
  });
}

// =========================================================
// SCREEN: SUSPECT DETAIL (two-column with portrait)
// =========================================================
function screenSuspect(name, lastAnswer = null, lastQuestion = null) {
  setBackground('drawing');
  const s = STATE.suspects.find(x => x.name === name);
  if (!s) return;

  const questionButtons = s.questions.map(q => {
    const cls = q.asked ? 'btn asked' : 'btn';
    return `<button class="${cls}" data-q="${escapeXML(q.text)}">
      ${escapeXML(q.text)}
    </button>`;
  }).join('');

  const dialogue = lastAnswer ? `
    <div class="dialogue">
      <span class="speaker">${escapeXML(name)}</span>
      ${escapeXML(lastAnswer)}
    </div>
    <div class="note-hint">This exchange has been recorded in your notebook.</div>
  ` : '';

  render(`
    <h2 class="section-title">${escapeXML(name)}</h2>
    <div class="two-col">
      <div>
        ${imagePlate('suspects', s.image, name, true)}
      </div>
      <div>
        <div class="prose"><p>${escapeXML(s.description)}</p></div>
        ${dialogue}
        <div class="divider">QUESTIONS</div>
        <div class="center-buttons">
          ${questionButtons}
        </div>
      </div>
    </div>
    <div class="divider">❦</div>
    <div class="button-row">
      <button class="btn back" id="back-list">Choose Another Suspect</button>
      <button class="btn back" id="back-hub">Back to the Hall</button>
    </div>
  `);

  stage().querySelectorAll('button[data-q]').forEach(b => {
    b.addEventListener('click', async () => {
      if (b.classList.contains('asked')) return;
      try {
        const data = await api('/api/question', 'POST', {
          suspect: name, question: b.dataset.q,
        });
        STATE = data.state;
        updateNotebook();
        playSound('click');
        // Re-render the same suspect with the answer revealed
        screenSuspect(name, data.answer, b.dataset.q);
      } catch (e) { toast(e.message); }
    });
  });
  document.getElementById('back-list').addEventListener('click', () => {
    playSound('click'); screenSuspectList();
  });
  document.getElementById('back-hub').addEventListener('click', () => {
    playSound('click'); screenHub();
  });
}

// =========================================================
// SCREEN: SCENE ITEM LIST
// =========================================================
function screenSceneList() {
  setBackground('study');
  const buttons = STATE.items.map(it => `
    <button class="btn ${it.examined ? 'asked' : ''}" data-item="${escapeXML(it.name)}">
      ${escapeXML(it.short)}
      ${it.examined ? '<span style="float:right; font-size:0.75rem;">(examined)</span>' : ''}
    </button>
  `).join('');

  render(`
    <h2 class="section-title">The Crime Scene</h2>
    <div class="prose" style="text-align:center;">
      <p>Examine each item carefully. Not every detail is significant —
      but every item has something to teach a careful eye.</p>
    </div>
    <div class="center-buttons">
      ${buttons}
      <button class="btn back" id="back-hub">Back to the Hall</button>
    </div>
  `);

  stage().querySelectorAll('button[data-item]').forEach(b => {
    if (b.classList.contains('asked')) {
      // Still allow re-examination
      b.classList.remove('asked');
      b.style.opacity = '0.7';
    }
    b.addEventListener('click', () => {
      playSound('click');
      examineItem(b.dataset.item);
    });
  });
  document.getElementById('back-hub').addEventListener('click', () => {
    playSound('click'); screenHub();
  });
}

async function examineItem(itemName) {
  try {
    const data = await api('/api/examine', 'POST', { item: itemName });
    STATE = data.state;
    updateNotebook();
    playSound('discovery');
    screenItemDetail(itemName, data.item);
  } catch (e) { toast(e.message); }
}

// =========================================================
// SCREEN: ITEM DETAIL (two-column with picture)
// =========================================================
function screenItemDetail(itemName, itemData) {
  setBackground('study');
  render(`
    <h2 class="section-title">${escapeXML(capitalize(itemName))}</h2>
    <div class="two-col">
      <div>
        ${imagePlate('items', itemData.image, itemName)}
      </div>
      <div>
        <div class="prose" style="white-space:pre-wrap;">
          ${itemData.description.split('\n\n').map(p => `<p>${escapeXML(p)}</p>`).join('')}
        </div>
        <div class="note-hint">A note has been added to your book.</div>
      </div>
    </div>
    <div class="divider">❦</div>
    <div class="button-row">
      <button class="btn back" id="back-scene">Examine Another Item</button>
      <button class="btn back" id="back-hub">Back to the Hall</button>
    </div>
  `);

  document.getElementById('back-scene').addEventListener('click', () => {
    playSound('click'); screenSceneList();
  });
  document.getElementById('back-hub').addEventListener('click', () => {
    playSound('click'); screenHub();
  });
}

// =========================================================
// SCREEN: DEDUCTION MATRIX
// =========================================================
function screenMatrix() {
  setBackground('drawing');
  const m = STATE.matrix;
  let html = `<table class="matrix-table"><thead><tr><th>Suspect</th>`;
  m.headers.forEach(h => html += `<th>${escapeXML(h)}</th>`);
  html += `</tr></thead><tbody>`;
  m.suspects.forEach((sName, rowIdx) => {
    html += `<tr><td class="label">${escapeXML(sName)}</td>`;
    m.rows[rowIdx].forEach(cell => {
      let cls = 'cell-dot', show = '·';
      if (cell === 'X') { cls = 'cell-x'; show = '✕'; }
      else if (cell === '~') { cls = 'cell-tilde'; show = '~'; }
      html += `<td class="${cls}">${show}</td>`;
    });
    html += `</tr>`;
  });
  html += `</tbody></table>`;

  render(`
    <h2 class="section-title">Deduction Board</h2>
    <div class="prose" style="text-align:center;">
      <p><strong>✕</strong> examined / fully questioned &nbsp; · &nbsp;
         <strong>~</strong> partially questioned &nbsp; · &nbsp;
         <strong>·</strong> untouched</p>
    </div>
    ${html}
    <div class="divider">❦</div>
    <div class="center-buttons">
      <button class="btn back" id="back-hub">Back to the Hall</button>
    </div>
  `);
  document.getElementById('back-hub').addEventListener('click', () => {
    playSound('click'); screenHub();
  });
}

// =========================================================
// SCREEN: ACCUSATION CONFIRM
// =========================================================
function screenAccuseConfirm() {
  setBackground('study');
  render(`
    <h2 class="section-title">A Solemn Moment</h2>
    <div class="prose" style="text-align:center;">
      <p class="lead">Are you certain you are ready to name the killer?</p>
      <p style="font-style:italic; color:var(--blood);">
        You have only one accusation. There is no going back.
      </p>
    </div>
    <div class="divider">❦</div>
    <div class="center-buttons">
      <button class="btn danger" id="confirm-yes">Yes — I am ready to accuse</button>
      <button class="btn back" id="confirm-no">No — keep investigating</button>
    </div>
  `);
  document.getElementById('confirm-yes').addEventListener('click', () => {
    playSound('click'); screenAccuse();
  });
  document.getElementById('confirm-no').addEventListener('click', () => {
    playSound('click'); screenHub();
  });
}

// =========================================================
// SCREEN: ACCUSATION
// =========================================================
function screenAccuse() {
  setBackground('study');
  ACCUSE_CULPRIT = null;
  ACCUSE_EVIDENCE = null;

  render(`
    <h2 class="section-title">The Final Accusation</h2>

    <div class="divider">PART I — THE CULPRIT</div>
    <div class="prose" style="text-align:center;">
      <p>Detective ${escapeXML(STATE.player.name)}, name the killer.</p>
    </div>
    <div class="accuse-grid" id="culprit-grid"></div>

    <div class="divider">PART II — THE EVIDENCE</div>
    <div class="prose" style="text-align:center;">
      <p>What single piece of evidence conclusively convicts them?</p>
    </div>
    <div class="accuse-grid" id="evidence-grid"></div>

    <div class="divider">❦</div>
    <div class="button-row">
      <button class="btn back" id="back-hub">Reconsider</button>
      <button class="btn danger" id="submit-accusation" disabled>J'accuse!</button>
    </div>
  `);

  // Build culprit cards
  const cg = document.getElementById('culprit-grid');
  STATE.suspects.forEach(s => {
    const card = document.createElement('div');
    card.className = 'accuse-card';
    card.textContent = s.name;
    card.addEventListener('click', () => {
      ACCUSE_CULPRIT = s.name;
      cg.querySelectorAll('.accuse-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      updateSubmit();
      playSound('click');
    });
    cg.appendChild(card);
  });

  // Build evidence cards (dim those not examined yet)
  const eg = document.getElementById('evidence-grid');
  STATE.items.forEach(it => {
    const card = document.createElement('div');
    card.className = 'accuse-card' + (it.examined ? '' : ' dim');
    card.textContent = capitalize(it.name);
    if (!it.examined) card.title = "You haven't examined this yet.";
    card.addEventListener('click', () => {
      ACCUSE_EVIDENCE = it.name;
      eg.querySelectorAll('.accuse-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      updateSubmit();
      playSound('click');
    });
    eg.appendChild(card);
  });

  document.getElementById('back-hub').addEventListener('click', () => {
    playSound('click'); screenHub();
  });
  document.getElementById('submit-accusation').addEventListener('click', submitAccusation);
}

function updateSubmit() {
  document.getElementById('submit-accusation').disabled =
    !(ACCUSE_CULPRIT && ACCUSE_EVIDENCE);
}

async function submitAccusation() {
  try {
    const data = await api('/api/accuse', 'POST', {
      culprit: ACCUSE_CULPRIT,
      evidence: ACCUSE_EVIDENCE,
    });
    STATE = data.state;
    updateNotebook();
    screenEnding();
  } catch (e) { toast(e.message); }
}

// =========================================================
// SCREEN: ENDING
// =========================================================
function screenEnding() {
  const win = STATE.result === 'win';
  setBackground(win ? 'drawing' : 'manor');
  playSound(win ? 'success' : 'failure');

  const textHTML = STATE.ending_text.map(line =>
    line === '' ? '<p>&nbsp;</p>' : `<p>${escapeXML(line)}</p>`
  ).join('');

  render(`
    <div class="ending ${win ? 'win' : 'lose'}">
      <div class="verdict">${win ? '✦ Case Solved ✦' : '✕ Case Failed ✕'}</div>
      <div class="prose">${textHTML}</div>
      <div class="divider">❦</div>
      <div class="button-row">
        <button class="btn" id="play-again">Take Another Case</button>
        <button class="btn back" id="download-final">Download Notebook</button>
      </div>
    </div>
  `);

  document.getElementById('play-again').addEventListener('click', async () => {
    await api('/api/reset', 'POST');
    location.reload();
  });
  document.getElementById('download-final').addEventListener('click', downloadNotebook);
}

// =========================================================
// NOTEBOOK PANEL
// =========================================================
const nbPanel    = document.getElementById('notebook-panel');
const nbBackdrop = document.getElementById('notebook-backdrop');
const nbToggle   = document.getElementById('notebook-toggle');
const nbClose    = document.getElementById('notebook-close');
const nbBadge    = document.getElementById('notebook-badge');
const nbBody     = document.getElementById('notebook-body');

function toggleNotebook(forceOpen) {
  const willOpen = forceOpen !== undefined ? forceOpen : !nbPanel.classList.contains('open');
  nbPanel.classList.toggle('open', willOpen);
  nbBackdrop.classList.toggle('show', willOpen);
  if (willOpen) playSound('page');
}

nbToggle.addEventListener('click', () => toggleNotebook());
nbClose.addEventListener('click', () => toggleNotebook(false));
nbBackdrop.addEventListener('click', () => toggleNotebook(false));

document.querySelectorAll('.notebook-tab').forEach(t => {
  t.addEventListener('click', () => {
    document.querySelectorAll('.notebook-tab').forEach(x => x.classList.remove('active'));
    t.classList.add('active');
    NOTEBOOK_FILTER = t.dataset.tab;
    renderNotebookBody();
  });
});

document.getElementById('thought-add').addEventListener('click', async () => {
  const ta = document.getElementById('thought-input');
  const text = ta.value.trim();
  if (!text) { toast('Write something first.'); return; }
  try {
    const data = await api('/api/thought', 'POST', { text });
    STATE = data.state;
    ta.value = '';
    updateNotebook();
    playSound('click');
    toast('Thought recorded.');
  } catch (e) {
    if (e.message.includes('No active game')) {
      toast('Begin a case first, detective.');
    } else { toast(e.message); }
  }
});

document.getElementById('notebook-download').addEventListener('click', downloadNotebook);

function updateNotebook() {
  if (!STATE) {
    nbBadge.classList.add('hidden');
    return;
  }
  const entries = STATE.notebook_entries || [];
  if (entries.length > 0) {
    nbBadge.textContent = entries.length;
    nbBadge.classList.remove('hidden');
  } else {
    nbBadge.classList.add('hidden');
  }
  // Update title
  const t = document.getElementById('notebook-title');
  if (STATE.player && STATE.player.name) {
    t.textContent = `${STATE.player.name}'s Notebook`;
  }
  renderNotebookBody();
}

function renderNotebookBody() {
  if (!STATE) { return; }
  let entries = STATE.notebook_entries || [];
  if (NOTEBOOK_FILTER !== 'all') {
    entries = entries.filter(e => e.category.startsWith(NOTEBOOK_FILTER));
  }
  if (entries.length === 0) {
    nbBody.innerHTML = '<div class="empty-notes">No entries here yet.</div>';
    return;
  }
  nbBody.innerHTML = entries.map(e => {
    const cls = e.category === 'THOUGHT' ? 'note-entry thought' : 'note-entry';
    return `<div class="${cls}">
      <span class="cat">${escapeXML(e.category)}</span>
      <span class="ts">· ${escapeXML(e.time)}</span>
      <span class="text">${escapeXML(e.text)}</span>
    </div>`;
  }).join('');
  nbBody.scrollTop = nbBody.scrollHeight;
}

async function downloadNotebook() {
  try {
    const data = await api('/api/notebook_file');
    const blob = new Blob([data.contents], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const name = (STATE && STATE.player) ? STATE.player.name.replace(/\s+/g, '_') : 'detective';
    a.download = `notebook_${name}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast('Notebook downloaded.');
  } catch (e) { toast(e.message); }
}

// =========================================================
// SOUND TOGGLE
// =========================================================
document.getElementById('sound-toggle').addEventListener('click', toggleSound);

// =========================================================
// KEYBOARD
// =========================================================
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') toggleNotebook(false);
});

// =========================================================
// BOOT
// =========================================================
(async function init() {
  await loadAssetPresence();
  setupAudio();
  screenHome();
})();
