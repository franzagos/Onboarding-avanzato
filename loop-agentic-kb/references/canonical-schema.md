# Schema canonico e integrità referenziale

## Autorità

| Oggetto | Fonte canonica |
|---|---|
| fonti | `sources.yaml` |
| evidenze | `evidence-ledger.yaml` |
| prodotti e offerte | `11-product-offer-registry.yaml` |
| claim pubblicabili | `12-claims-proof-library.yaml` |
| asset e diritti | `18-asset-library.yaml` |
| esperimenti e learning | `21-experiment-memory.yaml` |

`brand-database.yaml` è l'entry point del database e indicizza queste autorità. Non è un contenitore duplicato.

Gli altri file referenziano gli ID canonici. Non duplicare record completi in `context-pack.yaml`, strategic summary o brief di canale.

## Prefissi ID

| Entità | Prefisso |
|---|---|
| fonte | `SRC-` |
| evidenza | `EV-` |
| famiglia | `FAM-` |
| prodotto | `PROD-` |
| offerta | `OFF-` |
| competitor | `COMP-` |
| corpus VOC | `VOC-` |
| sample voce | `VOICE-` |
| persona | `PER-` |
| tensione | `TEN-` |
| frizione | `FRIC-` |
| claim analitico | `CLM-` |
| claim ADV | `ACL-` |
| route funnel | `FUN-` |
| angolo creativo | `ANG-` |
| intento | `INT-` |
| landing | `LND-` |
| asset | `AST-` |
| obiettivo | `OBJ-` |
| metrica | `MET-` |
| esperimento | `EXP-` |
| input mancante | `INP-` |
| issue QA | `QA-` |

Usare slug minuscoli stabili dopo il prefisso quando il significato è naturale; usare numeri progressivi quando l'entità non ha un nome stabile. Non riutilizzare ID e non incorporare valori volatili nell'ID.

## Vocabolari controllati

- Epistemico: `evidence`, `inference`, `hypothesis`, `missing`, `blocked`.
- Confidence: `high`, `moderate`, `low`, `unknown`.
- Readiness: `pass`, `conditional`, `blocked`, `not_applicable`.
- Handoff: `complete`, `degraded`, `blocked`.
- Advertising claim: `approved_for_ads`, `observed_not_approved`, `qualified_only`, `blocked`.
- Missing input: `identified`, `requested`, `provided`, `declined`, `unavailable`, `resolved`.

Usare `null`, non `to_define`, stringhe vuote o placeholder, per valori sconosciuti. Una lista realmente vuota usa `[]`; una lista non ancora censita deve essere accompagnata da stato/gap.

## Metadata minimi YAML

```yaml
meta:
  schema_version: "2.1"
  brand_id: "brand-slug"
  generated_at: "YYYY-MM-DD"
  last_reviewed_at: "YYYY-MM-DD"
  status: "draft"
  source_of_truth: false
```

Ogni YAML di modulo aggiunge `standalone_context` e `module_quality`. Ogni Markdown espone gli stessi concetti in frontmatter e nelle sezioni `Contesto autonomo`, `Coverage` e `Quality gate`.

## Brand database index

```yaml
database:
  database_id: "KB-brand-slug"
  schema_version: "2.1"
  brand_id: "brand-slug"
  authorities:
    sources: "sources.yaml"
    evidence: "evidence-ledger.yaml"
    products_offers: "11-product-offer-registry.yaml"
    claims: "12-claims-proof-library.yaml"
    assets: "18-asset-library.yaml"
    experiments: "21-experiment-memory.yaml"
  modules: []
  entity_index: {}
  freshness: {}
  readiness: {}
```

I moduli dichiarano `generated_from` con path/versione. Se una vista autonoma e un'autorità divergono, vince l'autorità e il QA apre un errore critico.

## Readiness record

```yaml
readiness:
  framework_ready:
    status: "pass"
    blocking_input_ids: []
    conditions: []
    last_checked_at: "YYYY-MM-DD"
```

## Regole referenziali

- Ogni `EV-*` deve esistere in `evidence-ledger.yaml` e referenziare un `SRC-*` esistente.
- Ogni `ACL-*` deve esistere nella claim library e referenziare prove esistenti, salvo stato `blocked` con gap esplicito.
- Ogni prodotto, persona, funnel route, angolo, intento, landing, asset ed esperimento referenziato deve esistere nel proprio registro.
- Un record downstream non può elevare lo stato di un record canonico.
- Un prezzo, stock, policy, promo o diritto asset senza data non può contribuire a `publish_ready: pass`.
- `context-pack.yaml` contiene ID, sintesi e readiness; non copie di claim, prodotti o fonti.

## Versionamento

Aggiornare `schema_version` solo per cambi incompatibili. Registrare `generated_from` e, quando pratico, checksum/versione delle dipendenze. Se un record canonico cambia, rieseguire QA su tutti i file che ne referenziano l'ID.

## Migrazione da output legacy

- Leggere file V1/legacy come input, ma scrivere sempre filename e formato canonici V2.1.
- Non mantenere due versioni attive dello stesso modulo (`.md` e `.yaml`). Archiviare la legacy fuori dal package finale.
- Migrare gli ID ai prefissi canonici; conservare il precedente valore in `legacy_aliases`, senza usarlo downstream.
- Registrare mapping e decisioni in `migration_map` dentro `brand-database.yaml` o nel merge log.
- Se una dipendenza legacy è incompleta, importare soltanto i record verificabili, assegnare `dependency_quality: conditional|fail` e propagare il limite. Non copiare i suoi status di completezza.
