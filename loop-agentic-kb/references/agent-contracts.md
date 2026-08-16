# Contratti degli agenti — `loop-agentic-kb`

## Contratto universale

Ogni task delegato deve contenere un contratto completo. Un agente non deve ricostruire lo scope dalla conversazione o modificare file non assegnati.

```yaml
task:
  run_id: "kb-<brand>-<YYYYMMDD>-<nonce>"
  task_id: "A1-brand-portfolio"
  brand: "<name>"
  objective: "<bounded objective>"
  markets: ["global"]
  languages: ["it"]
  depth: "standard" # lean | standard | deep
  as_of: "YYYY-MM-DD"
  dependencies:
    - path: "staging/merged/evidence-ledger.yaml"
      version: "sha256-or-run-version"
  source_scope:
    allowed_source_ids: ["SRC-..."]
    allowed_paths: ["/absolute/path"]
    allowed_urls: ["https://..."]
  write_scope:
    directory: "staging/a1-brand-portfolio"
    files: ["01-knowledge-base.md", "11-product-offer-registry.yaml", "evidence-ledger.yaml"]
  forbidden:
    - "invent missing data"
    - "edit final package"
    - "present hypothesis as fact"
  completion:
    required_sections: []
    validation_schema: "references/schemas/<schema>.yaml"
  missing_input_policy:
    classify_with: "references/blocking-input-protocol.md"
    user_contact_owner: "orchestrator"
```

## Output envelope universale

Ogni agente restituisce un breve handoff e salva gli artefatti. Non deve incollare l'intero report nel messaggio di completamento.

```yaml
handoff:
  run_id: "..."
  task_id: "..."
  status: "complete" # complete | degraded | blocked
  files_written:
    - path: "staging/..."
      schema_version: "1.0"
  counts:
    sources_used: 0
    evidence_items: 0
    inferences: 0
    hypotheses: 0
    unresolved_conflicts: 0
  high_impact_findings: []
  blocked_items: []
  blocking_input_ids: []
  assumptions_added: []
  dependencies_for_next: []
  validation:
    schema: "pass"
    evidence: "pass"
    self_check: "pass"
```

## Evidence contract

### Source record

```yaml
source:
  source_id: "SRC-0001"
  source_type: "first_party" # internal | first_party | regulator | independent | retailer | review | social
  publisher: "<entity>"
  title: "<title>"
  url: "<url-or-null>"
  local_path: "<absolute-path-or-null>"
  market: "IT"
  language: "it"
  published_at: null
  observed_at: "YYYY-MM-DD"
  extraction_scope: "<page/section/corpus>"
  credibility_for:
    - "product specification"
  not_credible_for:
    - "market leadership"
  limitations: []
```

### Evidence item

```yaml
evidence:
  evidence_id: "EV-0001"
  source_id: "SRC-0001"
  subject_id: "PROD-monkey-lamp"
  predicate: "listed_price"
  value: 254
  unit: "EUR"
  market: "IT"
  observed_at: "YYYY-MM-DD"
  location: "product page / price block"
  excerpt: "<short excerpt or null>"
  extraction: "direct" # direct | calculated
  notes: []
```

Un estratto deve essere breve e necessario. Gli agenti devono parafrasare e rispettare limiti di copyright; una citazione non sostituisce il link e la data.

### Analytical claim

```yaml
claim:
  claim_id: "CLM-0001"
  statement: "<atomic statement>"
  epistemic_status: "inference" # evidence | inference | hypothesis
  confidence: "moderate" # high | moderate | low
  evidence_ids: ["EV-0001", "EV-0002"]
  counterevidence_ids: []
  applies_to:
    products: []
    markets: []
    channels: []
  advertising_status: "needs_approval" # approved | needs_approval | blocked | not_applicable
  freshness:
    volatile: false
    recheck_before_publish: false
  limitations: []
```

### Regole epistemiche

