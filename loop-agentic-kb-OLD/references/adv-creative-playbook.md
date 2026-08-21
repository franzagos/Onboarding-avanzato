# ADV & Creative Playbook — riferimento per skill

Versione: 1.0  
Scopo: trasformare una Brand KB verificabile in moduli riutilizzabili da agenti di strategia ADV, creative strategy e Meta Ads, senza inventare target, prove, offerta, economics o performance.

## 1. Contratto del sistema

Il sistema genera tre artefatti distinti:

1. `13-funnel-awareness-matrix.yaml`: collega persona, job, prodotto, consapevolezza, messaggio, prova, obiezione, CTA e landing page.
2. `14-creative-strategy-library.yaml`: conserva territori, concept e pattern creativi come ipotesi testabili, non come campagne già validate.
3. `15-meta-ads-brief.yaml`: verifica la readiness della campagna e produce un brief eseguibile solo quando gli input bloccanti sono disponibili.

Questi moduli non sostituiscono la Brand KB. La Brand KB stabilisce cosa è vero; il playbook stabilisce come organizzare ciò che è vero per l'attivazione.

Ogni file deve tuttavia essere autonomo: incorporare il contesto rilevante del brand, definire gli ID consumati e includere l'intera analisi necessaria al proprio uso consentito. Un file Meta composto soltanto da readiness audit e blocker fallisce il gate di completezza.

## 2. Input minimi

### Input richiesti dalla Brand KB

- identità, posizionamento e portfolio;
- Product Message Map con gerarchia primaria, secondaria e terziaria;
- personas o segmenti con stato epistemico;
- psicografiche e ponti prodotto-persona;
- pain point e obiezioni;
- competitor e alternative;
- recensioni/VOC con limiti del campione;
- Brand Voice dedicata con stato e campioni;
- Tone of Voice e lessico;
- claim governance e fonti.

### Input bloccanti per una campagna live

- mercato e lingua;
- prodotto o famiglia precisa;
- offerta, prezzo aggiornato, stock e validità temporale;
- target reale o segmento accettato come ipotesi di test;
- obiettivo di campagna;
- destinazione del click;
- proof autorizzate per advertising;
- economics: margine, AOV, soglia CAC/ROAS o altro criterio di sostenibilità;
- tracking e KPI primario;
- diritti e disponibilità degli asset.

Se mancano prodotto/offerta, target o obiettivo, il sistema non genera copy Meta. Applicare `blocking-input-protocol.md`: chiedere all'utente iniziando con `Mi serve X`, spiegare cosa blocca e indicare il formato minimo. Se il blocker riguarda soltanto il lancio o la pubblicazione, consegnare il massimo draft affidabile con stato esplicito, senza elevarlo a ready.

## 3. Modello epistemico obbligatorio

Ogni record deve avere uno stato:

| Stato | Significato | Uso operativo |
|---|---|---|
| `evidence` | osservato in fonte tracciata | utilizzabile entro il perimetro della fonte |
| `inference` | interpretazione supportata | utilizzabile come strategia, non come fatto pubblico |
| `hypothesis` | idea da verificare | utilizzabile solo in test esplicitamente etichettato |
| `approved_for_ads` | validato da owner e prova | pubblicabile entro mercato, prodotto e data definiti |
| `blocked` | mancano prova o autorizzazione | non deve entrare nel copy pubblico |

Mai promuovere automaticamente `observed_not_approved` ad `approved_for_ads`. Prezzi, stock, tempi, policy e promozioni devono avere una data di ricontrollo.

## 4. Architettura multi-agente

Quando l'ambiente consente parallelismo, l'orchestratore assegna quattro stream indipendenti e li riunisce prima della scrittura:

| Agente | Legge | Produce | Veto |
|---|---|---|---|
| Funnel Strategist | prodotto, personas, psicografiche, pain point | matrice funnel/awareness | blocca salti tra tensione, beneficio e prova |
| Creative Strategist | voice, tone, lessico, product map, competitor | territori, format, asset requirements | blocca concept generici o dipendenti da asset inesistenti |
| Evidence & Claims Auditor | fonti, claims, VOC, gap | ledger claim-prova e rischi | blocca claim non dimostrati, testimonianze e scarsità inventate |
| Channel Planner | campaign input, funnel matrix, platform rules | brief Meta e piano di test | blocca campagne senza prodotto/offerta, target o obiettivo |

