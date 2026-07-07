# -*- coding: utf-8 -*-
"""Patch NEXUS COMMAND app.html — v9.1 upgrade."""
import io, sys

PATH = '/sessions/kind-dazzling-darwin/mnt/outputs/app.html'
src = io.open(PATH, encoding='utf-8').read()
count_applied = 0

def rep(old, new, n=1):
    global src, count_applied
    c = src.count(old)
    assert c == n, 'ANCHOR x%d (expected %d): %r' % (c, n, old[:90])
    src = src.replace(old, new)
    count_applied += 1

# ============ A. NAV TAB ============
rep("""    <button class="nav-tab" onclick="showPanel('p-league', this)">◉ LEAGUE</button>""",
"""    <button class="nav-tab" onclick="showPanel('p-league', this)">◉ LEAGUE</button>
    <button class="nav-tab" onclick="showPanel('p-history', this); renderHistory()">🏛 HISTORY</button>""")

# ============ B. MARKET ROLE FILTER ============
rep("""                  <option value="awper">Awper (AWP)</option>
                  <option value="igl">IGL</option>
                  <option value="anchor">Anchor (ANC)</option>
                  <option value="entry fragger">Entry Fragger (EF)</option>
                  <option value="closer/star player">Closer/Star Player (ST)</option>
                  <option value="dynamic">Dynamic — Support/Rotator/Rifler/Trader (DY)</option>""",
"""                  <option value="igl">IGL</option>
                  <option value="star player">Star Player</option>
                  <option value="entry fragger">Entry Fragger</option>
                  <option value="awper">AWPer</option>
                  <option value="anchor">Anchor</option>
                  <option value="dynamic">Dynamic</option>""")

# ============ C. SEM TIME ============
rep("""<option value="none">🚫 Sem Time</option>""",
    """<option value="none">🚫 No Team</option>""")

# ============ D. ROLE CATALOG + MIGRATION ============
rep("""const ROLE_OPTIONS = [
  { value:'awper',              label:'Awper (AWP)' },
  { value:'igl',                label:'IGL' },
  { value:'anchor',             label:'Anchor (ANC)' },
  { value:'entry fragger',      label:'Entry Fragger (EF)' },
  { value:'closer/star player', label:'Closer/Star Player (ST)' },
  { value:'dynamic',            label:'Dynamic — Support/Rotator/Rifler/Trader (DY)' },
];""",
"""const ROLE_OPTIONS = [
  { value:'igl',           label:'IGL' },
  { value:'star player',   label:'Star Player' },
  { value:'entry fragger', label:'Entry Fragger' },
  { value:'awper',         label:'AWPer' },
  { value:'anchor',        label:'Anchor' },
  { value:'dynamic',       label:'Dynamic' },
];""")

rep("""const ROLE_MIGRATION = {
  'support': 'dynamic',
  'lurker': 'dynamic',
  'rifler': 'dynamic',
  'rotator': 'dynamic',
  'trader': 'dynamic',
  'star player': 'closer/star player',
  'closer': 'closer/star player',
};""",
"""const ROLE_MIGRATION = {
  'support': 'dynamic',
  'lurker': 'dynamic',
  'rifler': 'dynamic',
  'rotator': 'dynamic',
  'trader': 'dynamic',
  'closer': 'star player',
  'star rifle': 'star player',
  'star rifler': 'star player',
  'closer/star player': 'star player',
};""")

# ============ E. OFFICE PANEL HTML (rebuild) ============
start = src.index('    <div class="panel" id="p-office">')
end = src.index('    <!-- ═══ MARKET PANEL ═══ -->')
new_office = """    <div class="panel" id="p-office">
      <div id="fo-pipeline" class="fo-pipeline"></div>
      <div class="card orange" id="fo-inbox-card">
        <div class="card-title" style="justify-content:space-between;">
          <span>📥 INCOMING OFFERS — TALKS ON MY PLAYERS</span>
          <span id="fo-inbox-count" class="badge badge-orange">0</span>
        </div>
        <div id="fo-inbox" class="fo-inbox-row"></div>
      </div>
      <div class="fo-grid">
        <div style="display:flex; flex-direction:column; gap:12px; min-height:0;">
          <div class="card" style="display:flex; flex-direction:column; min-height:0; flex:1;">
            <div class="card-title">🛡 LOCKER ROOM — CONTRACT CONTROL</div>
            <input type="text" class="nx-input" id="fo-squad-search" placeholder="🔍 Filter squad..." oninput="renderOffice()" style="margin-bottom:8px; padding:6px 10px; font-size:11px;">
            <div id="fo-squad" class="scroll-list" style="flex:1; max-height:none;"></div>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:12px; min-height:0;">
          <div class="card" style="display:flex; flex-direction:column; min-height:0; flex:1;">
            <div class="card-title">🗣 NEGOTIATION DESK</div>
            <div id="fo-desk" class="scroll-list" style="flex:1; max-height:none;"></div>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:12px; min-height:0;">
          <div class="card purple" style="border-color:rgba(177,140,240,0.25);">
            <div class="card-title" style="color:var(--purple);">🎮 USER-CONTROLLED PLAYERS</div>
            <input type="text" class="nx-input" id="fo-managed-search" placeholder="🔍 Search any player to toggle..." oninput="renderFoManaged()" style="margin-bottom:8px; padding:6px 10px; font-size:11px;">
            <div id="fo-managed" class="scroll-list" style="max-height:200px;"></div>
          </div>
          <div class="card">
            <div class="card-title">ℹ HOW DEALS WORK</div>
            <div style="font-family:var(--font-data); font-size:10px; color:var(--text-dim); line-height:1.8;">
              🏷 <b>On Sale</b> / ⚡ <b>Buyout</b> — instant purchase at the listed price.<br>
              🔑 <b>Release clause</b> — paid once to unlock fee talks (non-refundable).<br>
              📬 <b>Open to Offers</b> — clubs bid a fee directly, no clause needed.<br>
              📜 Deal history now lives in the <b>🏛 HISTORY</b> tab.
            </div>
          </div>
        </div>
      </div>
    </div>

"""
src = src[:start] + new_office + src[end:]
count_applied += 1