- `evidence`: direttamente presente in una fonte citata.
- `inference`: conclusione supportata da almeno due osservazioni convergenti o da una catena esplicita.
- `hypothesis`: modello utile ma non validato; deve includere un test.
- `approved_for_ads`: stato di governance conferito solo da un owner autorizzato, mai dedotto dall'agente.
- `blocked`: non utilizzabile in output pubblici finché la condizione indicata non viene risolta.
- Usare confidence verbale, non percentuali pseudo-precise.
- Una fonte ufficiale prova cosa dichiara il brand, non superiorità oggettiva.
- Frequenze di recensioni valgono soltanto per il corpus dichiarato.
- Assenza di evidenza non è evidenza di assenza.

## Contratti specialistici

### A1 — Brand & Portfolio Analyst

**Input obbligatori**

- URL ufficiale o materiali brand;
- mercati e lingua del run;
- source plan;
- data di osservazione.

**Output di proprietà**

- `01-knowledge-base.md`;
- `02-product-message-map.md`;
- `portfolio.yaml`;
- `product-registry-draft.yaml`;
- `evidence.yaml`;
- `gaps.yaml`.

**Schema minimo per prodotto**

```yaml
product:
  product_id: "PROD-..."
  name: "..."
  family_id: "FAM-..."
  commercial_role: "unknown" # hero | acquisition | margin | retention | seasonal | unknown
  status: "evidence"
  markets: []
  price_snapshots: []
  stock_snapshots: []
  features: []
  jobs: []
  proof_evidence_ids: []
  landing_page: null
  margin_band: null
  internal_priority: null
```

**Stop condition:** catalogo non accessibile e nessuna fonte alternativa. Consegnare brand-only come `degraded`, non inventare portafoglio.

### A2 — Voice & Language Analyst

**Input obbligatori**

- corpus ufficiale multi-contesto;
- source ledger;
- lingua e mercati.

**Output di proprietà**

- `brand-voice.md`;
- `tone-of-voice.md`;
- `lexicon.md`;
- `voice-corpus.yaml`;
- `evidence.yaml`.

**Voice sample schema**

```yaml
voice_sample:
  sample_id: "VOICE-001"
  source_id: "SRC-..."
  context: "product_page"
  funnel_stage: "consideration"
  text_excerpt: "<brief>"
  observed_patterns: []
  status: "evidence" # evidence | approved | rejected
```

**Regole:** almeno tre contesti quando disponibili; separare personalità stabile da modulazione; nessun esempio è `approved` senza conferma; VOC mantenuta fuori dal corpus brand.

### A3 — Market, Competitor & VOC Analyst

**Input obbligatori**

- brand/portfolio draft o scope di categoria;
- mercati;
- fonti competitor e corpus recensioni disponibili.

**Output di proprietà**

- `03-competitors.md`;
- `competitors.yaml`;
- `reviews-voc.md`;
- `review-corpus-summary.yaml`;
- `evidence.yaml`.

**Competitor schema minimo**

```yaml
competitor:
  competitor_id: "COMP-..."
  name: "..."
  type: "direct" # direct | adjacent | substitute
  jobs_overlapped: []
  products_overlapped: []
  evidence_ids: []
  strengths_observed: []
  vulnerabilities_inferred: []
```

**Review corpus schema minimo**

```yaml
review_corpus:
  corpus_id: "VOC-..."
  subject: "brand" # brand | product | retailer
  platform: "..."
  sample_size: 0
  date_range: {from: null, to: null}
  collection_method: "manual_public"
  selection_bias: []
  themes: []
  representative: false
```

**Regole:** non unire brand, prodotto e retailer senza tag; non convertire rating di piattaforma in soddisfazione della clientela complessiva.

### A4 — Audience & Motivation Analyst

**Input obbligatori**

- brand, portfolio e message map;
- competitor e VOC;
- eventuali dati CRM/analytics/interviste.

**Output di proprietà**

- `personas.md`;
- `psychographics.md`;
- `audience-model.yaml`;
- `hypotheses.yaml`.

**Persona schema minimo**

```yaml
persona:
  persona_id: "PER-..."
  label: "..."
  model_type: "functional_hypothesis" # validated_segment only with data
  jobs: []
  triggers: []
  tensions: []
  objections: []
  proof_required: []
  products: []
  evidence_ids: []
  confidence: "moderate"
  validation_tests: []
```

