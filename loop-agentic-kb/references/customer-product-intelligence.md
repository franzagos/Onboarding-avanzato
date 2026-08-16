# Customer e Product Intelligence

## Catalog discovery e copertura

Non limitarsi ai prodotti visibili in homepage. Cercare, quando autorizzato e tecnicamente possibile:

- sitemap, collezioni, categorie e sottocategorie;
- PDP, varianti, designer/collaborazioni e manuali;
- feed, listini, cataloghi PDF e pagine retailer;
- pagine servizi, shipping, resi, ricambi e assistenza;
- dati interni di vendita, stock, margine e reso, se forniti.

Registrare `discovered`, `analyzed`, `excluded`, metodo e data. Se il catalogo è molto ampio, costruire prima tassonomia completa delle famiglie e poi analizzare tutti i prodotti prioritari. Senza criterio osservabile di priorità, non chiamare hero un prodotto.

## Product intelligence record

Per ogni SKU/variante in scope includere:

- identità: `PROD-*`, `FAM-*`, variante, designer/collaborazione;
- funzione, categoria, materiale, dimensioni, compatibilità, cura;
- prezzo, valuta, mercato, stock e data;
- visual signature e meccanismo distintivo;
- functional benefit;
- emotional/social meaning, marcato come inference quando necessario;
- jobs e occasioni;
- personas plausibili e tensioni collegate;
- desire drivers, obiezioni e rischio percepito;
- proof disponibili e proof mancanti;
- claim consentiti/bloccati;
- alternative e competitor pertinenti;
- landing, content opportunities, cross-sell/upsell;
- rischi operativi: fragilità, installazione, consegna, reso, ricambi;
- ruolo commerciale e relativa evidenza/confidence.

Produrre anche una family synthesis: logica della gamma, price ladder, entry point, upgrade path, cannibalizzazione, gaps e priorità da validare.

## Psychographic depth

Non descrivere persone con aggettivi generici come "creative", "design lover" o "audaci" senza decomporre la decisione. Per ogni coppia prioritaria `PER-* × job × FAM-*` analizzare:

- identità attuale e identità desiderata;
- cambiamento che la persona vuole rendere visibile;
- paura privata e rischio sociale/estetico;
- tensione centrale e compromesso rifiutato;
- desiderio funzionale, emotivo e sociale;
- trigger situazionali e occasioni;
- anti-trigger e segnali di rigetto;
- alternative considerate e motivo del rifiuto;
- soglia di prezzo/proof, senza inventare numeri;
- proof che riduce il rischio;
- parole/metafore plausibili, separate dalla VOC osservata;
- comportamento che confermerebbe o falsificherebbe il modello;
- differenze attese per mercato e cultura;
- confidence ed evidence IDs.

Creare un `product_persona_bridge` per mostrare esattamente perché un meccanismo del prodotto risponde a una tensione. Vietare ponti generici del tipo "vuole distinguersi → prodotto originale" senza meccanismo, prova e obiezione.

## Personas e rilevanza

Separare tre domande:

1. La persona è plausibile?
2. Esiste nei dati clienti?
3. È economicamente rilevante?

Le risposte possono avere stati diversi. Non promuovere una persona a target prioritario usando soltanto coerenza narrativa.

## VOC e pain

Collegare ogni tema VOC a corpus, source, oggetto recensito e count nel corpus. Separare sempre linguaggio osservato, parafrasi e interpretazione. Per i pain distinguere prevalence, severity, economic impact e confidence. Se i dati interni mancano, lasciare prevalence/economic impact sconosciuti e definire il test necessario.

## QA

- La Product Message Map copre tutte le famiglie prioritarie.
- Il registry dichiara coverage e non usa quattro SKU come catalogo implicito.
- Ogni tensione psicografica ha un ponte prodotto-persona e un test.
- Ogni persona dichiara plausibilità, validazione e rilevanza economica separatamente.
- Ogni claim di beneficio/meaning è evidence, inference o hypothesis.
- Nessun dato interno assente viene sostituito da prominenza sul sito.
