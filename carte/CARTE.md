# Carte — come sono fatte

Mazzo francese di `burraco.html`: 55 file WebP 200x280 (rapporto 1:1,4).
**Non e' un mazzo scaricato: e' generato da `genmazzo.py`** (nel repo, accanto
a questo file), rifacendo lo stile del burraco di riferimento perche' i mazzi
trovati online avevano l'indice troppo sottile per restare leggibile quando le
carte si sovrappongono.

## Disegno
- Colonna sinistra: **valore grande** in alto, **seme grande** sotto. E' l'unica
  parte che resta scoperta quando le carte si sovrappongono, quindi comanda tutto.
- In alto, accanto al valore, un seme piccolo.
- A destra un **pannello avorio** bordato con i pips disposti alla maniera classica
  (file basse capovolte dalla 4 in su), o la figura per J/Q/K.

## Unica dipendenza esterna
L'arte delle 12 figure e' ritagliata dal set *English pattern* di **Dmitry Fomin**
(Wikimedia Commons, **CC0**), scalata dentro il pannello. Gli SVG sorgente stanno
in `carte/*.svg` nella cartella di lavoro del generatore, non nel repo.
Jolly e dorso sono disegnati interamente da `genmazzo.py`.

## Trappole
- La **J** ha una discendente: va rimpicciolita del 10% e alzata, altrimenti tocca
  il seme grande sottostante.
- Il **10** ha due cifre: va al 74% della dimensione degli altri valori o sborda.
- Il **jolly non deve mostrare una "J"**: si confonde col fante. Usa una stella
  piu' la scritta JOLLY.
- Il rapporto 1:1,4 e' fissato in **due** punti: qui in `genmazzo.py` e nel
  fattore dentro `ventaglio()` / `colonna()` in `burraco.html`. Cambiarne uno solo
  da carte deformate.

## Rigenerazione
`python3 genmazzo.py` (serve cairosvg + Pillow). Scrive in `webp/`.
Per una versione a risoluzione maggiore basta alzare la costante `S`
(supersampling) e la dimensione finale in `salva()`.

Nomenclatura: `{valore}{seme}.webp`, valore A,2..10,J,Q,K e seme s,h,d,c.
Esempi: `As.webp`, `10h.webp`, `Kc.webp`. Piu' `JK-r`, `JK-b`, `BACK`.
