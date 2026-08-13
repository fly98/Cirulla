/* Confronto fra due configurazioni del computer.
   I posti si alternano a ogni partita, cosi' il vantaggio di chi comincia
   non falsa il risultato. */
const {carica} = require('./banco.js');

function turnoDi(G, cfg){
  G.CPU = cfg;
  G.cpuPesca();
  for(let k = 0; k < 60; k++){
    if(G.cpuAttaccaUno()) continue;
    if(G.cpuCalaUna()) continue;
    break;
  }
  G.cpuScarta();
}

function unaPartita(G, cfgA, cfgB, aParte){
  G.nuovaPartita();
  // aParte: 0 se A gioca come giocatore 0
  const cfg = aParte === 0 ? [cfgA, cfgB] : [cfgB, cfgA];
  let giri = 0, era = -1, fermo = 0;
  while(!G.ST.finita && giri < 400){
    const p = G.ST.turno;
    turnoDi(G, cfg[p]);
    if(G.ST.turno === p){ if(++fermo > 2) return null; } else fermo = 0;
    giri++;
  }
  const pa = aParte === 0 ? G.ST.punti[0] : G.ST.punti[1];
  const pb = aParte === 0 ? G.ST.punti[1] : G.ST.punti[0];
  const chiudeA = G.ST.chiusuraDi !== null && (G.ST.chiusuraDi === aParte);
  const melds = aParte === 0 ? G.ST.melds[0] : G.ST.melds[1];
  return {pa, pb, giri, chiudeA,
          scaleA: melds.filter(m => m.tipo === 'scala').length,
          gruppiA: melds.filter(m => m.tipo === 'gruppo').length,
          burrA: melds.filter(m => G.isBurraco(m)).length};
}

function confronta(cfgA, cfgB, n, etichetta){
  const G = carica('burraco.html');
  let vA = 0, vB = 0, sa = 0, sb = 0, ko = 0, chiusure = 0, giri = 0;
  let scale = 0, gruppi = 0, burr = 0;
  const t0 = Date.now();
  for(let i = 0; i < n; i++){
    const r = unaPartita(G, cfgA, cfgB, i % 2);
    if(!r){ ko++; continue; }
    if(r.pa > r.pb) vA++; else if(r.pb > r.pa) vB++;
    sa += r.pa; sb += r.pb; giri += r.giri;
    if(r.chiudeA) chiusure++;
    scale += r.scaleA; gruppi += r.gruppiA; burr += r.burrA;
  }
  const gio = vA + vB;
  const pct = gio ? (vA / gio * 100) : 0;
  // margine grossolano a due sigma sulla proporzione
  const err = gio ? 2 * Math.sqrt(0.25 / gio) * 100 : 0;
  console.log(
    (etichetta || 'A vs B').padEnd(30) +
    'A vince ' + pct.toFixed(1) + '% \u00b1' + err.toFixed(1) +
    '  (' + vA + '-' + vB + ')' +
    '  punti ' + Math.round(sa / gio) + ' vs ' + Math.round(sb / gio) +
    '  scale ' + (scale + gruppi ? (scale / (scale + gruppi) * 100).toFixed(0) : 0) + '%' +
    '  burraco/partita ' + (burr / gio).toFixed(2) +
    '  turni ' + Math.round(giri / gio) +
    (ko ? '  [' + ko + ' bloccate]' : '') +
    '  ' + ((Date.now() - t0) / 1000).toFixed(1) + 's');
  return {pct, err, ko};
}

module.exports = {confronta, unaPartita, turnoDi};

if(require.main === module){
  const n = +(process.argv[2] || 200);
  console.log('--- controllo del banco: due configurazioni identiche ---');
  confronta({livello:'medio'}, {livello:'medio'}, n, 'medio vs medio');
  console.log('--- livelli a confronto ---');
  confronta({livello:'difficile'}, {livello:'medio'}, n, 'difficile vs medio');
  confronta({livello:'medio'}, {livello:'facile'}, n, 'medio vs facile');
}
