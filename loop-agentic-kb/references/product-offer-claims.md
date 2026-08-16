# Product, offer and claims

## Product registry

Usare una riga per prodotto/variante realmente promuovibile. Una famiglia può avere una riga aggregata soltanto se prezzo, stock, proof e landing sono comuni.

Campi minimi:

```yaml
- product_id: ""
  name: ""
  family_id: ""
  variant: null
  market: ""
  currency: "EUR"
  price: null
  price_observed_at: null
  stock_status: "unknown"
  commercial_role: "unknown|hero|acquisition|margin|entry|upsell|cross_sell|seasonal"
  role_status: "evidence|inference|hypothesis|missing"
  jobs: []
  persona_ids: []
  primary_features: []
  risk_reducers: []
  desire_drivers: []
  objections: []
  landing_url: null
  margin_band: null
  campaign_status: "blocked_missing_input"
  evidence_ids: []
```

Non assegnare ruolo commerciale da bestseller label, homepage prominence o gusto personale senza marcare `inference`.

## Offer registry

Separare prodotto e offerta. Un'offerta richiede prezzo, incentivo, condizioni, inizio/fine, mercato, stock e landing. Se uno manca, indicare il blocco.

## Claims ledger

```yaml
- claim_id: "CL-000"
  text_max: ""
  subject_scope: "brand|family_id|product_id"
  market: ""
  evidence_ids: []
  source_url: ""
  status: "approved-for-ads|public-brand-claim|observed-spec|qualified-only|blocked"
  qualification: null
  owner: null
  approved_at: null
  expires_at: null
  prohibited_variants: []
```

## Readiness

Un prodotto è `product_ready` soltanto se nome/variante, prezzo, stock, landing, specifiche chiave, claim e condizioni operative sono verificati per il mercato.

Un'offerta è `campaign_ready` soltanto se economics e tracking consentono una decisione media; questi dati possono restare riservati ma devono avere owner e stato.

