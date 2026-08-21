# Measurement and experiment governance

## Measurement framework

Per ogni obiettivo dichiarare:

| Campo | Contenuto |
|---|---|
| objective_id | ID stabile |
| business outcome | risultato economico |
| primary KPI | `MET-*` della metrica decisionale |
| diagnostic KPI | metriche esplicative |
| source | piattaforma o analytics |
| attribution window | definita, non assunta |
| owner | responsabile |
| baseline | valore e periodo, oppure null |
| guardrail | margine, stock, brand safety, resi |

Non ottimizzare su CTR o engagement se l'obiettivo dichiarato è vendita senza spiegare il ruolo diagnostico.

## Event dictionary

Registrare nome evento, definizione, trigger, piattaforma, deduplica, valore, valuta, consenso e QA status. Non assumere che eventi omonimi tra piattaforme misurino la stessa cosa.

## Experiment memory

```yaml
- experiment_id: "EXP-000"
  hypothesis: ""
  brand: ""
  market: ""
  channel: ""
  product_ids: []
  persona_ids: []
  awareness_stage: ""
  variable_tested: ""
  control: ""
  variant: ""
  start_date: null
  end_date: null
  primary_metric_id: null
  result: null
  sample_context: null
  lifecycle: "planned|qa|running|completed|cancelled"
  decision: "pending|adopt|iterate|reject|inconclusive"
  learning: null
  limitations: []
  reusable_when: []
  do_not_generalize_to: []
```

Un learning è riutilizzabile solo se conserva contesto e limitazioni. `Winner` senza metrica, periodo e confronto è un'etichetta, non conoscenza.