**Regole:** vietati età, genere, reddito, professione e frequenza se non provati. Preferire jobs, occasioni, rischi e criteri decisionali.

### A5 — Friction & Funnel Analyst

**Input obbligatori**

- personas, VOC, customer journey, claim library;
- prodotti e pagine.

**Output di proprietà**

- `pain-points.md`;
- `funnel-awareness-matrix.md`;
- `frictions.yaml`.

**Pain schema minimo**

```yaml
friction:
  friction_id: "FRIC-..."
  stage: "pre_purchase"
  persona_ids: []
  product_ids: []
  description: "..."
  status: "evidence" # evidence | inference | hypothesis
  evidence_ids: []
  severity: "unknown"
  frequency: "unknown"
  risk_reducers: []
  validation_needed: []
```

**Regole:** severity e frequency non sono sinonimi; un tema ricorrente in una piccola piattaforma non diventa automaticamente prioritario.

### A6 — Commercial Truth & Claims Analyst

**Input obbligatori**

- product registry draft;
- prove, policy e dati interni disponibili;
- mercati e canali richiesti.

**Output di proprietà**

- `product-offer-registry.yaml`;
- `claims-proof-library.yaml`;
- `claims-gaps.yaml`.

**Claim governance schema minimo**

```yaml
ad_claim:
  claim_id: "ACL-..."
  canonical_text: "..."
  variants_allowed: []
  status: "observed_not_approved"
  proof_evidence_ids: []
  products: []
  markets: []
  channels: []
  owner: null
  approved_at: null
  expires_at: null
  recheck_before_publish: true
  forbidden_variants: []
```

**Regole:** fatti osservati non equivalgono ad approvazione legale/brand; `bestseller`, `limited`, sostenibilità, qualità, durata e superiorità richiedono prova specifica.

### A7 — Creative Activation Analyst

**Input obbligatori**

- voice/tone/lexicon;
- personas, funnel, pain e claim library;
- asset registry, se esiste;
- canali e mercati.

**Output di proprietà**

- `14-creative-strategy-library.yaml`;
- `15-meta-ads-brief.yaml`;
- `creative-gaps.yaml`.

```yaml
creative_angle:
  angle_id: "ANG-..."
  name: "..."
  persona_ids: []
  product_ids: []
  funnel_stage: "problem_aware"
  tension: "..."
  promise_claim_ids: []
  proof_evidence_ids: []
  hook_hypotheses: []
  scenes: []
  formats: []
  ctas: []
  required_asset_ids: []
  status: "test_hypothesis"
  prohibited_claim_ids: []
```

**Regole:** angolo creativo ≠ copy approvato; un hook deve risalire a pain/tensione e prova; humor disattivato nei contesti di incidente e assistenza.

### A8 — Search & Landing Analyst

**Input obbligatori**

- prodotti, personas, pain, funnel e claim;
- URL/pagine esistenti;
- mercato e lingua;
- dati keyword/query, se disponibili.

**Output di proprietà**

- `16-google-ads-playbook.md`;
- `search-intents.yaml`;
- `17-landing-page-map.yaml`.

```yaml
search_intent:
  intent_id: "INT-..."
  query_cluster: "..."
  intent_type: "category" # brand | product | category | problem | gifting | designer | competitor
  status: "hypothesis" # evidence only with query data
  product_ids: []
  persona_ids: []
  landing_page_id: null
  claim_ids: []
  negatives: []
  demand_metric: null
  source_ids: []
```

**Regole:** mai inventare volume, CPC o domanda; competitor terms richiedono review legale/policy; distinguere pagina esistente da landing proposta.

### A9 — Asset & Market Readiness Analyst

**Input obbligatori**

- cartelle asset e URL autorizzati;
- mercati richiesti;
- prodotti, claim e requisiti canale.

**Output di proprietà**

- `18-asset-library.yaml`;
- `19-market-packs/<market>.md`;
- `market-gaps.yaml`.

```yaml
asset:
  asset_id: "AST-..."
  path_or_url: "..."
  media_type: "image"
  product_ids: []
  scenes: []
  dimensions: null
  markets: []
  channels: []
  rights_status: "unknown" # verified | restricted | unknown
  rights_evidence_id: null
  expiry: null
  usable_live: false
```