# ============ F. HISTORY PANEL HTML ============
hist_panel = """    <!-- ═══ HISTORY PANEL ═══ -->
    <div class="panel" id="p-history">
      <div class="g2">
        <div style="display:flex; flex-direction:column; gap:16px;">
          <div class="card yellow">
            <div class="card-title">🏆 RECORD TEAM ACHIEVEMENT</div>
            <div style="font-family:var(--font-data); font-size:10px; color:var(--text-dim); margin-bottom:10px;">Record-only — no money is moved. The event is written to the team's history AND to every player on the active roster (starters only, bench excluded).</div>
            <div class="g2" style="gap:10px; margin-bottom:8px;">
              <div class="form-group"><div class="form-label">TEAM</div><select class="nx-select" id="hist-ev-team"></select></div>
              <div class="form-group"><div class="form-label">EVENT NAME</div><input type="text" class="nx-input" id="hist-ev-name" placeholder="e.g. Blast Premier Fall"></div>
            </div>
            <div class="g3" style="gap:10px; margin-bottom:8px;">
              <div class="form-group"><div class="form-label">TIER</div>
                <select class="nx-select" id="hist-ev-tier" onchange="histTierChanged('ev')">
                  <option value="5">⭐⭐⭐⭐⭐ SS+ — MAJOR (Global)</option>
                  <option value="4">⭐⭐⭐⭐ S</option>
                  <option value="3">⭐⭐⭐ A</option>
                  <option value="2">⭐⭐ B</option>
                  <option value="1">⭐ C</option>
                </select>
              </div>
              <div class="form-group"><div class="form-label">SCOPE</div>
                <select class="nx-select" id="hist-ev-scope" disabled>
                  <option value="Global">🌍 Global</option>
                  <option value="State">🏳 State</option>
                </select>
              </div>
              <div class="form-group"><div class="form-label">POSITION</div>
                <select class="nx-select" id="hist-ev-pos">
                  <option value="Winner">🥇 Winner</option>
                  <option value="Second">🥈 Second</option>
                  <option value="Third">🥉 Third</option>
                </select>
              </div>
            </div>
            <div class="g2" style="gap:10px; margin-bottom:10px;">
              <div class="form-group"><div class="form-label">EVENT PRIZE POOL ($)</div><input type="number" class="nx-input" id="hist-ev-pool" placeholder="0.00"></div>
              <div class="form-group"><div class="form-label">TEAM WINNINGS ($)</div><input type="number" class="nx-input" id="hist-ev-won" placeholder="0.00"></div>
            </div>
            <button class="btn btn-yellow btn-full" onclick="applyTeamAchievement()">🏆 ADD TO HISTORY (TEAM + STARTERS)</button>
          </div>

          <div class="card">
            <div class="card-title">🥇 RECORD PLAYER AWARD — MVP / EVP / VP</div>
            <div style="font-family:var(--font-data); font-size:10px; color:var(--text-dim); margin-bottom:10px;">Record-only — medals &amp; money are still granted in ⚙ OPS. This writes the award to the player's personal history.</div>
            <div class="g2" style="gap:10px; margin-bottom:8px;">
              <div class="form-group"><div class="form-label">PLAYER</div><input type="text" class="nx-input" id="hist-aw-player" list="hist-player-list" placeholder="Type player name..."><datalist id="hist-player-list"></datalist></div>
              <div class="form-group"><div class="form-label">AWARD</div>
                <select class="nx-select" id="hist-aw-kind">
                  <option value="MVP">🥇 MVP</option>
                  <option value="EVP">🥈 EVP</option>
                  <option value="VP">🥉 VP</option>
                </select>
              </div>
            </div>
            <div class="g3" style="gap:10px; margin-bottom:8px;">
              <div class="form-group"><div class="form-label">TIER</div>
                <select class="nx-select" id="hist-aw-tier" onchange="histTierChanged('aw')">
                  <option value="5">⭐⭐⭐⭐⭐ SS+ — MAJOR (Global)</option>
                  <option value="4">⭐⭐⭐⭐ S</option>
                  <option value="3">⭐⭐⭐ A</option>
                  <option value="2">⭐⭐ B</option>
                  <option value="1">⭐ C</option>
                </select>
              </div>
              <div class="form-group"><div class="form-label">SCOPE</div>
                <select class="nx-select" id="hist-aw-scope" disabled>
                  <option value="Global">🌍 Global</option>
                  <option value="State">🏳 State</option>
                </select>
              </div>
              <div class="form-group"><div class="form-label">POSITION</div>
                <select class="nx-select" id="hist-aw-pos">
                  <option value="Winner">🥇 Winner</option>
                  <option value="Second">🥈 Second</option>
                  <option value="Third">🥉 Third</option>
                </select>
              </div>
            </div>
            <div class="form-group" style="margin-bottom:10px;"><div class="form-label">EVENT NAME</div><input type="text" class="nx-input" id="hist-aw-event" placeholder="e.g. IEM Cologne"></div>
            <button class="btn btn-cyan btn-full" onclick="applyPlayerAward()">🥇 ADD AWARD TO PLAYER HISTORY</button>
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:16px;">
          <div class="card">
            <div class="card-title" style="justify-content:space-between;">
              <span>🏛 TEAM HISTORY</span>
              <select class="nx-select" id="hist-view-team" onchange="renderHistory()" style="max-width:220px; padding:4px 8px; font-size:11px;"></select>
            </div>
            <div class="pm-section-title" style="margin-top:0;">🏆 ACHIEVEMENTS</div>
            <div id="hist-team-events" class="scroll-list" style="max-height:220px; margin-bottom:10px;"></div>
            <div class="pm-section-title">🥇 PLAYER AWARDS (CURRENT ROSTER)</div>
            <div id="hist-team-awards" class="scroll-list" style="max-height:160px; margin-bottom:10px;"></div>
            <div class="pm-section-title">📜 DEAL HISTORY</div>
            <div id="hist-team-deals" class="scroll-list" style="max-height:180px;"></div>
          </div>
          <div class="card purple">
            <div class="card-title" style="justify-content:space-between;">
              <span>🔄 TRANSACTIONS — ALL PLAYER MOVEMENTS</span>
              <input type="text" class="nx-input" id="hist-tx-search" placeholder="🔍 Filter player / team..." oninput="renderTransactions()" style="max-width:200px; padding:4px 8px; font-size:11px;">
            </div>
            <div id="hist-transactions" class="scroll-list" style="max-height:320px;"></div>
          </div>
        </div>
      </div>
    </div>

"""
rep('    <!-- ═══ OPS PANEL ═══ -->', hist_panel + '    <!-- ═══ OPS PANEL ═══ -->')

# ============ G. normalizePlayers: OpenToOffers ============
rep("""    row.OnSale = Number(row.OnSale) || 0;""",
"""    row.OnSale = Number(row.OnSale) || 0;
    row.OpenToOffers = Number(row.OpenToOffers) || 0;""")

# ============ H. globals ============
rep("""let transferHistory = [], negotiations = [], clauseTalks = [];""",
"""let transferHistory = [], negotiations = [], clauseTalks = [];
let teamHistory = [], playerHistory = [], transactions = [];""")

# ============ I. saveState / undo ============
rep("""  history.push({f:JSON.parse(JSON.stringify(finances)), p:JSON.parse(JSON.stringify(players)), ng:JSON.parse(JSON.stringify(negotiations)), ct:JSON.parse(JSON.stringify(clauseTalks)), th:JSON.parse(JSON.stringify(transferHistory)), mc:monthCounter});""",
"""  history.push({f:JSON.parse(JSON.stringify(finances)), p:JSON.parse(JSON.stringify(players)), ng:JSON.parse(JSON.stringify(negotiations)), ct:JSON.parse(JSON.stringify(clauseTalks)), th:JSON.parse(JSON.stringify(transferHistory)), thist:JSON.parse(JSON.stringify(teamHistory)), phist:JSON.parse(JSON.stringify(playerHistory)), tx:JSON.parse(JSON.stringify(transactions)), mc:monthCounter});""")

rep("""  const s=history.pop(); finances=s.f; players=s.p; negotiations=s.ng||[]; clauseTalks=s.ct||[]; transferHistory=s.th||[]; monthCounter=s.mc||monthCounter;""",
"""  const s=history.pop(); finances=s.f; players=s.p; negotiations=s.ng||[]; clauseTalks=s.ct||[]; transferHistory=s.th||[]; teamHistory=s.thist||[]; playerHistory=s.phist||[]; transactions=s.tx||[]; monthCounter=s.mc||monthCounter;""")