### Merge dell'orchestratore

1. Risolve conflitti usando questa priorità: prove approvate → fonti primarie → Brand KB → inferenze → ipotesi.
2. Elimina concept che non possiedono una catena completa.
3. Propaga i gap nei tre artefatti; non li nasconde con placeholder ambigui.
4. Consegna readiness per dimensione con `pass`, `conditional`, `blocked` o `not_applicable`.

## 5. Workflow

### Fase A — Intake e gate

1. Inventariare i file disponibili.
2. Verificare Brand Voice e Product Message Map.
3. Compilare il campaign readiness gate.
4. Separare fatti, inferenze e ipotesi.
5. Registrare campi mancanti e owner atteso.

### Fase B — Funnel matrix

Per ogni coppia prodotto-persona costruire:

`stato attuale → tensione → job → risposta prodotto → meccanismo → beneficio → prova → obiezione → next step`

La prova deve corrispondere al claim. Una feature dimostra la propria esistenza, non automaticamente un effetto o una superiorità.

### Fase C — Creative library

Ogni concept deve contenere:

- ID stabile;
- stato epistemico;
- persona e prodotto;
- livello di consapevolezza;
- tensione concreta;
- idea creativa e meccanismo visivo;
- messaggio dominante;
- proof visibile;
- asset necessari e diritti;
- placement compatibili;
- guardrail di Brand Voice;
- ipotesi e metrica di test;
- condizioni che lo bloccano.

Un concept non è una promessa di performance. Non assegnare CTR, CPA, ROAS o probabilità di vittoria.

### Fase D — Brief Meta

Prima del copy definire:

`Consapevolezza → Framework/struttura → Tipo di hook → Lunghezza → Leva → CTA → Placement`

Per conversione devono essere presenti offerta e azione. Per awareness non forzare scarsità o CTA transazionale. Feed e Reels/Stories richiedono adattamenti, non semplici tagli.

Il Meta brief completo deve includere anche quando il lancio è bloccato:

1. ruolo di Meta nel customer journey e confini rispetto a Search/CRM;
2. sintesi autonoma di brand, prodotti/famiglie, personas, psicografia e proof;
3. architettura per prospecting, consideration, retargeting e retention, marcando `not_applicable` dove motivato;
4. audience hypotheses con fonte logica, esclusioni, sovrapposizioni e metodo di validazione;
5. route `product × persona × awareness × tension × proof × CTA × landing`;
6. creative territories e concept collegati a `ANG-*`, non categorie generiche;
7. hook families, message hierarchy, visual mechanism e proof on screen;
8. matrice placement/formato con adattamenti Feed, Reels, Stories e catalogo;
9. offer/landing logic, risk reducers e claim guardrails;
10. asset inventory/gaps e diritti;
11. test roadmap con ipotesi, variabile, KPI, guardrail e criterio di decisione;
12. measurement, attribution assumptions e blocker launch/publish.

La mancanza di economics o tracking blocca l'attivazione, non autorizza a consegnare un file strategico superficiale. La mancanza di prodotto, mercato o obiettivo può invece bloccare il brief richiesto: applicare `Mi serve X` prima di scegliere arbitrariamente.

### Coverage Meta

- coprire ogni famiglia/prodotto prioritario o spiegare l'esclusione;
- coprire ogni persona/job prioritario con almeno una route completa;
- coprire tutti gli awareness stage realmente applicabili;
- collegare ogni concept a claim/proof, asset requirement, placement e landing;
- separare sempre strategia esplorativa, draft interno, activation-ready e publish-ready.

### Fase E — QA avversariale

Bloccare l'output se compare uno dei seguenti casi:

