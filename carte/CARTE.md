# Carte — provenienza e licenza

Mazzo francese usato da `burraco.html`. 55 file WebP **200x280 (rapporto 1:1,4)**,
generati da SVG con cairosvg, qualità 82.

- **52 numerali e figure** — set *English pattern* di **Dmitry Fomin**,
  Wikimedia Commons, **CC0**. Categoria `Category:SVG English pattern playing cards`.
- **JK-r / JK-b (jolly)** — arte da `Cards-Joker-Red.svg` / `Cards-Joker-Black.svg`,
  Wikimedia Commons, **pubblico dominio**, rimontata nella cornice del set Fomin
  (bianco, rx=30, filetto nero 1px). Il set Fomin non contiene jolly.
- **BACK (dorso)** — disegnato per questo progetto.

## Nota sul rapporto
Gli SVG sorgente sono 360x540, cioè 1:1,5. Una carta da poker reale e' 63x88 mm,
cioe' 1:1,4. In fase di rasterizzazione l'arte viene compressa del 6,7% in verticale
per arrivare a 1:1,4, che e' il rapporto usato anche a video (`height = width * 1.4`).
Se un domani si volesse tornare al rapporto nativo bisogna cambiare **entrambe** le
cose: l'altezza di rasterizzazione qui e il fattore in `ventaglio()`.

## Rigenerazione
Scaricare gli SVG dalla categoria Commons, rasterizzare a 200x280 e salvare in
WebP q82. Le figure originali pesano ~190 KB l'una in SVG (2,3 MB il mazzo);
in WebP l'intero set sta in ~360 KB.

Nomenclatura: `{indice}{seme}.webp`, indice A,2..10,J,Q,K e seme s,h,d,c.
Esempi: `As.webp`, `10h.webp`, `Kc.webp`. Piu' `JK-r`, `JK-b`, `BACK`.