# ============ J. roster helpers ============
rep("""function canAddBench(team) {
  return players.filter(p => p.TeamName===team && p.Roster==='Bench').length < 3;
}""",
"""function canAddBench(team) {
  return players.filter(p => p.TeamName===team && p.Roster==='Bench').length < 3;
}

/* Roster capacity: teams fill the 5 starter slots FIRST; the bench (max 3) only
   starts being used once the active roster is complete. */
function starterCount(team){ return players.filter(p => p.TeamName===team && p.Roster==='Starter').length; }
function benchCount(team){ return players.filter(p => p.TeamName===team && p.Roster==='Bench').length; }
function canAcquire(team){ return starterCount(team) < 5 || benchCount(team) < 3; }
function placementFor(team){ return starterCount(team) < 5 ? 'Starter' : 'Bench'; }
function teamLabel(t){ return t==='none' ? 'No Team' : t; }

/* Global player-movement ledger (shown in 🏛 HISTORY → TRANSACTIONS) */
function addTransaction(type, playerName, from, to, amount, note){
  transactions.unshift({id:Date.now()+Math.floor(Math.random()*999), month:monthCounter, type, playerName, from:from||'—', to:to||'—', amount:amount||0, note:note||''});
  if (transactions.length>400) transactions.length=400;
}""")

# ============ K. executeTransfer ============
rep("""function executeTransfer(playerName, buyerName, fee, label){
  const p=players.find(x=>String(x.PlayerName)===playerName);
  const buyer=finances.find(t=>t.TeamName===buyerName);
  const seller=finances.find(t=>t.TeamName===p.TeamName);
  buyer.CurrentBank-=fee; if (seller) seller.CurrentBank+=fee;
  transferHistory.unshift({id:Date.now(), buyer:buyerName, seller:p.TeamName, playerName, amount:fee, status:'✅ '+label});
  voidPlayerBusiness(playerName); // poached — any parallel talks die
  p.TeamName=buyerName; p.Roster='Bench';
  p.Salary=0; p.ContractMonths=0; p.Buyout=0; p.ReleaseClause=0; p.OnSale=0;
  addLog(`✅ TRANSFER [${label}]: ${playerName} → ${buyerName} for ${fmt(fee)}.`,'good');
}""",
"""function executeTransfer(playerName, buyerName, fee, label){
  const p=players.find(x=>String(x.PlayerName)===playerName);
  const buyer=finances.find(t=>t.TeamName===buyerName);
  const fromTeam=p.TeamName;
  const seller=finances.find(t=>t.TeamName===fromTeam);
  buyer.CurrentBank-=fee; if (seller) seller.CurrentBank+=fee;
  transferHistory.unshift({id:Date.now(), buyer:buyerName, seller:fromTeam, playerName, amount:fee, status:'✅ '+label});
  voidPlayerBusiness(playerName); // poached — any parallel talks die
  const slot=placementFor(buyerName); // auto-starter until the 5-man roster is full, then bench
  p.TeamName=buyerName; p.Roster=slot;
  p.Salary=0; p.ContractMonths=0; p.Buyout=0; p.ReleaseClause=0; p.OnSale=0; p.OpenToOffers=0;
  addTransaction('TRANSFER', playerName, fromTeam, buyerName, fee, label+' · joined as '+slot);
  addLog(`✅ TRANSFER [${label}]: ${playerName} → ${buyerName} for ${fmt(fee)} — placed as ${slot.toUpperCase()}.`,'good');
}""")

# ============ L. capacity checks ============
rep("""  if (!canAddBench(buyerName)) return alert('Bench full (max 3).');""",
    """  if (!canAcquire(buyerName)) return alert('Squad full — 5 starters and 3 bench players already.');""")

rep("""  if (!canAddBench(t.buyer)) return alert(`${t.buyer}'s bench is full (max 3).`);""",
    """  if (!canAcquire(t.buyer)) return alert(`${t.buyer}'s squad is full (5 starters + 3 bench).`);""")

rep("""  if (type==='signing' && origin==='fa' && !canAddBench(teamName)) return alert('Bench full (max 3).');""",
    """  if (type==='signing' && origin==='fa' && !canAcquire(teamName)) return alert('Squad full — 5 starters and 3 bench players already.');""")

rep("""  if (neg.type==='signing' && neg.origin==='fa'){
    if (!canAddBench(neg.team)){ neg.status='closed'; return alert('Bench filled up during talks — signing collapsed.'); }
    p.TeamName=neg.team; p.Roster='Bench';
    transferHistory.unshift({id:Date.now(), buyer:neg.team, seller:'FREE AGENCY', playerName:neg.playerName, amount:0, status:'✅ FA SIGNING'});
  }""",
"""  if (neg.type==='signing' && neg.origin==='fa'){
    if (!canAcquire(neg.team)){ neg.status='closed'; return alert('Squad filled up during talks — signing collapsed.'); }
    const slot=placementFor(neg.team); // auto-starter until roster is full
    p.TeamName=neg.team; p.Roster=slot;
    transferHistory.unshift({id:Date.now(), buyer:neg.team, seller:'FREE AGENCY', playerName:neg.playerName, amount:0, status:'✅ FA SIGNING'});
    addTransaction('FA SIGNING', neg.playerName, 'Free Agency', neg.team, 0, 'joined as '+slot);
  }""")

# ============ M. payReleaseClause: never double-charge ============
rep("""  if (clauseTalks.some(t=>t.status==='open'&&t.buyer===buyerName&&t.playerName===name)) return alert('You already have an open clause talk for this player.');""",
"""  if (clauseTalks.some(t=>t.status==='open'&&t.buyer===buyerName&&t.playerName===name)){ gotoOffice(); return; } // clause already paid — NEVER charge twice, just reopen the talk""")

rep("""  clauseTalks.unshift({id:Date.now()+Math.floor(Math.random()*999), buyer:buyerName, seller:p.TeamName, playerName:name, clausePaid:clause, thread:[], pending:'buyer', status:'open'});
  addLog(`🔑 ${buyerName} paid the ${fmt(clause)} release clause of ${name} (${p.TeamName}). Fee talks unlocked.`,'good');""",
"""  clauseTalks.unshift({id:Date.now()+Math.floor(Math.random()*999), kind:'clause', buyer:buyerName, seller:p.TeamName, playerName:name, clausePaid:clause, thread:[], pending:'buyer', status:'open'});
  addTransaction('CLAUSE PAID', name, buyerName, p.TeamName, clause, 'release clause paid — fee talks unlocked');
  addLog(`🔑 ${buyerName} paid the ${fmt(clause)} release clause of ${name} (${p.TeamName}). Fee talks unlocked.`,'good');""")

# ============ N. ctReject kind-aware ============
rep("""  if (!confirm(`End clause talks for ${t.playerName}?\\n⚠ The ${fmt(t.clausePaid)} clause payment is NOT refunded.`)) return;
  saveState(); t.status='closed';
  transferHistory.unshift({id:Date.now(), buyer:t.buyer, seller:t.seller, playerName:t.playerName, amount:t.clausePaid, status:'❌ CLAUSE TALKS COLLAPSED'});
  addLog(`❌ Clause talks over ${t.playerName} collapsed. ${t.buyer} loses the ${fmt(t.clausePaid)} clause fee.`,'bad');""",
"""  if (!confirm(t.kind==='offer' ? `End transfer talks for ${t.playerName}? (nothing was paid)` : `End clause talks for ${t.playerName}?\\n⚠ The ${fmt(t.clausePaid)} clause payment is NOT refunded.`)) return;
  saveState(); t.status='closed';
  transferHistory.unshift({id:Date.now(), buyer:t.buyer, seller:t.seller, playerName:t.playerName, amount:t.clausePaid, status:t.kind==='offer'?'❌ OFFER TALKS ENDED':'❌ CLAUSE TALKS COLLAPSED'});
  addLog(t.kind==='offer' ? `❌ Transfer talks over ${t.playerName} ended.` : `❌ Clause talks over ${t.playerName} collapsed. ${t.buyer} loses the ${fmt(t.clausePaid)} clause fee.`,'bad');""")

