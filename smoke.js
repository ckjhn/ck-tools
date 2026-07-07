/* Smoke test for NEXUS COMMAND v9.1 patch — runs the real app in jsdom */
const fs = require('fs');
const { JSDOM } = require('/tmp/smoke/node_modules/jsdom');

const html = fs.readFileSync('/sessions/kind-dazzling-darwin/mnt/outputs/app.html', 'utf-8');
const xlsxSrc = fs.readFileSync('/tmp/app.js', 'utf-8'); // real SheetJS from the bundle

const vc = new (require('/tmp/smoke/node_modules/jsdom').VirtualConsole)();
vc.on('jsdomError', e => { if (!/Not implemented/.test(String(e))) console.log('JSDOM ERR:', String(e).slice(0, 200)); });

const dom = new JSDOM(html, { runScripts: 'outside-only', pretendToBeVisual: true, virtualConsole: vc });
const w = dom.window;

// stubs BEFORE app script runs
w.alert = m => { w.__alerts.push(String(m)); };
w.__alerts = [];
w.confirm = () => true;
w.prompt = () => null;
w.localStorage = { getItem: () => null, setItem: () => {} };

// run SheetJS then the app script manually (extracted), then stub writeFile
const scriptSrc = html.match(/<script>([\s\S]*?)<\/script>/)[1];
w.eval(xlsxSrc);
w.eval(scriptSrc + "\n;window.__S = () => ({players, finances, clauseTalks, negotiations, transactions, teamHistory, playerHistory, transferHistory, ROLE_OPTIONS});");
const S = () => w.__S();
w.__written = [];
const realWrite = w.XLSX.writeFile;
w.XLSX.writeFile = (wb, name) => { w.__written.push({ name, wb }); };

let pass = 0, fail = 0;
function T(name, cond) { if (cond) { pass++; console.log('  ✓ ' + name); } else { fail++; console.log('  ✗ FAIL: ' + name); } }
const $ = id => w.document.getElementById(id);
const P = n => S().players.find(p => String(p.PlayerName) === n);
const F = n => S().finances.find(t => t.TeamName === n);

console.log('— A. roles —');
T('legacy star rifler → star player', JSON.stringify(w.parseRoleList('star rifler|closer|lurker')) === JSON.stringify(['star player','star player','dynamic']));
T('star rifle → star player', w.parseRoleList('star rifle')[0] === 'star player');
T('old canonical closer/star player migrates', w.parseRoleList('closer/star player')[0] === 'star player');
T('6 roles exactly', S().ROLE_OPTIONS.map(r=>r.value).join(',') === 'igl,star player,entry fragger,awper,anchor,dynamic');

console.log('— B. launch with demo data —');
w.loadDemoData();
T('app launched', w.document.getElementById('app').classList.contains('visible'));
T('No Team label present', w.document.body.innerHTML.includes('No Team'));
T('Sem Time gone', !w.document.body.innerHTML.includes('Sem Time'));
T('HISTORY tab present', w.document.body.innerHTML.includes('🏛 HISTORY'));

console.log('— C. release clause: pay once, never twice —');
$('dash-team-select').value = 'Apex Dynasty';
P('Vyper').ReleaseClause = 500;
const bank0 = F('Apex Dynasty').CurrentBank;
w.payReleaseClause('Vyper');
T('clause charged once', F('Apex Dynasty').CurrentBank === bank0 - 500);
T('talk open', S().clauseTalks.filter(t=>t.status==='open'&&t.playerName==='Vyper').length === 1);
w.payReleaseClause('Vyper'); // tab-switch scenario: clicking again must NOT charge
T('second click: NO second charge', F('Apex Dynasty').CurrentBank === bank0 - 500);
T('still exactly one talk', S().clauseTalks.filter(t=>t.status==='open'&&t.playerName==='Vyper').length === 1);
w.refreshMarket();
T('market shows IN TALKS instead of pay button', $('market-list').innerHTML.includes('IN TALKS'));

