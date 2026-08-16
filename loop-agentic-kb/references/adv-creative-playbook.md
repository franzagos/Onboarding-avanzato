# ADV & Creative Playbook — riferimento per skill

Versione: 1.0  
Scopo: trasformare una Brand KB verificabile in moduli riutilizzabili da agenti di strategia ADV, creative strategy e Meta Ads, senza inventare target, prove, offerta, economics o performance.

## 1. Contratto del sistema

Il sistema genera tre artefatti distinti:

1. `13-funnel-awareness-matrix.yaml`: collega persona, job, prodotto, consapevolezza, messaggio, prova, obiezione, CTA e landing page.
2. `14-creative-strategy-library.yaml`: conserva territori, concept e pattern creativi come ipotesi testabili, non come campagne già validate.
3. `15-meta-ads-brief.yaml`: verifica la readiness della campagna e produce un brief eseguibile solo quando gli input bloccanti sono disponibili.

Questi moduli non sostituiscono la Brand KB. La Brand KB stabilisce cosa è vero; il playbook stabilisce come organizzare ciò che è vero per l'attivazione.

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
  schema_version: "2.0"
  readiness:
    activation_ready: {status: blocked, blocking_input_ids: [], conditions: [], last_checked_at: "YYYY-MM-DD"}
    publish_ready: {status: blocked, blocking_input_ids: [], conditions: [], last_checked_at: "YYYY-MM-DD"}
  market: null
  language: null
  product: null
  offer: null
  stock_verified_at: null
  audience: null
  audience_status: null
  objective: null
  awareness: problem-aware
  placements: [feed, reels, stories]
  destination_url: null
  approved_claim_ids: []
  blocked_claims: []
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

## 10. Regole di aggiornamento

- Ogni record ha `owner`, `updated_at` e `review_by`.
- Le performance entrano nella KB solo con mercato, audience, offerta, placement, periodo e spend associati.
- Un apprendimento creativo non viene generalizzato oltre il contesto del test.
- Le varianti perdenti non vengono eliminate: restano come `rejected-with-evidence` con motivazione.
- La Brand Voice passa da osservata in `evidence` ad approvata solo dopo revisione del brand.
- Gli agenti a valle devono citare gli ID usati e segnalare qualsiasi campo mancante.
