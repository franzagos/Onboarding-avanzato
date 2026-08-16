# Product, offer and claims

## Product registry

Usare una riga per prodotto/variante realmente promuovibile. Una famiglia può avere una riga aggregata soltanto se prezzo, stock, proof e landing sono comuni.

Prima di compilare il registry, censire il catalogo con sitemap, collezioni, PDP, feed/listini e materiali disponibili. Dichiarare universo scoperto, copertura, esclusioni e metodo. Quattro prodotti esemplificativi non costituiscono un product database completo.

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
  functional_benefits: []
  emotional_social_meanings: []
  visual_signature: []
  use_cases: []
  risk_reducers: []
  desire_drivers: []
  objections: []
  landing_url: null
  alternative_product_ids: []
  competitor_ids: []
  cross_sell_product_ids: []
  upsell_product_ids: []
  content_opportunities: []
  operational_risks: []
  margin_band: null
  campaign_status: "blocked_missing_input"
  evidence_ids: []
```

Non assegnare ruolo commerciale da bestseller label, homepage prominence o gusto personale senza marcare `inference`.

Produrre una sintesi per famiglia con gamma, price ladder, differenze fra varianti, entry point, upgrade path, cannibalizzazione, proof gaps e rilevanza per personas/jobs. Leggere `customer-product-intelligence.md` per il contratto completo.

## Offer registry

Separare prodotto e offerta. Un'offerta richiede prezzo, incentivo, condizioni, inizio/fine, mercato, stock e landing. Se uno manca, indicare il blocco.

## Claims ledger

```yaml
- claim_id: "ACL-000"
  canonical_text: null
  subject_type: "brand|family|product"
  subject_id: null
  market: ""
  evidence_ids: []
  status: "approved_for_ads|observed_not_approved|qualified_only|blocked"
  qualification: null
  owner: null
  approved_at: null
  expires_at: null
  prohibited_variants: []
```

## Readiness

Un prodotto è `product_ready` soltanto se nome/variante, prezzo, stock, landing, specifiche chiave, claim e condizioni operative sono verificati per il mercato.

Un'offerta contribuisce ad `activation_ready: pass` soltanto se economics e tracking consentono una decisione media; questi dati possono restare riservati ma devono avere owner e stato. Se l'utente richiede una campagna eseguibile e tali dati mancano, applicare `blocking-input-protocol.md`.