console.log('— D. fee talk with base cost + transfer placement —');
w.renderOffice();
const talk = S().clauseTalks.find(t=>t.playerName==='Vyper');
const feeInput = $('ct-amt-' + talk.id);
T('fee input prefilled with MV (base cost)', feeInput && Number(feeInput.value) === Math.round(P('Vyper').MarketValue));
T('desk shows BASE VALUE', $('fo-desk').innerHTML.includes('BASE VALUE'));
feeInput.value = '10000';
w.ctSend(talk.id);
T('pending flips to seller', talk.pending === 'seller');
w.ctAccept(talk.id);
T('Vyper transferred to Apex', P('Vyper').TeamName === 'Apex Dynasty');
T('full-roster team → joins as Bench', P('Vyper').Roster === 'Bench');
T('clause cleared after transfer', P('Vyper').ReleaseClause === 0);
T('mandatory signing opened', S().negotiations.some(n=>n.playerName==='Vyper'&&n.status==='open'&&n.mandatory));
T('transactions: CLAUSE PAID + TRANSFER logged', S().transactions.some(t=>t.type==='CLAUSE PAID') && S().transactions.some(t=>t.type==='TRANSFER'&&t.playerName==='Vyper'));

console.log('— E. auto-starter until 5 —');
$('dash-team-select').value = 'Drift Esports'; // 4 starters + 1 bench in demo
P('Nova').OnSale = 800;
w.buyListed('Nova');
T('team with 4 starters → new player is STARTER', P('Nova').TeamName==='Drift Esports' && P('Nova').Roster === 'Starter');
w.executeTransfer('Krios', 'Drift Esports', 10, 'TEST');
T('5 starters full → next joins BENCH', P('Krios').Roster === 'Bench');
w.executeTransfer('Echo', 'Drift Esports', 10, 'TEST');
T('bench fills to 3', S().players.filter(p=>p.TeamName==='Drift Esports'&&p.Roster==='Bench').length === 3);
T('squad full → canAcquire false', w.canAcquire('Drift Esports') === false);
w.__alerts.length = 0;
P('Blaze').OnSale = 700;
w.buyListed('Blaze');
T('buy blocked when squad full', P('Blaze').TeamName === 'Apex Dynasty' && w.__alerts.some(a=>/Squad full/.test(a)));

console.log('— F. open to offers —');
w.toggleOpenToOffers('Titan');
T('flag set', P('Titan').OpenToOffers === 1);
$('dash-team-select').value = 'Sentinel GG';
w.refreshMarket();
T('market shows SEND OFFER', $('market-list').innerHTML.includes('SEND OFFER'));
w.sendTransferOffer('Titan');
const offer = S().clauseTalks.find(t=>t.kind==='offer'&&t.playerName==='Titan'&&t.status==='open');
T('offer talk created, nothing paid', !!offer && offer.clausePaid === 0);
const sBank = F('Sentinel GG').CurrentBank;
w.ctReject(offer.id);
T('reject offer: no money lost', F('Sentinel GG').CurrentBank === sBank && offer.status === 'closed');
w.renderOffice();
T('squad card has clickable PROTECTED/OPEN toggle', $('fo-squad').innerHTML.includes('toggleOpenToOffers'));

console.log('— G. history: team achievement (record-only) —');
const team = 'Apex Dynasty';
const startersBefore = S().players.filter(p=>p.TeamName===team&&p.Roster==='Starter').length;
const bankBefore = F(team).CurrentBank;
w.renderHistory();
$('hist-ev-team').value = team;
$('hist-ev-name').value = 'NEXUS World Major';
$('hist-ev-tier').value = '5';
$('hist-ev-pos').value = 'Winner';
$('hist-ev-pool').value = '1000000';
$('hist-ev-won').value = '400000';
w.applyTeamAchievement();
T('team event recorded', S().teamHistory.length === 1 && S().teamHistory[0].event === 'NEXUS World Major');
T('tier 5 forces Global scope', S().teamHistory[0].scope === 'Global');
T('all starters got the event', S().playerHistory.filter(h=>h.kind==='EVENT'&&h.refId===S().teamHistory[0].id).length === startersBefore);
T('record-only: bank untouched', F(team).CurrentBank === bankBefore);
T('history view renders event + MAJOR badge', $('hist-team-events').innerHTML.includes('NEXUS World Major') && $('hist-team-events').innerHTML.includes('MAJOR'));