- claim non sostenuto o proof mismatch;
- target descritto come reale senza dati;
- falsa scarsità, falsa recensione o dato inventato;
- feature dump senza beneficio;
- prodotto non selezionato;
- CTA non coerente con obiettivo;
- voce decorativa o intercambiabile;
- visual indispensabile ma non disponibile;
- uso di IP o asset senza diritti verificati;
- landing page non coerente con query/promessa;
- test senza metrica e condizione di successo definite.

## 6. Schema del Funnel Record

```yaml
funnel_record:
  id: ""
  status: evidence|inference|hypothesis
  persona_id: ""
  persona_validation: hypothetical|validated
  product_family: ""
  awareness: unaware|problem-aware|solution-aware|product-aware|most-aware
  job: ""
  tension: ""
  message_job: ""
  dominant_message: ""
  mechanism: ""
  proof_required: []
  proof_available: []
  objections: []
  cta_type: discovery|comparison|purchase|lead|retention
  landing_page_requirement: ""
  blocked_claims: []
  source_files: []
```

## 7. Schema del Creative Concept

```yaml
creative_concept:
  angle_id: "ANG-000"
  status: hypothesis
  title: ""
  product: ""
  persona: ""
  awareness: ""
  objective_family: awareness|engagement|traffic|conversion|retargeting
  tension: ""
  concept: ""
  visual_mechanism: ""
  message: ""
  proof_on_screen: []
  required_assets: []
  rights_check: required
  placements: []
  brand_voice_patterns: []
  do_not: []
  test_hypothesis: ""
  primary_metric: ""
  result: null
  learning: null
  source_files: []
```

## 8. Schema del Meta Brief

```yaml
meta_brief:
  schema_version: "2.1"
  standalone_context: {}
  module_quality: {}
  readiness:
    activation_ready: {status: blocked, blocking_input_ids: [], conditions: [], last_checked_at: "YYYY-MM-DD"}
    publish_ready: {status: blocked, blocking_input_ids: [], conditions: [], last_checked_at: "YYYY-MM-DD"}
  market: null
  language: null
  product_ids: []
  offer_ids: []
  stock_verified_at: null
  persona_ids: []
  audience_hypotheses: []
  objective: null
  awareness: problem-aware
  placements: [feed, reels, stories]
  destination_url: null
  approved_claim_ids: []
  blocked_claim_ids: []
  funnel_architecture: []
  routes: []
  angle_ids: []
  placement_matrix: []
  asset_requirements: []
  test_roadmap: []
  economics:
    margin: null
    aov: null
    target_cac: null
  measurement:
    primary_kpi: null
    conversion_event: null
  asset_ids: []
  missing_blockers: []
```

## 9. Quality score senza falsa precisione

Usare solo `pass`, `conditional` o `blocked`:

| Gate | Pass | Conditional | Blocked |
|---|---|---|---|
| Evidence | claim approvati e tracciati | fonti pubbliche da approvare | claim assenti/incoerenti |
| Audience | segmento validato | persona ipotetica accettata come test | target assente |
| Offer | prezzo, stock, scadenza verificati | dati da ricontrollare prima del lancio | offerta assente |
| Voice | campioni approvati | voce osservata | voce mancante/parziale |
| Assets | disponibili e autorizzati | produzione pianificata | concept dipende da asset inesistenti |
| Measurement | evento e KPI definiti | tracking da QA | metrica assente |

Non calcolare un punteggio numerico di readiness: maschererebbe la natura bloccante di alcuni campi. Ogni gate bloccato deve avere almeno un `INP-*` in `assumptions-and-gaps.yaml`.

Il quality gate del modulo è separato: `module_quality.overall: pass` richiede coverage, evidence, depth, actionability, standalone usability e consistency tutte `pass`.

## 10. Regole di aggiornamento

- Ogni record ha `owner`, `updated_at` e `review_by`.
- Le performance entrano nella KB solo con mercato, audience, offerta, placement, periodo e spend associati.
- Un apprendimento creativo non viene generalizzato oltre il contesto del test.
- Le varianti perdenti non vengono eliminate: restano come `rejected-with-evidence` con motivazione.
- La Brand Voice passa da osservata in `evidence` ad approvata solo dopo revisione del brand.
- Gli agenti a valle devono citare gli ID usati e segnalare qualsiasi campo mancante.
