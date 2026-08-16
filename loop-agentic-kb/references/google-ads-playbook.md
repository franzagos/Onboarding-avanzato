# Google Ads Playbook — Reference per KB agent-ready

## Scopo

Questo modulo trasforma una Brand KB in istruzioni eseguibili per agenti Google Ads. Non propone budget, CPC, volumi o performance senza dati. Se Search Console, Keyword Planner, Merchant Center o account Google Ads non sono disponibili, keyword, priorità e struttura restano **ipotesi da validare**.

## Input obbligatori

- mercato, lingua e valuta;
- obiettivo commerciale e conversione primaria;
- catalogo con URL, prezzo e stock aggiornati;
- ruoli commerciali degli SKU: hero, acquisition, profit, cross-sell, seasonal;
- margine o almeno una fascia di marginalità;
- spedizione, reso e disponibilità applicabili al mercato;
- claim e asset autorizzati;
- tracking e consenso verificati.

Se mancano prezzo, stock, margine o tracking, l'agente può produrre una strategia esplorativa ma deve impostare `activation_ready.status: blocked`. Se l'utente chiede un piano eseguibile o launch-ready, applicare `blocking-input-protocol.md` e chiedere il dato iniziando con `Mi serve X`.

## Regole epistemiche

Etichettare ogni elemento come:

- `evidence`: presente in fonte primaria o dato interno datato;
- `inference`: deduzione ragionevole dalla KB;
- `hypothesis`: proposta da verificare con query e test;
- `blocked`: non utilizzabile senza dato o approvazione.

Non trasformare volume del catalogo, popolarità culturale o presenza nei retailer in una stima di domanda. Non chiamare un prodotto “bestseller”, “iconico”, “esclusivo” o “limited” senza prova applicabile allo SKU.

## Workflow

### 1. Readiness audit

Valutare separatamente:

| Area | Gate minimo |
|---|---|
| Business | obiettivo, conversione, paese, valuta |
| Prodotto | URL valido, prezzo, stock, immagine, identificatore |
| Economics | margine o proxy autorizzata, soglia CPA/ROAS definita internamente |
| Messaggio | claim con fonte, ambito e data |
| Operazioni | spedizione, resi, ETA e colli voluminosi |
| Measurement | purchase con valore/valuta, deduplica, consenso, test ordine |
| Feed | diagnostica Merchant Center, corrispondenza feed–landing–checkout |

Un solo blocco critico su tracking, checkout, policy o feed rende il lancio `blocked`, non semplicemente “da ottimizzare”.

### 2. Costruire l'intent universe

Usare cluster, non liste piatte:

1. **Brand:** brand e combinazioni brand+categoria.
2. **Prodotto nominato:** nome esatto, varianti, designer/collaborazione.
3. **Categoria commerciale:** tipologia + attributo realmente disponibile.
4. **Job/occasione:** regalo, punto focale, stanza, progetto.
5. **Confronto:** alternative, competitor, retailer; applicare policy legali e di trademark.
6. **Informativo:** cura, misure, lampadina, montaggio; monetizzare solo con landing utile.
7. **B2B/contract:** hospitality, retail, progettisti; solo se esiste un'offerta dedicata.

Per ogni cluster registrare:

```yaml
intent_cluster:
  id: product_named
  query_examples: []
  status: hypothesis
  commercial_intent: high|medium|low|unknown
  product_scope: []
  landing_page: null
  proof_required: []
  exclusions: []
  validation_sources: [keyword_planner, search_console, search_terms]
```

### 3. Validare keyword e query

- usare Keyword Planner per varianti e ordine di grandezza, mai copiarne i dati senza paese/data;
- usare Search Console per lessico organico e pagine già associate alle query;
- usare il report termini di ricerca per promuovere query utili e aggiornare negative;
- distinguere keyword target, query osservata e search theme PMax;
- partire da exact/phrase quando il rischio di ambiguità è alto;
- ampliare a broad solo con conversion tracking affidabile, Smart Bidding coerente e controllo dei termini.

Google descrive exact, phrase e broad come livelli crescenti di copertura; non trattare exact come corrispondenza letterale assoluta. Le negative non coprono automaticamente tutte le varianti: mantenere singolari, plurali e sinonimi utili.

### 4. Disegnare Search

Struttura minima suggerita, da adattare alla domanda reale:

```text
Brand
├── Core brand
├── Brand + categorie
└── Brand + prodotti
Product named
├── Famiglia A
└── Famiglia B
Non-brand category
├── Lighting
├── Objects/gifting
├── Tableware
└── Furniture
Job/occasion
└── Solo cluster con landing e prova coerenti
```

Separare Brand da Non-brand per leggere domanda catturata e domanda incrementale. Non frammentare campagne e gruppi oltre la capacità di raccogliere dati. Ogni gruppo deve avere:

- un'intenzione leggibile;
- una pagina coerente;
- almeno una proof specifica;
- copy senza claim non approvati;
- negative cross-cluster dove servono.

### 5. Generare annunci

Per ogni gruppo produrre un message pack, non solo headline:

```yaml
ad_group_message:
  intent: ""
  product_scope: []
  user_question: ""
  promise: ""
  proof: []
  risk_reducer: ""
  landing_page: ""
  headline_concepts: []
  description_concepts: []
  assets: [sitelink, callout, structured_snippet, image]
  blocked_claims: []
```

Principio: query nominata → prodotto e specifica; query categoria → selezione e criterio; query regalo → simbolo + consegna/resi verificati; query B2B → documentazione e lead time, se disponibili.