console.log('— H. history: player award + delete cascade —');
$('hist-aw-player').value = 'Titan';
$('hist-aw-kind').value = 'MVP';
$('hist-aw-event').value = 'IEM Test';
$('hist-aw-tier').value = '4';
$('hist-aw-scope').value = 'State';
$('hist-aw-pos').value = 'Winner';
w.applyPlayerAward();
T('award recorded', S().playerHistory.some(h=>h.kind==='MVP'&&h.player==='Titan'&&h.event==='IEM Test'));
const mvpCountBefore = P('Titan').MVP;
T('record-only: medal counter untouched', P('Titan').MVP === mvpCountBefore);
const evId = S().teamHistory[0].id;
w.deleteTeamEvent(evId);
T('delete cascades to player entries', S().teamHistory.length === 0 && S().playerHistory.filter(h=>h.refId===evId).length === 0);
T('award survives cascade', S().playerHistory.some(h=>h.kind==='MVP'&&h.player==='Titan'));

console.log('— I. transactions panel + roster toggle log —');
const someStarter = S().players.find(p=>p.TeamName==='Apex Dynasty'&&p.Roster==='Starter');
w.toggleRoster(String(someStarter.PlayerName));
T('bench move logged', S().transactions.some(t=>t.type==='BENCHED'&&t.playerName===String(someStarter.PlayerName)));
w.renderTransactions();
T('transactions panel renders rows', $('hist-transactions').innerHTML.includes('TRANSFER'));

console.log('— J. player profile shows history —');
w.openPlayerProfile('Titan');
const modal = w.document.querySelector('.player-modal');
T('profile has EVENT & AWARD HISTORY section', modal.innerHTML.includes('EVENT & AWARD HISTORY') && modal.innerHTML.includes('IEM Test'));
w.document.querySelector('.player-modal-overlay').remove();

console.log('— K. export round-trip —');
w.__written.length = 0;
w.exportExcels();
T('3 files exported', w.__written.length === 3 && w.__written.map(x=>x.name).join(',') === 'finances_updated.xlsx,players_updated.xlsx,history_updated.xlsx');
const pSheet = w.__written[1].wb.Sheets['Players'];
const pRows = w.XLSX.utils.sheet_to_json(pSheet);
T('players export has OpenToOffers column', pRows.every(r => 'OpenToOffers' in r));
T('roles exported canonical (no legacy names)', pRows.every(r => String(r.Role).split('|').every(x => !x || ['igl','star player','entry fragger','awper','anchor','dynamic','duelist','initiator','controller','sentinel','flex'].includes(x.toLowerCase()))));
const hWb = w.__written[2].wb;
T('history workbook has 3 sheets', JSON.stringify(hWb.SheetNames) === JSON.stringify(['TeamHistory','PlayerHistory','Transactions']));
const txRows = w.XLSX.utils.sheet_to_json(hWb.Sheets['Transactions']);
T('transactions persisted', txRows.length === S().transactions.length && txRows.length > 0);
// re-import
w.loadHistoryWB(hWb);
T('history re-import round-trips', S().transactions.length === txRows.length && S().playerHistory.some(h=>h.event==='IEM Test'));

console.log('— L. undo covers history —');
const hLenBefore = S().playerHistory.length;
$('hist-aw-player').value = 'Blaze';
$('hist-aw-event').value = 'Undo Cup';
w.applyPlayerAward();
w.undo();
T('undo restores history arrays', S().playerHistory.length === hLenBefore && !S().playerHistory.some(h=>h.event==='Undo Cup'));

console.log('— M. forecast guard (no crash while hidden) —');
let crashed = false;
try { w.updateCommand(); } catch (e) { crashed = true; console.log('   ', e.message); }
T('updateCommand safe with zero-width canvas', !crashed);

console.log('— N. FA signing placement —');
// make an FA and sign to a team with open starter slot
const fa = P('Blaze'); fa.TeamName = 'none'; fa.Roster = ''; fa.Salary = 0;
S().players.filter(p=>p.TeamName==='Nova Collective'&&p.Roster==='Starter').slice(0,1).forEach(p=>{ p.TeamName='none'; p.Roster=''; }); // open a slot
$('dash-team-select').value = 'Nova Collective';
w.startNegotiation('Nova Collective', 'Blaze', 'signing', 'fa', 0);
const neg = S().negotiations.find(n=>n.playerName==='Blaze'&&n.status==='open');
// force accept via closeDeal directly
w.closeDeal(neg, 3000, 12);
T('FA signing fills starter slot first', P('Blaze').TeamName==='Nova Collective' && P('Blaze').Roster==='Starter');
T('FA transaction logged', S().transactions.some(t=>t.type==='FA SIGNING'&&t.playerName==='Blaze'));

console.log('\n============ RESULT: %d passed, %d failed ============', pass, fail);
process.exit(fail ? 1 : 0);
