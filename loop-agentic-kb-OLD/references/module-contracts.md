# Module contracts

## Indice

1. Contratto comune
2. Moduli foundation
3. Moduli customer e voice
4. Moduli activation
5. Moduli learning
6. Handoff

## Contratto comune

Ogni modulo Markdown deve contenere:

- executive summary e conclusioni prioritarie;
- scopo e decisione supportata;
- contesto autonomo: brand, scope, mercato/data, entità rilevanti e usi consentiti;
- metodologia e coverage;
- stato/readiness;
- risultati;
- evidenze con fonte e data;
- inferenze e ipotesi separate;
- gap e confidence;
- implicazioni;
- handoff al modulo successivo.

Il file deve essere utilizzabile senza aprire dipendenze. Includere una vista compatta delle entità e prove necessarie, generata dalle autorità canoniche. Non usare rinvii come sostituto dell'analisi.

Ogni YAML deve usare ID stabili, stringhe quotate quando ambigue, `null` per dati mancanti e stato esplicito. Deve contenere `standalone_context` e `module_quality` secondo `standalone-completeness.md`.

Ogni file deve dichiarare `schema_version: "2.1"`. Usare esclusivamente nomi, ID, vocabolari e readiness definiti in `canonical-schema.md`. Ogni modulo deve elencare `blocking_input_ids`; se non ne ha, usare `[]`.

## Moduli foundation

| File | Scopo | Dipendenze |
|---|---|---|
| 00-agent-manifest | scope, agenti, DAG, ownership e stato | intake |
| 01-knowledge-base | identità, business, offerta, journey | fonti |
| 02-product-message-map | feature → benefit → proof per famiglia | 01 |
| 03-competitors | diretti, adiacenti, sostituti e gap | 01–02 |

## Customer e voice

| File | Scopo | Dipendenze |
|---|---|---|
| 04-personas | segmenti funzionali verificabili | 01, 03, 07 |
| 05-psychographics | tensioni e soglie di prova | 02, 04, 07 |
| 06-pain-points | frizioni per fase/persona/prodotto | 04, 07 |
| 07-reviews-voc | linguaggio cliente e red flag | fonti review |
| 08-brand-voice | abitudini stabili del brand | corpus brand |
| 09-tone-of-voice | variazioni per contesto | 08 |
| 10-lexicon | parole preferite, cautele e divieti | 07–09 |

## Activation

| File | Scopo | Dipendenze |
|---|---|---|
| 11-product-offer-registry | fatti commerciali per prodotto | 01–02 + dati interni |
| 12-claims-proof-library | governare pubblicabilità | tutte le fonti |
| 13-funnel-awareness-matrix.yaml | messaggi per fase con `FUN-*` | 02, 04–07, 12 |
| 14-creative-strategy-library.yaml | angoli e format con `ANG-*` | 08–13 |
| 15-meta-ads-brief.yaml | handoff Meta e blocker | 11–14 |
| 16-google-ads-playbook | intenti e readiness Google | 11–13 |
| 17-landing-page-map.yaml | `INT-*` → `LND-*` | 11–13, 16 |
| 18-asset-library | inventario asset e diritti | repository asset |
| 19-market-packs | localizzazione senza contaminare core | 01–18 |

## Learning

| File | Scopo | Dipendenze |
|---|---|---|
| 20-measurement-framework.yaml | KPI, eventi e fonti | obiettivi canale |
| 21-experiment-memory | memoria contestuale dei test | 20 + risultati |

## Handoff minimo tra agenti

```yaml
module: ""
producer: ""
status: "complete|degraded|blocked"
inputs_used: []
outputs_created: []
evidence_ids: []
decisions: []
hypotheses: []
blocking_gaps: []
module_quality: {}
standalone_test: "pass|fail"
downstream_ready_for: []
do_not_assume: []
```

L'orchestratore deve rifiutare un handoff che non distingue decisioni, ipotesi e gap.

## Registri trasversali

| File | Autorità |
|---|---|
| `sources.yaml` | record `SRC-*` |
| `evidence-ledger.yaml` | record `EV-*` |
| `assumptions-and-gaps.yaml` | assunzioni, gap e `INP-*` |
| `context-pack.yaml` | indice compatto per ID, senza duplicare record canonici |
| `brand-database.yaml` | entry point unico: versione, autorità, moduli, entity index, freshness e readiness |
| `review-checklist.yaml` | decisioni umane con owner, due date e pass/fail |
| `qa-report.yaml` | errori atomici `QA-*` e gate finali |

Se un input bloccante emerge, applicare `blocking-input-protocol.md` prima di dichiarare completo il modulo interessato.

## Completezza e readiness sono assi separati

`module_quality.overall` misura completezza sostanziale e autonomia. La readiness misura se il modulo può sostenere onboarding, strategia, attivazione o pubblicazione. Un Meta brief può avere analisi strategica completa ma `activation_ready: blocked`; non può avere `module_quality.overall: pass` se contiene soltanto un intake e una lista di dati mancanti.

Quando si aggiorna una KB precedente, i file legacy sono input, non output alternativi. Generare il filename canonico, migrare gli ID con alias tracciati e valutare nuovamente la qualità delle dipendenze prima di usarle.

Ogni modulo deve documentare universo, copertura, esclusioni e metodo. Usare `complete` soltanto quando supera il contratto specifico in `standalone-completeness.md`.