### 6. Shopping e Performance Max

#### Feed minimo

Verificare la specifica corrente di Merchant Center. In genere il nucleo comprende:

- `id`, `title`, `description`;
- `link`, `image_link`, eventuali `additional_image_link`;
- `availability`, `price`, `condition`;
- `brand`;
- identificatori reali `gtin` e/o `mpn`, gestendo correttamente `identifier_exists`;
- `google_product_category` e `product_type`;
- attributi variante pertinenti come `item_group_id`, `color`, `size`, `material`, `pattern`;
- dati o impostazioni per shipping e returns applicabili al paese.

Non inventare GTIN/MPN e non usare lo stesso ID per prodotti diversi. Prezzo e disponibilità devono corrispondere tra feed, landing page e checkout. Titoli e descrizioni devono descrivere il prodotto, senza keyword stuffing o testo promozionale.

#### Campi commerciali interni

Usare `custom_label` soltanto da dati affidabili:

- ruolo SKU;
- fascia margine;
- fascia prezzo;
- stagionalità;
- stock depth;
- hero family;
- fragile/bulky o vincolo logistico.

Se margine e stock non sono disponibili, non simulare una segmentazione economica.

#### PMax governance

- collegare Merchant Center e Google Ads;
- definire listing group coerenti con famiglie e priorità;
- non mescolare paesi, lingue, economics o obiettivi incompatibili;
- aggiungere asset group per tema/prodotto con immagini, video e copy coerenti;
- controllare URL expansion, brand exclusions, search themes e negative secondo le opzioni correnti dell'account;
- evitare di presentare PMax come sostituto automatico di Search brand/product-named;
- registrare quali asset sono originali, adattati o generati con AI e applicare le etichette richieste.

Google consente anche configurazioni feed-only in alcuni setup retail, ma la decisione va presa esplicitamente: l'aggiunta successiva di asset può cambiare i requisiti e il comportamento della campagna.

### 7. Negative keyword system

Creare tre livelli:

1. **Account:** intenti universalmente irrilevanti.
2. **Campagna:** ambiguità proprie di categoria/mercato.
3. **Gruppo:** negative cross-cluster per indirizzare la query corretta.

Classificare ogni proposta:

```yaml
negative:
  term: ""
  match_type: broad|phrase|exact
  level: account|campaign|ad_group
  reason: irrelevant|ambiguity|unsupported_offer|cross_routing
  status: proposed|approved
  exception_queries: []
```

Non escludere automaticamente “prezzo”, “recensioni”, “reso”, “ricambi”, “sconto” o “usato”: possono essere segnali commerciali o di assistenza. Decidere in base a offerta, landing e obiettivo. Controllare sempre che le negative non blocchino nomi di prodotto ambigui.

### 8. Intent-to-landing mapping

Per ogni intento produrre:

| Intento | Query esemplificative | Pagina | Above-the-fold richiesto | Proof | CTA | Stato |
|---|---|---|---|---|---|---|

Regole:

- prodotto nominato → PDP o collezione esatta;
- categoria → PLP filtrata, non homepage;
- regalo/job → landing dedicata; se manca, segnare `landing_gap`;
- query tecnica → PDP/FAQ che risponde direttamente;
- B2B → pagina contract; se manca, non usare homepage come sostituto silenzioso.

### 9. Measurement e memoria

Minimo:

- acquisto con value e currency;
- deduplica browser/server se entrambi attivi;
- add_to_cart e begin_checkout come diagnostica, non obiettivo sostitutivo senza ragione;
- consent mode e policy applicabili;
- Enhanced Conversions solo dopo verifica e documentazione;
- Merchant Center diagnostics, disapprovals e mismatch;
- query, landing, prodotto, paese e new/returning dove consentito.

Registrare ogni test con ipotesi, segmento, campagna, periodo, cambiamenti, metrica primaria, risultato e limiti. Non dichiarare causalità da confronti pre/post non controllati.

## Output obbligatori del modulo

1. `google-ads-playbook.md`: strategia applicata al brand.
2. `17-landing-page-map.yaml`: intento → pagina → proof → gap.
3. `keyword-hypotheses.csv|yaml`: opzionale, solo se richiesto.
4. `feed-readiness.md`: può essere incluso nel playbook.
5. `sources-and-assumptions`: fonti, data, status e gap.

## Quality gate finale

- [ ] Nessun volume, CPC, ROAS o domanda inventati.
- [ ] Ogni keyword è dichiarata ipotesi finché non validata.
- [ ] Brand, product-named e non-brand sono distinguibili.
- [ ] Ogni cluster ha una landing coerente o un gap esplicito.
- [ ] Feed e sito concordano su prezzo, stock e varianti.
- [ ] GTIN/MPN non sono inventati.
- [ ] Negative ambigue hanno eccezioni controllate.
- [ ] Claim e promozioni hanno fonte, mercato e scadenza.
- [ ] Tracking e checkout sono testati prima del lancio.
- [ ] PMax non nasconde categorie con economics incompatibili.
- [ ] Ogni blocker launch/publish ha un `INP-*` e una richiesta utente `Mi serve X`.

## Fonti Google da ricontrollare prima dell'uso

- [Product data specification](https://support.google.com/merchants/answer/7052112)
- [Performance Max campaigns](https://support.google.com/google-ads/answer/10724817)
- [Keyword matching](https://support.google.com/google-ads/answer/14996023)
- [Negative keywords](https://support.google.com/google-ads/answer/2453972)

