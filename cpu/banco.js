/* Banco di prova per il giocatore automatico del Burraco.
   Carica il codice VERO di burraco.html dentro una finta pagina, cosi' si misura
   quello che gira davvero e non una copia che diverge. Nessuna animazione,
   nessuna attesa: migliaia di partite in pochi secondi. */
const fs = require('fs');

function finto(){
  const e = {
    style:{setProperty(){}}, classList:{add(){}, remove(){}, contains:()=>false},
    children:[], dataset:{}, textContent:'', innerHTML:'', value:'',
    clientWidth:800, clientHeight:600, isConnected:false, firstElementChild:null,
    getBoundingClientRect:()=>({left:0,top:0,width:10,height:14}),
    appendChild(){}, remove(){}, removeAttribute(){}, addEventListener(){},
    querySelector:()=>null, querySelectorAll:()=>[], cloneNode:()=>finto(),
    closest:()=>null, focus(){}, onclick:null
  };
  return e;
}

function carica(file){
  const html = fs.readFileSync(file, 'utf8');
  const blocchi = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const src = blocchi.sort((a,b)=>b.length-a.length)[0];

  const memoria = {};
  const ctx = {
    document:{
      getElementById:()=>finto(), querySelector:()=>null, querySelectorAll:()=>[],
      createElement:()=>finto(), addEventListener(){}, body:finto(), hidden:false
    },
    localStorage:{ getItem:k=>memoria[k]||null, setItem:(k,v)=>{memoria[k]=v}, removeItem:k=>{delete memoria[k]} },
    innerWidth:900, innerHeight:800, addEventListener(){},
    requestAnimationFrame(f){}, setTimeout(){}, setInterval(){}, clearInterval(){}, clearTimeout(){},
    Image:function(){ return {}; }, fetch:()=>Promise.reject(new Error('rete spenta')),
    WebSocket:function(){ return {readyState:3, send(){}, close(){}}; },
    location:{pathname:'/burraco.html', replace(){}},
    navigator:{}, caches:null, Math, JSON, Set, Map, Object, Array, String, Number,
    Date, console, isNaN, parseInt, parseFloat
  };
  ctx.window = ctx;
  ctx.globalThis = ctx;

  const nomi = Object.keys(ctx);
  const esporta = ['CFG','ST','SEL','CPU','valida','riattacca','valCarta','bonusBurraco',
    'isBurraco','tipoBurraco','puoWild','nuovaPartita','pesca','cala','attacca','scarta',
    'mano','io','haBurraco','vicoloCieco','conta','candidati','scegliCalate','puntiMeld',
    'potenziale','cpuPesca','cpuAttaccaUno','cpuCalaUna','cpuScarta','utilita','pericolo',
    'serveAllAvversario','valoreCalate'];
  const coda = '\nreturn {' + esporta.map(n =>
      `get ${n}(){ return typeof ${n}!=="undefined" ? ${n} : undefined },` +
      `set ${n}(v){ try{ ${n}=v; }catch(e){} }`).join(',') + '};';

  const f = new Function(...nomi, src + coda);
  return f(...nomi.map(n => ctx[n]));
}

/* --- una partita fra due strategie --- */
function partita(G, stratA, stratB, seme){
  G.nuovaPartita();
  const strat = [stratA, stratB];
  let giri = 0;
  while(!G.ST.finita && giri < 400){
    const p = G.ST.turno;
    const ok = turno(G, p, strat[p]);
    if(!ok) return {ko:true, giri};
    giri++;
  }
  return {ko:false, giri, punti:G.ST.punti.slice(), chiusuraDi:G.ST.chiusuraDi,
          melds:[G.ST.melds[0].length, G.ST.melds[1].length]};
}

// Un turno completo, guidato a mano: niente attese, niente animazioni.
function turno(G, p, strat){
  const era = G.ST.turno;
  G.CPU = {livello: strat.livello || 'medio'};
  strat.pesca(G, p);
  for(let k = 0; k < 60; k++){
    if(strat.attacca(G, p)) continue;
    if(strat.cala(G, p)) continue;
    break;
  }
  strat.scarta(G, p);
  return G.ST.turno !== era || G.ST.finita;
}

module.exports = {carica, partita, turno};