# ============ O. renderTalkCard (kind-aware + base cost) ============
rep("""function renderTalkCard(t, mySide){
  const last=t.thread.length?t.thread[t.thread.length-1]:null;
  const myTurn=t.pending===mySide;
  const bubbles=t.thread.map(m=>`<div class="ng-msg ${m.by==='buyer'?'team':'player'}">${m.by==='buyer'?t.buyer:t.seller}: <b>${fmt(m.amount)}</b></div>`).join('');
  let controls='';
  if (myTurn){
    controls=`
      ${last&&last.by!==mySide?`<button class="btn btn-green btn-sm btn-full" style="margin-bottom:6px;" onclick="ctAccept('${t.id}')">✅ ACCEPT ${fmt(last.amount)}</button>`:''}
      <div class="ng-form ng-form-2">
        <div class="ng-field"><label>${last?'COUNTER FEE':'OPENING FEE'}</label><input type="number" class="nx-input" id="ct-amt-${t.id}" value="${last?last.amount:''}" placeholder="transfer fee"></div>
        <button class="btn btn-cyan btn-sm" style="align-self:end;" onclick="ctSend('${t.id}')">📨 SEND</button>
      </div>
      <button class="btn btn-red btn-sm btn-full" style="margin-top:6px;" onclick="ctReject('${t.id}')">❌ ${mySide==='buyer'?'WALK AWAY (fee lost)':'REFUSE TO SELL (their fee kept)'}</button>`;
  } else {
    controls=`<div class="fo-empty">Awaiting ${t.pending==='buyer'?t.buyer:t.seller}…</div>`;
  }
  return `<div class="ng-card ng-card-clause">
    <div class="ng-head">
      <div><span class="badge badge-orange">🔑 CLAUSE TALK</span> <b>${t.playerName}</b></div>
      <div class="ng-band">${t.buyer} ↔ ${t.seller} · clause paid: ${fmtK(t.clausePaid)}</div>
    </div>
    <div class="ng-thread">${bubbles||'<div class="fo-empty">Clause paid — buyer opens with a fee.</div>'}</div>
    ${controls}
  </div>`;
}""",
"""function renderTalkCard(t, mySide){
  const p=players.find(x=>String(x.PlayerName)===t.playerName);
  const mv=p?(p.MarketValue||0):0; // base cost reference for the fee negotiation
  const isOffer=t.kind==='offer';
  const last=t.thread.length?t.thread[t.thread.length-1]:null;
  const myTurn=t.pending===mySide;
  const bubbles=t.thread.map(m=>`<div class="ng-msg ${m.by==='buyer'?'team':'player'}">${m.by==='buyer'?t.buyer:t.seller}: <b>${fmt(m.amount)}</b></div>`).join('');
  let controls='';
  if (myTurn){
    controls=`
      ${last&&last.by!==mySide?`<button class="btn btn-green btn-sm btn-full" style="margin-bottom:6px;" onclick="ctAccept('${t.id}')">✅ ACCEPT ${fmt(last.amount)}</button>`:''}
      <div class="ng-form ng-form-2">
        <div class="ng-field"><label>${last?'COUNTER FEE':'OPENING FEE'} · BASE ${fmtK(mv)}</label><input type="number" class="nx-input" id="ct-amt-${t.id}" value="${last?last.amount:Math.round(mv)}" placeholder="transfer fee"></div>
        <button class="btn btn-cyan btn-sm" style="align-self:end;" onclick="ctSend('${t.id}')">📨 SEND</button>
      </div>
      <button class="btn btn-red btn-sm btn-full" style="margin-top:6px;" onclick="ctReject('${t.id}')">❌ ${mySide==='buyer'?(isOffer?'WITHDRAW OFFER':'WALK AWAY (fee lost)'):(isOffer?'REFUSE TO SELL':'REFUSE TO SELL (their fee kept)')}</button>`;
  } else {
    controls=`<div class="fo-empty">Awaiting ${t.pending==='buyer'?t.buyer:t.seller}…</div>`;
  }
  return `<div class="ng-card ${isOffer?'ng-card-offer':'ng-card-clause'}">
    <div class="ng-head">
      <div>${isOffer?'<span class="badge badge-purple">📨 TRANSFER OFFER</span>':'<span class="badge badge-orange">🔑 CLAUSE TALK</span>'} <b>${t.playerName}</b></div>
      <div class="ng-band">${t.buyer} ↔ ${t.seller} · BASE VALUE ${fmtK(mv)}${isOffer?'':' · CLAUSE PAID '+fmtK(t.clausePaid)}</div>
    </div>
    <div class="ng-thread">${bubbles||`<div class="fo-empty">${isOffer?'Open with a transfer fee — player market value: '+fmt(mv)+'.':'Clause paid — buyer opens with a fee. Player market value: '+fmt(mv)+'.'}</div>`}</div>
    ${controls}
  </div>`;
}""")

# ============ P. renderNegCard band (base cost) ============
rep("""      <div class="ng-band">FAIR ${fmtK(b.fair)} · BAND ${fmtK(b.min)}–${fmtK(b.max)}${neg.type==='renewal'&&p.Salary>0?' · FLOOR '+fmtK(p.Salary):''}</div>""",
"""      <div class="ng-band">MV ${fmtK(p.MarketValue||0)} · FAIR SALARY ${fmtK(b.fair)}/mo · BAND ${fmtK(b.min)}–${fmtK(b.max)}${neg.type==='renewal'&&p.Salary>0?' · FLOOR '+fmtK(p.Salary):''}${neg.feePaid>0?' · FEE PAID '+fmtK(neg.feePaid):''}</div>""")

# ============ Q. renderFoDesk grouping ============
rep("""function renderFoDesk(at, myNegs, buyTalks){
  const html=[...myNegs.map(renderNegCard), ...buyTalks.map(t=>renderTalkCard(t,'buyer'))].join('');
  $('fo-desk').innerHTML = html || `<div class="fo-empty" style="padding:30px; text-align:center;">No active negotiations.<br>Scout the <b>MARKET</b>, renew from the <b>LOCKER ROOM</b>, or pay a clause to open talks.</div>`;
}""",
"""function renderFoDesk(at, myNegs, buyTalks){
  let html='';
  if (buyTalks.length) html+=`<div class="pm-section-title" style="margin-top:0;">💰 FEE TALKS — BUYING (${buyTalks.length})</div>`+buyTalks.map(t=>renderTalkCard(t,'buyer')).join('');
  const contracts=myNegs.filter(n=>n.type!=='renewal'), renewals=myNegs.filter(n=>n.type==='renewal');
  if (contracts.length) html+=`<div class="pm-section-title" ${buyTalks.length?'':'style="margin-top:0;"'}>🖋 CONTRACT TALKS — PLAYER TERMS (${contracts.length})</div>`+contracts.map(renderNegCard).join('');
  if (renewals.length) html+=`<div class="pm-section-title">📋 RENEWALS (${renewals.length})</div>`+renewals.map(renderNegCard).join('');
  $('fo-desk').innerHTML = html || `<div class="fo-empty" style="padding:30px; text-align:center;">No active negotiations.<br>Scout the <b>MARKET</b>, renew from the <b>LOCKER ROOM</b>, pay a clause, or send an offer for an OPEN-TO-OFFERS player.</div>`;
}""")