**Regole:** presenza online non prova licenza; il market pack distingue traduzione, transcreation, domanda, operazioni e compliance.

### A10 — Measurement & Learning Analyst

**Input obbligatori**

- obiettivi di business e canale;
- funnel, creative angles e search intent;
- tracking esistente, se fornito.

**Output di proprietà**

- `20-measurement-framework.yaml`;
- `21-experiment-memory.yaml`;
- `tracking-gaps.yaml`.

```yaml
experiment:
  experiment_id: "EXP-..."
  hypothesis: "..."
  market: "..."
  channel: "..."
  persona_ids: []
  product_ids: []
  angle_ids: []
  variable: "..."
  control: null
  variants: []
  primary_metric: "..."
  guardrails: []
  baseline: null
  target: null
  result: null
  learning: null
  context: {}
```

**Regole:** nessun benchmark o target senza fonte o dato interno; una metrica proxy non viene presentata come risultato di business.

## Contratto del QA reviewer

**Input:** package candidate completo, manifest, evidence ledger e merge log.

**Output:** `qa-report.yaml` con errori atomici, severità e percorso esatto.

```yaml
qa_issue:
  issue_id: "QA-001"
  severity: "critical" # critical | major | minor
  file: "12-claims-proof-library.yaml"
  record_id: "ACL-..."
  rule: "claim_requires_proof"
  evidence: "missing proof_evidence_ids"
  required_fix: "block claim or attach valid evidence"
```

Il reviewer non riscrive il package. L'orchestratore applica fix mirati e registra l'esito.

## Handoff tra agenti

1. Un agente conclude scrivendo file completi e un `handoff.yaml`.
2. L'orchestratore valida schema, write scope e source IDs.
3. Solo output validati entrano in `staging/merged/`.
4. L'agente a valle riceve path e versione, non copie incollate o riassunti non tracciati.
5. Se una dipendenza è `degraded`, il downstream deve propagare il limite.
6. Se una dipendenza è `blocked`, il downstream può produrre struttura e gap, ma non conclusioni fondate sul dato mancante.
7. Il sub-agent assegna un `INP-*` a ogni blocker e lo restituisce all'orchestratore. Solo l'orchestratore chiede all'utente, usando obbligatoriamente il formato `Mi serve X` definito in `blocking-input-protocol.md`.

## Convenzioni ID

| Entità | Prefisso | Esempio |
|---|---|---|
| fonte | `SRC` | `SRC-0042` |
| evidenza | `EV` | `EV-0108` |
| prodotto | `PROD` | `PROD-love-in-bloom` |
| famiglia | `FAM` | `FAM-sculptural-lighting` |
| competitor | `COMP` | `COMP-qeeboo` |
| corpus VOC | `VOC` | `VOC-trustpilot-brand-it` |
| persona | `PER` | `PER-expressive-homeowner` |
| friction | `FRIC` | `FRIC-scale-uncertainty` |
| claim analitico | `CLM` | `CLM-0021` |
| claim ADV | `ACL` | `ACL-bic-scale-12x` |
| asset | `AST` | `AST-monkey-room-01` |
| intento | `INT` | `INT-statement-lamp` |
| angolo | `ANG` | `ANG-room-signature` |
| esperimento | `EXP` | `EXP-de-meta-001` |

Gli slug devono essere stabili, minuscoli, senza spazi. Non riutilizzare un ID per un'entità diversa.

## Criteri di accettazione per task

Un task è `complete` quando:

- tutti i file assegnati esistono e rispettano lo schema;
- ogni fatto ha almeno un `evidence_id` valido;
- inferenze e ipotesi mostrano ragionamento e confidence;
- campione, date e limiti sono presenti per dati aggregati;
- unknown e blocchi sono espliciti;
- non sono stati toccati file fuori write scope;
- l'handoff indica ciò che il downstream può e non può usare.

È `degraded` quando l'output è utile ma una fonte o sezione non critica manca. È `blocked` solo quando non può produrre nemmeno un artefatto strutturale affidabile.
