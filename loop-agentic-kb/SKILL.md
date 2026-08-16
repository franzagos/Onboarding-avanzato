---
name: loop-agentic-kb
description: "Genera, aggiorna e valida knowledge base e-commerce agent-ready per brand onboarding, product intelligence, competitor, personas, psicografia, recensioni/VOC, Brand Voice, Tone of Voice, lessico, ADV, creative strategy, Google Ads, landing page mapping, market packs, measurement ed experiment memory. Usare quando Codex deve trasformare un sito e materiali interni in una fonte di verità riutilizzabile da più agenti, creare brief channel-ready senza inventare dati, oppure orchestrare analisi specialistiche in parallelo."
---

# Loop Agentic KB

Costruire una KB operativa che separi identità stabile, decisioni di mercato, decisioni di campagna e memoria delle performance.

## Principi non negoziabili

- Separare `evidence`, `inference`, `hypothesis`, `missing` e `blocked`.
- Citare fonte, data e perimetro per fatti, prezzi, policy, claim e recensioni.
- Non inventare target reali, demographics, volumi, CPC, margini, stock, performance o approvazioni.
- Separare Brand Voice, Tone of Voice, lessico e Voice of Customer.
- Trattare personas e keyword non misurate come ipotesi.
- Non dichiarare `campaign-ready` senza prodotto/offerta, mercato, target, obiettivo, destinazione, proof ed economics minimi.
- Mantenere i moduli brand-neutral separati dai market pack e dai campaign brief.
- Conservare output validi esistenti; aggiornare solo moduli obsoleti o insufficienti.

Leggere sempre [evidence-governance.md](references/evidence-governance.md). Leggere [module-contracts.md](references/module-contracts.md) prima di creare file e [agent-contracts.md](references/agent-contracts.md) prima di delegare.

## Intake

Raccogliere ciò che esiste senza richiedere di nuovo informazioni già presenti:

- brand e URL;
- obiettivo della KB e agenti downstream;
- mercato e lingua, se specifici;
- materiali interni, catalogo e asset;
- prodotto/offerta prioritari;
- dati economici, stock e performance disponibili;
- claim approvati e vincoli;
- esempi on-brand/off-brand;
- canali previsti.

Se un dato cambia la pubblicabilità ma manca, procedere con schema compilato e stato `blocked_missing_input`.

## Modalità

### Brand onboarding

Produrre moduli 01–10, fonti, gap e context pack.

### Agent-ready KB

Produrre moduli 00–21. I moduli 11–21 possono contenere campi mancanti espliciti: la completezza strutturale non equivale a campaign readiness.

### Channel pack

Aggiornare soltanto il brief del canale e le sue dipendenze. Per ADV/creative leggere [adv-creative-playbook.md](references/adv-creative-playbook.md). Per Google leggere [google-ads-playbook.md](references/google-ads-playbook.md).

### Market pack

Creare `markets/<country-code>.md`; non riscrivere la KB centrale con conclusioni locali.

## Orchestrazione multi-agent

Leggere [orchestration.md](references/orchestration.md) quando sono disponibili sub-agent o il task richiede una KB completa.

1. Eseguire localmente intake, manifest e registro fonti.
2. Costruire prima la KB foundation: brand, portafoglio e source registry.
3. Avviare in parallelo soltanto task con input stabili e output distinti.
4. Non delegare la lettura delle istruzioni della Skill.
5. Assegnare a ogni agente un file o gruppo di file senza overlap.
6. Richiedere output atomici con schema, fonti, confidence, gap e handoff.
7. Integrare centralmente contraddizioni, claim e readiness.
8. Eseguire validazione deterministica e quality gate semantico.

DAG consigliato:

```text
intake + sources
  └─ foundation KB + portfolio
       ├─ competitors
       ├─ reviews/VOC
       └─ brand corpus
            ├─ personas + psychographics + pain points
            ├─ Brand Voice + Tone + lexicon
            └─ product/offer + claims/proof
                 ├─ funnel + creative + Meta brief
                 ├─ Google Ads + landing map
                 └─ assets + market packs
                      └─ measurement + experiment memory + synthesis
```