# ============ R. renderFoInbox (prioritized) ============
rep("""function renderFoInbox(at, sellTalks){
  $('fo-inbox').innerHTML = sellTalks.length
    ? sellTalks.map(t=>renderTalkCard(t,'seller')).join('')
    : '<div class="fo-empty">No incoming clause talks.</div>';
}""",
"""function renderFoInbox(at, sellTalks){
  const box=$('fo-inbox'); if (!box) return;
  const badge=$('fo-inbox-count'); if (badge) badge.textContent=sellTalks.length;
  const card=$('fo-inbox-card');
  if (card) card.style.boxShadow = sellTalks.some(t=>t.pending==='seller') ? '0 0 0 1px var(--orange)' : 'none';
  box.innerHTML = sellTalks.length
    ? sellTalks.map(t=>renderTalkCard(t,'seller')).join('')
    : '<div class="fo-empty">No incoming talks — clubs paying a clause or bidding on your OPEN-TO-OFFERS players appear here first.</div>';
}""")

# ============ S. renderOffice: drop deal-history card ============
rep("""  renderFoManaged();
  renderFoHistory(at);
}""",
"""  renderFoManaged();
}""")

# ============ T. renderFoSquad: MV + clickable PROTECTED toggle ============
rep("""        <span>${fmt(getPlayerSalary(p))}/mo ${isLegacyContract(p)?'<span class="badge" style="font-size:8px;">LEGACY</span>':''}</span>""",
"""        <span>${fmt(getPlayerSalary(p))}/mo · MV ${fmtK(p.MarketValue||0)} ${isLegacyContract(p)?'<span class="badge" style="font-size:8px;">LEGACY</span>':''}</span>""")

rep("""        ${(!p.Buyout&&!p.ReleaseClause&&!p.OnSale)?`<span class="fo-tag" style="--c:var(--text-dim)">🔒 PROTECTED</span>`:''}""",
"""        ${p.OpenToOffers>0?`<button class="fo-tag fo-tag-btn" style="--c:var(--green)" title="OPEN TO OFFERS — clubs can bid a fee directly. Click to protect again." onclick="toggleOpenToOffers('${e}')">📬 OPEN TO OFFERS</button>`:((!p.Buyout&&!p.ReleaseClause&&!p.OnSale)?`<button class="fo-tag fo-tag-btn" style="--c:var(--text-dim)" title="PROTECTED — untouchable. Click to set OPEN TO OFFERS so clubs can bid a fee directly (no clause / no sale listing needed)." onclick="toggleOpenToOffers('${e}')">🔒 PROTECTED</button>`:'')}""")

# ============ U. market buttons + badge ============
rep("""      const bits=[];
      if (p.OnSale>0) bits.push(`<button class="btn btn-green btn-sm" onclick="buyListed('${eN}')">🏷 BUY ${fmtK(p.OnSale)}</button>`);
      if (p.Buyout>0) bits.push(`<button class="btn btn-cyan btn-sm" onclick="payBuyout('${eN}')">⚡ BUYOUT ${fmtK(p.Buyout)}</button>`);
      if (p.ReleaseClause>0) bits.push(`<button class="btn btn-orange btn-sm" onclick="payReleaseClause('${eN}')">🔑 CLAUSE ${fmtK(p.ReleaseClause)}</button>`);
      btnHtml = bits.length ? `<div style="display:flex; gap:4px; flex-wrap:wrap; justify-content:flex-end;">${bits.join('')}</div>` : `<span class="badge" title="No buyout, clause or listing — untouchable">🔒 LOCKED</span>`;""",
"""      const bits=[];
      const myTalk=clauseTalks.find(t=>t.status==='open'&&t.buyer===activeTeam&&t.playerName===p.pn);
      if (myTalk){
        bits.push(`<button class="btn btn-ghost btn-sm" onclick="gotoOffice()">${myTalk.kind==='offer'?'📨 OFFER SENT':'🔑 CLAUSE PAID'} — IN TALKS</button>`);
      } else {
        if (p.OnSale>0) bits.push(`<button class="btn btn-green btn-sm" onclick="buyListed('${eN}')">🏷 BUY ${fmtK(p.OnSale)}</button>`);
        if (p.Buyout>0) bits.push(`<button class="btn btn-cyan btn-sm" onclick="payBuyout('${eN}')">⚡ BUYOUT ${fmtK(p.Buyout)}</button>`);
        if (p.ReleaseClause>0) bits.push(`<button class="btn btn-orange btn-sm" onclick="payReleaseClause('${eN}')">🔑 CLAUSE ${fmtK(p.ReleaseClause)}</button>`);
        if (p.OpenToOffers>0) bits.push(`<button class="btn btn-purple btn-sm" onclick="sendTransferOffer('${eN}')">📨 SEND OFFER</button>`);
      }
      btnHtml = bits.length ? `<div style="display:flex; gap:4px; flex-wrap:wrap; justify-content:flex-end;">${bits.join('')}</div>` : `<span class="badge" title="Protected — no buyout, clause or listing, and not open to offers">🔒 LOCKED</span>`;""")

rep("""          ${p.OnSale>0?'<span class="badge badge-orange">🏷 ON SALE</span>':''}""",
"""          ${p.OnSale>0?'<span class="badge badge-orange">🏷 ON SALE</span>':''}
          ${p.OpenToOffers>0?'<span class="badge badge-purple">📬 OPEN TO OFFERS</span>':''}""")

rep("""<span style="color:var(--text-dim); font-size:11px; display:inline-flex; align-items:center; gap:3px;">${getTeamLogo(p.TeamName, 14)}[${p.TeamName}]</span>""",
"""<span style="color:var(--text-dim); font-size:11px; display:inline-flex; align-items:center; gap:3px;">${getTeamLogo(p.TeamName, 14)}[${teamLabel(p.TeamName)}]</span>""")

# ============ V. player profile: routes + history section ============
rep("""  const routeTxt = p.TeamName==='none' ? 'FREE AGENT' : (routes.length ? routes.map(r=>(ROUTE_ICON[r.key]||'')+' '+fmtK(r.price)).join(' · ') : '🔒 LOCKED');""",
"""  const routeTxt = p.TeamName==='none' ? 'FREE AGENT' : (routes.length ? routes.map(r=>(ROUTE_ICON[r.key]||'')+' '+fmtK(r.price)).join(' · ') : (p.OpenToOffers>0 ? '📬 OPEN TO OFFERS' : '🔒 LOCKED'));""")

