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
  schema_version: "2.0"
  brand_id: "brand-slug"
  generated_at: "YYYY-MM-DD"
  last_reviewed_at: "YYYY-MM-DD"
  status: "draft"
  source_of_truth: false
```

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