## Output contract

Usare questa struttura; vedere dettagli in [module-contracts.md](references/module-contracts.md):

```text
00-agent-manifest.md
01-knowledge-base.md
02-product-message-map.md
03-competitors.md
04-personas.md
05-psychographics.md
06-pain-points.md
07-reviews-voc.md
08-brand-voice.md
09-tone-of-voice.md
10-lexicon.md
11-product-offer-registry.yaml
12-claims-proof-library.yaml
13-funnel-awareness-matrix.md
14-creative-strategy-library.md
15-meta-ads-brief.md
16-google-ads-playbook.md
17-landing-page-map.md
18-asset-library.yaml
19-market-packs/
20-measurement-framework.md
21-experiment-memory.yaml
sources.md
assumptions-and-gaps.md
context-pack.yaml
```

## Moduli commerciali strutturati

Leggere [product-offer-claims.md](references/product-offer-claims.md) per compilare 11 e 12.

- Il registry prodotto descrive fatti e ruolo commerciale; non elegge hero sulla sola prominenza visiva.
- Il claim ledger contiene formulazione massima, fonte, perimetro, stato, owner e scadenza.
- `observed` non significa `approved-for-ads`.
- Prezzo e disponibilità devono avere mercato, valuta e data.

## ADV e creative

Leggere [adv-creative-playbook.md](references/adv-creative-playbook.md).

- Collegare sempre `product × persona × awareness × objection × proof × CTA`.
- Separare direct response da awareness/engagement.
- Marcare gli angoli come `supported`, `hypothesis` o `blocked`.
- Non generare testimonianze, urgenza o scene clienti come fatti.
- Un creative brief può essere pronto per ideazione ma non per pubblicazione.

## Google Ads

Leggere [google-ads-playbook.md](references/google-ads-playbook.md).

- Classificare intenti brand, product, category, problem/job, gifting, designer/collab e competitor.
- Trattare keyword, negative e query mapping come ipotesi finché non validate con Search Console, Keyword Planner o search terms.
- Non inventare volumi, CPC, ROAS o ranking.
- Verificare landing, feed, GTIN/MPN, stock, shipping e policy prima di dichiarare Shopping/PMax ready.

## Measurement e memoria

Leggere [measurement-governance.md](references/measurement-governance.md).

- Definire KPI per obiettivo e fonte dati.
- Registrare test con ipotesi, contesto, variante, periodo, risultato e limiti.
- Non chiamare “learning” una variazione senza campione o contesto sufficiente.
- Non trasferire automaticamente un risultato tra mercati, prodotti o placement.

## Script

Per creare una nuova cartella KB:

```bash
python3 scripts/init_kb.py --brand "Brand" --output /absolute/path
```

Per validare struttura e stati:

```bash
python3 scripts/validate_kb.py /absolute/path --mode full
```

Usare `--mode nucleus` per un handoff ADV/Google deliberatamente ridotto. Gli script verificano struttura, non correttezza strategica.

## Readiness

Assegnare separatamente:

- `brand_ready`: identità, portafoglio, voce e fonti sufficienti;
- `product_ready`: prodotto, prezzo, stock e prove sufficienti;
- `channel_ready`: struttura del canale e asset disponibili;
- `campaign_ready`: mercato, target, obiettivo, offer, destination, economics e tracking definiti;
- `publish_ready`: claim approvati, asset autorizzati e QA completata.

Non comprimere questi stati in un unico sì/no.

## Quality gate finale

- Ogni file dichiara scopo, stato, fonti, inferenze, gap e handoff.
- Nessun claim operativo manca di fonte e perimetro.
- Nessun dato mutevole manca di data.
- Personas, keyword e psicografia non sono presentate come dati osservati quando non lo sono.
- Brand Voice e VOC sono separate.
- Product registry, claim ledger e landing mapping usano ID coerenti.
- I brief di canale espongono input bloccanti.
- Contraddizioni tra fonti sono conservate e risolte esplicitamente.
- `validate_kb.py` termina senza errori strutturali.
- Un revisore può usare la KB senza ricostruire il contesto dalla chat.