rep("""        <!-- PRIZE POOL -->""",
"""        <!-- EVENT & AWARD HISTORY -->
        <div class="pm-section-title">🏛 EVENT & AWARD HISTORY</div>
        ${(()=>{ const hist=playerHistory.filter(h=>h.player===String(p.PlayerName)); return hist.length ? '<div class="scroll-list" style="max-height:180px; margin-bottom:14px;">'+hist.map(h=>`
          <div class="list-row" style="padding:5px 0;">
            <div><div class="name" style="font-size:11px;">${h.kind==='EVENT'?'🏆':h.kind==='MVP'?'🥇':h.kind==='EVP'?'🥈':'🥉'} ${h.event}${h.kind!=='EVENT'?' — '+h.kind:''}</div>
            <div class="meta" style="font-size:9px;">${histStars(h.tier)} · ${h.scope} · ${h.position}${h.team?' · '+h.team:''} · Month ${h.month}</div></div>
          </div>`).join('')+'</div>' : '<div class="fo-empty" style="margin-bottom:14px;">No recorded events yet — add entries in the 🏛 HISTORY tab.</div>'; })()}

        <!-- PRIZE POOL -->""")

# ============ W. new feature JS block ============
rep("""function getFormScore(p) {""",
"""/* ── 📬 OPEN TO OFFERS ──────────────────────────────────────────────── */
function toggleOpenToOffers(name){
  const p=players.find(x=>String(x.PlayerName)===name); if (!p) return;
  saveState();
  p.OpenToOffers = p.OpenToOffers>0 ? 0 : 1;
  addLog(p.OpenToOffers
    ? `📬 ${name} is now OPEN TO OFFERS — any club can negotiate a fee directly (no clause payment needed).`
    : `🔒 ${name} is PROTECTED again — direct offers blocked.`);
  updateAll();
}

function sendTransferOffer(name){
  const buyerName=$('dash-team-select').value;
  const p=players.find(x=>String(x.PlayerName)===name);
  if (!p||p.TeamName===buyerName||p.TeamName==='none') return;
  if (!(p.OpenToOffers>0)) return alert('This player is not open to offers.');
  if (clauseTalks.some(t=>t.status==='open'&&t.buyer===buyerName&&t.playerName===name)){ gotoOffice(); return; }
  if (activeNegFor(name)) return alert(`${name} is locked in an active negotiation.`);
  if (!canAcquire(buyerName)) return alert('Squad full — 5 starters and 3 bench players already.');
  if (!confirm(`Open transfer talks for ${name} (${p.TeamName})?\\nFREE — no clause payment. You negotiate the fee directly with ${p.TeamName}.\\nReference: Market Value ${fmt(p.MarketValue||0)}.`)) return;
  saveState();
  clauseTalks.unshift({id:Date.now()+Math.floor(Math.random()*999), kind:'offer', buyer:buyerName, seller:p.TeamName, playerName:name, clausePaid:0, thread:[], pending:'buyer', status:'open'});
  addLog(`📨 ${buyerName} opened transfer talks for ${name} (${p.TeamName}) — player is OPEN TO OFFERS.`);
  gotoOffice(); updateAll();
}

/* ── 🏛 HISTORY — TROPHIES, AWARDS & TRANSACTIONS (record-only) ─────── */
function histStars(tier){ tier=Number(tier)||1; return tier>=5 ? '⭐⭐⭐⭐⭐ SS+' : '⭐'.repeat(Math.max(1,Math.min(4,tier))); }
function histTierChanged(prefix){
  const tier=$(`hist-${prefix}-tier`).value, scope=$(`hist-${prefix}-scope`);
  if (!scope) return;
  if (tier==='5'){ scope.value='Global'; scope.disabled=true; } else { scope.disabled=false; } // 5★ / SS+ = Major ⇒ always a GLOBAL event
}
function populateHistoryControls(){
  if (!$('hist-ev-team')) return;
  const opts=finances.map(t=>`<option value="${t.TeamName}">${t.TeamName}</option>`).join('');
  ['hist-ev-team','hist-view-team'].forEach(id=>{ const el=$(id); if (!el) return; const cur=el.value; el.innerHTML=opts; if (cur&&finances.some(t=>t.TeamName===cur)) el.value=cur; });
  const dl=$('hist-player-list'); if (dl) dl.innerHTML=players.map(p=>`<option value="${String(p.PlayerName)}">`).join('');
}
function applyTeamAchievement(){
  const team=$('hist-ev-team').value;
  const event=($('hist-ev-name').value||'').trim();
  const tier=Number($('hist-ev-tier').value)||1;
  const scope=tier>=5?'Global':$('hist-ev-scope').value;
  const position=$('hist-ev-pos').value;
  const prizePool=parseFloat($('hist-ev-pool').value)||0;
  const wonAmount=parseFloat($('hist-ev-won').value)||0;
  if (!team) return alert('Select a team.');
  if (!event) return alert('Enter the event name.');
  const starters=players.filter(p=>p.TeamName===team&&p.Roster==='Starter');
  if (!confirm(`Record "${event}" (${histStars(tier)} · ${scope} · ${position}) for ${team}?\\nPrize pool ${fmt(prizePool)} · team won ${fmt(wonAmount)}.\\nThe event is also written to ${starters.length} active-roster player(s).\\nRECORD-ONLY — no money moves (use ⚙ OPS for payouts).`)) return;
  saveState();
  const id=Date.now()+Math.floor(Math.random()*999);
  teamHistory.unshift({id, team, event, tier, scope, position, prizePool, wonAmount, month:monthCounter});
  starters.forEach(p=>playerHistory.unshift({id:id+'-'+String(p.PlayerName), refId:id, player:String(p.PlayerName), team, kind:'EVENT', event, tier, scope, position, month:monthCounter}));
  addLog(`🏛 HISTORY: ${team} — ${event} (${histStars(tier)}, ${scope}, ${position}) recorded for the team and ${starters.length} starter(s).`,'good');
  $('hist-ev-name').value=''; $('hist-ev-pool').value=''; $('hist-ev-won').value='';
  renderHistory(); updateAll();
}
function applyPlayerAward(){
  const name=($('hist-aw-player').value||'').trim();
  const p=players.find(x=>String(x.PlayerName)===name);
  if (!p) return alert('Player not found — pick a name from the list.');
  const kind=$('hist-aw-kind').value;
  const event=($('hist-aw-event').value||'').trim();
  if (!event) return alert('Enter the event name.');
  const tier=Number($('hist-aw-tier').value)||1;
  const scope=tier>=5?'Global':$('hist-aw-scope').value;
  const position=$('hist-aw-pos').value;
  saveState();
  playerHistory.unshift({id:Date.now()+Math.floor(Math.random()*999), refId:null, player:name, team:p.TeamName==='none'?'':p.TeamName, kind, event, tier, scope, position, month:monthCounter});
  addLog(`🏛 HISTORY: ${kind} at ${event} (${histStars(tier)}, ${scope}, ${position}) recorded for ${name}.`,'good');
  $('hist-aw-event').value='';
  renderHistory(); updateAll();
}
function deleteTeamEvent(id){
  const ev=teamHistory.find(e=>String(e.id)===String(id)); if (!ev) return;
  if (!confirm(`Delete "${ev.event}" from ${ev.team}'s history?\\nAlso removes the linked entry from every player who received it.`)) return;
  saveState();
  teamHistory=teamHistory.filter(e=>String(e.id)!==String(id));
  playerHistory=playerHistory.filter(h=>String(h.refId)!==String(id));
  renderHistory(); updateAll();
}
function deletePlayerAward(id){
  const h=playerHistory.find(x=>String(x.id)===String(id)); if (!h) return;
  if (!confirm(`Delete ${h.kind} — "${h.event}" from ${h.player}'s history?`)) return;
  saveState();
  playerHistory=playerHistory.filter(x=>String(x.id)!==String(id));
  renderHistory(); updateAll();
}
function renderHistory(){
  if (!$('hist-view-team')) return;
  populateHistoryControls();
  const team=$('hist-view-team').value;
  const evs=teamHistory.filter(e=>e.team===team);
  $('hist-team-events').innerHTML = evs.length ? evs.map(e=>`
    <div class="list-row" style="padding:6px 0; align-items:flex-start;">
      <div style="flex:1;">
        <div class="name" style="font-size:12px;">${e.position==='Winner'?'🥇':e.position==='Second'?'🥈':'🥉'} ${e.event} ${Number(e.tier)>=5?'<span class="badge badge-yellow">👑 MAJOR</span>':''}</div>
        <div class="meta" style="font-size:9px;">${histStars(e.tier)} · ${e.scope} · ${e.position} · Pool ${fmtK(e.prizePool)} · Won <span style="color:var(--green);">${fmtK(e.wonAmount)}</span> · Month ${e.month}</div>
      </div>
      <button class="fo-ico" title="Delete entry" onclick="deleteTeamEvent('${e.id}')">🗑</button>
    </div>`).join('') : '<div class="fo-empty">No achievements recorded for this team yet.</div>';
  const rosterNames=new Set(players.filter(p=>p.TeamName===team).map(p=>String(p.PlayerName)));
  const awards=playerHistory.filter(h=>h.kind!=='EVENT'&&rosterNames.has(h.player));
  $('hist-team-awards').innerHTML = awards.length ? awards.map(h=>`
    <div class="list-row" style="padding:5px 0;">
      <div style="flex:1;">
        <div class="name" style="font-size:11px;">${h.kind==='MVP'?'🥇':h.kind==='EVP'?'🥈':'🥉'} ${h.player} — ${h.kind} · ${h.event}</div>
        <div class="meta" style="font-size:9px;">${histStars(h.tier)} · ${h.scope} · ${h.position} · Month ${h.month}</div>
      </div>
      <button class="fo-ico" title="Delete entry" onclick="deletePlayerAward('${h.id}')">🗑</button>
    </div>`).join('') : '<div class="fo-empty">No individual awards recorded for this roster.</div>';
  const deals=transferHistory.filter(o=>o.buyer===team||o.seller===team).slice(0,25);
  $('hist-team-deals').innerHTML = deals.length ? deals.map(o=>{
    const c=String(o.status).includes('✅')?'var(--green)':'var(--red)';
    return `<div class="list-row" style="padding:5px 0;"><div><div class="name" style="font-size:11px;">${o.playerName}</div><div class="meta" style="font-size:9px;">${o.seller} → ${o.buyer} · ${fmt(o.amount)}</div></div><span style="color:${c}; font-family:var(--font-data); font-size:9px; font-weight:700; text-align:right;">${o.status}</span></div>`;
  }).join('') : '<div class="fo-empty">No deals involving this team yet.</div>';
  renderTransactions();
}
function renderTransactions(){
  const box=$('hist-transactions'); if (!box) return;
  const q=($('hist-tx-search')&&$('hist-tx-search').value||'').toLowerCase();
  const TXC={'TRANSFER':'var(--green)','FA SIGNING':'var(--cyan)','LEFT TEAM':'var(--red)','BENCHED':'var(--orange)','PROMOTED':'var(--cyan)','CLAUSE PAID':'var(--yellow)'};
  const rows=transactions.filter(t=>!q||String(t.playerName).toLowerCase().includes(q)||String(t.from).toLowerCase().includes(q)||String(t.to).toLowerCase().includes(q)).slice(0,80);
  box.innerHTML = rows.length ? rows.map(t=>`
    <div class="list-row" style="padding:5px 0;">
      <div style="flex:1;">
        <div class="name" style="font-size:11px;">${t.playerName} <span class="badge badge-ghost" style="color:${TXC[t.type]||'var(--text)'};">${t.type}</span></div>
        <div class="meta" style="font-size:9px;">${t.from} → ${t.to}${t.amount?' · '+fmt(t.amount):''}${t.note?' · '+t.note:''} · Month ${t.month}</div>
      </div>
    </div>`).join('') : '<div class="fo-empty">No player movements yet — buys, signings, releases and bench moves will appear here.</div>';
}
function loadHistoryWB(wb){
  const sheet=n=>wb.Sheets[n]?XLSX.utils.sheet_to_json(wb.Sheets[n]):[];
  teamHistory=sheet('TeamHistory').filter(r=>r.event).map(r=>({id:r.id||Date.now()+Math.random(), team:String(r.team||''), event:String(r.event||''), tier:Number(r.tier)||1, scope:String(r.scope||'Global'), position:String(r.position||'Winner'), prizePool:Number(r.prizePool)||0, wonAmount:Number(r.wonAmount)||0, month:Number(r.month)||1}));
  playerHistory=sheet('PlayerHistory').filter(r=>r.player&&r.event).map(r=>({id:r.id||Date.now()+Math.random(), refId:r.refId||null, player:String(r.player||''), team:String(r.team||''), kind:String(r.kind||'EVENT'), event:String(r.event||''), tier:Number(r.tier)||1, scope:String(r.scope||'Global'), position:String(r.position||'Winner'), month:Number(r.month)||1}));
  transactions=sheet('Transactions').filter(r=>r.type).map(r=>({id:r.id||Date.now()+Math.random(), month:Number(r.month)||1, type:String(r.type||''), playerName:String(r.playerName||''), from:String(r.from||''), to:String(r.to||''), amount:Number(r.amount)||0, note:String(r.note||'')}));
}

function getFormScore(p) {""")

