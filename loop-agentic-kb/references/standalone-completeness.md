# Completezza autonoma dei moduli

## Principio

La KB è un database normalizzato; i file analitici sono viste materializzate. Ogni vista deve essere utilizzabile singolarmente senza creare una seconda fonte di verità.

## Contratto autonomo comune

Ogni Markdown deve contenere, nell'ordine più utile:

1. executive summary con conclusioni e confidence;
2. scopo, decisioni supportate, usi consentiti e vietati;
3. contesto autonomo del brand rilevante per il modulo;
4. scope, mercato/lingua, periodo e metodologia;
5. analisi completa, non soltanto framework;
6. evidence map con `EV-*`, fonte e data;
7. implicazioni operative prioritarie;
8. assunzioni, limiti e blocker `INP-*`;
9. next actions e criterio di validazione;
10. dizionario degli ID utilizzati e freshness.

Ogni YAML deve contenere:

```yaml
standalone_context:
  brand_summary: null
  scope: []
  markets: []
  languages: []
  as_of: null
  decisions_supported: []
  allowed_uses: []
  prohibited_uses: []
  positioning_summary: null
  relevant_family_ids: []
  relevant_persona_ids: []
  essential_evidence_ids: []
  definitions: {}
  limitations: []
  blocking_input_ids: []
module_quality:
  coverage: "fail"
  evidence: "fail"
  depth: "fail"
  actionability: "fail"
  standalone_usability: "fail"
  consistency: "fail"
  freshness: "fail"
  overall: "fail"
```

Valori consentiti: `pass`, `conditional`, `fail`. `overall: pass` richiede `pass` in coverage, evidence, depth, actionability, standalone usability e consistency. Freshness può essere `conditional` solo se nessuna decisione corrente dipende dal dato scaduto.

## Definizione di completo

Un modulo non è completo se:

- contiene soprattutto istruzioni su cosa analizzare invece dell'analisi;
- usa pochi esempi come rappresentazione implicita dell'intero catalogo;
- elenca concetti senza priorizzarli o collegarli a prove;
- rinvia ad altri file per capire il brand, le entità o le conclusioni;
- confonde gap di attivazione con incompletezza analitica;
- ha tabelle vuote, placeholder o campi `null` essenziali per il proprio scopo;
- non dichiara metodo e copertura.

Se una fonte necessaria non è accessibile, chiedere l'input quando bloccante. Se l'utente non lo possiede, ridurre formalmente lo scope e usare `overall: conditional|fail`; non mantenere l'etichetta `complete`.

## Gate per modulo

| File | Contenuto minimo sostanziale per `overall: pass` |
|---|---|
| `01` | identità, storia, modello business, portfolio, distribuzione, value architecture, journey, servizi, proof, rischi e priorità |
| `02` | tutte le famiglie prioritarie; feature → functional benefit → emotional/social meaning → proof → objection → message hierarchy |
| `03` | competitor per categoria/mercato; direct/adjacent/substitute; price basket, assortment, positioning, channel, proof, service, creative/search footprint e whitespace |
| `04` | personas funzionali con job, trigger, obiezioni, proof threshold, prodotti, evidenze, falsificazione e rilevanza economica separata |
| `05` | tensioni profonde per persona×job×famiglia, identity stakes, paure, desideri, trade-off, trigger, anti-trigger, proof e test |
| `06` | frizioni per journey con prevalenza/severità/impatto separati, evidenze, cause, risk reducer, owner e misura |
| `07` | corpus, metodo, bias, temi per fonte/oggetto, verbatim/parafrasi distinti, segnali positivi/negativi, implicazioni e review ledger |
| `08` | corpus multi-contesto, pattern osservati, sintassi, ritmo, stance, esempi positivi/negativi, guardrail, canali e stato di approvazione |
| `09` | variazioni per contesto, rischio, customer state, canale e mercato con template e QA rule |
| `10` | term registry per locale con observed/preferred/qualified/rejected, esempi, dipendenza claim e traduzione/transcreation |
| `11` | catalog coverage dichiarata, famiglie, prodotti/varianti, specifiche, prezzo/stock datati, job, meaning, proof, obiezioni, ruolo, landing, cross-sell e rischi |
| `12` | claim atomici per brand/famiglia/prodotto/servizio con proof, scope, qualifica, owner, approvazione e scadenza |
| `13` | route complete prodotto×persona×awareness per tutte le priorità, con tensione, meccanismo, proof, obiezione, CTA e landing |
| `14` | territori e angoli per ogni route prioritaria, meccanismo visivo, asset, placement, voice guardrail, ipotesi e metrica |
| `15` | contesto brand/prodotto, ruolo Meta, architettura funnel, audience hypotheses, route creative, placement, offer/landing, test, measurement, guardrail e blocker |
| `16` | scope mercato, intent universe, campaign/ad-group map, query hypotheses, negatives, message pack, landing, Shopping/PMax, feed, measurement e roadmap |
| `17` | ogni intento prioritario collegato a pagina esistente/proposta, above-the-fold, proof, CTA, moduli, gap, analytics e owner |
| `18` | asset atomici, master/derivati, product/angle/placement tags, diritti, scadenze, specifiche, gap e performance context |
| `19` | domanda, competitor/retailer, lingua, cultura, pricing, operations, payments, policy/compliance, channel, landing e readiness locali |
| `20` | obiettivi, KPI, diagnostiche, guardrail, event dictionary, fonte, attribution, consent, QA, baseline e reconciliation |
| `21` | ogni test con contesto, ipotesi, variabile, control, sample, metrica, periodo, risultato, decisione, limiti e riuso |

## Copertura

Ogni modulo dichiara:

- universo scoperto;
- universo incluso;
- esclusioni e motivo;
- criterio di priorità;
- quota coperta quando il denominatore è noto;
- cosa impedisce la copertura completa.

Non usare `complete` quando si sono analizzati soltanto prodotti hero scelti dalla homepage, tre competitor o poche recensioni senza dichiarare il perimetro.

## Test in isolamento

Il QA reviewer riceve un solo modulo e risponde:

1. So quale brand, mercato, data e decisione sto guardando?
2. Capisco quali conclusioni sono evidence, inference o hypothesis?
3. Posso risalire alle prove senza conoscere la chat?
4. Posso compiere l'azione prevista senza aprire altri moduli?
5. So cosa non devo assumere e cosa manca?

Un solo `no` alle domande 1–4 impedisce `standalone_usability: pass`.