# ============ X. toggleRoster transactions ============
rep("""    saveState(); p.Roster='Bench'; addLog(`🔄 ${name} → Bench.`); updateAll();""",
    """    saveState(); p.Roster='Bench'; addTransaction('BENCHED', name, p.TeamName, p.TeamName, 0, 'moved to bench'); addLog(`🔄 ${name} → Bench.`); updateAll();""")
rep("""    saveState(); p.Roster='Starter'; addLog(`🔄 ${name} → Starter.`,'good'); updateAll();""",
    """    saveState(); p.Roster='Starter'; addTransaction('PROMOTED', name, p.TeamName, p.TeamName, 0, 'promoted to starter'); addLog(`🔄 ${name} → Starter.`,'good'); updateAll();""")

# ============ Y. contract expiry transaction ============
rep("""    addLog(`⌛ CONTRACT EXPIRED: ${pn} left ${p.TeamName} — now a FREE AGENT.`,'warn');
    voidPlayerBusiness(pn);""",
"""    addLog(`⌛ CONTRACT EXPIRED: ${pn} left ${p.TeamName} — now a FREE AGENT.`,'warn');
    addTransaction('LEFT TEAM', pn, p.TeamName, 'Free Agency', 0, 'contract expired');
    voidPlayerBusiness(pn);""")

# ============ Z. exportExcels ============
rep("""    'Role': p.Role || '',""",
    """    'Role': (p.roleList && p.roleList.length) ? p.roleList.join('|') : (p.Role || ''),""")

rep("""    'OnSale': p.OnSale || 0,
    'Managed': p.Managed || ''""",
"""    'OnSale': p.OnSale || 0,
    'OpenToOffers': p.OpenToOffers || 0,
    'Managed': p.Managed || ''""")

rep("""  const wb2=XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb2,XLSX.utils.json_to_sheet(pData),'Players'); XLSX.writeFile(wb2,'players_updated.xlsx');
  addLog('📥 Exported finances_updated.xlsx & players_updated.xlsx.','good');""",
"""  const wb2=XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb2,XLSX.utils.json_to_sheet(pData),'Players'); XLSX.writeFile(wb2,'players_updated.xlsx');
  // History workbook: achievements, awards & transactions survive between sessions
  const hData=teamHistory.map(e=>({id:e.id, team:e.team, event:e.event, tier:e.tier, scope:e.scope, position:e.position, prizePool:e.prizePool, wonAmount:e.wonAmount, month:e.month}));
  const aData=playerHistory.map(h=>({id:h.id, refId:h.refId||'', player:h.player, team:h.team, kind:h.kind, event:h.event, tier:h.tier, scope:h.scope, position:h.position, month:h.month}));
  const tData=transactions.map(t=>({id:t.id, month:t.month, type:t.type, playerName:t.playerName, from:t.from, to:t.to, amount:t.amount, note:t.note}));
  const wb3=XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb3,XLSX.utils.json_to_sheet(hData),'TeamHistory');
  XLSX.utils.book_append_sheet(wb3,XLSX.utils.json_to_sheet(aData),'PlayerHistory');
  XLSX.utils.book_append_sheet(wb3,XLSX.utils.json_to_sheet(tData),'Transactions');
  XLSX.writeFile(wb3,'history_updated.xlsx');
  addLog('📥 Exported finances_updated.xlsx, players_updated.xlsx & history_updated.xlsx.','good');""")

# ============ AA. scanFiles: optional history file ============
rep("""  } catch(e) {
    errors.push('file/players_updated.xlsx');
    $('ply-status').textContent = `✗ NOT FOUND`;
    $('ply-status').style.color = 'var(--red)';
  }""",
"""  } catch(e) {
    errors.push('file/players_updated.xlsx');
    $('ply-status').textContent = `✗ NOT FOUND`;
    $('ply-status').style.color = 'var(--red)';
  }

  // --- history_updated.xlsx (optional — achievements, awards & transactions) ---
  try {
    const res = await fetch('file/history_updated.xlsx');
    if (res.ok){
      const buf = await res.arrayBuffer();
      loadHistoryWB(XLSX.read(buf, {type:'array'}));
      const hb=$('hist-box'); if (hb){ hb.classList.add('loaded'); $('hist-status').textContent='✓ HISTORY LOADED'; }
    }
  } catch(e) { /* optional file — start with an empty history */ }""")

# ============ AB. upload overlay history box + listener ============
rep("""    <div class="upload-box" id="logo-box">""",
"""    <div class="upload-box" id="hist-box">
      <input type="file" id="upload-history" accept=".xlsx">
      <div class="corner-tl"></div><div class="corner-tr"></div>
      <div class="corner-bl"></div><div class="corner-br"></div>
      <div class="upload-icon">🏛</div>
      <div class="upload-label">HISTORY.XLSX (OPTIONAL)</div>
      <div class="upload-status" id="hist-status">AWAITING DATA</div>
    </div>
    <div class="upload-box" id="logo-box">""")

rep("""$('upload-logos').addEventListener('change', e => {""",
"""$('upload-history').addEventListener('change', e => {
  const r = new FileReader();
  r.onload = ev => {
    loadHistoryWB(XLSX.read(ev.target.result, {type:'binary'}));
    $('hist-box').classList.add('loaded');
    $('hist-status').textContent = '✓ HISTORY LOADED';
  };
  r.readAsBinaryString(e.target.files[0]);
});

$('upload-logos').addEventListener('change', e => {""")

# ============ AC. forecast first-render fix + redraw hooks ============
rep("""function drawForecast(tName, team, netMonth) {
  const canvas = $('forecast-canvas');
  if (!canvas) return;""",
"""function drawForecast(tName, team, netMonth) {
  const canvas = $('forecast-canvas');
  if (!canvas) return;
  if (!canvas.offsetWidth) { // hidden or not laid out yet — retry next frame (fixes the broken first render)
    drawForecast._tries=(drawForecast._tries||0)+1;
    if (drawForecast._tries<60) requestAnimationFrame(()=>drawForecast(tName, team, netMonth));
    return;
  }
  drawForecast._tries=0;""")

rep("""function showPanel(id, btn) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  $(id).classList.add('active');
  if (btn) btn.classList.add('active');
}""",
"""function showPanel(id, btn) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  $(id).classList.add('active');
  if (btn) btn.classList.add('active');
  if (id==='p-command' && finances.length) updateCommand(); // redraw the forecast with real dimensions
}
window.addEventListener('resize', () => {
  const pc=document.getElementById('p-command');
  if (pc && pc.classList.contains('active') && finances.length) updateCommand();
});""")

# ============ AD. updateAll → renderHistory ============
rep("""  updateMarketTeamLogo();
  renderOffice();
}""",
"""  updateMarketTeamLogo();
  renderOffice();
  renderHistory();
}""")

# ============ AE. English-only labels ============
rep("""  status.textContent = 'Buscando arquivos em file/ e assets/...';""",
    """  status.textContent = 'Scanning for files in file/ and assets/...';""")
rep("""✗ NÃO ENCONTRADO:""", """✗ NOT FOUND:""")
rep("""(logos ausentes — upload manual disponível)""", """(logos missing — manual upload available)""")
rep("""❓ NÃO CLASSIFICADO""", """❓ UNCLASSIFIED""")
rep("""<div class="lbl">EM ASCENSÃO</div>""", """<div class="lbl">RISING</div>""")
rep("""<div class="sub">times sólidos</div>""", """<div class="sub">solid teams</div>""")
rep("""<div class="lbl">EM COLAPSO</div>""", """<div class="lbl">COLLAPSING</div>""")
rep("""<div class="sub">precisam de ação</div>""", """<div class="sub">need action</div>""")
rep("""DIAGNÓSTICO ATUAL""", """CURRENT DIAGNOSIS""")
rep("""PONTOS FORTES (${strengths.length})""", """STRENGTHS (${strengths.length})""")
rep("""PROBLEMAS DETECTADOS (${issues.length})""", """ISSUES DETECTED (${issues.length})""")
rep("""PLANO DE AÇÃO — ${actions.length} RECOMENDAÇÃO(ÕES)""", """ACTION PLAN — ${actions.length} RECOMMENDATION(S)""")

# ============ AF. CSS additions ============
rep(""".ng-asplayer { font-family:var(--font-data); font-size:9px; font-weight:700; letter-spacing:2px; color:var(--purple); text-align:center; padding:4px; border:1px dashed rgba(177,140,240,0.5); border-radius:6px; margin-bottom:6px; }""",
""".ng-asplayer { font-family:var(--font-data); font-size:9px; font-weight:700; letter-spacing:2px; color:var(--purple); text-align:center; padding:4px; border:1px dashed rgba(177,140,240,0.5); border-radius:6px; margin-bottom:6px; }
/* ── v9.1 additions ── */
.fo-tag-btn { cursor:pointer; transition:all .12s; }
.fo-tag-btn:hover { filter:brightness(1.4); transform:translateY(-1px); }
.fo-inbox-row { display:grid; grid-template-columns:repeat(auto-fill,minmax(330px,1fr)); gap:10px; max-height:360px; overflow-y:auto; }
.ng-card-offer { border-left-color:var(--purple); }""")

io.open(PATH, 'w', encoding='utf-8').write(src)
print('OK — %d patches applied. New size: %d bytes' % (count_applied, len(src)))
